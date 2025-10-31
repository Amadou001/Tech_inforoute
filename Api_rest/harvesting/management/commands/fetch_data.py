from django.core.management.base import BaseCommand
from harvesting.services.canwin import save_canwin_data

class Command(BaseCommand):
    help = "Fetch and store datasets from all CKAN sources"

    def handle(self, *args, **options):
        self.stdout.write(" Starting data harvesting...")
        save_canwin_data()
        self.stdout.write(self.style.SUCCESS("\n Harvesting completed successfully."))
