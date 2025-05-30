from django.core.management.base import BaseCommand
from audit_trail.models import AuditLog

class Command(BaseCommand):
    help = 'Check audit log records'

    def handle(self, *args, **options):
        self.stdout.write(f'Total AuditLog entries: {AuditLog.objects.count()}')
        self.stdout.write(f'Logout entries: {AuditLog.objects.filter(action_type=\
LOGOUT\).count()}')
        self.stdout.write('Latest 5 logs:')
        for log in AuditLog.objects.order_by('-timestamp')[:5]:
            self.stdout.write(f'- {log.timestamp}: {log.action_type} by {log.user or \Anonymous\} - {log.action_detail}')

