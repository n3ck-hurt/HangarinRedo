/* Hangarin Arms PWA service worker */
const CACHE_VERSION = 'hangarin-arms-v1';
const STATIC_CACHE = `${CACHE_VERSION}-static`;
const PRECACHE_URLS = [
  '/offline/',
  '/static/css/bootstrap.min.css',
  '/static/css/ready.css',
  '/static/css/hangarin-theme.css',
  '/static/css/demo.css',
  '/static/pwa/icon-192.png',
  '/static/pwa/icon-512.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => cache.addAll(PRECACHE_URLS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.filter((key) => key.startsWith('hangarin-arms-') && key !== STATIC_CACHE).map((key) => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;

  if (request.method !== 'GET') {
    return;
  }

  const url = new URL(request.url);

  if (url.pathname === '/manifest.webmanifest' || url.pathname === '/service-worker.js') {
    return;
  }

  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response && response.status === 200) {
            return response;
          }
          return caches.match('/offline/');
        })
        .catch(() => caches.match('/offline/'))
    );
    return;
  }

  if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(request).then((cached) => cached || fetch(request).then((response) => {
        if (response && response.status === 200) {
          const copy = response.clone();
          caches.open(STATIC_CACHE).then((cache) => cache.put(request, copy));
        }
        return response;
      }))
    );
  }
});
