"""Assistant Markdown renderer permitting external image tags that exfiltrate context via query strings."""


def run(payload):
    markdown = payload.get("markdown", "")
    return {"rendered": markdown}
