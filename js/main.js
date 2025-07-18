// Main JavaScript functionality
document.addEventListener('DOMContentLoaded', () => {
  // Initialize common functionality
  initNavigation();
  initSmoothScrolling();
  initAnalytics();
  initPerformanceMonitoring();
});

// Performance monitoring
function initPerformanceMonitoring() {
  // Monitor Core Web Vitals
  if ('PerformanceObserver' in window) {
    try {
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (entry.entryType === 'largest-contentful-paint') {
            if (typeof umami !== 'undefined') {
              umami.track('web_vital', {
                metric: 'LCP',
                value: Math.round(entry.startTime)
              });
            }
          }
        }
      });
      observer.observe({ entryTypes: ['largest-contentful-paint'] });
    } catch (e) {
      console.warn('Performance monitoring not supported');
    }
  }
}

// Navigation functionality
function initNavigation() {
  // Highlight current page in navigation
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  const navTabs = document.querySelectorAll('.nav-tab');
  
  navTabs.forEach(tab => {
    const href = tab.getAttribute('href');
    if (href === currentPage) {
      tab.classList.add('active');
    }
  });
}

// Smooth scrolling for anchor links
function initSmoothScrolling() {
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
      }
    });
  });
}

// Analytics tracking
function initAnalytics() {
  // Track page views
  if (typeof umami !== 'undefined') {
    umami.track('page_view', {
      page: window.location.pathname,
      title: document.title
    });
  }
  
  // Track external link clicks
  const externalLinks = document.querySelectorAll('a[href^="http"]');
  externalLinks.forEach(link => {
    link.addEventListener('click', () => {
      if (typeof umami !== 'undefined') {
        umami.track('external_link_click', {
          url: link.href,
          text: link.textContent.trim()
        });
      }
    });
  });
}

// Utility functions
function debounce(func, wait) {
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

// Lazy loading for images
function initLazyLoading() {
  const images = document.querySelectorAll('img[data-src]');
  
  if (images.length === 0) return;
  
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        const src = img.dataset.src;
        
        if (src) {
          img.src = src;
          img.onload = () => {
            img.removeAttribute('data-src');
            img.classList.add('loaded');
          };
          img.onerror = () => {
            console.warn('Failed to load image:', src);
            img.removeAttribute('data-src');
          };
        }
        
        observer.unobserve(img);
      }
    });
  }, {
    rootMargin: '50px 0px',
    threshold: 0.01
  });
  
  images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading if supported
if ('IntersectionObserver' in window) {
  initLazyLoading();
} 