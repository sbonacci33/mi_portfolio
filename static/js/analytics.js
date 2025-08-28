(function(){
  function sendEvent(name, params){
    if (!window.gtag) return;
    window.gtag('event', name, params || {});
  }

  // Delegado para elementos con data-gtag
  function bindDataGtagClicks(){
    document.querySelectorAll('[data-gtag]').forEach(function(el){
      el.addEventListener('click', function(){
        const name  = el.dataset.gtag || 'click';
        const params = {
          event_category: el.dataset.category || undefined,
          event_label: el.dataset.label || (el.textContent || '').trim() || undefined,
          platform: el.dataset.platform || undefined,
          url: el.dataset.url || el.getAttribute('href') || undefined,
          path: location.pathname
        };
        sendEvent(name, params);
      }, {passive:true});
    });
  }

  // Descargas de archivos comunes
  function bindDownloadTracking(){
    const exts = ['pdf','doc','docx','xls','xlsx','csv','ppt','pptx','zip','rar'];
    document.querySelectorAll('a[href]').forEach(function(a){
      try{
        const href = a.getAttribute('href');
        if(!href) return;
        const url  = new URL(href, location.origin);
        const ext  = (url.pathname.split('.').pop() || '').toLowerCase();
        if(exts.includes(ext)){
          a.addEventListener('click', function(){
            sendEvent('file_download', {
              file_name: url.pathname.split('/').pop(),
              file_ext: ext,
              url: url.href,
              path: location.pathname
            });
          }, {passive:true});
        }
      }catch(_e){}
    });
  }

  // Clicks outbound
  function bindOutboundTracking(){
    document.querySelectorAll('a[href]').forEach(function(a){
      try{
        const href = a.getAttribute('href');
        if(!href) return;
        const url = new URL(href, location.origin);
        if(url.host !== location.host){
          a.addEventListener('click', function(){
            sendEvent('outbound_click', { url: url.href, host: url.host, path: location.pathname });
          }, {passive:true});
        }
      }catch(_e){}
    });
  }

  // Scroll depth 25/50/75/100
  function bindScrollDepth(){
    const thresholds = [25,50,75,100];
    const fired = new Set();
    const onScroll = function(){
      const doc = document.documentElement;
      const scrolled = (window.scrollY + window.innerHeight) / doc.scrollHeight * 100;
      thresholds.forEach(function(t){
        if(!fired.has(t) && scrolled >= t){
          fired.add(t);
          sendEvent('scroll_depth', { percent: t, path: location.pathname });
        }
      });
      if(fired.size === thresholds.length){
        window.removeEventListener('scroll', throttled);
      }
    };
    // throttle simple
    let ticking = false;
    const throttled = function(){
      if(!ticking){
        window.requestAnimationFrame(function(){ onScroll(); ticking=false; });
        ticking = true;
      }
    };
    window.addEventListener('scroll', throttled, {passive:true});
    onScroll(); // inicial
  }

  // Vistas de shorts (iframes de TikTok/Instagram ≥50% visibles por ≥1.5s)
  function bindShortsView(){
    const iframes = Array.from(document.querySelectorAll('iframe[src*="tiktok.com"], iframe[src*="instagram.com"]'));
    if(!('IntersectionObserver' in window) || iframes.length === 0) return;

    const seen = new WeakSet();
    const timers = new WeakMap();

    const observer = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        const el = entry.target;
        if(seen.has(el)) return;
        const ratio = entry.intersectionRatio || 0;
        if(ratio >= 0.5 && entry.isIntersecting){
          // espera 1.5s sostenidos
          if(!timers.has(el)){
            const t = setTimeout(function(){
              seen.add(el);
              timers.delete(el);
              const src = (el.getAttribute('src') || '').toLowerCase();
              const platform = src.includes('tiktok.com') ? 'tiktok' : (src.includes('instagram.com') ? 'instagram' : 'unknown');
              sendEvent('short_view', { platform: platform, path: location.pathname });
              observer.unobserve(el);
            }, 1500);
            timers.set(el, t);
          }
        }else{
          // sale del umbral: cancela conteo
          if(timers.has(el)){
            clearTimeout(timers.get(el));
            timers.delete(el);
          }
        }
      });
    }, { threshold: [0, 0.5, 1] });

    iframes.forEach(function(el){ observer.observe(el); });
  }

  document.addEventListener('DOMContentLoaded', function(){
    bindDataGtagClicks();
    bindDownloadTracking();
    bindOutboundTracking();
    bindScrollDepth();
    bindShortsView();
  });
})();
