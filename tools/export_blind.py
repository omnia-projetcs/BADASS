#!/usr/bin/env python3
"""Export source fixtures under neutral paths; keep the answer key outside the corpus."""
import argparse
import hashlib
import json
from pathlib import Path
import secrets
import shutil

from lab import read_catalog, validate
from runner import ROOT


def export(cases, destination, mapping_path):
    destination = Path(destination).resolve()
    mapping_path = Path(mapping_path).resolve()
    if mapping_path.is_relative_to(destination):
        raise ValueError("The private mapping must be outside the scanner corpus")
    if destination.exists() or mapping_path.exists():
        raise ValueError("Choose new output paths; existing files are never overwritten")
    validate(cases)
    if not cases:
        raise ValueError("Cannot export an empty corpus")
    manifest = {"schema_version": 1, "files": {}, "source_pairs": len(cases)}
    variants = [(case, variant) for case in cases for variant in ("vulnerable", "fixed")]
    secrets.SystemRandom().shuffle(variants)
    destination.mkdir(parents=True)
    for case, variant in variants:
        opaque = secrets.token_hex(12)
        source = ROOT / case[variant]
        folder = destination / opaque
        folder.mkdir()
        # Keep compilation companions (.csproj etc.), but no README or answer key.
        for companion in sorted(source.parent.iterdir()):
            if companion.is_file() and not companion.is_symlink() and companion.suffix.lower() not in {".md", ".pyc"}:
                shutil.copyfile(companion, folder / companion.name)
        relative = str((folder / source.name).relative_to(destination))
        manifest["files"][relative] = {
            "case_id": case["id"], "variant": variant,
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        }
    mapping_path.parent.mkdir(parents=True, exist_ok=True)
    with mapping_path.open("x", encoding="utf-8") as stream:
        json.dump(manifest, stream, indent=2, sort_keys=True)
        stream.write("\n")
    return {"source_pairs": len(cases), "sources": len(manifest["files"]),
            "corpus": str(destination), "mapping": str(mapping_path)}


def normalize(findings, manifest):
    if not isinstance(findings, list) or manifest.get("schema_version") != 1:
        raise ValueError("Expected a findings array and a schema_version=1 mapping")
    result = []
    for finding in findings:
        if not isinstance(finding, dict) or not isinstance(finding.get("cwe"), str):
            raise ValueError("Each finding requires a relative path and a CWE")
        path = finding.get("path")
        if not isinstance(path, str) or path not in manifest["files"]:
            raise ValueError("Unknown source path in scanner output: " + repr(path))
        original = manifest["files"][path]
        result.append({"case_id": original["case_id"], "variant": original["variant"], "cwe": finding["cwe"]})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="New corpus directory, or normalized findings file")
    parser.add_argument("--mapping", required=True, type=Path, help="Private mapping outside the scanner input")
    parser.add_argument("--language")
    parser.add_argument("--normalize", type=Path, help="Normalize findings with path and cwe fields")
    args = parser.parse_args()
    if args.normalize:
        if args.output.exists():
            parser.error("The normalized output already exists")
        result = normalize(json.loads(args.normalize.read_text()), json.loads(args.mapping.read_text()))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, indent=2)
            stream.write("\n")
        print(json.dumps({"normalized_findings": len(result)}))
    else:
        cases = [case for case in read_catalog() if not args.language or case["language"] == args.language]
        print(json.dumps(export(cases, args.output, args.mapping), indent=2))


if __name__ == "__main__":
    main()
