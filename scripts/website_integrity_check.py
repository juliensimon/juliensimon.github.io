#!/usr/bin/env python3
"""
Website Integrity Checker
Verifies that nothing was broken during the alt text generation process.
"""

import os
import re
import glob
from pathlib import Path
from typing import Dict, List, Tuple
import json

class WebsiteIntegrityChecker:
    def __init__(self):
        self.issues = {
            'critical': [],
            'warnings': [],
            'info': []
        }
        self.stats = {
            'files_checked': 0,
            'html_files': 0,
            'images_found': 0,
            'images_with_alt': 0,
            'broken_tags': 0,
            'malformed_html': 0
        }
    
    def add_issue(self, severity: str, file_path: str, issue: str, line_number: int = None):
        """Add an issue to the report."""
        issue_data = {
            'file': file_path,
            'issue': issue,
            'line': line_number
        }
        self.issues[severity].append(issue_data)
    
    def check_html_validity(self, file_path: str, content: str) -> bool:
        """Check basic HTML validity and structure."""
        issues_found = False
        
        # Check for basic HTML structure
        if not re.search(r'<!DOCTYPE\s+html>', content, re.IGNORECASE):
            if 'index.html' in file_path:  # Only flag main pages
                self.add_issue('warnings', file_path, 'Missing DOCTYPE declaration')
                issues_found = True
        
        # Check for unmatched tags
        tag_pattern = r'<(/?)(\w+)[^>]*>'
        tags = re.findall(tag_pattern, content, re.IGNORECASE)
        tag_stack = []
        
        for is_closing, tag_name in tags:
            tag_name = tag_name.lower()
            if tag_name in ['img', 'br', 'hr', 'meta', 'link', 'input']:
                continue  # Self-closing tags
            
            if is_closing:
                if tag_stack and tag_stack[-1] == tag_name:
                    tag_stack.pop()
                else:
                    self.add_issue('warnings', file_path, f'Unmatched closing tag: </{tag_name}>')
                    issues_found = True
            else:
                tag_stack.append(tag_name)
        
        return not issues_found
    
    def check_img_tags(self, file_path: str, content: str) -> Dict[str, int]:
        """Check img tags for validity and alt attributes."""
        img_stats = {
            'total': 0,
            'with_alt': 0,
            'empty_alt': 0,
            'malformed': 0
        }
        
        # Find all img tags
        img_pattern = r'<img([^>]*?)>'
        img_matches = re.finditer(img_pattern, content, re.IGNORECASE)
        
        for match in img_matches:
            img_stats['total'] += 1
            img_tag = match.group(0)
            img_attrs = match.group(1)
            
            # Check for src attribute
            if not re.search(r'src\s*=\s*["\'][^"\']*["\']', img_attrs, re.IGNORECASE):
                self.add_issue('critical', file_path, f'Img tag missing src attribute: {img_tag[:100]}...')
                img_stats['malformed'] += 1
                continue
            
            # Check for alt attribute
            alt_match = re.search(r'alt\s*=\s*["\']([^"\']*)["\']', img_attrs, re.IGNORECASE)
            if alt_match:
                img_stats['with_alt'] += 1
                if not alt_match.group(1).strip():
                    img_stats['empty_alt'] += 1
            else:
                self.add_issue('warnings', file_path, f'Img tag missing alt attribute: {img_tag[:100]}...')
            
            # Check for malformed attributes
            if '=""' in img_tag or 'alt=""' in img_tag:
                # This is actually OK for empty alt
                pass
            elif re.search(r'[a-zA-Z]=[^"\s][^\s>]*[^"\s>](?=\s|>)', img_attrs):
                self.add_issue('warnings', file_path, f'Potentially unquoted attribute in img tag')
        
        return img_stats
    
    def check_file_links(self, file_path: str, content: str) -> bool:
        """Check for broken internal links and missing images."""
        issues_found = False
        base_dir = os.path.dirname(file_path)
        
        # Check image src paths
        img_src_pattern = r'src\s*=\s*["\']([^"\']*)["\']'
        img_srcs = re.findall(img_src_pattern, content, re.IGNORECASE)
        
        for src in img_srcs:
            if src.startswith('http'):
                continue  # External link, skip
            
            # Resolve relative path
            if src.startswith('/'):
                img_path = src[1:]  # Remove leading slash
            else:
                img_path = os.path.join(base_dir, src)
            
            # Normalize path
            img_path = os.path.normpath(img_path)
            
            if not os.path.exists(img_path):
                self.add_issue('critical', file_path, f'Missing image file: {src} (resolved to {img_path})')
                issues_found = True
        
        return not issues_found
    
    def check_encoding_and_syntax(self, file_path: str) -> bool:
        """Check file encoding and basic syntax."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for common encoding issues
            if '\ufffd' in content:  # Unicode replacement character
                self.add_issue('warnings', file_path, 'File contains Unicode replacement characters (encoding issues)')
                return False
            
            # Check for unescaped characters in HTML
            if re.search(r'[<>&](?![a-zA-Z0-9]+;)', content):
                # This is too broad, skip for now
                pass
            
            return True
            
        except UnicodeDecodeError:
            self.add_issue('critical', file_path, 'File encoding error (not valid UTF-8)')
            return False
        except Exception as e:
            self.add_issue('critical', file_path, f'Error reading file: {str(e)}')
            return False
    
    def check_single_file(self, file_path: str) -> bool:
        """Check a single HTML file for integrity."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.add_issue('critical', file_path, f'Cannot read file: {str(e)}')
            return False
        
        # Update stats
        self.stats['files_checked'] += 1
        if file_path.endswith('.html'):
            self.stats['html_files'] += 1
        
        # Run checks
        encoding_ok = self.check_encoding_and_syntax(file_path)
        html_ok = self.check_html_validity(file_path, content)
        links_ok = self.check_file_links(file_path, content)
        
        # Check img tags and update stats
        img_stats = self.check_img_tags(file_path, content)
        self.stats['images_found'] += img_stats['total']
        self.stats['images_with_alt'] += img_stats['with_alt']
        self.stats['broken_tags'] += img_stats['malformed']
        
        return encoding_ok and html_ok and links_ok
    
    def run_integrity_check(self):
        """Run comprehensive integrity check on all HTML files."""
        print("🔍 Starting Website Integrity Check")
        print("=" * 60)
        
        # Find all HTML files
        html_files = glob.glob("**/*.html", recursive=True)
        html_files = [f for f in html_files if not f.startswith('.git')]
        
        print(f"Found {len(html_files)} HTML files to check")
        print()
        
        problematic_files = []
        
        # Check each file
        for file_path in html_files:
            print(f"📄 Checking: {file_path}")
            
            if not self.check_single_file(file_path):
                problematic_files.append(file_path)
                print(f"  ⚠️  Issues found in {file_path}")
            else:
                print(f"  ✅ {file_path} - OK")
        
        # Generate report
        self.generate_report(problematic_files)
    
    def generate_report(self, problematic_files: List[str]):
        """Generate integrity check report."""
        print("\n" + "=" * 60)
        print("🎯 WEBSITE INTEGRITY CHECK REPORT")
        print("=" * 60)
        
        # Summary statistics
        print("📊 SUMMARY STATISTICS:")
        print(f"  Files checked: {self.stats['files_checked']}")
        print(f"  HTML files: {self.stats['html_files']}")
        print(f"  Images found: {self.stats['images_found']}")
        print(f"  Images with alt text: {self.stats['images_with_alt']}")
        if self.stats['images_found'] > 0:
            alt_percentage = (self.stats['images_with_alt'] / self.stats['images_found']) * 100
            print(f"  Alt text coverage: {alt_percentage:.1f}%")
        print(f"  Broken/malformed tags: {self.stats['broken_tags']}")
        print()
        
        # Issues breakdown
        total_issues = len(self.issues['critical']) + len(self.issues['warnings']) + len(self.issues['info'])
        
        if total_issues == 0:
            print("🎉 EXCELLENT! No issues found.")
            print("✅ Website integrity is PERFECT!")
        else:
            print(f"📋 ISSUES FOUND: {total_issues} total")
            
            if self.issues['critical']:
                print(f"🚨 CRITICAL ISSUES: {len(self.issues['critical'])}")
                for issue in self.issues['critical'][:10]:  # Show first 10
                    print(f"  ❌ {issue['file']}: {issue['issue']}")
                if len(self.issues['critical']) > 10:
                    print(f"  ... and {len(self.issues['critical']) - 10} more critical issues")
                print()
            
            if self.issues['warnings']:
                print(f"⚠️  WARNING ISSUES: {len(self.issues['warnings'])}")
                for issue in self.issues['warnings'][:5]:  # Show first 5
                    print(f"  ⚠️  {issue['file']}: {issue['issue']}")
                if len(self.issues['warnings']) > 5:
                    print(f"  ... and {len(self.issues['warnings']) - 5} more warnings")
                print()
        
        # Overall assessment
        critical_count = len(self.issues['critical'])
        warning_count = len(self.issues['warnings'])
        
        print("🎯 OVERALL ASSESSMENT:")
        if critical_count == 0 and warning_count <= 5:
            print("✅ EXCELLENT - Website is in great shape!")
        elif critical_count == 0 and warning_count <= 20:
            print("✅ GOOD - Minor issues only, website is functional")
        elif critical_count <= 5:
            print("⚠️  NEEDS ATTENTION - Some critical issues to fix")
        else:
            print("🚨 URGENT - Multiple critical issues need immediate attention")
        
        print()
        print("📈 ALT TEXT IMPROVEMENT:")
        if self.stats['images_found'] > 0:
            coverage = (self.stats['images_with_alt'] / self.stats['images_found']) * 100
            if coverage >= 95:
                print("🎉 OUTSTANDING alt text coverage!")
            elif coverage >= 85:
                print("✅ EXCELLENT alt text coverage!")
            elif coverage >= 70:
                print("✅ GOOD alt text coverage!")
            else:
                print("⚠️  Alt text coverage needs improvement")

def main():
    """Main function to run the integrity check."""
    checker = WebsiteIntegrityChecker()
    checker.run_integrity_check()

if __name__ == "__main__":
    main() 