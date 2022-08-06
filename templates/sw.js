const VERSION = 'v1';
var urlsToCache = [
  '',
];

self.addEventListener('fetch', function(e){
    // Perform some task
});


self.addEventListener('activate', function(event) {
    // Perform some task
});

self.addEventListener('install', function(event) {
  // Perform install steps
  event.waitUntil(
    caches.open(VERSION)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});