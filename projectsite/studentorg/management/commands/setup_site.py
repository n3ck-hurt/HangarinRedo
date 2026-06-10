import os

from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Set Django Sites domain for OAuth callbacks (run after migrate)'

    def handle(self, *args, **options):
        domain = os.getenv('SITE_DOMAIN', '127.0.0.1:8000')
        site, created = Site.objects.update_or_create(
            pk=1,
            defaults={'domain': domain, 'name': 'Hangarin Arms'},
        )
        action = "created" if created else "updated"
        self.stdout.write(
            self.style.SUCCESS(f'Site {action}: {site.domain} (id={site.pk})')
        )
        
        protocol = 'https' if not os.getenv('DEBUG', 'True').lower() in ('1', 'true', 'yes') else 'http'
        self.stdout.write('\n--- GOOGLE CONSOLE CONFIGURATION ---')
        self.stdout.write(f'Authorized Javascript Origins: {protocol}://{site.domain}')
        self.stdout.write(f'Authorized redirect URIs:      {protocol}://{site.domain}/accounts/google/login/callback/')
        self.stdout.write('------------------------------------\n')
