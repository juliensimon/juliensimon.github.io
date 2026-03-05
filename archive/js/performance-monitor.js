// Enhanced Performance Monitoring for SEO
class SEOPerformanceMonitor {
  constructor() {
    this.metrics = {};
    this.init();
  }

  init() {
    this.initWebVitals();
    this.initResourceTiming();
    this.initUserTiming();
    this.initErrorTracking();
  }

  initWebVitals() {
    if ('PerformanceObserver' in window) {
      // LCP (Largest Contentful Paint)
      const lcpObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        this.metrics.lcp = Math.round(lastEntry.startTime);
        this.trackMetric('LCP', this.metrics.lcp);
      });
      lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });

      // FID (First Input Delay)
      const fidObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach(entry => {
          this.metrics.fid = Math.round(entry.processingStart - entry.startTime);
          this.trackMetric('FID', this.metrics.fid);
        });
      });
      fidObserver.observe({ entryTypes: ['first-input'] });

      // CLS (Cumulative Layout Shift)
      const clsObserver = new PerformanceObserver((list) => {
        let clsValue = 0;
        const entries = list.getEntries();
        entries.forEach(entry => {
          if (!entry.hadRecentInput) {
            clsValue += entry.value;
          }
        });
        this.metrics.cls = Math.round(clsValue * 1000) / 1000;
        this.trackMetric('CLS', this.metrics.cls);
      });
      clsObserver.observe({ entryTypes: ['layout-shift'] });

      // INP (Interaction to Next Paint)
      const inpObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach(entry => {
          if (entry.interactionId) {
            this.metrics.inp = Math.round(entry.processingStart - entry.startTime);
            this.trackMetric('INP', this.metrics.inp);
          }
        });
      });
      inpObserver.observe({ entryTypes: ['interaction'] });
    }
  }

  initResourceTiming() {
    if ('PerformanceObserver' in window) {
      const resourceObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach(entry => {
          if (entry.initiatorType === 'img' || entry.initiatorType === 'css' || entry.initiatorType === 'script') {
            this.trackResource(entry);
          }
        });
      });
      resourceObserver.observe({ entryTypes: ['resource'] });
    }
  }

  initUserTiming() {
    // Custom user timing marks
    window.addEventListener('load', () => {
      performance.mark('page-fully-loaded');
      performance.measure('total-load-time', 'navigationStart', 'page-fully-loaded');
      
      const measure = performance.getEntriesByName('total-load-time')[0];
      this.trackMetric('TotalLoadTime', Math.round(measure.duration));
    });
  }

  initErrorTracking() {
    window.addEventListener('error', (event) => {
      this.trackError('JavaScript Error', event.message, event.filename, event.lineno);
    });

    window.addEventListener('unhandledrejection', (event) => {
      this.trackError('Unhandled Promise Rejection', event.reason);
    });
  }

  trackMetric(name, value) {
    // Send to analytics
    if (typeof umami !== 'undefined') {
      umami.track('web_vital', {
        metric: name,
        value: value,
        page: window.location.pathname,
        timestamp: Date.now()
      });
    } else {
      // Fallback: wait for Umami to load
      setTimeout(() => {
        if (typeof umami !== 'undefined') {
          umami.track('web_vital', {
            metric: name,
            value: value,
            page: window.location.pathname,
            timestamp: Date.now()
          });
        }
      }, 1000);
    }

    // Store for debugging
    try {
      const metrics = JSON.parse(localStorage.getItem('seo_metrics') || '{}');
      metrics[name] = value;
      localStorage.setItem('seo_metrics', JSON.stringify(metrics));
    } catch (e) {
      // Ignore localStorage errors
    }

    // Console logging in development
    if (window.location.hostname === 'localhost') {
      console.log(`📊 ${name}: ${value}`);
    }
  }

  trackResource(entry) {
    if (entry.duration > 3000) { // Track slow resources
      this.trackMetric('SlowResource', {
        name: entry.name,
        duration: Math.round(entry.duration),
        type: entry.initiatorType
      });
    }
  }

  trackError(type, message, filename, lineno) {
    if (typeof umami !== 'undefined') {
      umami.track('error', {
        type: type,
        message: message,
        filename: filename,
        lineno: lineno,
        page: window.location.pathname,
        timestamp: Date.now()
      });
    }
  }

  getMetrics() {
    return this.metrics;
  }
}

// Initialize performance monitoring
const seoPerformanceMonitor = new SEOPerformanceMonitor();

// Export for debugging
window.seoPerformanceMonitor = seoPerformanceMonitor; 