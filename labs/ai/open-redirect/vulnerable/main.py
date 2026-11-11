"""AI agent post-action redirect builder that trusts model-chosen URLs."""


def build_agent_redirect(value):
    return "Location: " + value


def run(tool_call):
    return build_agent_redirect(tool_call["value"])
