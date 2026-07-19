/**
 * sw.js — Service Worker for STRATOS PWA
 * Enables offline support and asset caching
 */

const CACHE  = 'stratos-v2';
const ASSETS = [
  './',
  './index.html',
  './style.css',
  './script.js',
  './modules/weatherAPI.js',
  './modules/uiManager.js',
  './modules/storage.js',
  './manifest.json',
  './assets/icons/icon-192.svg',
  './assets/icons/icon-512.svg',
  'https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap',
  'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js',
];

// Install: pre-cache static assets
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

// Activate: clean old caches
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Fetch: cache-first for assets, network-first for API
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  // API calls → network only (stale is handled by app-level cache)
  if (url.hostname === 'api.openweathermap.org') return;
  // Static assets → cache first
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(res => {
        if (res && res.status === 200 && res.type === 'basic') {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return res;
      }).catch(() => cached);
    })
  );
});
