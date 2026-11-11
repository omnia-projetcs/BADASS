"""HTML renderer that escapes untrusted model completions before insertion."""
import html


def run(output):
    if not isinstance(output, str):
        return "DENIED"
    return "<p>" + html.escape(output, quote=False) + "</p>"
