import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema, webPageSchema, dataCatalogSchema, faqSchema, DATASETS_FAQS } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import Breadcrumbs from '@/components/ui/Breadcrumbs';
import { SITE } from '@/lib/constants';
import { FEATURED_DATASETS, TOTAL_DATASETS } from '@/data/datasets';
import DatasetsContent from './DatasetsContent';

export const metadata = buildMetadata({
  title: `${TOTAL_DATASETS} Space Datasets — Astronomy & Physics`,
  description: `${TOTAL_DATASETS} open datasets for orbital mechanics, space weather, astronomy, and physics. Parquet format on Hugging Face, sourced from NASA, ESA, NOAA, and more.`,
  path: '/datasets',
  keywords: [
    'space datasets',
    'astronomy data',
    'orbital mechanics',
    'space weather',
    'Hugging Face datasets',
    'NASA open data',
    'Parquet',
  ],
});

export default function DatasetsPage() {
  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: SITE.url },
        { name: 'Datasets', url: `${SITE.url}/datasets` },
      ])} />
      <StructuredData data={webPageSchema(
        'Space Datasets',
        `${TOTAL_DATASETS} open datasets for orbital mechanics, space weather, astronomy, and physics on Hugging Face.`,
        `${SITE.url}/datasets`,
      )} />
      <StructuredData data={dataCatalogSchema(FEATURED_DATASETS)} />
      <StructuredData data={faqSchema(DATASETS_FAQS, `${SITE.url}/datasets`)} />
      <Breadcrumbs items={[
        { name: 'Home', href: '/' },
        { name: 'Datasets', href: '/datasets' },
      ]} />
      <DatasetsContent />
    </>
  );
}
