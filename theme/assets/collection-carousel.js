(() => {
  const init = (root = document) => root.querySelectorAll('.collection-carousel, .customer-reviews').forEach(section => {
    if (section.dataset.ready) return;
    section.dataset.ready = 'true';
    const track = section.querySelector('.collection-track, .reviews-grid');
    const move = direction => {
      const card = track.firstElementChild;
      const step = card.getBoundingClientRect().width + parseFloat(getComputedStyle(track).columnGap);
      track.scrollBy({ left: direction * step, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
    };
    const dots = [...section.querySelectorAll('[data-review-index]')];
    if (dots.length) {
      const updateDots = () => {
        const step = track.firstElementChild.getBoundingClientRect().width + parseFloat(getComputedStyle(track).columnGap);
        const current = Math.round(track.scrollLeft / step);
        dots.forEach((dot, i) => dot.setAttribute('aria-pressed', String(i === current)));
      };
      dots.forEach((dot, i) => dot.addEventListener('click', () => {
        const step = track.firstElementChild.getBoundingClientRect().width + parseFloat(getComputedStyle(track).columnGap);
        track.scrollTo({ left: i * step, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
      }));
      track.addEventListener('scroll', updateDots, { passive: true });
      new ResizeObserver(updateDots).observe(track);
      updateDots();
    }
    track.addEventListener('keydown', event => {
      if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
        event.preventDefault();
        move(event.key === 'ArrowRight' ? 1 : -1);
      }
    });
  });
  init();
  document.addEventListener('shopify:section:load', event => init(event.target));
})();
