// Modern JavaScript with performance optimizations
'use strict';

// Performance monitoring with modern APIs
class PerformanceMonitor {
  constructor() {
    this.metrics = {};
    this.initObservers();
    this.initWebVitals();
  }

  initObservers() {
    // Core Web Vitals monitoring
    if ('PerformanceObserver' in window) {
      try {
        // LCP monitoring
        const lcpObserver = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lastEntry = entries[entries.length - 1];
          this.metrics.lcp = Math.round(lastEntry.startTime);
          this.trackMetric('LCP', this.metrics.lcp);
        });
        lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });

        // FID monitoring
        const fidObserver = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          entries.forEach(entry => {
            this.metrics.fid = Math.round(entry.processingStart - entry.startTime);
            this.trackMetric('FID', this.metrics.fid);
          });
        });
        fidObserver.observe({ entryTypes: ['first-input'] });

        // CLS monitoring
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

        // INP monitoring
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

      } catch (e) {
        // Performance monitoring not supported
        if (window.location.hostname === 'localhost') {
          console.warn('Performance monitoring not supported:', e);
        }
      }
    }
  }

  initWebVitals() {
    // Track page load performance
    window.addEventListener('load', () => {
      setTimeout(() => {
        const navigation = performance.getEntriesByType('navigation')[0];
        if (navigation) {
          this.trackMetric('DOMContentLoaded', Math.round(navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart));
          this.trackMetric('LoadComplete', Math.round(navigation.loadEventEnd - navigation.loadEventStart));
          this.trackMetric('TotalLoadTime', Math.round(navigation.loadEventEnd - navigation.fetchStart));
        }
      }, 0);
    });
  }

  trackMetric(name, value) {
    if (typeof umami !== 'undefined') {
      umami.track('web_vital', {
        metric: name,
        value: value,
        page: window.location.pathname,
        timestamp: Date.now()
      });
    }
    
    // Send to console in development
    if (window.location.hostname === 'localhost') {
      console.log(`📊 ${name}: ${value}`);
    }

    // Store in localStorage for debugging
    try {
      const stored = JSON.parse(localStorage.getItem('performance_metrics') || '{}');
      stored[name] = value;
      localStorage.setItem('performance_metrics', JSON.stringify(stored));
    } catch (e) {
      // Ignore localStorage errors
    }
  }
}

// Enhanced image lazy loading with Intersection Observer
class LazyLoader {
  constructor() {
    this.images = document.querySelectorAll('img[loading="lazy"]');
    this.init();
  }

  init() {
    if (!('IntersectionObserver' in window) || this.images.length === 0) return;

    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.loadImage(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, {
      rootMargin: '50px 0px',
      threshold: 0.01
    });

    this.images.forEach(img => imageObserver.observe(img));
  }

  loadImage(img) {
    const src = img.dataset.src || img.src;
    if (!src) return;

    // Create a new image to preload
    const tempImg = new Image();
    tempImg.onload = () => {
      img.src = src;
      img.classList.add('loaded');
      img.removeAttribute('data-src');
      // Track successful image load
      if (typeof umami !== 'undefined') {
        umami.track('image_loaded', {
          src: src,
          page: window.location.pathname
        });
      }
    };
    tempImg.onerror = () => {
      if (window.location.hostname === 'localhost') {
        console.warn('Failed to load image:', src);
      }
      img.classList.add('error');
      // Track failed image load
      if (typeof umami !== 'undefined') {
        umami.track('image_error', {
          src: src,
          page: window.location.pathname
        });
      }
    };
    tempImg.src = src;
  }
}

// Modern navigation with smooth scrolling
class Navigation {
  constructor() {
    this.init();
  }

  init() {
    this.highlightCurrentPage();
    this.initSmoothScrolling();
    this.initAnalytics();
    this.initKeyboardNavigation();
  }

  highlightCurrentPage() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navTabs = document.querySelectorAll('.nav-tab');
    
    navTabs.forEach(tab => {
      const href = tab.getAttribute('href');
      if (href === currentPage) {
        tab.classList.add('active');
      }
    });
  }

  initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        
        if (targetElement) {
          targetElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
          
          // Update URL without page jump
          history.pushState(null, null, `#${targetId}`);
          
          // Track internal link clicks
          if (typeof umami !== 'undefined') {
            umami.track('internal_link_click', {
              target: targetId,
              page: window.location.pathname
            });
          }
        }
      });
    });
  }

  initKeyboardNavigation() {
    // Add keyboard navigation for accessibility
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
      }
    });

    document.addEventListener('mousedown', () => {
      document.body.classList.remove('keyboard-navigation');
    });
  }

  initAnalytics() {
    // Bot detection
    const isBot = this.detectBot();
    
    // Track page views with bot detection
    if (typeof umami !== 'undefined') {
      umami.track('page_view', {
        page: window.location.pathname,
        title: document.title,
        referrer: document.referrer,
        userAgent: navigator.userAgent,
        viewport: `${window.innerWidth}x${window.innerHeight}`,
        isBot: isBot,
        botType: isBot ? this.getBotType() : null,
        timestamp: Date.now()
      });
    }
    
    // Track external link clicks with better data
    const externalLinks = document.querySelectorAll('a[href^="http"]');
    externalLinks.forEach(link => {
      link.addEventListener('click', () => {
        if (typeof umami !== 'undefined') {
          umami.track('external_link_click', {
            url: link.href,
            text: link.textContent.trim(),
            page: window.location.pathname,
            target: link.target || '_self',
            isBot: isBot
          });
        }
      });
    });

    // Track form interactions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
      form.addEventListener('submit', () => {
        if (typeof umami !== 'undefined') {
          umami.track('form_submit', {
            form: form.id || form.className,
            page: window.location.pathname,
            isBot: isBot
          });
        }
      });
    });
  }

  detectBot() {
    const userAgent = navigator.userAgent.toLowerCase();
    const botPatterns = [
      'bot', 'crawler', 'spider', 'scraper', 'gptbot', 'ccbot', 
      'anthropic-ai', 'claude-web', 'omgilibot', 'google-extended',
      'bingbot', 'perplexitybot', 'youbot', 'phindbot', 'deepseek-chat',
      'gemini-pro', 'meta-ai', 'arceebot', 'huggingfacebot', 'aio-bot'
    ];
    
    return botPatterns.some(pattern => userAgent.includes(pattern));
  }

  getBotType() {
    const userAgent = navigator.userAgent.toLowerCase();
    
    if (userAgent.includes('gptbot')) return 'OpenAI GPTBot';
    if (userAgent.includes('ccbot')) return 'Common Crawl';
    if (userAgent.includes('anthropic-ai')) return 'Anthropic Claude';
    if (userAgent.includes('claude-web')) return 'Claude Web';
    if (userAgent.includes('omgilibot')) return 'Omgili';
    if (userAgent.includes('google-extended')) return 'Google AI';
    if (userAgent.includes('bingbot')) return 'Bing Bot';
    if (userAgent.includes('perplexitybot')) return 'Perplexity';
    if (userAgent.includes('youbot')) return 'You.com';
    if (userAgent.includes('phindbot')) return 'Phind';
    if (userAgent.includes('deepseek-chat')) return 'DeepSeek';
    if (userAgent.includes('gemini-pro')) return 'Google Gemini';
    if (userAgent.includes('meta-ai')) return 'Meta AI';
    if (userAgent.includes('arceebot')) return 'Arcee Bot';
    if (userAgent.includes('huggingfacebot')) return 'Hugging Face';
    if (userAgent.includes('aio-bot')) return 'AIO Bot';
    
    return 'Unknown Bot';
  }
}

// Error handling and monitoring
class ErrorMonitor {
  constructor() {
    this.init();
  }

  init() {
    window.addEventListener('error', (e) => {
      this.trackError('JavaScript Error', e.error || e.message, e.filename, e.lineno);
    });

    window.addEventListener('unhandledrejection', (e) => {
      this.trackError('Unhandled Promise Rejection', e.reason, '', 0);
    });
  }

  trackError(type, message, filename, lineno) {
    if (typeof umami !== 'undefined') {
      umami.track('error', {
        type: type,
        message: message,
        filename: filename,
        lineno: lineno,
        page: window.location.pathname,
        userAgent: navigator.userAgent
      });
    }

    if (window.location.hostname === 'localhost') {
      console.error(`🚨 ${type}:`, message, filename, lineno);
    }
  }
}

// Utility functions with modern ES6+ features
const utils = {
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  throttle(func, limit) {
    let inThrottle;
    return function() {
      const args = arguments;
      const context = this;
      if (!inThrottle) {
        func.apply(context, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  },

  // Modern fetch wrapper with error handling
  async fetchWithTimeout(url, options = {}) {
    const { timeout = 5000, ...fetchOptions } = options;
    
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    
    try {
      const response = await fetch(url, {
        ...fetchOptions,
        signal: controller.signal
      });
      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      clearTimeout(timeoutId);
      throw error;
    }
  },

  // Copy to clipboard utility
  async copyToClipboard(text) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (err) {
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      return true;
    }
  },

  // Get device type
  getDeviceType() {
    const ua = navigator.userAgent;
    if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
      return 'tablet';
    }
    if (/mobile|android|iphone|ipod|blackberry|opera mini|iemobile/i.test(ua)) {
      return 'mobile';
    }
    return 'desktop';
  }
};

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  // Initialize performance monitoring
  window.performanceMonitor = new PerformanceMonitor();
  
  // Initialize lazy loading
  window.lazyLoader = new LazyLoader();
  
  // Initialize navigation
  window.navigation = new Navigation();
  
  // Initialize error monitoring
  window.errorMonitor = new ErrorMonitor();
  
  // Add utility functions to window for debugging
  if (window.location.hostname === 'localhost') {
    window.utils = utils;
  }

  // Track page load completion
  if (typeof umami !== 'undefined') {
    umami.track('page_loaded', {
      page: window.location.pathname,
      loadTime: performance.now(),
      deviceType: utils.getDeviceType()
    });
  }
});

// Service Worker registration for PWA capabilities
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then(registration => {
        if (window.location.hostname === 'localhost') {
          console.log('SW registered: ', registration);
        }
      })
      .catch(registrationError => {
        if (window.location.hostname === 'localhost') {
          console.log('SW registration failed: ', registrationError);
        }
      });
  });
} 