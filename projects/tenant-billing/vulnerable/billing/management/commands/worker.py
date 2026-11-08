from django.core.management.base import BaseCommand
from django.db import close_old_connections
from billing.services.exports import queue, execute


class Command(BaseCommand):
    help = "Consume invoice export jobs from Redis"

    def handle(self, **options):
        while True:
            item = queue.blpop("billing:exports", timeout=1)
            if item:
                close_old_connections()
                execute(item[1])
