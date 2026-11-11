"""AI agent post-action redirect builder restricted to allowlisted local routes."""

ALLOWED_AGENT_ROUTES = frozenset({"/home", "/profile"})


def build_agent_redirect(value):
    if not isinstance(value, str) or value not in ALLOWED_AGENT_ROUTES:
        return "DENIED"
    return "Location: " + value


def run(tool_call):
    if not isinstance(tool_call, dict):
        return "DENIED"
    return build_agent_redirect(tool_call.get("value"))
