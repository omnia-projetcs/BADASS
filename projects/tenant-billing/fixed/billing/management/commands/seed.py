from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from billing.models import Tenant, Membership, Invoice


class Command(BaseCommand):
    help = "Initialize an empty laboratory database with synthetic accounts"

    def handle(self, **options):
        if Tenant.objects.exists():
            raise CommandError("Refusing to seed a nonempty database")
        alpha = Tenant.objects.create(name="Alpha")
        beta = Tenant.objects.create(name="Beta")
        for name, tenant, role in [("alice", alpha, "admin"), ("eve", alpha, "reader"),
                                   ("bob", beta, "admin"), ("guest", None, None)]:
            user = User.objects.create_user(name, email=f"{name}@example.test", password="Lab-only-password-42")
            if tenant:
                Membership.objects.create(user=user, tenant=tenant, role=role)
        for tenant, customer in [(alpha, "ALPHA_CUSTOMER"), (beta, "BETA_PRIVATE_CUSTOMER")]:
            Invoice.objects.create(tenant=tenant, number="INV-001", customer=customer, amount=10000)
        Invoice.objects.create(tenant=alpha, number="INV-002", customer="ALPHA_SECOND_CUSTOMER", amount=5000)
