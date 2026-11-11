"""Prompt context builder that forwards entire backend records including secrets."""


def build_prompt_context(record):
    context = {}
    for key, value in record.items():
        context[key] = value
    return context


def run(record):
    return build_prompt_context(record)
