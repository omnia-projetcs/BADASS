"""Tag validator with nested quantifier backtracking that explodes on non-matching suffixes."""


def backtrack_match(text):
    steps = [0]

    def search(idx):
        steps[0] += 1
        if idx == len(text):
            return True
        for end in range(len(text), idx, -1):
            chunk = text[idx:end]
            if chunk.isalpha() and chunk.islower():
                if search(end):
                    return True
        return False

    matched = bool(text) and search(0)
    if matched:
        return {"valid": True, "tag": text}
    return {"valid": False, "steps": steps[0]}


def run(tag):
    return backtrack_match(tag)
