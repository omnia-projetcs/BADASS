"""Compile and exercise both variants against the same regression vectors."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
RUNTIMES = {
    "c": ["cc"], "cpp": ["c++"], "go": ["go"], "php": ["php"],
    "node": ["node"], "typescript": ["tsc", "node"], "java": ["javac", "java"],
    "ruby": ["ruby"], "rust": ["rustc"], "dotnet": ["dotnet"],
    "python": [], "cgi": [], "rest-api": [], "ai": [],
}


def process(command, cwd, timeout=30):
    # Recent .NET runtimes need an owned runtime directory for named mutexes when
    # a container is run as a host UID without a matching /etc/passwd entry.
    runtime_dir = ROOT / ".build/runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", GOCACHE=str(ROOT / ".build/go-cache"),
               DOTNET_CLI_HOME=str(ROOT / ".build/dotnet-home"),
               XDG_RUNTIME_DIR=str(runtime_dir), XDG_DATA_HOME=str(ROOT / ".build/data"),
               NUGET_PACKAGES=str(ROOT / ".build/nuget"),
               DOTNET_SKIP_FIRST_TIME_EXPERIENCE="1", DOTNET_CLI_TELEMETRY_OPTOUT="1",
               ASAN_OPTIONS="detect_leaks=0:abort_on_error=0")
    return subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True,
                          timeout=timeout, check=False)


def prepare(case, variant, build):
    source = ROOT / case[variant]
    lang = case["language"]
    output = build / "fixture"
    commands = []
    if lang in {"python", "cgi", "rest-api", "ai"}:
        return [sys.executable, str(ROOT / "tools/invoke.py"), str(source)]
    if lang in {"c", "cpp"}:
        compiler = "cc" if lang == "c" else "c++"
        commands = [[compiler, "-g", "-O0", "-Wall", "-Wextra", "-fsanitize=address,undefined", "-fno-pie", "-no-pie", str(source), "-o", str(output)]]
    elif lang == "go":
        commands = [["go", "build", "-o", str(output), str(source)]]
    elif lang == "rust":
        commands = [["rustc", "--edition=2021", str(source), "-o", str(output)]]
    elif lang == "java":
        commands = [["javac", "-d", str(build), str(source)]]
        output = ["java", "-cp", str(build), "Main"]
    elif lang == "typescript":
        commands = [["tsc", "--strict", "--target", "ES2020", "--module", "commonjs", "--outDir", str(build), str(source)]]
        output = ["node", str(build / (source.stem + ".js"))]
    elif lang == "dotnet":
        commands = [["dotnet", "build", str(source.parent / "Lab.csproj"), "--output", str(build / "out"),
                     "--property:BaseIntermediateOutputPath=" + str(build / "obj") + "/", "--nologo", "--verbosity", "quiet"]]
        output = ["dotnet", str(build / "out/Lab.dll")]
    else:
        return [{"node": "node", "php": "php", "ruby": "ruby"}[lang], str(source)]
    for command in commands:
        result = process(command, ROOT, timeout=120)
        if result.returncode:
            raise RuntimeError((result.stdout + result.stderr)[-4000:])
    return output if isinstance(output, list) else [str(output)]


def matches(result, expected, structured):
    if "stderr_contains" in expected:
        return result.returncode != 0 and expected["stderr_contains"] in result.stderr
    if result.returncode != 0:
        return False
    actual = result.stdout.strip()
    if structured:
        try:
            actual = json.loads(actual)
        except ValueError:
            return False
    if structured:
        # Python considers True == 1; a JSON contract must distinguish those types.
        return json.dumps(actual, sort_keys=True) == json.dumps(expected["equals"], sort_keys=True)
    return actual == expected["equals"]


def run_cases(cases, strict=False):
    records = []
    (ROOT / ".build").mkdir(exist_ok=True)
    for case in cases:
        start = time.monotonic()
        missing = [x for x in RUNTIMES[case["language"]] if not shutil.which(x)]
        if missing:
            records.append({"id": case["id"], "status": "skip", "reason": "Missing: " + ", ".join(missing)})
            print("SKIP", case["id"], records[-1]["reason"])
            continue
        checks = []
        try:
            with tempfile.TemporaryDirectory(prefix="badass-", dir=ROOT / ".build") as td:
                base = Path(td)
                for variant in ("vulnerable", "fixed"):
                    build = base / variant
                    build.mkdir()
                    command = prepare(case, variant, build)
                    for index, vector in enumerate(case["tests"]):
                        work = build / str(index)
                        work.mkdir()
                        (work / "public").mkdir()
                        (work / "public/welcome.txt").write_text("WELCOME")
                        (work / "secret.txt").write_text("LAB_SECRET")
                        (work / "private.txt").write_text("LAB_SECRET")
                        structured = case["language"] in {"python", "cgi", "rest-api", "ai"}
                        arg = json.dumps(vector["input"]) if structured else vector["input"]
                        result = process(command + [arg], work, timeout=10)
                        passed = matches(result, vector[variant], structured)
                        checks.append({"variant": variant, "name": vector["name"], "passed": passed,
                                       **({} if passed else {"stdout": result.stdout[-2000:], "stderr": result.stderr[-2000:], "exit": result.returncode})})
            record = {"id": case["id"], "status": "pass" if all(c["passed"] for c in checks) else "fail", "checks": checks}
        except (OSError, subprocess.TimeoutExpired, RuntimeError) as exc:
            record = {"id": case["id"], "status": "fail", "reason": str(exc), "checks": checks}
        record["seconds"] = round(time.monotonic() - start, 3)
        record["source_sha256"] = {
            variant: hashlib.sha256((ROOT / case[variant]).read_bytes()).hexdigest()
            for variant in ("vulnerable", "fixed")
        }
        record["vectors_sha256"] = hashlib.sha256(json.dumps(case["tests"], sort_keys=True).encode()).hexdigest()
        records.append(record)
        print(record["status"].upper(), case["id"])
        if record["status"] == "fail":
            print(json.dumps(record, ensure_ascii=False))
    failed = any(r["status"] == "fail" or (strict and r["status"] == "skip") for r in records)
    return records, failed
