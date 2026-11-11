"""Dataset ingestion pipeline that merges unreviewed user labels into ground truth."""


def run(submission):
    labels = {"sql-concatenation": "vulnerable"}
    labels.update(submission)
    return labels["sql-concatenation"]
