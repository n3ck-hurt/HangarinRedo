from django.conf import settings


def auth_flags(request):
    return {
        'google_oauth_enabled': getattr(settings, 'GOOGLE_OAUTH_ENABLED', False),
    }
