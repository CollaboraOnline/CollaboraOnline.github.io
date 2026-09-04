/* The markup carries no autoplay attribute, so the poster frame stands on its
   own with scripting off or with reduced motion requested. */
(function () {
  'use strict';

  var video = document.getElementById('home-video');
  if (!video) {
    return;
  }

  var reduced = window.matchMedia
    && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduced) {
    return;
  }

  video.preload = 'auto';
  video.muted = true;
  var attempt = video.play();
  if (attempt && typeof attempt.catch === 'function') {
    /* a browser that refuses autoplay keeps the poster, nothing to recover */
    attempt.catch(function () {});
  }
}());
