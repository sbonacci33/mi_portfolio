(function () {
  function sendEvent(name, params) {
    if (!window.gtag) return;
    window.gtag('event', name, params || {});
  }

  const DOWNLOAD_EXTENSIONS = new Set([
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'csv', 'ppt', 'pptx', 'zip', 'rar'
  ]);

  function getLinkInfo(anchor) {
    if (!anchor) return null;
    const href = anchor.getAttribute('href');
    if (!href) return null;

    let url;
    try {
      url = new URL(href, window.location.origin);
    } catch (_e) {
      return null;
    }

    const path = url.pathname || '';
    const ext = (path.split('.').pop() || '').toLowerCase();

    return {
      href,
      url,
      ext,
      isDownload: DOWNLOAD_EXTENSIONS.has(ext),
      isOutbound: url.host !== window.location.host,
    };
  }

  function bindDataGtagClicks() {
    document.addEventListener(
      'click',
      function (event) {
        const el = event.target.closest('[data-gtag]');
        if (!el) return;

        const name = el.dataset.gtag || 'click';
        sendEvent(name, {
          event_category: el.dataset.category || undefined,
          event_label: el.dataset.label || (el.textContent || '').trim() || undefined,
          platform: el.dataset.platform || undefined,
          url: el.dataset.url || el.getAttribute('href') || undefined,
          path: window.location.pathname,
        });
      },
      { passive: true }
    );
  }

  function bindLinkTracking() {
    document.addEventListener(
      'click',
      function (event) {
        const anchor = event.target.closest('a[href]');
        const linkInfo = getLinkInfo(anchor);
        if (!linkInfo) return;

        if (linkInfo.isDownload) {
          sendEvent('file_download', {
            file_name: linkInfo.url.pathname.split('/').pop(),
            file_ext: linkInfo.ext,
            url: linkInfo.url.href,
            path: window.location.pathname,
          });
        }

        if (linkInfo.isOutbound) {
          sendEvent('outbound_click', {
            url: linkInfo.url.href,
            host: linkInfo.url.host,
            path: window.location.pathname,
          });
        }
      },
      { passive: true }
    );
  }

  function bindScrollDepth() {
    const thresholds = [25, 50, 75, 100];
    const fired = new Set();

    const onScroll = function () {
      const doc = document.documentElement;
      const scrollHeight = Math.max(doc.scrollHeight, document.body.scrollHeight);
      if (scrollHeight <= 0) return;

      const scrolled = ((window.scrollY + window.innerHeight) / scrollHeight) * 100;

      thresholds.forEach(function (threshold) {
        if (!fired.has(threshold) && scrolled >= threshold) {
          fired.add(threshold);
          sendEvent('scroll_depth', { percent: threshold, path: window.location.pathname });
        }
      });

      if (fired.size === thresholds.length) {
        window.removeEventListener('scroll', throttled);
      }
    };

    let ticking = false;
    const throttled = function () {
      if (!ticking) {
        window.requestAnimationFrame(function () {
          onScroll();
          ticking = false;
        });
        ticking = true;
      }
    };

    window.addEventListener('scroll', throttled, { passive: true });
    onScroll();
  }

  function bindShortsView() {
    const selector = 'iframe[src*="tiktok.com"], iframe[src*="instagram.com"]';
    const iframes = Array.from(document.querySelectorAll(selector));
    if (!('IntersectionObserver' in window) || iframes.length === 0) return;

    const seen = new WeakSet();
    const timers = new WeakMap();

    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          const el = entry.target;
          if (seen.has(el)) return;

          if (entry.isIntersecting && (entry.intersectionRatio || 0) >= 0.5) {
            if (!timers.has(el)) {
              const timeoutId = setTimeout(function () {
                seen.add(el);
                timers.delete(el);

                const src = (el.getAttribute('src') || '').toLowerCase();
                const platform = src.includes('tiktok.com')
                  ? 'tiktok'
                  : src.includes('instagram.com')
                  ? 'instagram'
                  : 'unknown';

                sendEvent('short_view', {
                  platform,
                  path: window.location.pathname,
                });
                observer.unobserve(el);
              }, 1500);

              timers.set(el, timeoutId);
            }
          } else if (timers.has(el)) {
            clearTimeout(timers.get(el));
            timers.delete(el);
          }
        });
      },
      { threshold: [0, 0.5, 1] }
    );

    iframes.forEach(function (iframe) {
      observer.observe(iframe);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    bindDataGtagClicks();
    bindLinkTracking();
    bindScrollDepth();
    bindShortsView();
  });
})();
