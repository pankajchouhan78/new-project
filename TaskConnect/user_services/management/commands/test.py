from django.core.management.base import BaseCommand, CommandError
from user_services.API.utilse import run_faker
class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        run_faker()
