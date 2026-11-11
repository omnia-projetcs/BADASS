"""AI agent tool that passes model arguments as an explicit argv vector."""
import subprocess


def dispatch_shell_tool(value):
    if not isinstance(value, str) or "\x00" in value:
        return "DENIED"
    return subprocess.check_output(["/usr/bin/printf", "%s", value], text=True)


def run(tool_call):
    if not isinstance(tool_call, dict) or "value" not in tool_call:
        return "DENIED"
    return dispatch_shell_tool(tool_call["value"])
