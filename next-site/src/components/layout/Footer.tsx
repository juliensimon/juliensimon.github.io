import { SITE } from '@/lib/constants';

export default function Footer() {
  return (
    <footer className="border-t border-border py-8 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-text-muted">
        <p>&copy; {new Date().getFullYear()} {SITE.name}</p>
      </div>
    </footer>
  );
}
