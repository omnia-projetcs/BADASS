import uuid
from django.conf import settings
from django.db import models


class Tenant(models.Model):
    name = models.CharField(max_length=80)


class Membership(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=16, default="reader")
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["tenant", "user"], name="one_membership")]


class Invoice(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    number = models.CharField(max_length=40)
    customer = models.CharField(max_length=120)
    amount = models.PositiveIntegerField()
    paid = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["tenant", "number"], name="tenant_invoice_number")]


class Export(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    numbers = models.JSONField()
    status = models.CharField(max_length=16, default="queued")
    content = models.TextField(default="")


class Invitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    email = models.EmailField()
    revoked = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)


class PaymentEvent(models.Model):
    event_id = models.CharField(max_length=100, unique=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
