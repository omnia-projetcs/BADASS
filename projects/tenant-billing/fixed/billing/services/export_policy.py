from billing.models import Membership


def may_execute(job):
    return Membership.objects.filter(user_id=job.requested_by_id, tenant_id=job.tenant_id, active=True).exists()
