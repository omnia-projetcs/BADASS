import csv
import io
import redis
from django.db import transaction
from billing.models import Export, Membership
from billing.services.export_policy import may_execute
from billing.services.export_query import invoices_for

queue = redis.Redis(host="cache", decode_responses=True)


def submit(user, tenant_id, numbers):
    job = Export.objects.create(tenant_id=tenant_id, requested_by=user, numbers=numbers)
    queue.rpush("billing:exports", str(job.id))
    return job


def execute(job_id):
    with transaction.atomic():
        job = Export.objects.select_for_update().get(id=job_id)
        if job.status != "queued":
            return
        # Serialize execution with membership revocation, even in another process.
        list(Membership.objects.select_for_update().filter(user_id=job.requested_by_id, tenant_id=job.tenant_id))
        if not may_execute(job):
            job.status = "denied"
        else:
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["number", "customer", "amount"])
            for invoice in invoices_for(job):
                writer.writerow([invoice.number, invoice.customer, invoice.amount])
            job.content = output.getvalue()
            job.status = "ready"
        job.save(update_fields=["content", "status"])
