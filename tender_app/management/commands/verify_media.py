from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Verify and create required media directories'

    def handle(self, *args, **kwargs):
        # Ensure media directories exist
        media_dirs = [
            settings.MEDIA_ROOT,
            os.path.join(settings.MEDIA_ROOT, 'breakfast_items'),
        ]
        
        for directory in media_dirs:
            if not os.path.exists(directory):
                os.makedirs(directory)
                self.stdout.write(
                    self.style.SUCCESS(f'Created directory: {directory}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Directory already exists: {directory}')
                )