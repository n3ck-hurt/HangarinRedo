from pathlib import Path

from django.conf import settings
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET


@require_GET
@cache_control(max_age=0, no_cache=True, must_revalidate=True)
def manifest(request):
    icon_192 = request.build_absolute_uri(f'{settings.STATIC_URL}pwa/icon-192.png')
    icon_512 = request.build_absolute_uri(f'{settings.STATIC_URL}pwa/icon-512.png')
    data = {
        'id': '/',
        'name': 'Hangarin Arms',
        'short_name': 'Hangarin',
        'description': 'Gun store inventory and sales dashboard',
        'start_url': '/',
        'scope': '/',
        'display': 'standalone',
        'background_color': '#0a0a0a',
        'theme_color': '#c41e3a',
        'orientation': 'any',
        'icons': [
            {
                'src': icon_192,
                'sizes': '192x192',
                'type': 'image/png',
                'purpose': 'any',
            },
            {
                'src': icon_512,
                'sizes': '512x512',
                'type': 'image/png',
                'purpose': 'any maskable',
            },
        ],
    }
    response = HttpResponse(
        json.dumps(data, indent=2),
        content_type='application/manifest+json; charset=utf-8',
    )
    return response


@require_GET
@cache_control(max_age=86400)
def service_worker(request):
    path = Path(settings.BASE_DIR) / 'static' / 'pwa' / 'service-worker.js'
    content = path.read_text(encoding='utf-8')
    return HttpResponse(content, content_type='application/javascript; charset=utf-8')


@require_GET
def offline(request):
    return render(request, 'pwa/offline.html')
