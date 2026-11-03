"""Extract a small TAR upload while observing real local filesystem effects."""
import io
from pathlib import Path, PurePosixPath
import tarfile


def run(request):
    members = request.get("members") if isinstance(request, dict) else None
    if not isinstance(members, list) or not 1 <= len(members) <= 8:
        return {"status": 400, "error": "invalid archive"}
    data = io.BytesIO()
    try:
        with tarfile.open(fileobj=data, mode="w") as tar:
            for entry in members:
                if not isinstance(entry, dict) or set(entry) not in ({"name", "content"}, {"name", "link"}):
                    raise ValueError("invalid member")
                name = entry["name"]
                text = entry.get("content", entry.get("link"))
                if not isinstance(name, str) or not name or len(name) > 128 or not isinstance(text, str) or len(text) > 4096 or "\x00" in name + text or "\\" in name + text:
                    raise ValueError("invalid member")
                payload = text.encode("utf-8")
                if len(payload) > 4096:
                    raise ValueError("oversized member")
                info = tarfile.TarInfo(name)
                if "link" in entry:
                    info.type, info.linkname = tarfile.SYMTYPE, text
                    tar.addfile(info)
                else:
                    info.size = len(payload)
                    tar.addfile(info, io.BytesIO(payload))
        data.seek(0)
        root = Path("unpacked").resolve()
        with tarfile.open(fileobj=data, mode="r:") as tar:
            entries = tar.getmembers()
            seen = set()
            for info in entries:
                name = PurePosixPath(info.name)
                if name.is_absolute() or ".." in name.parts or not name.parts or str(name) in seen:
                    return {"status": 400, "error": "unsafe archive member"}
                seen.add(str(name))
                target = root / str(name)
                if info.issym() and not (target.parent / info.linkname).resolve().is_relative_to(Path.cwd().resolve()):
                    return {"status": 400, "error": "unsafe archive member"}
                pass
            root.mkdir(exist_ok=True)
            for info in entries:
                target = root / info.name
                target.parent.mkdir(parents=True, exist_ok=True)
                if info.issym():
                    target.symlink_to(info.linkname, target_is_directory=True)
                else:
                    with tar.extractfile(info) as source:
                        target.write_bytes(source.read())
        return {"status": 200, "extracted": len(entries)}
    except (OSError, ValueError, UnicodeError, tarfile.TarError, RuntimeError):
        return {"status": 400, "error": "invalid archive"}
