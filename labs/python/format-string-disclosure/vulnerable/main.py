"""An untrusted str.format template can traverse attributes of a rich object."""


class Profile:
    def __init__(self):
        self.name = "Alice"
        self.team = "Engineering"
        self.private = {"api_key": "LAB_FORMAT_PRIVATE_KEY"}


def render(template, profile):
    # VULNERABLE: attribute and item lookups can reach non-public context data.
    return template.format(name=profile.name, team=profile.team, profile=profile)


def run(template):
    if not isinstance(template, str) or len(template) > 512:
        return {"status": 400, "error": "invalid template"}
    try:
        return {"status": 200, "text": render(template, Profile())}
    except (ValueError, KeyError, AttributeError, IndexError, TypeError):
        return {"status": 400, "error": "invalid template"}
