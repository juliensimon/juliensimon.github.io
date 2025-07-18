// Modern JavaScript with performance optimizations
'use strict';

// Performance monitoring with modern APIs
class PerformanceMonitor {
  constructor() {
    this.metrics = {};
    this.initObservers();
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

      } catch (e) {
        console.warn('Performance monitoring not supported:', e);
      }
    }
  }

  trackMetric(name, value) {
    if (typeof umami !== 'undefined') {
      umami.track('web_vital', {
        metric: name,
        value: value,
        page: window.location.pathname
      });
    }
    
    // Send to console in development
    if (window.location.hostname === 'localhost') {
      console.log(`📊 ${name}: ${value}`);
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
    };
    tempImg.onerror = () => {
      console.warn('Failed to load image:', src);
      img.classList.add('error');
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
        }
      });
    });
  }

  initAnalytics() {
    // Track page views
    if (typeof umami !== 'undefined') {
      umami.track('page_view', {
        page: window.location.pathname,
        title: document.title,
        referrer: document.referrer
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
            page: window.location.pathname
          });
        }
      });
    });
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
  
  // Add utility functions to window for debugging
  if (window.location.hostname === 'localhost') {
    window.utils = utils;
  }
});

// Service Worker registration for PWA capabilities
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then(registration => {
        console.log('SW registered: ', registration);
      })
      .catch(registrationError => {
        console.log('SW registration failed: ', registrationError);
      });
  });
} 