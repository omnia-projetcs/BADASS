def run(submission):
    labels = {'sql-concatenation': 'vulnerable'}
    quarantine = dict(submission)
    # Human review is required before promotion from quarantine.
    return labels['sql-concatenation']
