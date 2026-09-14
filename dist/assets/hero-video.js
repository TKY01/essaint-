(() => {
  const init = (root = document) => {
    root.querySelectorAll('[data-hero-video]').forEach(video => {
      if (video.dataset.initialized) return;
      video.dataset.initialized = 'true';
      const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
      const desktop = matchMedia('(min-width: 761px)');
      let visible = true;
      video.muted = true;
      video.autoplay = false;
      const play = () => {
        const source = video.querySelector('source');
        const src = desktop.matches ? source.dataset.desktopSrc : source.dataset.src;
        if (source.getAttribute('src') !== src) {
          source.setAttribute('src', src);
          video.load();
        }
        video.play().catch(() => {});
      };
      const sync = () => {
        video.poster = desktop.matches ? video.dataset.desktopPoster : video.dataset.mobilePoster;
        if (reducedMotion.matches || !visible || document.hidden) video.pause();
        else play();
      };
      reducedMotion.addEventListener('change', sync);
      desktop.addEventListener('change', sync);
      document.addEventListener('visibilitychange', sync);
      new IntersectionObserver(([entry]) => {
        visible = entry.isIntersecting;
        sync();
      }, { threshold: 0 }).observe(video);
      video.poster = desktop.matches ? video.dataset.desktopPoster : video.dataset.mobilePoster;
    });
  };
  init();
  document.addEventListener('shopify:section:load', event => init(event.target));
})();
