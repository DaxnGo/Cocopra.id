const CACHE_NAME = 'cocopra-v2';
const OFFLINE_URL = '/offline.html';

// Assets to pre-cache during install
const PRE_CACHE_ASSETS = [
    '/',
    '/offline.html',
    '/manifest.json',
];

// Install: pre-cache essential assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[SW] Pre-caching offline assets');
            return cache.addAll(PRE_CACHE_ASSETS);
        })
    );
    self.skipWaiting();
});

// Activate: clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames
                    .filter((name) => name !== CACHE_NAME)
                    .map((name) => caches.delete(name))
            );
        })
    );
    self.clients.claim();
});

// Fetch: Network-first for API, Cache-first for static assets
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // Skip non-GET requests
    if (request.method !== 'GET') return;

    // API calls: Network-first strategy
    if (url.pathname.startsWith('/api')) {
        event.respondWith(
            fetch(request)
                .then((response) => {
                    const cloned = response.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(request, cloned));
                    return response;
                })
                .catch(() => caches.match(request))
        );
        return;
    }

    // Navigation requests (HTML pages) - Network first, fallback to index.html, then offline.html
    if (request.mode === 'navigate') {
        event.respondWith(
            fetch(request)
                .then((response) => {
                    caches.open(CACHE_NAME).then((cache) => cache.put(request, response.clone()));
                    return response;
                })
                .catch(() => {
                    // Try to return cached index.html for SPA routing, else offline page
                    return caches.match('/')
                        .then(cachedIndex => cachedIndex || caches.match(OFFLINE_URL))
                        .catch(() => caches.match(OFFLINE_URL));
                })
        );
        return;
    }

    // Static assets (CSS, JS, Images) - Cache-first, fallback to network
    event.respondWith(
        caches.match(request).then((cached) => {
            if (cached) return cached;
            return fetch(request).then((response) => {
                if (response.status === 200) {
                    const cloned = response.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(request, cloned));
                }
                return response;
            }).catch(() => {
                // Ignore other failures
            });
        })
    );
});

// Background Sync: queue offline form submissions
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-pest-scan') {
        event.waitUntil(syncPestScans());
    }
    if (event.tag === 'sync-harga-input') {
        event.waitUntil(syncHargaInputs());
    }
});

async function syncPestScans() {
    console.log('[SW] Syncing pest scan queue...');
    try {
        const { getAllFromQueue, removeFromQueue, STORES } = await import('/src/lib/db.js');
        const scans = await getAllFromQueue(STORES.PEST);

        for (const scan of scans) {
            try {
                // Gunakan relative path agar Vite proxy / Production server menangani routing
                const response = await fetch('/api/pest/scan', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(scan)
                });

                if (response.ok) {
                    console.log('[SW] Successfully synced pest scan:', scan.filename);
                    await removeFromQueue(STORES.PEST, scan.id);
                } else {
                    console.error('[SW] API rejected pest scan sync:', response.status);
                }
            } catch (err) {
                console.error('[SW] Failed to sync pest scan (Network error or CORS):', err);
            }
        }
    } catch (err) {
        console.error('[SW] Error accessing IDB in syncPestScans', err);
    }
}

async function syncHargaInputs() {
    console.log('[SW] Syncing harga input queue...');
    try {
        const { getAllFromQueue, removeFromQueue, STORES } = await import('/src/lib/db.js');
        const inputs = await getAllFromQueue(STORES.HARGA);

        for (const input of inputs) {
            try {
                const response = await fetch('/api/harga/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(input)
                });

                if (response.ok) {
                    console.log('[SW] Successfully synced harga input:', input.harga);
                    await removeFromQueue(STORES.HARGA, input.id);
                } else {
                    console.error('[SW] API rejected harga input sync:', response.status);
                }
            } catch (err) {
                console.error('[SW] Failed to sync harga input (Network error or CORS):', err);
            }
        }
    } catch (err) {
        console.error('[SW] Error accessing IDB in syncHargaInputs', err);
    }
}
