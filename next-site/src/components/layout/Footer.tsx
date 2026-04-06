import Link from 'next/link';
import { SITE, NAV_ITEMS, SOCIAL_LINKS } from '@/lib/constants';

const FOOTER_LABEL_OVERRIDES: Record<string, string> = {
  '/code': 'Code & Projects',
  '/computers': 'Computers',
};

const FOOTER_NAV = NAV_ITEMS
  .filter((item) => item.href !== '/')
  .map((item) => ({ label: FOOTER_LABEL_OVERRIDES[item.href] ?? item.label, href: item.href }));

const FOOTER_SOCIAL_HREFS = new Set([
  'https://linkedin.com/in/juliensimon',
  'https://youtube.com/@juliensimonfr',
  'https://www.airealist.ai/',
  'https://github.com/juliensimon',
  'https://x.com/julsimon',
]);

const FOOTER_SOCIAL = SOCIAL_LINKS
  .filter((link) => FOOTER_SOCIAL_HREFS.has(link.href))
  .map((link) => ({ label: link.name, href: link.href }));

export default function Footer() {
  return (
    <footer className="border-t border-border mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid sm:grid-cols-3 gap-8">
          {/* Brand + contact */}
          <div>
            <p className="font-heading font-bold text-text mb-2">Julien Simon</p>
            <p className="text-sm text-text-muted mb-3">AI Operating Partner at Fortino Capital</p>
            <a
              href={`mailto:${SITE.email}`}
              className="text-sm text-primary hover:text-primary-hover font-medium transition-colors"
            >
              {SITE.email}
            </a>
          </div>

          {/* Navigation */}
          <div>
            <p className="text-sm font-semibold text-text mb-3">Pages</p>
            <ul className="space-y-1.5">
              {FOOTER_NAV.map((item) => (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className="text-sm text-text-muted hover:text-primary transition-colors"
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Social + subscribe */}
          <div>
            <p className="text-sm font-semibold text-text mb-3">Connect</p>
            <ul className="space-y-1.5">
              {FOOTER_SOCIAL.map((item) => (
                <li key={item.href}>
                  <a
                    href={item.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-text-muted hover:text-primary transition-colors"
                  >
                    {item.label}
                    <span className="sr-only"> (opens in new tab)</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Newsletter signup */}
        <div className="mt-10 text-center">
          <h3 className="text-lg font-heading font-semibold text-text mb-2">The AI Realist</h3>
          <p className="text-sm text-text-muted mb-4">Practical AI analysis for builders, operators, and investors.</p>
          <a
            href="https://www.airealist.ai/subscribe"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center px-5 py-2.5 text-sm font-medium text-white rounded-lg gradient-brand hover:opacity-90 transition-opacity"
          >
            Subscribe to The AI Realist
            <span className="sr-only"> (opens in new tab)</span>
          </a>
        </div>

        <div className="mt-8 pt-6 border-t border-border text-center text-xs text-text-muted">
          <p>&copy; {new Date().getFullYear()} {SITE.name}</p>
        </div>
      </div>
    </footer>
  );
}
