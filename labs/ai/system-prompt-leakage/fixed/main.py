"""Agent diagnostic handler that never exposes internal system instructions."""

SYSTEM_PROMPT = "LAB_INTERNAL_PROMPT"


def run(request):
    if not isinstance(request, str) or request == "debug":
        return "DENIED"
    return "READY"
