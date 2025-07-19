// Optimized JavaScript for maximum performance
'use strict';

// Performance monitoring with modern APIs
class PerformanceMonitor {
  constructor() {
    this.metrics = {};
    this.initObservers();
    this.initWebVitals();
  }

  initObservers() {
    // Observe LCP
    if ('PerformanceObserver' in window) {
      try {
        const lcpObserver = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lastEntry = entries[entries.length - 1];
          this.metrics.lcp = lastEntry.startTime;
          this.reportMetric('LCP', lastEntry.startTime);
        });
        lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
      } catch (e) {
        console.warn('LCP observer failed:', e);
      }

      // Observe FID
      try {
        const fidObserver = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          entries.forEach((entry) => {
            this.metrics.fid = entry.processingStart - entry.startTime;
            this.reportMetric('FID', this.metrics.fid);
          });
        });
        fidObserver.observe({ entryTypes: ['first-input'] });
      } catch (e) {
        console.warn('FID observer failed:', e);
      }

      // Observe CLS
      try {
        let clsValue = 0;
        const clsObserver = new PerformanceObserver((list) => {
          for (const entry of list.getEntries()) {
            if (!entry.hadRecentInput) {
              clsValue += entry.value;
            }
          }
          this.metrics.cls = clsValue;
          this.reportMetric('CLS', clsValue);
        });
        clsObserver.observe({ entryTypes: ['layout-shift'] });
      } catch (e) {
        console.warn('CLS observer failed:', e);
      }
    }
  }

  initWebVitals() {
    // Report FCP
    if ('PerformanceObserver' in window) {
      try {
        const fcpObserver = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const firstEntry = entries[0];
          this.metrics.fcp = firstEntry.startTime;
          this.reportMetric('FCP', firstEntry.startTime);
        });
        fcpObserver.observe({ entryTypes: ['first-contentful-paint'] });
      } catch (e) {
        console.warn('FCP observer failed:', e);
      }
    }
  }

  reportMetric(name, value) {
    if (window.umami) {
      window.umami.track('web-vital', {
        metric: name,
        value: Math.round(value),
        rating: this.getRating(name, value)
      });
    }
  }

  getRating(metric, value) {
    const thresholds = {
      FCP: { good: 1800, poor: 3000 },
      LCP: { good: 2500, poor: 4000 },
      FID: { good: 100, poor: 300 },
      CLS: { good: 0.1, poor: 0.25 }
    };

    const threshold = thresholds[metric];
    if (!threshold) return 'unknown';

    if (value <= threshold.good) return 'good';
    if (value <= threshold.poor) return 'needs-improvement';
    return 'poor';
  }
}

// Lazy loading implementation
class LazyLoader {
  constructor() {
    this.images = [];
    this.observer = null;
    this.init();
  }

  init() {
    if ('IntersectionObserver' in window) {
      this.observer = new IntersectionObserver(
        (entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              this.loadImage(entry.target);
              this.observer.unobserve(entry.target);
            }
          });
        },
        {
          rootMargin: '50px 0px',
          threshold: 0.01
        }
      );

      // Observe all images with data-src
      document.querySelectorAll('img[data-src]').forEach(img => {
        this.observer.observe(img);
      });
    } else {
      // Fallback for older browsers
      this.loadAllImages();
    }
  }

  loadImage(img) {
    const src = img.dataset.src;
    if (src) {
      img.src = src;
      img.removeAttribute('data-src');
      img.classList.add('loaded');
    }
  }

  loadAllImages() {
    document.querySelectorAll('img[data-src]').forEach(img => {
      this.loadImage(img);
    });
  }
}

// Navigation enhancement
class Navigation {
  constructor() {
    this.init();
  }

  init() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(anchor.getAttribute('href'));
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });

    // Active navigation highlighting
    this.highlightActiveNav();
    window.addEventListener('scroll', this.debounce(this.highlightActiveNav.bind(this), 100));
  }

  highlightActiveNav() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav a[href^="#"]');
    
    let current = '';
    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.clientHeight;
      if (window.pageYOffset >= sectionTop - 200) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${current}`) {
        link.classList.add('active');
      }
    });
  }

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
  }
}

// Accessibility enhancements
class Accessibility {
  constructor() {
    this.init();
  }

  init() {
    // Skip link functionality
    const skipLink = document.querySelector('.skip-link');
    if (skipLink) {
      skipLink.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(skipLink.getAttribute('href'));
        if (target) {
          target.focus();
          target.scrollIntoView();
        }
      });
    }

    // Keyboard navigation
    this.initKeyboardNavigation();
    
    // Focus management
    this.initFocusManagement();
  }

  initKeyboardNavigation() {
    // Add keyboard navigation for interactive elements
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
      }
    });

    document.addEventListener('mousedown', () => {
      document.body.classList.remove('keyboard-navigation');
    });
  }

  initFocusManagement() {
    // Trap focus in modals (if any)
    const modals = document.querySelectorAll('[role="dialog"]');
    modals.forEach(modal => {
      const focusableElements = modal.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      
      if (focusableElements.length > 0) {
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        modal.addEventListener('keydown', (e) => {
          if (e.key === 'Tab') {
            if (e.shiftKey) {
              if (document.activeElement === firstElement) {
                e.preventDefault();
                lastElement.focus();
              }
            } else {
              if (document.activeElement === lastElement) {
                e.preventDefault();
                firstElement.focus();
              }
            }
          }
        });
      }
    });
  }
}

// Error tracking
class ErrorTracker {
  constructor() {
    this.init();
  }

  init() {
    window.addEventListener('error', (e) => {
      this.trackError('JavaScript Error', e.message, e.filename, e.lineno);
    });

    window.addEventListener('unhandledrejection', (e) => {
      this.trackError('Unhandled Promise Rejection', e.reason);
    });
  }

  trackError(type, message, filename = '', lineno = '') {
    if (window.umami) {
      window.umami.track('error', {
        type,
        message: message.toString().substring(0, 100),
        filename,
        lineno,
        url: window.location.href,
        userAgent: navigator.userAgent.substring(0, 100)
      });
    }
  }
}

// Utility functions
class Utils {
  static debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        timeout = null;
        if (!immediate) func(...args);
      };
      const callNow = immediate && !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      if (callNow) func(...args);
    };
  }

  static throttle(func, limit) {
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
  }

  static isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
  }
}

// Main application class
class App {
  constructor() {
    this.performanceMonitor = null;
    this.lazyLoader = null;
    this.navigation = null;
    this.accessibility = null;
    this.errorTracker = null;
    this.init();
  }

  init() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.setup());
    } else {
      this.setup();
    }
  }

  setup() {
    try {
      // Initialize performance monitoring
      this.performanceMonitor = new PerformanceMonitor();

      // Initialize lazy loading
      this.lazyLoader = new LazyLoader();

      // Initialize navigation
      this.navigation = new Navigation();

      // Initialize accessibility
      this.accessibility = new Accessibility();

      // Initialize error tracking
      this.errorTracker = new ErrorTracker();

      // Add loading animation
      this.addLoadingAnimation();

      // Initialize service worker
      this.initServiceWorker();

      console.log('App initialized successfully');
    } catch (error) {
      console.error('App initialization failed:', error);
      this.errorTracker?.trackError('App Initialization', error.message);
    }
  }

  addLoadingAnimation() {
    // Remove loading class after page load
    window.addEventListener('load', () => {
      document.querySelectorAll('.loading').forEach(el => {
        el.classList.remove('loading');
      });
    });
  }

  async initServiceWorker() {
    if ('serviceWorker' in navigator) {
      try {
        const registration = await navigator.serviceWorker.register('/sw.js');
        console.log('Service Worker registered:', registration);
      } catch (error) {
        console.warn('Service Worker registration failed:', error);
      }
    }
  }
}

// Initialize app when script loads
const app = new App();

// Export for potential external use
window.App = app; 