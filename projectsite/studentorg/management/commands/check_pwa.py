from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.test import Client


class Command(BaseCommand):
    help = 'Verify PWA files, URLs, and template integration'

    def handle(self, *args, **options):
        errors = []
        static_pwa = Path(settings.BASE_DIR) / 'static' / 'pwa'
        for name in ('icon-192.png', 'icon-512.png', 'service-worker.js'):
            path = static_pwa / name
            if not path.is_file():
                errors.append(f'Missing file: {path}')
            else:
                self.stdout.write(self.style.SUCCESS(f'Found {path.name}'))

        client = Client(HTTP_HOST='127.0.0.1')
        checks = [
            ('/manifest.webmanifest', 'application/manifest+json'),
            ('/service-worker.js', 'javascript'),
            ('/offline/', 'text/html'),
        ]
        for path, content_hint in checks:
            response = client.get(path)
            if response.status_code != 200:
                errors.append(f'{path} returned HTTP {response.status_code}')
                continue
            ct = response.get('Content-Type', '')
            if content_hint not in ct:
                errors.append(f'{path} unexpected Content-Type: {ct}')
            else:
                self.stdout.write(self.style.SUCCESS(f'{path} -> 200 ({ct.split(";")[0]})'))

        templates_dir = Path(settings.BASE_DIR) / 'templates'
        for tpl in ('base.html', 'base_auth.html'):
            text = (templates_dir / tpl).read_text(encoding='utf-8')
            if 'pwa_head.html' not in text or 'pwa_register.html' not in text:
                errors.append(f'{tpl} missing PWA includes')
            else:
                self.stdout.write(self.style.SUCCESS(f'{tpl} includes PWA head + service worker'))

        if errors:
            for msg in errors:
                self.stdout.write(self.style.ERROR(msg))
            raise SystemExit(1)

        self.stdout.write(self.style.SUCCESS('PWA integration OK'))
