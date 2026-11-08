def run(submission):
    labels = {'sql-concatenation': 'vulnerable'}
    labels.update(submission)
    return labels['sql-concatenation']
