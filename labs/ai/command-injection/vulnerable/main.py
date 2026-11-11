"""AI agent shell tool that interpolates model arguments into a shell command."""
import subprocess


def dispatch_shell_tool(value):
    return subprocess.check_output("printf %s " + value, text=True, shell=True)


def run(tool_call):
    return dispatch_shell_tool(tool_call["value"])
