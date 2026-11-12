"""Tag validator using bounded linear-time character class validation."""


def run(tag):
    if not isinstance(tag, str) or not 1 <= len(tag) <= 32:
        return "DENIED"
    if not (tag.isalpha() and tag.islower()):
        return "DENIED"
    return {"valid": True, "tag": tag}
