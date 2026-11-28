/**
 * Serializes data as JSON for a JSON-LD script block. Every `<` is written as its JSON
 * unicode escape, so a string containing `</script>` cannot close the block.
 * JSON.parse returns the original data.
 */
export function serializeJsonLd(data: Record<string, unknown>): string {
  return JSON.stringify(data).replace(/</g, '\\u003c');
}

/**
 * Renders JSON-LD structured data as a script tag.
 * The data is mostly developer-defined, but some of it comes from feed text, so the
 * output goes through serializeJsonLd, which escapes `<`.
 */
export default function StructuredData({ data }: { data: Record<string, unknown> }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: serializeJsonLd(data) }}
    />
  );
}
