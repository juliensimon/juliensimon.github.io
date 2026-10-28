import {
  SPEAKING_BIO_LONG,
  SPEAKING_BIO_SHORT,
  SPEAKING_FORMATS,
  SPEAKING_PHOTOS,
  SPEAKING_REQUEST_FIELDS,
  SPEAKING_TOPICS,
  type SpeakingFormat,
  type SpeakingPhoto,
  type SpeakingTopic,
} from './speaking-booking';

export type SpeakingLang = 'en' | 'fr';

export interface SpeakingCopy {
  heroTitle: string;
  heroSubtitle: string;
  ctaRequest: string;
  ctaBio: string;
  switchLabel: string;
  switchHref: string;
  switchLang: SpeakingLang;
  photoCredit: string;
  metrics: { events: string; countries: string; cities: string };
  talksHeading: string;
  talksIntro: string;
  audienceLabel: string;
  formatsHeading: string;
  recentHeading: string;
  mapHeading: string;
  yearsHeading: string | null;
  bioHeading: string;
  bioShort: string;
  bioLong: string;
  bioShortLabel: string;
  bioLongLabel: string;
  requestHeading: string;
  requestIntro: string;
  requestButton: (email: string) => string;
  requestSubject: string;
  linkedinLead: string;
  linkedinTrail: string;
  sessionizeLead: string;
  breadcrumbHome: string;
  breadcrumbPage: string;
  faqHeading: string;
  topics: SpeakingTopic[];
  formats: SpeakingFormat[];
  photos: SpeakingPhoto[];
  requestFields: readonly string[];
}

const EN: SpeakingCopy = {
  heroTitle: 'Keynote Speaker on Enterprise AI',
  heroSubtitle:
    'Keynotes, executive workshops and panels on AI in production, small language models and the AI industry. In English and French.',
  ctaRequest: 'Request a talk',
  ctaBio: 'Bio',
  switchLabel: 'Version française',
  switchHref: '/fr/conferencier-ia',
  switchLang: 'fr',
  photoCredit: 'Photo:',
  metrics: { events: 'Speaking Engagements', countries: 'Countries', cities: 'Cities' },
  talksHeading: 'Sample talks',
  talksIntro:
    'Three examples from a wider range. Julien covers AI strategy, engineering, open models, hardware, cloud and the AI industry, and builds each talk around your audience, your sector and the question you need answered.',
  audienceLabel: 'For',
  formatsHeading: 'Formats',
  recentHeading: 'Recent talks',
  mapHeading: 'Speaking Locations Worldwide',
  yearsHeading: 'Browse by Year',
  bioHeading: 'Bio',
  bioShort: SPEAKING_BIO_SHORT,
  bioLong: SPEAKING_BIO_LONG,
  bioShortLabel: 'Short bio',
  bioLongLabel: 'Long bio',
  requestHeading: 'Request a talk',
  requestIntro:
    'Keynotes and workshops for companies are paid engagements, quoted on the format, the travel and the rights you need. Send the brief below and Julien replies within two business days.',
  requestButton: (email) => `Email the brief to ${email}`,
  requestSubject: 'Speaking request',
  linkedinLead: 'Or message Julien on',
  linkedinTrail: '.',
  sessionizeLead: 'Event organizers can also find Julien on',
  breadcrumbHome: 'Home',
  breadcrumbPage: 'Speaking',
  faqHeading: 'Frequently Asked Questions',
  topics: SPEAKING_TOPICS,
  formats: SPEAKING_FORMATS,
  photos: SPEAKING_PHOTOS,
  requestFields: SPEAKING_REQUEST_FIELDS,
};

const FR: SpeakingCopy = {
  heroTitle: 'Conférencier IA pour l\'entreprise',
  heroSubtitle:
    'Keynotes, ateliers de direction et tables rondes sur l\'IA en production, les petits modèles de langage et l\'industrie de l\'IA. En français et en anglais.',
  ctaRequest: 'Demander une intervention',
  ctaBio: 'Biographie',
  switchLabel: 'English version',
  switchHref: '/speaking',
  switchLang: 'en',
  photoCredit: 'Photo :',
  metrics: { events: 'Interventions', countries: 'Pays', cities: 'Villes' },
  talksHeading: 'Exemples d\'interventions',
  talksIntro:
    'Trois exemples parmi un éventail plus large. Julien couvre la stratégie IA, l\'ingénierie, les modèles ouverts, le matériel, le cloud et l\'industrie de l\'IA, et construit chaque intervention autour de votre public, de votre secteur et de la question à traiter.',
  audienceLabel: 'Pour',
  formatsHeading: 'Formats',
  recentHeading: 'Interventions récentes',
  mapHeading: 'Où Julien est intervenu',
  yearsHeading: null,
  bioHeading: 'Biographie',
  bioShort:
    'Julien Simon est Operating Partner et responsable de l\'AI Studio chez Fortino Capital, où il aide les sociétés du portefeuille à faire passer l\'IA du pilote à la production. Il a dirigé l\'évangélisation chez Arcee AI, Hugging Face et AWS, et écrit The AI Realist, une newsletter fondée sur des sources primaires.',
  bioLong:
    'Julien Simon est Operating Partner et responsable de l\'AI Studio chez Fortino Capital, un fonds de capital-investissement et de capital-risque. Il travaille avec les sociétés du portefeuille sur l\'étape que la plupart des programmes d\'IA manquent : mettre un agent ou un petit modèle de langage en usage quotidien, et mesurer ce qu\'il rapporte. Avant Fortino Capital, il a été VP et Chief Evangelist chez Arcee AI, Chief Evangelist chez Hugging Face, et Global Evangelist pour l\'IA et le machine learning chez AWS. Il est l\'auteur de Learn Amazon SageMaker, anime une chaîne YouTube sur l\'ingénierie de l\'IA, et publie The AI Realist, une newsletter qui lit les documents réglementaires, les fiches de modèles et les textes de loi plutôt que les communiqués de presse. Il intervient en français et en anglais.',
  bioShortLabel: 'Biographie courte',
  bioLongLabel: 'Biographie longue',
  requestHeading: 'Demander une intervention',
  requestIntro:
    'Les keynotes et ateliers pour entreprises sont des prestations payantes, chiffrées selon le format, les déplacements et les droits souhaités. Envoyez le brief ci-dessous, Julien répond sous deux jours ouvrés.',
  requestButton: (email) => `Envoyer le brief à ${email}`,
  requestSubject: 'Demande d\'intervention',
  linkedinLead: 'Ou écrivez à Julien sur',
  linkedinTrail: '.',
  sessionizeLead: 'Les organisateurs d\'événements trouvent aussi Julien sur',
  breadcrumbHome: 'Accueil',
  breadcrumbPage: 'Conférencier IA',
  faqHeading: 'Questions fréquentes',
  topics: [
    {
      title: 'Pourquoi les pilotes d\'IA en entreprise s\'enlisent, et ce que font autrement les équipes en production',
      audience: 'dirigeants, comités exécutifs, responsables de portefeuille',
      takeaway:
        'Cinq erreurs qui empêchent les agents IA d\'atteindre la production, et les changements qui font passer un pilote au compte de résultat.',
    },
    {
      title: 'Petits modèles de langage : gratuits, privés, locaux',
      audience: 'directeurs techniques, responsables ingénierie, équipes produit',
      takeaway:
        'Quand un petit modèle sur votre propre matériel bat une API hébergée sur le coût, la confidentialité et le contrôle, et comment le prouver sur vos données.',
    },
    {
      title: 'Modèles ouverts, souveraineté et matériel : choisir quoi exécuter où',
      audience: 'directeurs techniques, conseils d\'administration, responsables technologiques du secteur public',
      takeaway:
        'Poids ouverts, auto-hébergé et souverain sont trois propriétés différentes. Comment choisir modèles et infrastructure selon la licence, le coût et le périmètre juridique.',
    },
  ],
  formats: [
    {
      name: 'Keynote',
      length: '30 à 45 minutes',
      audience: 'Conférences, événements clients, séminaires de direction',
      description:
        'Un argument, raconté avec des déploiements réels, qui se termine sur ce que le public change dès lundi.',
    },
    {
      name: 'Atelier de direction',
      length: 'Demi-journée',
      audience: 'PDG, comités exécutifs, conseils d\'administration',
      description:
        'Une séance de travail sur votre propre portefeuille d\'IA : quels projets arrêter, lesquels financer, comment mesurer un résultat.',
    },
    {
      name: 'Table ronde ou échange animé',
      length: '30 à 60 minutes',
      audience: 'Journées investisseurs, événements de fondateurs et de portefeuille',
      description: 'Conversation animée, réponses directes et exemples nommés. Aucune slide requise.',
    },
    {
      name: 'Approfondissement technique',
      length: '60 à 90 minutes',
      audience: 'CTO et équipes d\'ingénierie',
      description:
        'Démos en direct sur les petits modèles de langage, l\'inférence locale et l\'évaluation d\'agents, avec le code que l\'équipe conserve.',
    },
  ],
  photos: SPEAKING_PHOTOS.map((p) => ({
    ...p,
    alt: 'Julien Simon face à des dirigeants à La Galerie Bourbon, à Paris, devant une slide sur cinq erreurs qui bloquent l\'IA en entreprise',
    caption: 'Sommet de la Transformation Agentique, La Galerie Bourbon, Paris, 22 septembre 2026',
  })),
  requestFields: [
    'Nom de l\'événement et organisateur',
    'Date et ville, ou en ligne',
    'Public : qui et combien',
    'Format et durée',
    'Langue',
    'Budget ou fourchette de cachet',
    'Plans d\'enregistrement et de diffusion',
  ],
};

export const SPEAKING_COPY: Record<SpeakingLang, SpeakingCopy> = { en: EN, fr: FR };

const FR_MONTHS: Record<string, string> = {
  January: 'janvier',
  February: 'février',
  March: 'mars',
  April: 'avril',
  May: 'mai',
  June: 'juin',
  July: 'juillet',
  August: 'août',
  September: 'septembre',
  October: 'octobre',
  November: 'novembre',
  December: 'décembre',
};

const FR_PLACES: Record<string, string> = {
  Germany: 'Allemagne',
  Netherlands: 'Pays-Bas',
  Online: 'En ligne',
};

/** "October 6, 2026" becomes "6 octobre 2026"; anything else passes through. */
export function formatEventDate(lang: SpeakingLang, date?: string): string | undefined {
  if (!date || lang === 'en') return date;
  const m = /^([A-Z][a-z]+) (\d{1,2}), (\d{4})$/.exec(date);
  if (!m || !FR_MONTHS[m[1]]) return date;
  return `${m[2] === '1' ? '1er' : m[2]} ${FR_MONTHS[m[1]]} ${m[3]}`;
}

export function formatEventLocation(lang: SpeakingLang, location?: string): string | undefined {
  if (!location || lang === 'en') return location;
  return location
    .split(', ')
    .map((part) => FR_PLACES[part] ?? part)
    .join(', ');
}
