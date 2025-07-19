#!/usr/bin/env node

/**
 * Performance Optimization Script for Julien Simon's Website
 * This script applies various performance optimizations to all HTML files
 */

const fs = require('fs');
const path = require('path');
const { minify } = require('terser');
const CleanCSS = require('clean-css');

// Configuration
const config = {
  inputDir: '.',
  outputDir: '.',
  files: [
    'index.html',
    'experience.html',
    'speaking.html',
    'publications.html',
    'code.html',
    'youtube.html',
    'books.html',
    'computers.html'
  ],
  optimizations: {
    minifyCSS: true,
    minifyJS: true,
    optimizeImages: true,
    addResourceHints: true,
    addSecurityHeaders: true,
    addPerformanceHeaders: true
  }
};

// Performance optimizations
class PerformanceOptimizer {
  constructor() {
    this.stats = {
      filesProcessed: 0,
      bytesSaved: 0,
      optimizationsApplied: 0
    };
  }

  async optimizeAll() {
    console.log('🚀 Starting performance optimization...\n');

    for (const file of config.files) {
      if (fs.existsSync(file)) {
        await this.optimizeFile(file);
      }
    }

    this.printStats();
  }

  async optimizeFile(filePath) {
    console.log(`📄 Processing ${filePath}...`);
    
    try {
      let content = fs.readFileSync(filePath, 'utf8');
      const originalSize = Buffer.byteLength(content, 'utf8');
      
      // Apply optimizations
      content = await this.applyOptimizations(content, filePath);
      
      const optimizedSize = Buffer.byteLength(content, 'utf8');
      const bytesSaved = originalSize - optimizedSize;
      
      // Write optimized file
      fs.writeFileSync(filePath, content, 'utf8');
      
      this.stats.filesProcessed++;
      this.stats.bytesSaved += bytesSaved;
      
      console.log(`✅ ${filePath}: ${this.formatBytes(originalSize)} → ${this.formatBytes(optimizedSize)} (${this.formatBytes(bytesSaved)} saved)`);
      
    } catch (error) {
      console.error(`❌ Error processing ${filePath}:`, error.message);
    }
  }

  async applyOptimizations(content, filePath) {
    // Add resource hints
    if (config.optimizations.addResourceHints) {
      content = this.addResourceHints(content);
    }

    // Add security headers
    if (config.optimizations.addSecurityHeaders) {
      content = this.addSecurityHeaders(content);
    }

    // Add performance headers
    if (config.optimizations.addPerformanceHeaders) {
      content = this.addPerformanceHeaders(content);
    }

    // Optimize CSS
    if (config.optimizations.minifyCSS) {
      content = await this.optimizeCSS(content);
    }

    // Optimize JavaScript
    if (config.optimizations.minifyJS) {
      content = await this.optimizeJavaScript(content);
    }

    // Add service worker registration
    content = this.addServiceWorkerRegistration(content);

    // Add performance monitoring
    content = this.addPerformanceMonitoring(content);

    return content;
  }

  addResourceHints(content) {
    const hints = [
      '<link rel="dns-prefetch" href="//fonts.googleapis.com">',
      '<link rel="dns-prefetch" href="//cdnjs.cloudflare.com">',
      '<link rel="dns-prefetch" href="//cloud.umami.is">',
      '<link rel="dns-prefetch" href="//maps.googleapis.com">',
      '<link rel="preconnect" href="https://fonts.googleapis.com">',
      '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
      '<link rel="preconnect" href="https://cdnjs.cloudflare.com">',
      '<link rel="preconnect" href="https://cloud.umami.is">',
      '<link rel="preconnect" href="https://maps.googleapis.com">'
    ].join('\n  ');

    // Add after existing resource hints
    const resourceHintsPattern = /(<link rel="dns-prefetch"[^>]*>)/;
    if (resourceHintsPattern.test(content)) {
      content = content.replace(
        /(<link rel="dns-prefetch"[^>]*>)/,
        `$1\n  ${hints}`
      );
    } else {
      content = content.replace(
        /(<head>)/,
        `$1\n  ${hints}`
      );
    }

    return content;
  }

  addSecurityHeaders(content) {
    const securityHeaders = [
      '<meta http-equiv="X-Content-Type-Options" content="nosniff">',
      '<meta http-equiv="X-Frame-Options" content="DENY">',
      '<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">',
      '<meta http-equiv="X-XSS-Protection" content="1; mode=block">',
      '<meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=(), interest-cohort=(), payment=(), usb=(), magnetometer=(), gyroscope=(), accelerometer=()">',
      '<meta http-equiv="Cross-Origin-Opener-Policy" content="same-origin">',
      '<meta http-equiv="Cross-Origin-Embedder-Policy" content="require-corp">'
    ].join('\n  ');

    // Add if not already present
    if (!content.includes('X-Content-Type-Options')) {
      content = content.replace(
        /(<title>)/,
        `${securityHeaders}\n  $1`
      );
    }

    return content;
  }

  addPerformanceHeaders(content) {
    const performanceHeaders = [
      '<meta http-equiv="Accept-CH" content="DPR, Viewport-Width, Width">',
      '<meta http-equiv="Accept-CH-Lifetime" content="86400">'
    ].join('\n  ');

    // Add if not already present
    if (!content.includes('Accept-CH')) {
      content = content.replace(
        /(<title>)/,
        `${performanceHeaders}\n  $1`
      );
    }

    return content;
  }

  async optimizeCSS(content) {
    // Extract and minify inline CSS
    const cssPattern = /<style[^>]*>([\s\S]*?)<\/style>/g;
    content = content.replace(cssPattern, (match, css) => {
      try {
        const minified = new CleanCSS({
          level: 2,
          format: 'keep-breaks'
        }).minify(css);
        
        this.stats.optimizationsApplied++;
        return match.replace(css, minified.styles);
      } catch (error) {
        console.warn('CSS minification failed:', error.message);
        return match;
      }
    });

    return content;
  }

  async optimizeJavaScript(content) {
    // Extract and minify inline JavaScript
    const jsPattern = /<script[^>]*>([\s\S]*?)<\/script>/g;
    content = content.replace(jsPattern, async (match, js) => {
      try {
        const minified = await minify(js, {
          compress: true,
          mangle: true,
          format: {
            comments: false
          }
        });
        
        this.stats.optimizationsApplied++;
        return match.replace(js, minified.code);
      } catch (error) {
        console.warn('JavaScript minification failed:', error.message);
        return match;
      }
    });

    return content;
  }

  addServiceWorkerRegistration(content) {
    const swRegistration = `
  <script>
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
  </script>`;

    // Add before closing body tag
    if (!content.includes('serviceWorker.register')) {
      content = content.replace(
        /(<\/body>)/,
        `${swRegistration}\n$1`
      );
    }

    return content;
  }

  addPerformanceMonitoring(content) {
    const performanceMonitoring = `
  <script>
    // Performance monitoring
    if ('PerformanceObserver' in window) {
      const observer = new PerformanceObserver((list) => {
        list.getEntries().forEach((entry) => {
          if (entry.entryType === 'largest-contentful-paint') {
            console.log('LCP:', entry.startTime);
          }
        });
      });
      observer.observe({ entryTypes: ['largest-contentful-paint'] });
    }
  </script>`;

    // Add before closing head tag
    if (!content.includes('PerformanceObserver')) {
      content = content.replace(
        /(<\/head>)/,
        `${performanceMonitoring}\n$1`
      );
    }

    return content;
  }

  formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  printStats() {
    console.log('\n📊 Optimization Summary:');
    console.log(`Files processed: ${this.stats.filesProcessed}`);
    console.log(`Bytes saved: ${this.formatBytes(this.stats.bytesSaved)}`);
    console.log(`Optimizations applied: ${this.stats.optimizationsApplied}`);
    console.log('\n✨ Performance optimization complete!');
  }
}

// Run optimization
async function main() {
  try {
    const optimizer = new PerformanceOptimizer();
    await optimizer.optimizeAll();
  } catch (error) {
    console.error('❌ Optimization failed:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = PerformanceOptimizer; 