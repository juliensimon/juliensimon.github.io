#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Performance audit criteria
const auditCriteria = {
  criticalOptimizations: {
    preloadDirectives: {
      description: 'Critical resource preloading',
      check: (content) => content.includes('<!-- Preload critical images -->'),
      weight: 10
    },
    securityHeaders: {
      description: 'Enhanced security headers',
      check: (content) => content.includes('<!-- Enhanced Security Headers -->'),
      weight: 8
    },
    imageOptimization: {
      description: 'Image optimization attributes',
      check: (content) => content.includes('decoding="async"') || content.includes('fetchpriority="high"'),
      weight: 7
    },
    javascriptLoading: {
      description: 'JavaScript loading optimization',
      check: (content) => content.includes('js/main.js'),
      weight: 6
    },
    structuredData: {
      description: 'Structured data markup',
      check: (content) => content.includes('application/ld+json'),
      weight: 8
    },
    metaTags: {
      description: 'Comprehensive meta tags',
      check: (content) => content.includes('og:title') && content.includes('twitter:card'),
      weight: 6
    },
    accessibility: {
      description: 'Accessibility features',
      check: (content) => content.includes('skip-link') && content.includes('aria-label'),
      weight: 7
    },
    responsiveDesign: {
      description: 'Responsive design',
      check: (content) => content.includes('viewport') && content.includes('width=device-width'),
      weight: 6
    },
    fontOptimization: {
      description: 'Font optimization',
      check: (content) => content.includes('font-display: swap') || content.includes('preload.*font'),
      weight: 5
    },
    cssOptimization: {
      description: 'CSS optimization',
      check: (content) => content.includes('contain: layout') || content.includes('will-change'),
      weight: 5
    }
  },
  
  performanceMetrics: {
    fileSize: {
      description: 'File size optimization',
      check: (filePath) => {
        const stats = fs.statSync(filePath);
        const sizeKB = stats.size / 1024;
        return sizeKB < 100; // Less than 100KB
      },
      weight: 4
    },
    imageCount: {
      description: 'Image count optimization',
      check: (content) => {
        const imgMatches = content.match(/<img[^>]+>/g) || [];
        return imgMatches.length <= 20; // Reasonable image count
      },
      weight: 3
    },
    scriptCount: {
      description: 'Script count optimization',
      check: (content) => {
        const scriptMatches = content.match(/<script[^>]*>/g) || [];
        return scriptMatches.length <= 10; // Reasonable script count
      },
      weight: 3
    }
  }
};

// Audit a single file
function auditFile(filename) {
  console.log(`\n🔍 Auditing ${filename}...`);
  
  const content = fs.readFileSync(filename, 'utf8');
  const results = {
    filename,
    score: 0,
    maxScore: 0,
    issues: [],
    passed: []
  };
  
  // Check critical optimizations
  Object.entries(auditCriteria.criticalOptimizations).forEach(([key, criteria]) => {
    results.maxScore += criteria.weight;
    
    if (criteria.check(content)) {
      results.score += criteria.weight;
      results.passed.push(`✅ ${criteria.description}`);
    } else {
      results.issues.push(`❌ Missing: ${criteria.description}`);
    }
  });
  
  // Check performance metrics
  Object.entries(auditCriteria.performanceMetrics).forEach(([key, criteria]) => {
    results.maxScore += criteria.weight;
    
    if (criteria.check(filename, content)) {
      results.score += criteria.weight;
      results.passed.push(`✅ ${criteria.description}`);
    } else {
      results.issues.push(`❌ Issue: ${criteria.description}`);
    }
  });
  
  // Calculate percentage
  results.percentage = Math.round((results.score / results.maxScore) * 100);
  
  return results;
}

// Generate audit report
function generateReport(auditResults) {
  console.log('\n📊 PERFORMANCE AUDIT REPORT');
  console.log('=' .repeat(50));
  
  let totalScore = 0;
  let totalMaxScore = 0;
  let overallIssues = [];
  let overallPassed = [];
  
  auditResults.forEach(result => {
    console.log(`\n📄 ${result.filename}`);
    console.log(`   Score: ${result.score}/${result.maxScore} (${result.percentage}%)`);
    
    if (result.passed.length > 0) {
      console.log('   ✅ Passed:');
      result.passed.forEach(item => console.log(`      ${item}`));
    }
    
    if (result.issues.length > 0) {
      console.log('   ❌ Issues:');
      result.issues.forEach(item => console.log(`      ${item}`));
    }
    
    totalScore += result.score;
    totalMaxScore += result.maxScore;
    overallIssues.push(...result.issues);
    overallPassed.push(...result.passed);
  });
  
  const overallPercentage = Math.round((totalScore / totalMaxScore) * 100);
  
  console.log('\n🎯 OVERALL PERFORMANCE SCORE');
  console.log('=' .repeat(50));
  console.log(`Total Score: ${totalScore}/${totalMaxScore} (${overallPercentage}%)`);
  
  // Grade the performance
  let grade = 'F';
  if (overallPercentage >= 95) grade = 'A+';
  else if (overallPercentage >= 90) grade = 'A';
  else if (overallPercentage >= 85) grade = 'A-';
  else if (overallPercentage >= 80) grade = 'B+';
  else if (overallPercentage >= 75) grade = 'B';
  else if (overallPercentage >= 70) grade = 'B-';
  else if (overallPercentage >= 65) grade = 'C+';
  else if (overallPercentage >= 60) grade = 'C';
  else if (overallPercentage >= 55) grade = 'C-';
  else if (overallPercentage >= 50) grade = 'D';
  
  console.log(`Performance Grade: ${grade}`);
  
  // Summary of issues
  if (overallIssues.length > 0) {
    console.log('\n🚨 CRITICAL ISSUES TO FIX:');
    const uniqueIssues = [...new Set(overallIssues)];
    uniqueIssues.forEach(issue => console.log(`   ${issue}`));
  }
  
  // Recommendations
  console.log('\n💡 RECOMMENDATIONS:');
  if (overallPercentage >= 90) {
    console.log('   🎉 Excellent performance! Your site is well-optimized.');
    console.log('   🔍 Consider running Lighthouse audits for detailed insights.');
  } else if (overallPercentage >= 80) {
    console.log('   👍 Good performance with room for improvement.');
    console.log('   🚀 Focus on the critical issues above.');
  } else if (overallPercentage >= 70) {
    console.log('   ⚠️  Moderate performance issues detected.');
    console.log('   🔧 Prioritize fixing critical optimizations.');
  } else {
    console.log('   🚨 Significant performance issues detected.');
    console.log('   🛠️  Immediate optimization required.');
  }
  
  return {
    overallScore: totalScore,
    overallMaxScore: totalMaxScore,
    overallPercentage,
    grade,
    issues: overallIssues,
    passed: overallPassed
  };
}

// Main audit function
function runPerformanceAudit() {
  console.log('🚀 Starting comprehensive performance audit...\n');
  
  // Get all HTML files
  const files = fs.readdirSync('.');
  const htmlFiles = files.filter(file => 
    file.endsWith('.html') && 
    file !== 'index-redirect.html' && 
    file !== 'redirect.html' &&
    file !== 'critical-css.html'
  );
  
  console.log(`Found ${htmlFiles.length} HTML files to audit:\n`);
  
  // Audit each file
  const auditResults = htmlFiles.map(file => auditFile(file));
  
  // Generate report
  const report = generateReport(auditResults);
  
  // Save detailed report
  const reportData = {
    timestamp: new Date().toISOString(),
    files: auditResults,
    summary: report
  };
  
  fs.writeFileSync('performance-audit-report.json', JSON.stringify(reportData, null, 2));
  console.log('\n📄 Detailed report saved to: performance-audit-report.json');
  
  return report;
}

// Run audit
if (require.main === module) {
  runPerformanceAudit();
}

module.exports = { runPerformanceAudit, auditFile, generateReport }; 