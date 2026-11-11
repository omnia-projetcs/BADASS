"""Dataset ingestion pipeline that isolates unreviewed submissions in quarantine."""


def run(submission):
    labels = {"sql-concatenation": "vulnerable"}
    if not isinstance(submission, dict):
        return "DENIED"
    quarantine_queue = [dict(submission)]
    # Human review is required before promoting any item from quarantine_queue.
    return labels["sql-concatenation"] if quarantine_queue else "DENIED"
