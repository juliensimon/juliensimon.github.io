import StructuredData from '@/components/seo/StructuredData';
import { faqSchema } from '@/lib/structured-data';

interface FaqSectionProps {
  faqs: readonly { question: string; answer: string }[];
  pageUrl: string;
}

/**
 * Renders a page's FAQs as visible text together with the matching FAQPage
 * JSON-LD, so the markup never describes content a reader cannot see.
 */
export default function FaqSection({ faqs, pageUrl }: FaqSectionProps) {
  return (
    <section aria-labelledby="faq-heading" className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
      <StructuredData data={faqSchema([...faqs], pageUrl)} />
      <h2 id="faq-heading" className="text-2xl font-bold font-heading gradient-brand-text mb-6 text-center">
        Frequently Asked Questions
      </h2>
      <dl className="space-y-4">
        {faqs.map((faq) => (
          <div key={faq.question} className="glass-card rounded-xl p-6">
            <dt className="text-lg font-semibold text-text mb-2">{faq.question}</dt>
            <dd className="text-sm text-text-muted leading-relaxed">{faq.answer}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}
