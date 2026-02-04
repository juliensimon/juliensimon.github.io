import Link from 'next/link';
import { SPEAKING_YEARS } from '@/data/speaking';
import SpeakingYearContent from './SpeakingYearContent';

export function generateStaticParams() {
  return SPEAKING_YEARS.map((y) => ({ year: y.year.toString() }));
}

interface Props {
  params: Promise<{ year: string }>;
}

export default async function SpeakingYearPage({ params }: Props) {
  const { year } = await params;
  const yearData = SPEAKING_YEARS.find((y) => y.year.toString() === year);

  return <SpeakingYearContent year={year} count={yearData?.count} />;
}
