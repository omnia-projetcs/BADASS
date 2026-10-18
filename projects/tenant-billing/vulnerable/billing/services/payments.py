from django.db import transaction
from django.db.models import F
from billing.models import Invoice, PaymentEvent


def apply(event):
    with transaction.atomic():
        invoice = Invoice.objects.select_for_update().get(id=event["invoice"])
        receipt, created = PaymentEvent.objects.get_or_create(
            event_id=event["event_id"], defaults={"invoice": invoice, "amount": event["amount"]})
        if receipt.invoice_id != invoice.id or receipt.amount != event["amount"]:
            raise ValueError("Conflicting event")
        Invoice.objects.filter(id=invoice.id).update(paid=F("paid") + event["amount"])
