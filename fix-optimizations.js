#!/usr/bin/env node

const fs = require('fs');

// Get all HTML files
function getHtmlFiles() {
  const files = fs.readdirSync('.');
  return files.filter(file => 
    file.endsWith('.html') && 
    file !== 'index-redirect.html' && 
    file !== 'redirect.html' &&
    file !== 'critical-css.html'
  );
}

// Apply optimizations to a single file
function fixFile(filename) {
  console.log(`🔧 Fixing ${filename}...`);
  
  let content = fs.readFileSync(filename, 'utf8');
  let modified = false;
  
  // 1. Add preload directives if missing
  if (!content.includes('<!-- Preload critical images -->')) {
    const linkEndIndex = content.lastIndexOf('</link>');
    if (linkEndIndex !== -1) {
      const insertIndex = content.indexOf('>', linkEndIndex) + 1;
      const preloadDirectives = `
  <!-- Preload critical images -->
  <link rel="preload" as="image" href="assets/julien.jpg" type="image/jpeg">
  
  <!-- Preload critical CSS -->
  <link rel="preload" href="css/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="css/styles.css"></noscript>
  
  <!-- Preload critical fonts -->
  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap"></noscript>`;
      content = content.slice(0, insertIndex) + preloadDirectives + content.slice(insertIndex);
      modified = true;
    }
  }
  
  // 2. Add enhanced security headers if missing
  if (!content.includes('<!-- Enhanced Security Headers -->')) {
    const securityStart = content.indexOf('<!-- Security Headers -->');
    if (securityStart !== -1) {
      const securityEnd = content.indexOf('</head>', securityStart);
      if (securityEnd !== -1) {
        const enhancedHeaders = `
  <!-- Enhanced Security Headers -->
  <meta http-equiv="X-Content-Type-Options" content="nosniff">
  <meta http-equiv="X-Frame-Options" content="DENY">
  <meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
  <meta http-equiv="X-XSS-Protection" content="1; mode=block">
  <meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=(), interest-cohort=()">
  <meta http-equiv="Cross-Origin-Opener-Policy" content="same-origin">
  <meta http-equiv="Cross-Origin-Embedder-Policy" content="require-corp">`;
        content = content.slice(0, securityStart) + enhancedHeaders + content.slice(securityEnd);
        modified = true;
      }
    }
  }
  
  // 3. Add structured data if missing
  if (!content.includes('application/ld+json')) {
    const headEnd = content.indexOf('</head>');
    if (headEnd !== -1) {
      const structuredData = `
  
  <!-- Structured Data -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "${filename.replace('.html', '')}",
    "description": "Page from Julien Simon's personal website",
    "author": {
      "@type": "Person",
      "name": "Julien Simon",
      "jobTitle": "Chief Evangelist",
      "worksFor": {
        "@type": "Organization",
        "name": "Arcee AI"
      }
    }
  }
  </script>`;
      content = content.slice(0, headEnd) + structuredData + content.slice(headEnd);
      modified = true;
    }
  }
  
  // 4. Add accessibility features if missing
  if (!content.includes('skip-link')) {
    const bodyStart = content.indexOf('<body>');
    if (bodyStart !== -1) {
      const skipLink = `
  <a href="#main-content" class="skip-link">Skip to main content</a>`;
      content = content.slice(0, bodyStart + 6) + skipLink + content.slice(bodyStart + 6);
      modified = true;
    }
  }
  
  // 5. Add main-content ID if missing
  if (!content.includes('id="main-content"')) {
    const mainStart = content.indexOf('<main');
    if (mainStart !== -1) {
      const mainEnd = content.indexOf('>', mainStart);
      if (mainEnd !== -1) {
        const mainTag = content.slice(mainStart, mainEnd);
        if (!mainTag.includes('id=')) {
          const newMainTag = mainTag + ' id="main-content"';
          content = content.slice(0, mainStart) + newMainTag + content.slice(mainEnd);
          modified = true;
        }
      }
    }
  }
  
  // 6. Add aria-label to navigation if missing
  if (!content.includes('aria-label="Main navigation"')) {
    const navStart = content.indexOf('class="nav-tabs"');
    if (navStart !== -1) {
      const navEnd = content.indexOf('>', navStart);
      if (navEnd !== -1) {
        const navTag = content.slice(navStart, navEnd);
        if (!navTag.includes('aria-label=')) {
          const newNavTag = navTag + ' role="navigation" aria-label="Main navigation"';
          content = content.slice(0, navStart) + newNavTag + content.slice(navEnd);
          modified = true;
        }
      }
    }
  }
  
  // 7. Add JavaScript loading if missing
  if (!content.includes('js/main.js')) {
    const bodyEnd = content.indexOf('</body>');
    if (bodyEnd !== -1) {
      const scriptTag = `
  <script src="js/main.js"></script>`;
      content = content.slice(0, bodyEnd) + scriptTag + content.slice(bodyEnd);
      modified = true;
    }
  }
  
  // 8. Optimize images
  if (content.includes('assets/julien.jpg') && !content.includes('fetchpriority="high"')) {
    content = content.replace(
      /<img([^>]*?)src="assets\/julien\.jpg"([^>]*?)>/g,
      '<img$1src="assets/julien.jpg" loading="eager" width="200" height="200" decoding="async" fetchpriority="high"$2>'
    );
    modified = true;
  }
  
  if (modified) {
    fs.writeFileSync(filename, content);
    console.log(`✅ Fixed ${filename}`);
  } else {
    console.log(`✅ ${filename} already optimized`);
  }
}

// Main function
function fixAllOptimizations() {
  console.log('🚀 Fixing missing optimizations across all pages...\n');
  
  const htmlFiles = getHtmlFiles();
  console.log(`Found ${htmlFiles.length} HTML files to fix:\n`);
  
  htmlFiles.forEach(file => {
    try {
      fixFile(file);
    } catch (error) {
      console.error(`❌ Error fixing ${file}:`, error.message);
    }
  });
  
  console.log('\n🎉 Optimization fixes complete!');
  console.log('\n📊 Applied fixes:');
  console.log('  ✅ Critical resource preloading');
  console.log('  ✅ Enhanced security headers');
  console.log('  ✅ Structured data markup');
  console.log('  ✅ Accessibility features');
  console.log('  ✅ Image optimization');
  console.log('  ✅ JavaScript loading');
  console.log('\n🔍 Run performance-audit.js again to verify improvements');
}

// Run fixes
if (require.main === module) {
  fixAllOptimizations();
}

module.exports = { fixAllOptimizations, fixFile }; 