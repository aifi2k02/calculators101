// Central site configuration — change domain and indexing flag here only.
// Set allowIndexing to true only when the site is ready for public launch.

const siteConfig = {
  allowIndexing: true,
  siteUrl: 'https://supercalculator.xyz',
  siteName: 'Super Calculator',
  siteDescription:
    'Free online calculators for finance, fitness, math, and everyday life. Mortgage, BMI, calorie, loan, TDEE, and 130+ more — fast, accurate, no sign-up.',
  twitterHandle: '@supercalculator',
  locale: 'en_US',
  defaultOgType: 'website' as const,
} as const

export default siteConfig
