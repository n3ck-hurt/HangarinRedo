import os

from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Set Django Sites domain for OAuth callbacks (run after migrate)'

    def handle(self, *args, **options):
        domain = os.getenv('SITE_DOMAIN', '127.0.0.1:8000')
        site, _ = Site.objects.update_or_create(
            pk=1,
            defaults={'domain': domain, 'name': 'Hangarin Arms'},
        )
        self.stdout.write(
            self.style.SUCCESS(f'Site updated: {site.domain} (id={site.pk})')
        )
        self.stdout.write(
            'Google redirect URI: '
            f'http://{site.domain}/accounts/google/login/callback/'
        )
