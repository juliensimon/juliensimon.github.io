#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Critical optimizations to apply to all pages
const optimizations = {
  // Preload directives to add after existing link tags
  preloadDirectives: `
  <!-- Preload critical images -->
  <link rel="preload" as="image" href="assets/julien.jpg" type="image/jpeg">
  
  <!-- Preload critical CSS -->
  <link rel="preload" href="css/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="css/styles.css"></noscript>
  
  <!-- Preload critical fonts -->
  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap"></noscript>`,

  // Enhanced security headers
  securityHeaders: `
  <!-- Enhanced Security Headers -->
  <meta http-equiv="X-Content-Type-Options" content="nosniff">
  <meta http-equiv="X-Frame-Options" content="DENY">
  <meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
  <meta http-equiv="X-XSS-Protection" content="1; mode=block">
  <meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=(), interest-cohort=()">
  <meta http-equiv="Cross-Origin-Opener-Policy" content="same-origin">
  <meta http-equiv="Cross-Origin-Embedder-Policy" content="require-corp">`,

  // Image optimizations
  imageOptimizations: {
    'assets/julien.jpg': 'loading="eager" width="200" height="200" decoding="async" fetchpriority="high"',
    'class="computer-image"': 'loading="lazy" decoding="async" width="400" height="300"'
  }
};

// Get all HTML files
function getHtmlFiles() {
  const files = fs.readdirSync('.');
  return files.filter(file => file.endsWith('.html') && file !== 'index-redirect.html' && file !== 'redirect.html');
}

// Apply optimizations to a single file
function optimizeFile(filename) {
  console.log(`Optimizing ${filename}...`);
  
  let content = fs.readFileSync(filename, 'utf8');
  
  // Add preload directives
  if (!content.includes('<!-- Preload critical images -->')) {
    const linkEndIndex = content.lastIndexOf('</link>');
    if (linkEndIndex !== -1) {
      const insertIndex = content.indexOf('>', linkEndIndex) + 1;
      content = content.slice(0, insertIndex) + optimizations.preloadDirectives + content.slice(insertIndex);
    }
  }
  
  // Add enhanced security headers
  if (!content.includes('<!-- Enhanced Security Headers -->')) {
    const securityStart = content.indexOf('<!-- Security Headers -->');
    if (securityStart !== -1) {
      const securityEnd = content.indexOf('</head>', securityStart);
      if (securityEnd !== -1) {
        content = content.slice(0, securityStart) + optimizations.securityHeaders + content.slice(securityEnd);
      }
    }
  }
  
  // Optimize images
  Object.entries(optimizations.imageOptimizations).forEach(([search, replacement]) => {
    if (content.includes(search)) {
      // Replace existing attributes
      const regex = new RegExp(`(${search.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}[^>]*?)`, 'g');
      content = content.replace(regex, (match, prefix) => {
        if (match.includes('loading=') || match.includes('decoding=')) {
          return match; // Already optimized
        }
        return prefix + ' ' + replacement;
      });
    }
  });
  
  // Add missing script tag for main.js if not present
  if (!content.includes('js/main.js')) {
    const bodyStart = content.indexOf('<body>');
    if (bodyStart !== -1) {
      const scriptTag = '\n  <script src="js/main.js"></script>';
      content = content.slice(0, bodyStart) + scriptTag + content.slice(bodyStart);
    }
  }
  
  fs.writeFileSync(filename, content);
  console.log(`✅ Optimized ${filename}`);
}

// Main optimization process
function optimizeAllPages() {
  console.log('🚀 Starting comprehensive page optimization...\n');
  
  const htmlFiles = getHtmlFiles();
  console.log(`Found ${htmlFiles.length} HTML files to optimize:\n`);
  
  htmlFiles.forEach(file => {
    try {
      optimizeFile(file);
    } catch (error) {
      console.error(`❌ Error optimizing ${file}:`, error.message);
    }
  });
  
  console.log('\n🎉 Optimization complete!');
  console.log('\n📊 Applied optimizations:');
  console.log('  ✅ Critical resource preloading');
  console.log('  ✅ Enhanced security headers');
  console.log('  ✅ Image optimization attributes');
  console.log('  ✅ JavaScript loading optimization');
  console.log('\n🔍 Next steps:');
  console.log('  - Test all pages for functionality');
  console.log('  - Run Lighthouse audits');
  console.log('  - Verify Core Web Vitals');
}

// Run optimization
if (require.main === module) {
  optimizeAllPages();
}

module.exports = { optimizeAllPages, optimizeFile }; 