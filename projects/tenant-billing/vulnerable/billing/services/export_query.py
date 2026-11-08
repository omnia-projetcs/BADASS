from billing.models import Invoice


def invoices_for(job):
    return Invoice.objects.filter(number__in=job.numbers).order_by("id")
