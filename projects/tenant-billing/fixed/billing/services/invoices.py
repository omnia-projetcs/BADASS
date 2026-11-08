from django.core.cache import cache
from django.shortcuts import get_object_or_404
from billing.models import Invoice


def detail(tenant_id, number):
    key = f"invoice:{tenant_id}:{number}"
    result = cache.get(key)
    if result is None:
        invoice = get_object_or_404(Invoice, tenant_id=tenant_id, number=number)
        result = {"id": invoice.id, "number": invoice.number, "customer": invoice.customer,
                  "amount": invoice.amount, "paid": invoice.paid}
        cache.set(key, result, timeout=120)
    return result
