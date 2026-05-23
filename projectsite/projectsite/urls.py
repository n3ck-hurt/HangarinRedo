from django.contrib import admin
from django.urls import include, path

from studentorg.pwa_views import manifest, offline, service_worker

urlpatterns = [
    path('manifest.webmanifest', manifest, name='pwa-manifest'),
    path('service-worker.js', service_worker, name='pwa-service-worker'),
    path('offline/', offline, name='pwa-offline'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('studentorg.urls')),
]

