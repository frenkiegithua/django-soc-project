from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from alerts.permissions import ANALYST_GROUP, LEAD_GROUP


class Command(BaseCommand):
    help = "Create the SOC Analyst and SOC Lead groups (safe to run more than once)."

    def handle(self, *args, **options):
        for name in (ANALYST_GROUP, LEAD_GROUP):
            _, created = Group.objects.get_or_create(name=name)
            status = "created" if created else "already exists"
            self.stdout.write(f"{name}: {status}")
        self.stdout.write(self.style.SUCCESS("SOC roles ready."))
