// Central site configuration — change domain and indexing flag here only.
// Set allowIndexing to true only when the site is ready for public launch.

const siteConfig = {
  allowIndexing: false,
  siteUrl: 'https://www.calculatorsforfree.com',
  siteName: 'Calculators for Free',
  siteDescription:
    'Free online calculators for finance, fitness, math, and everyday life. Mortgage, BMI, calorie, loan, TDEE, and 130+ more — fast, accurate, no sign-up.',
  twitterHandle: '@calcsforfree',
  locale: 'en_US',
  defaultOgType: 'website' as const,
} as const

export default siteConfig
