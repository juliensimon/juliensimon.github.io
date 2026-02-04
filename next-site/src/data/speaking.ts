export interface SpeakingYear {
  year: number;
  count: number;
}

export const SPEAKING_STATS = {
  totalEvents: 684,
  countries: 37,
  cities: 95,
} as const;

export const SPEAKING_YEARS: SpeakingYear[] = [
  { year: 2025, count: 19 },
  { year: 2024, count: 44 },
  { year: 2023, count: 87 },
  { year: 2022, count: 65 },
  { year: 2021, count: 73 },
  { year: 2020, count: 90 },
  { year: 2019, count: 115 },
  { year: 2018, count: 97 },
  { year: 2017, count: 55 },
  { year: 2016, count: 39 },
];
