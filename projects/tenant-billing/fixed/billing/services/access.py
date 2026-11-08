from django.core.exceptions import PermissionDenied
from billing.models import Membership


def membership(user, tenant_id, admin=False):
    item = Membership.objects.filter(user=user, tenant_id=tenant_id, active=True).first()
    if item is None or (admin and item.role != "admin"):
        raise PermissionDenied("Membership required")
    return item
