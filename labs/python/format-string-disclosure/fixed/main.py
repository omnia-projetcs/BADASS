"""An untrusted str.format template can traverse attributes of a rich object."""

from string import Formatter


class Profile:
    def __init__(self):
        self.name = "Alice"
        self.team = "Engineering"
        self.private = {"api_key": "LAB_FORMAT_PRIVATE_KEY"}


def render(template, profile):
    # Only simple public placeholders belong to this renderer's contract.
    for literal, field, specification, conversion in Formatter().parse(template):
        if field is not None and (field not in {"name", "team"} or specification or conversion):
            raise ValueError("unsupported field")
    return template.format(name=profile.name, team=profile.team)


def run(template):
    if not isinstance(template, str) or len(template) > 512:
        return {"status": 400, "error": "invalid template"}
    try:
        return {"status": 200, "text": render(template, Profile())}
    except (ValueError, KeyError, AttributeError, IndexError, TypeError):
        return {"status": 400, "error": "invalid template"}
