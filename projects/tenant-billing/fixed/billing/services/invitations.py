from django.core import signing
from django.core.exceptions import PermissionDenied
from django.db import transaction
from billing.models import Invitation, Membership


def issue(tenant_id, email):
    invite = Invitation.objects.create(tenant_id=tenant_id, email=email)
    return invite, signing.dumps({"invite": str(invite.id)}, salt="invitation")


def accept(user, token):
    data = signing.loads(token, salt="invitation", max_age=3600)
    with transaction.atomic():
        invite = Invitation.objects.select_for_update().get(id=data["invite"])
        if invite.email != user.email or invite.revoked or invite.accepted:
            raise PermissionDenied("Invitation unavailable")
        existing = Membership.objects.select_for_update().filter(user=user, tenant=invite.tenant).first()
        role = "admin" if existing and existing.active and existing.role == "admin" else "reader"
        Membership.objects.update_or_create(user=user, tenant=invite.tenant, defaults={"active": True, "role": role})
        invite.accepted = True
        invite.save(update_fields=["accepted"])
