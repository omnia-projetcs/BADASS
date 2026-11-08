from billing.models import Invoice


def invoices_for(job):
    return Invoice.objects.filter(tenant_id=job.tenant_id, number__in=job.numbers).order_by("id")
