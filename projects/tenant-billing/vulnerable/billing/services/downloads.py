from django.core import signing
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from billing.models import Invoice
from billing.services.access import membership


def issue(user, tenant_id, number):
    invoice = get_object_or_404(Invoice, tenant_id=tenant_id, number=number)
    return signing.dumps({"invoice": invoice.id, "user": user.id}, salt="invoice-download")


def read(user, token):
    data = signing.loads(token, salt="invoice-download", max_age=600)
    if data["user"] != user.id:
        raise PermissionDenied("Wrong recipient")
    invoice = get_object_or_404(Invoice, id=data["invoice"])
    return f"{invoice.number},{invoice.customer},{invoice.amount}\n"
