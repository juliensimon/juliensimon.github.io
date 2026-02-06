import Link from 'next/link';
import { SITE } from '@/lib/constants';

const FOOTER_NAV = [
  { label: 'Experience', href: '/experience' },
  { label: 'Speaking', href: '/speaking' },
  { label: 'Publications', href: '/publications' },
  { label: 'Videos', href: '/youtube-videos' },
] as const;

const FOOTER_SOCIAL = [
  { label: 'LinkedIn', href: 'https://linkedin.com/in/juliensimon' },
  { label: 'YouTube', href: 'https://youtube.com/@juliensimonfr' },
  { label: 'Substack', href: 'https://julsimon.substack.com/' },
  { label: 'GitHub', href: 'https://github.com/juliensimon' },
  { label: 'Twitter/X', href: 'https://x.com/julsimon' },
] as const;

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
          <h3 className="text-lg font-heading font-semibold text-text mb-2">Stay Updated</h3>
          <p className="text-sm text-text-muted mb-4">Get the latest on AI, small language models, and enterprise ML.</p>
          <a
            href="https://julsimon.substack.com/"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center px-5 py-2.5 text-sm font-medium text-white rounded-lg gradient-brand hover:opacity-90 transition-opacity"
          >
            Subscribe on Substack
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
