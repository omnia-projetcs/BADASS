def run(record):
    return {key: record[key] for key in ('question', 'public_context') if key in record}
