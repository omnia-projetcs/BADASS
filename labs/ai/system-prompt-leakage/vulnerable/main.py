"""Agent diagnostic handler that exposes internal system instructions on debug requests."""

SYSTEM_PROMPT = "LAB_INTERNAL_PROMPT"


def run(request):
    if request == "debug":
        return SYSTEM_PROMPT
    return "READY"
