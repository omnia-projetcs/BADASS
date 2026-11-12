"""Assistant Markdown renderer blocking external Markdown images and untrusted URLs."""
import re


def run(payload):
    if not isinstance(payload, dict):
        return "DENIED"
    markdown = payload.get("markdown")
    if not isinstance(markdown, str) or len(markdown) > 512:
        return "DENIED"
    if "![" in markdown or re.search(r"https?://", markdown, re.IGNORECASE):
        return "DENIED"
    return {"rendered": markdown}
