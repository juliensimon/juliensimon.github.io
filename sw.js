// Service Worker for PWA capabilities with enhanced performance
const CACHE_NAME = 'julien-simon-v1.1.0';
const STATIC_CACHE = 'static-v1.1.0';
const DYNAMIC_CACHE = 'dynamic-v1.1.0';
const IMAGE_CACHE = 'images-v1.1.0';

// Assets to cache immediately
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/css/styles.css',
  '/js/main.js',
  '/assets/julien.jpg',
  '/assets/favicon.ico',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

// Install event - cache static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => {
        console.log('Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('Static assets cached successfully');
        return self.skipWaiting();
      })
      .catch(error => {
        console.error('Failed to cache static assets:', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE && cacheName !== IMAGE_CACHE) {
              console.log('Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('Service Worker activated');
        return self.clients.claim();
      })
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Handle different types of requests
  if (url.origin === self.location.origin) {
    // Same-origin requests
    event.respondWith(
      caches.match(request)
        .then(response => {
          if (response) {
            return response;
          }
          return fetch(request)
            .then(response => {
              // Cache successful responses for HTML pages
              if (response.status === 200 && response.type === 'basic') {
                const responseToCache = response.clone();
                caches.open(DYNAMIC_CACHE)
                  .then(cache => {
                    cache.put(request, responseToCache);
                  });
              }
              return response;
            })
            .catch(() => {
              // Return offline page for failed requests
              if (request.destination === 'document') {
                return caches.match('/index.html');
              }
            });
        })
    );
  } else {
    // Cross-origin requests (fonts, CDN resources)
    event.respondWith(
      caches.match(request)
        .then(response => {
          if (response) {
            return response;
          }
          return fetch(request)
            .then(response => {
              // Cache successful responses for fonts and CSS
              if (response.status === 200 && 
                  (request.destination === 'font' || 
                   request.destination === 'style' ||
                   request.destination === 'image')) {
                const responseToCache = response.clone();
                const cacheName = request.destination === 'image' ? IMAGE_CACHE : DYNAMIC_CACHE;
                caches.open(cacheName)
                  .then(cache => {
                    cache.put(request, responseToCache);
                  });
              }
              return response;
            })
            .catch(() => {
              // Return fallback for failed requests
              if (request.destination === 'image') {
                return caches.match('/assets/favicon.ico');
              }
              if (request.destination === 'font') {
                return new Response('', { status: 404 });
              }
            });
        })
    );
  }
});

// Background sync for offline actions
self.addEventListener('sync', event => {
  if (event.tag === 'background-sync') {
    event.waitUntil(doBackgroundSync());
  }
});

// Push notifications with enhanced features
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'New update available!',
    icon: '/assets/julien.jpg',
    badge: '/assets/favicon.ico',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1,
      url: '/'
    },
    actions: [
      {
        action: 'explore',
        title: 'View',
        icon: '/assets/favicon.ico'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/assets/favicon.ico'
      }
    ],
    requireInteraction: false,
    silent: false,
    tag: 'julien-simon-update'
  };

  event.waitUntil(
    self.registration.showNotification('Julien Simon', options)
  );
});

// Notification click handler with enhanced functionality
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  } else if (event.action === 'close') {
    // Just close the notification
    return;
  } else {
    // Default action - open the main page
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Background sync function with enhanced error handling
async function doBackgroundSync() {
  try {
    // Perform any background sync tasks here
    console.log('Background sync completed');
    
    // Send sync completion notification
    const clients = await self.clients.matchAll();
    clients.forEach(client => {
      client.postMessage({
        type: 'SYNC_COMPLETED',
        timestamp: Date.now()
      });
    });
  } catch (error) {
    console.error('Background sync failed:', error);
    
    // Send sync error notification
    const clients = await self.clients.matchAll();
    clients.forEach(client => {
      client.postMessage({
        type: 'SYNC_ERROR',
        error: error.message,
        timestamp: Date.now()
      });
    });
  }
}

// Message handling for communication with main thread
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({ version: CACHE_NAME });
  }

  if (event.data && event.data.type === 'CACHE_URLS') {
    event.waitUntil(
      caches.open(DYNAMIC_CACHE)
        .then(cache => {
          return cache.addAll(event.data.urls);
        })
        .then(() => {
          event.ports[0].postMessage({ success: true });
        })
        .catch(error => {
          event.ports[0].postMessage({ success: false, error: error.message });
        })
    );
  }

  if (event.data && event.data.type === 'CLEAR_CACHE') {
    event.waitUntil(
      caches.keys()
        .then(cacheNames => {
          return Promise.all(
            cacheNames.map(cacheName => {
              return caches.delete(cacheName);
            })
          );
        })
        .then(() => {
          event.ports[0].postMessage({ success: true });
        })
        .catch(error => {
          event.ports[0].postMessage({ success: false, error: error.message });
        })
    );
  }
});

// Periodic background sync for content updates
self.addEventListener('periodicsync', event => {
  if (event.tag === 'content-update') {
    event.waitUntil(updateContent());
  }
});

async function updateContent() {
  try {
    // Check for content updates
    const response = await fetch('/api/content-update', { cache: 'no-cache' });
    if (response.ok) {
      const data = await response.json();
      if (data.hasUpdates) {
        // Notify clients about updates
        const clients = await self.clients.matchAll();
        clients.forEach(client => {
          client.postMessage({
            type: 'CONTENT_UPDATE',
            data: data
          });
        });
      }
    }
  } catch (error) {
    console.error('Content update check failed:', error);
  }
} 