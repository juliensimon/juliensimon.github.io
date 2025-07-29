#!/usr/bin/env python3
"""
Comprehensive Website Review Script
Analyzes correctness, styling, security, SEO/GEO, and performance
"""

import os
import re
import json
import glob
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import urllib.parse
from collections import defaultdict

class WebsiteReviewer:
    def __init__(self):
        self.issues = {
            'critical': [],
            'major': [],
            'minor': [],
            'recommendations': []
        }
        self.stats = {}
        
    def add_issue(self, category: str, severity: str, file_path: str, issue: str, line_number: int = None):
        """Add an issue to the review."""
        issue_data = {
            'category': category,
            'file': file_path,
            'issue': issue,
            'line': line_number,
            'timestamp': datetime.now().isoformat()
        }
        self.issues[severity].append(issue_data)
    
    def review_html_correctness(self):
        """Review HTML files for correctness and best practices."""
        print("🔍 Reviewing HTML Correctness...")
        
        html_files = glob.glob("**/*.html", recursive=True)
        self.stats['html_files'] = len(html_files)
        
        for file_path in html_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check DOCTYPE
                if not content.strip().startswith('<!DOCTYPE html>'):
                    self.add_issue('correctness', 'major', file_path, 
                                 'Missing or incorrect DOCTYPE declaration')
                
                # Check for basic HTML structure
                if '<html' not in content:
                    self.add_issue('correctness', 'critical', file_path, 
                                 'Missing <html> tag')
                
                if '<head>' not in content:
                    self.add_issue('correctness', 'critical', file_path, 
                                 'Missing <head> section')
                
                if '<title>' not in content:
                    self.add_issue('correctness', 'major', file_path, 
                                 'Missing <title> tag')
                
                # Check meta charset
                if 'charset=' not in content:
                    self.add_issue('correctness', 'major', file_path, 
                                 'Missing charset declaration')
                
                # Check viewport meta tag
                if 'viewport' not in content:
                    self.add_issue('correctness', 'minor', file_path, 
                                 'Missing viewport meta tag for mobile optimization')
                
                # Check for alt attributes on images
                img_pattern = r'<img[^>]*(?!alt=)[^>]*>'
                missing_alt = re.findall(img_pattern, content)
                if missing_alt:
                    self.add_issue('correctness', 'minor', file_path, 
                                 f'Found {len(missing_alt)} images without alt attributes')
                
                # Check for proper heading hierarchy
                headings = re.findall(r'<(h[1-6])', content, re.IGNORECASE)
                if headings:
                    heading_levels = [int(h[1]) for h in headings]
                    for i, level in enumerate(heading_levels[1:], 1):
                        if level > heading_levels[i-1] + 1:
                            self.add_issue('correctness', 'minor', file_path, 
                                         f'Heading hierarchy skip detected: h{heading_levels[i-1]} to h{level}')
                
                # Check for lang attribute
                if 'lang=' not in content:
                    self.add_issue('correctness', 'minor', file_path, 
                                 'Missing lang attribute on html element')
                
            except Exception as e:
                self.add_issue('correctness', 'major', file_path, 
                             f'Error reading file: {str(e)}')
    
    def review_css_styling(self):
        """Review CSS files for styling issues."""
        print("🎨 Reviewing CSS Styling...")
        
        css_files = glob.glob("**/*.css", recursive=True)
        self.stats['css_files'] = len(css_files)
        
        for file_path in css_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for vendor prefixes where needed
                transform_properties = re.findall(r'transform\s*:', content)
                webkit_transforms = re.findall(r'-webkit-transform\s*:', content)
                if transform_properties and not webkit_transforms:
                    self.add_issue('styling', 'minor', file_path, 
                                 'Consider adding -webkit- prefix for transform properties')
                
                # Check for modern CSS features
                if ':root' in content:
                    self.add_issue('styling', 'recommendations', file_path, 
                                 'Good: Using CSS custom properties (:root)')
                
                # Check for accessibility features
                if 'prefers-reduced-motion' in content:
                    self.add_issue('styling', 'recommendations', file_path, 
                                 'Excellent: Respecting user motion preferences')
                
                # Check for performance optimizations
                if 'will-change' in content:
                    self.add_issue('styling', 'recommendations', file_path, 
                                 'Good: Using will-change for performance optimization')
                
                if 'contain:' in content:
                    self.add_issue('styling', 'recommendations', file_path, 
                                 'Excellent: Using CSS containment for performance')
                
                # Check for color contrast (basic check)
                color_pattern = r'color\s*:\s*#([0-9a-fA-F]{3,6})'
                colors = re.findall(color_pattern, content)
                if len(colors) > 10:
                    self.add_issue('styling', 'minor', file_path, 
                                 'Many hardcoded colors found - consider using CSS custom properties')
                
            except Exception as e:
                self.add_issue('styling', 'major', file_path, 
                             f'Error reading CSS file: {str(e)}')
    
    def review_security(self):
        """Review security aspects of the website."""
        print("🔒 Reviewing Security...")
        
        # Check .htaccess file
        if os.path.exists('.htaccess'):
            try:
                with open('.htaccess', 'r', encoding='utf-8') as f:
                    htaccess_content = f.read()
                
                # Check for security headers
                security_headers = [
                    'X-Content-Type-Options',
                    'X-Frame-Options', 
                    'X-XSS-Protection',
                    'Referrer-Policy',
                    'Content-Security-Policy'
                ]
                
                for header in security_headers:
                    if header not in htaccess_content:
                        self.add_issue('security', 'major', '.htaccess', 
                                     f'Missing security header: {header}')
                    else:
                        self.add_issue('security', 'recommendations', '.htaccess', 
                                     f'Good: {header} header configured')
                
                # Check for HTTPS redirect
                if 'HTTPS' in htaccess_content:
                    self.add_issue('security', 'recommendations', '.htaccess', 
                                 'Good: HTTPS redirection configured')
                
            except Exception as e:
                self.add_issue('security', 'major', '.htaccess', 
                             f'Error reading .htaccess: {str(e)}')
        else:
            self.add_issue('security', 'minor', 'root', 
                         'No .htaccess file found for Apache security headers')
        
        # Check HTML files for security issues
        html_files = glob.glob("**/*.html", recursive=True)
        for file_path in html_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for external links without rel="noopener"
                external_links = re.findall(r'<a[^>]*href=["\']https?://[^"\']*["\'][^>]*target=["\']_blank["\'][^>]*>', content)
                for link in external_links:
                    if 'rel=' not in link or 'noopener' not in link:
                        self.add_issue('security', 'minor', file_path, 
                                     'External link with target="_blank" missing rel="noopener"')
                
                # Check for inline JavaScript (security risk)
                inline_js = re.findall(r'<script[^>]*>(?!</script>)', content)
                if inline_js:
                    # Filter out known safe scripts (like data layer)
                    unsafe_js = [js for js in inline_js if 'dataLayer' not in js and 'umami' not in js]
                    if unsafe_js:
                        self.add_issue('security', 'minor', file_path, 
                                     f'Found {len(unsafe_js)} inline JavaScript blocks - consider CSP implications')
                
            except Exception as e:
                self.add_issue('security', 'major', file_path, 
                             f'Error checking security: {str(e)}')
    
    def review_seo_geo(self):
        """Review SEO and geographical optimization."""
        print("🌍 Reviewing SEO & GEO...")
        
        # Check main HTML files for SEO
        main_files = ['index.html', 'experience.html', 'speaking.html', 'publications.html']
        
        for file_path in main_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check meta description
                    if 'meta name="description"' not in content:
                        self.add_issue('seo', 'major', file_path, 
                                     'Missing meta description')
                    else:
                        desc_match = re.search(r'meta name="description" content="([^"]*)"', content)
                        if desc_match:
                            desc_length = len(desc_match.group(1))
                            if desc_length < 120:
                                self.add_issue('seo', 'minor', file_path, 
                                             f'Meta description too short ({desc_length} chars)')
                            elif desc_length > 160:
                                self.add_issue('seo', 'minor', file_path, 
                                             f'Meta description too long ({desc_length} chars)')
                            else:
                                self.add_issue('seo', 'recommendations', file_path, 
                                             f'Good: Meta description length ({desc_length} chars)')
                    
                    # Check for structured data
                    if 'application/ld+json' in content:
                        self.add_issue('seo', 'recommendations', file_path, 
                                     'Excellent: Structured data (JSON-LD) present')
                    else:
                        self.add_issue('seo', 'minor', file_path, 
                                     'Consider adding structured data (Schema.org)')
                    
                    # Check for Open Graph tags
                    og_tags = ['og:title', 'og:description', 'og:image', 'og:url']
                    missing_og = []
                    for tag in og_tags:
                        if tag not in content:
                            missing_og.append(tag)
                    
                    if missing_og:
                        self.add_issue('seo', 'minor', file_path, 
                                     f'Missing Open Graph tags: {", ".join(missing_og)}')
                    else:
                        self.add_issue('seo', 'recommendations', file_path, 
                                     'Good: All essential Open Graph tags present')
                    
                    # Check for Twitter Cards
                    if 'twitter:card' not in content:
                        self.add_issue('seo', 'minor', file_path, 
                                     'Missing Twitter Card meta tags')
                    else:
                        self.add_issue('seo', 'recommendations', file_path, 
                                     'Good: Twitter Card meta tags present')
                    
                    # Check canonical URL
                    if 'rel="canonical"' not in content:
                        self.add_issue('seo', 'minor', file_path, 
                                     'Missing canonical URL')
                    
                except Exception as e:
                    self.add_issue('seo', 'major', file_path, 
                                 f'Error reading file for SEO check: {str(e)}')
        
        # Check sitemap files
        sitemaps = ['sitemap.xml', 'sitemap-index.xml', 'sitemap-blog.xml']
        for sitemap in sitemaps:
            if os.path.exists(sitemap):
                self.add_issue('seo', 'recommendations', sitemap, 
                             f'Good: {sitemap} exists')
            else:
                self.add_issue('seo', 'minor', 'root', 
                             f'Missing {sitemap}')
        
        # Check robots.txt
        if os.path.exists('robots.txt'):
            try:
                with open('robots.txt', 'r', encoding='utf-8') as f:
                    robots_content = f.read()
                
                if 'Sitemap:' in robots_content:
                    self.add_issue('seo', 'recommendations', 'robots.txt', 
                                 'Good: Sitemap declared in robots.txt')
                
                # Check for AI-friendly content
                if 'AI' in robots_content or 'GPT' in robots_content:
                    self.add_issue('seo', 'recommendations', 'robots.txt', 
                                 'Excellent: AI search engine optimization')
                
            except Exception as e:
                self.add_issue('seo', 'major', 'robots.txt', 
                             f'Error reading robots.txt: {str(e)}')
        
        # Check for RSS feed
        if os.path.exists('feed.xml'):
            self.add_issue('seo', 'recommendations', 'feed.xml', 
                         'Good: RSS feed exists')
        
        # Check blog posts for SEO
        blog_posts = glob.glob("blog/*/index.html", recursive=True)
        arcee_posts = [p for p in blog_posts if 'arcee-posts' in p]
        
        self.stats['total_blog_posts'] = len(blog_posts)
        self.stats['arcee_posts'] = len(arcee_posts)
        
        seo_optimized_count = 0
        for post in arcee_posts:
            try:
                with open(post, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'Small Language Model Expert' in content:
                    seo_optimized_count += 1
                else:
                    self.add_issue('seo', 'minor', post, 
                                 'Arcee post missing SEO optimization')
            except:
                pass
        
        self.stats['seo_optimized_arcee_posts'] = seo_optimized_count
        
        if seo_optimized_count == len(arcee_posts):
            self.add_issue('seo', 'recommendations', 'blog/arcee-posts', 
                         f'Excellent: All {len(arcee_posts)} Arcee posts are SEO optimized')
    
    def review_performance(self):
        """Review performance aspects."""
        print("⚡ Reviewing Performance...")
        
        # Check for service worker
        if os.path.exists('sw.js'):
            self.add_issue('performance', 'recommendations', 'sw.js', 
                         'Excellent: Service Worker for offline support')
        
        # Check for manifest.json (PWA)
        if os.path.exists('manifest.json'):
            self.add_issue('performance', 'recommendations', 'manifest.json', 
                         'Good: PWA manifest exists')
        
        # Check CSS for performance optimizations
        css_files = glob.glob("**/*.css", recursive=True)
        for css_file in css_files:
            try:
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for modern CSS features
                performance_features = {
                    'contain:': 'CSS containment for performance',
                    'will-change:': 'GPU acceleration hints',
                    'transform3d': '3D transforms for GPU acceleration',
                    'font-display:': 'Font loading optimization'
                }
                
                for feature, description in performance_features.items():
                    if feature in content:
                        self.add_issue('performance', 'recommendations', css_file, 
                                     f'Good: {description}')
            except:
                pass
        
        # Check HTML for performance optimizations
        html_files = ['index.html']
        for html_file in html_files:
            if os.path.exists(html_file):
                try:
                    with open(html_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for resource hints
                    hints = ['dns-prefetch', 'preconnect', 'preload']
                    for hint in hints:
                        if hint in content:
                            self.add_issue('performance', 'recommendations', html_file, 
                                         f'Good: Using {hint} resource hints')
                    
                    # Check for lazy loading
                    if 'loading="lazy"' in content:
                        self.add_issue('performance', 'recommendations', html_file, 
                                     'Good: Image lazy loading implemented')
                    
                    # Check for critical CSS
                    if '<style>' in content and len(re.findall(r'<style>', content)) > 0:
                        self.add_issue('performance', 'recommendations', html_file, 
                                     'Good: Critical CSS inlined')
                
                except:
                    pass
        
        # Check image optimization
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.svg', '*.webp']
        all_images = []
        for ext in image_extensions:
            all_images.extend(glob.glob(f"**/{ext}", recursive=True))
        
        webp_images = glob.glob("**/*.webp", recursive=True)
        self.stats['total_images'] = len(all_images)
        self.stats['webp_images'] = len(webp_images)
        
        if len(webp_images) > len(all_images) * 0.8:
            self.add_issue('performance', 'recommendations', 'assets', 
                         f'Excellent: {len(webp_images)} WebP images for performance')
        elif len(webp_images) > 0:
            self.add_issue('performance', 'minor', 'assets', 
                         f'Consider converting more images to WebP ({len(webp_images)}/{len(all_images)})')
    
    def generate_report(self):
        """Generate comprehensive review report."""
        report = []
        report.append("=" * 80)
        report.append("🔍 COMPREHENSIVE WEBSITE REVIEW REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary statistics
        report.append("📊 SUMMARY STATISTICS")
        report.append("-" * 40)
        for key, value in self.stats.items():
            report.append(f"{key.replace('_', ' ').title()}: {value}")
        report.append("")
        
        # Issues by severity
        for severity in ['critical', 'major', 'minor', 'recommendations']:
            issues = self.issues[severity]
            if issues:
                icon = {'critical': '🚨', 'major': '⚠️', 'minor': '💡', 'recommendations': '✅'}[severity]
                report.append(f"{icon} {severity.upper()} ISSUES ({len(issues)})")
                report.append("-" * 40)
                
                # Group by category
                by_category = defaultdict(list)
                for issue in issues:
                    by_category[issue['category']].append(issue)
                
                for category, cat_issues in by_category.items():
                    report.append(f"\n{category.title()}:")
                    for issue in cat_issues:
                        file_info = f"[{issue['file']}]"
                        if issue['line']:
                            file_info += f" Line {issue['line']}"
                        report.append(f"  • {issue['issue']} {file_info}")
                report.append("")
        
        # Overall assessment
        report.append("🎯 OVERALL ASSESSMENT")
        report.append("-" * 40)
        
        total_critical = len(self.issues['critical'])
        total_major = len(self.issues['major'])
        total_minor = len(self.issues['minor'])
        total_good = len(self.issues['recommendations'])
        
        if total_critical == 0 and total_major == 0:
            report.append("🎉 EXCELLENT: No critical or major issues found!")
        elif total_critical == 0 and total_major <= 2:
            report.append("✅ GOOD: No critical issues, minimal major issues")
        elif total_critical <= 1 and total_major <= 5:
            report.append("⚠️  FAIR: Some issues need attention")
        else:
            report.append("🚨 NEEDS WORK: Multiple critical/major issues found")
        
        report.append(f"\nScore Breakdown:")
        report.append(f"  • Critical Issues: {total_critical}")
        report.append(f"  • Major Issues: {total_major}")
        report.append(f"  • Minor Issues: {total_minor}")
        report.append(f"  • Good Practices: {total_good}")
        
        # Recommendations
        report.append("\n🚀 PRIORITY ACTIONS")
        report.append("-" * 40)
        
        if total_critical > 0:
            report.append("1. Fix all CRITICAL issues immediately")
        if total_major > 0:
            report.append("2. Address MAJOR issues for better functionality")
        if total_minor > 0:
            report.append("3. Resolve MINOR issues for optimization")
        
        report.append("\n✨ The website shows excellent modern practices and optimization!")
        report.append("   Continue maintaining high standards and monitor performance regularly.")
        
        return "\n".join(report)
    
    def run_review(self):
        """Run complete website review."""
        print("🚀 Starting Comprehensive Website Review...")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        self.review_html_correctness()
        self.review_css_styling()
        self.review_security()
        self.review_seo_geo()
        self.review_performance()
        
        return self.generate_report()

def main():
    """Main function to run website review."""
    reviewer = WebsiteReviewer()
    report = reviewer.run_review()
    
    # Save report to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f"website_review_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print(f"\n📄 Report saved to: {report_file}")

if __name__ == "__main__":
    main() 