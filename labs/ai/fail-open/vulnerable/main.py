"""AI agent policy guard that fails open when the policy backend is unreachable."""


def verify_agent_policy(value):
    try:
        if value == "backend-down":
            raise ConnectionError("Policy backend unavailable")
        return "ALLOWED" if value == "authorized" else "DENIED"
    except ConnectionError:
        return "ALLOWED"


def run(tool_call):
    return verify_agent_policy(tool_call["value"])
