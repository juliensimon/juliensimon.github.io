import type { Metadata } from 'next';
import { SPEAKING_YEARS } from '@/data/speaking';
import { buildMetadata } from '@/lib/metadata';
import { breadcrumbSchema } from '@/lib/structured-data';
import StructuredData from '@/components/seo/StructuredData';
import SpeakingYearContent from './SpeakingYearContent';

export function generateStaticParams() {
  return SPEAKING_YEARS.map((y) => ({ year: y.year.toString() }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { year } = await params;
  const yearData = SPEAKING_YEARS.find((y) => y.year.toString() === year);
  const count = yearData?.count ?? 0;
  return buildMetadata({
    title: `Speaking ${year}`,
    description: `${count} talks and workshops delivered in ${year} at conferences worldwide on AI, machine learning, and cloud computing.`,
    path: `/speaking/${year}`,
    keywords: [`speaking ${year}`, 'conference talks', 'AI presentations'],
  });
}

interface Props {
  params: Promise<{ year: string }>;
}

export default async function SpeakingYearPage({ params }: Props) {
  const { year } = await params;
  const yearData = SPEAKING_YEARS.find((y) => y.year.toString() === year);

  return (
    <>
      <StructuredData data={breadcrumbSchema([
        { name: 'Home', url: 'https://www.julien.org' },
        { name: 'Speaking', url: 'https://www.julien.org/speaking' },
        { name: `Speaking ${year}`, url: `https://www.julien.org/speaking/${year}` },
      ])} />
      <SpeakingYearContent year={year} count={yearData?.count} />
    </>
  );
}
