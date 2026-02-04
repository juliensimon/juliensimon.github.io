/**
 * Renders JSON-LD structured data as a script tag.
 * Only used with developer-defined schema objects (never user input),
 * so XSS risk is not applicable here.
 */
export default function StructuredData({ data }: { data: Record<string, unknown> }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
