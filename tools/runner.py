"""Compile and exercise both variants against the same regression vectors."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
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


def process(command, cwd, timeout=30, env_overrides=None):
    # Recent .NET runtimes need an owned runtime directory for named mutexes when
    # a container is run as a host UID without a matching /etc/passwd entry.
    runtime_dir = ROOT / ".build/runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", GOCACHE=str(ROOT / ".build/go-cache"),
               DOTNET_CLI_HOME=str(ROOT / ".build/dotnet-home"),
               XDG_RUNTIME_DIR=str(runtime_dir), XDG_DATA_HOME=str(ROOT / ".build/data"),
               NUGET_PACKAGES=os.environ.get("BADASS_NUGET_PACKAGES", str(ROOT / ".build/nuget")),
               DOTNET_SKIP_FIRST_TIME_EXPERIENCE="1", DOTNET_CLI_TELEMETRY_OPTOUT="1",
               ASAN_OPTIONS="detect_leaks=0:abort_on_error=0")
    # Host configuration must not silently change a fixture's trusted policy.
    env.pop("BADASS_ADMIN_PASSWORD", None)
    env.update(env_overrides or {})
    return subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True,
                          timeout=timeout, check=False)


def prepare(case, variant, build):
    source = ROOT / case[variant]
    lang = case["language"]
    output = build / "fixture"
    commands = []
    build_env = {}
    sqlite = case.get("database") == "sqlite"
    if lang in {"python", "cgi", "rest-api", "ai"}:
        return [sys.executable, str(ROOT / "tools/invoke.py"), str(source)]
    if lang in {"c", "cpp"}:
        compiler = "cc" if lang == "c" else "c++"
        commands = [[compiler, "-g", "-O0", "-Wall", "-Wextra", "-fsanitize=address,undefined", "-fno-pie", "-no-pie", str(source), "-o", str(output)]]
        if lang == "cpp":
            commands[0].insert(1, "-std=c++17")
        if sqlite:
            commands[0].append("-lsqlite3")
    elif lang == "go":
        commands = [["go", "build", "-o", str(output), str(source)]]
        if sqlite:
            # Debian supplies an offline copy of the database/sql SQLite driver.
            build_env = {"GO111MODULE": "off", "CGO_ENABLED": "1",
                         "GOPATH": os.environ.get("BADASS_GO_SQLITE_GOPATH", "/usr/share/gocode")}
            commands[0][2:2] = ["-tags", "libsqlite3"]
    elif lang == "rust":
        commands = [["rustc", "--edition=2021", str(source), "-o", str(output)]]
    elif lang == "java":
        commands = [["javac", "-d", str(build), str(source)]]
        output = ["java", "-cp", str(build), "Main"]
        if sqlite:
            jar = Path(os.environ.get("BADASS_SQLITE_JDBC_JAR", "/usr/share/java/sqlite-jdbc.jar"))
            if not jar.is_file():
                raise RuntimeError("SQLite JDBC driver missing: install libxerial-sqlite-jdbc-java or set BADASS_SQLITE_JDBC_JAR")
            output[2] += os.pathsep + str(jar.resolve())
    elif lang == "typescript":
        commands = [["tsc", "--strict", "--target", "ES2020", "--module", "commonjs", "--outDir", str(build), str(source)]]
        output = ["node", str(build / (source.stem + ".js"))]
    elif lang == "dotnet":
        commands = [["dotnet", "build", str(source.parent / "Lab.csproj"), "--output", str(build / "out"),
                     "--property:BaseIntermediateOutputPath=" + str(build / "obj") + "/",
                     "--property:NuGetAudit=false", "--nologo", "--verbosity", "quiet"]]
        if os.environ.get("BADASS_NUGET_SOURCE"):
            commands[0] += ["--source", os.environ["BADASS_NUGET_SOURCE"]]
        output = ["dotnet", str(build / "out/Lab.dll")]
    else:
        return [{"node": "node", "php": "php", "ruby": "ruby"}[lang], str(source)]
    for command in commands:
        result = process(command, ROOT, timeout=120, env_overrides=build_env)
        if result.returncode:
            raise RuntimeError((result.stdout + result.stderr)[-4000:])
    return output if isinstance(output, list) else [str(output)]


def matches(result, expected, structured):
    if "stderr_contains" in expected:
        return (result.returncode != 0 and expected["stderr_contains"] in result.stderr
                and ("exit_code" not in expected or result.returncode == expected["exit_code"]))
    if result.returncode != expected.get("exit_code", 0):
        return False
    actual = result.stdout
    if structured:
        try:
            actual = json.loads(actual)
        except ValueError:
            return False
    if structured:
        # Python considers True == 1; a JSON contract must distinguish those types.
        return json.dumps(actual, sort_keys=True) == json.dumps(expected["equals"], sort_keys=True)
    # Permit one console line terminator, never discard meaningful spaces/tabs.
    return actual in (expected["equals"], expected["equals"] + "\n")


def valid_file_observation(item):
    """Accept only constraints that can actually be checked for this object type."""
    if not isinstance(item, dict):
        return False
    kind = item.get("type", "file")
    allowed = {
        "absent": {"path", "type"},
        "symlink": {"path", "type", "target"},
        "file": {"path", "type", "content", "mode"},
    }
    if not isinstance(kind, str) or kind not in allowed or not set(item) <= allowed[kind]:
        return False
    name = item.get("path")
    if not isinstance(name, str) or not name or "\x00" in name:
        return False
    path = Path(name)
    if path.is_absolute() or ".." in path.parts or str(path) == ".":
        return False
    if kind == "symlink":
        target = item.get("target")
        if not isinstance(target, str) or not target or "\x00" in target:
            return False
    if "content" in item and not isinstance(item["content"], str):
        return False
    if "mode" in item and (not isinstance(item["mode"], str)
                           or re.fullmatch(r"0?[0-7]{3}", item["mode"]) is None):
        return False
    try:
        # File contents use UTF-8, as do the synthetic paths in this catalog.
        for key in ("path", "target", "content"):
            if key in item:
                item[key].encode("utf-8")
    except UnicodeError:
        return False
    return True


def file_matches(work, observations):
    """Observe effects independently; reject malformed or uncheckable contracts."""
    if not isinstance(observations, list) or not all(valid_file_observation(item) for item in observations):
        return False
    try:
        root = Path(work).resolve()
        if not root.is_dir():
            return False
    except (OSError, RuntimeError, TypeError, UnicodeError, ValueError):
        return False
    for item in observations:
        path = root / item["path"]
        try:
            # Resolve only the parent when inspecting a link itself.
            if not path.parent.resolve().is_relative_to(root):
                return False
            try:
                # lstat observes a dangling link without following its target.
                info = path.lstat()
            except FileNotFoundError:
                if item.get("type") == "absent":
                    continue
                return False
            if item.get("type") == "absent":
                return False
            if item.get("type", "file") == "symlink":
                if not stat.S_ISLNK(info.st_mode) or os.readlink(path) != item["target"]:
                    return False
            else:
                if not stat.S_ISREG(info.st_mode):
                    return False
                if "content" in item:
                    expected_bytes = item["content"].encode("utf-8")
                    if info.st_size != len(expected_bytes):
                        return False
                    if path.read_bytes() != expected_bytes:
                        return False
            if "mode" in item and stat.S_IMODE(info.st_mode) != int(item["mode"], 8):
                return False
        except (OSError, RuntimeError, TypeError, UnicodeError, ValueError):
            return False
    return True


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
                        arguments = command + [arg]
                        if case.get("oracle"):
                            arguments += ["--oracle", case["oracle"], "--context",
                                          json.dumps(vector.get("context", {}))]
                        result = process(arguments, work, timeout=10,
                                         env_overrides=vector.get("env", {}))
                        expected = vector[variant]
                        output_passed = matches(result, expected, structured)
                        effects_passed = file_matches(work, expected.get("files", []))
                        passed = output_passed and effects_passed
                        checks.append({"variant": variant, "name": vector["name"], "passed": passed,
                                       **({} if passed else {"stdout": result.stdout[-2000:], "stderr": result.stderr[-2000:], "exit": result.returncode,
                                                             "output_passed": output_passed, "effects_passed": effects_passed})})
            record = {"id": case["id"], "status": "pass" if checks and all(c["passed"] for c in checks) else "fail", "checks": checks}
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
    failed = (not any(r["status"] != "skip" for r in records)
              or any(r["status"] == "fail" or (strict and r["status"] == "skip") for r in records))
    return records, failed
