"""Prompt context builder that allowlists only public fields for the model."""

PUBLIC_FIELDS = ("question", "public_context")


def run(record):
    if not isinstance(record, dict):
        return {}
    return {key: record[key] for key in PUBLIC_FIELDS if key in record}
