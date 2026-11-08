from billing.models import Membership


def may_execute(job):
    return job.requested_by_id is not None
