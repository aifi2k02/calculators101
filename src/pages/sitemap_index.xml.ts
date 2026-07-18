import type { APIRoute } from 'astro'
import siteConfig from '../lib/siteConfig'
const siteUrl = siteConfig.siteUrl

const pages = [
  { url: '/', priority: '1.0', changefreq: 'weekly' },
  // Category pages
  { url: '/calculators/financial', priority: '0.9', changefreq: 'weekly' },
  { url: '/calculators/fitness', priority: '0.9', changefreq: 'weekly' },
  { url: '/calculators/math', priority: '0.9', changefreq: 'weekly' },
  { url: '/calculators/other', priority: '0.9', changefreq: 'weekly' },
  // Financial calculators
  { url: '/calculators/mortgage-calculator', priority: '0.85', changefreq: 'monthly' },
  { url: '/calculators/loan-calculator', priority: '0.85', changefreq: 'monthly' },
  { url: '/calculators/compound-interest-calculator', priority: '0.85', changefreq: 'monthly' },
  { url: '/calculators/savings-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/retirement-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/investment-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/auto-loan-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/interest-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/credit-card-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/debt-payoff-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/inflation-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/roi-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/salary-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/budget-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/net-worth-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/amortization-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/house-affordability-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/refinance-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/down-payment-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/paycheck-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/401k-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/rent-vs-buy-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/currency-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/apr-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/car-lease-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/home-equity-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/cd-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/stock-profit-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/break-even-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/markup-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/mortgage-points-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/income-tax-calculator', priority: '0.85', changefreq: 'yearly' },
  { url: '/calculators/roth-ira-calculator', priority: '0.8', changefreq: 'yearly' },
  { url: '/calculators/pmi-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/emergency-fund-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/fire-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/capital-gains-calculator', priority: '0.8', changefreq: 'yearly' },
  // Fitness calculators
  { url: '/calculators/bmi-calculator', priority: '0.85', changefreq: 'monthly' },
  { url: '/calculators/calorie-calculator', priority: '0.85', changefreq: 'monthly' },
  { url: '/calculators/tdee-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/body-fat-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/ideal-weight-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/macro-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/heart-rate-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/water-intake-calculator', priority: '0.7', changefreq: 'monthly' },
  { url: '/calculators/due-date-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/ovulation-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/pace-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/sleep-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/calories-burned-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/protein-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/waist-hip-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/one-rep-max-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/bac-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/bmr-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/lean-body-mass-calculator', priority: '0.7', changefreq: 'monthly' },
  { url: '/calculators/caloric-deficit-calculator', priority: '0.8', changefreq: 'monthly' },
  // Math calculators
  { url: '/calculators/percentage-calculator', priority: '0.85', changefreq: 'monthly' },
  { url: '/calculators/average-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/fraction-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/ratio-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/area-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/volume-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/triangle-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/exponent-calculator', priority: '0.7', changefreq: 'monthly' },
  { url: '/calculators/square-root-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/logarithm-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/lcm-gcd-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/random-number-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/binary-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/quadratic-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/unit-converter-calculator', priority: '0.85', changefreq: 'monthly' },
  { url: '/calculators/scientific-notation-calculator', priority: '0.7', changefreq: 'monthly' },
  { url: '/calculators/combination-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/factorial-calculator', priority: '0.7', changefreq: 'monthly' },
  { url: '/calculators/prime-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/sig-figs-calculator', priority: '0.7', changefreq: 'monthly' },
  { url: '/calculators/slope-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/rounding-calculator', priority: '0.7', changefreq: 'monthly' },
  { url: '/calculators/modulo-calculator', priority: '0.7', changefreq: 'monthly' },
  // Other calculators
  { url: '/calculators/age-calculator', priority: '0.85', changefreq: 'monthly' },
  { url: '/calculators/date-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/gpa-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/tip-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/discount-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/sales-tax-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/grade-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/final-grade-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/time-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/roman-numeral-calculator', priority: '0.7', changefreq: 'monthly' },
  { url: '/calculators/speed-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/fuel-cost-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/electricity-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/word-count-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/password-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/paint-calculator', priority: '0.7', changefreq: 'monthly' },
  { url: '/calculators/concrete-calculator', priority: '0.7', changefreq: 'monthly' },
  { url: '/calculators/military-time-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/days-until-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/height-converter-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/zodiac-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/numerology-calculator', priority: '0.7', changefreq: 'monthly' },
  // Tier 6 Financial calculators
  { url: '/calculators/annuity-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/dividend-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/rule-of-72-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/npv-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/escrow-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/payback-period-calculator', priority: '0.75', changefreq: 'monthly' },
  // Tier 6 Fitness calculators
  { url: '/calculators/steps-to-miles-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/pregnancy-weight-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/vo2max-calculator', priority: '0.75', changefreq: 'monthly' },
  // Tier 6 Math calculators
  { url: '/calculators/z-score-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/percentage-error-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/circle-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/law-of-cosines-calculator', priority: '0.75', changefreq: 'monthly' },
  // Tier 6 Other calculators
  { url: '/calculators/color-converter-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/number-to-words-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/gst-vat-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/love-calculator', priority: '0.7', changefreq: 'monthly' },
  // Tier 7 Financial calculators
  { url: '/calculators/dca-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/debt-to-income-calculator', priority: '0.85', changefreq: 'monthly' },
  { url: '/calculators/bond-yield-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/college-savings-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/crypto-calculator', priority: '0.8', changefreq: 'monthly' },
  // Tier 7 Fitness calculators
  { url: '/calculators/keto-calculator', priority: '0.85', changefreq: 'monthly' },
  { url: '/calculators/body-surface-area-calculator', priority: '0.7', changefreq: 'monthly' },
  { url: '/calculators/running-calorie-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/intermittent-fasting-calculator', priority: '0.8', changefreq: 'monthly' },
  // Tier 7 Math calculators
  { url: '/calculators/angle-converter-calculator', priority: '0.75', changefreq: 'monthly' },
  { url: '/calculators/distance-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/number-base-calculator', priority: '0.75', changefreq: 'monthly' },
  // Tier 7 Other calculators
  { url: '/calculators/dog-age-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/cooking-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/shoe-size-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/roof-pitch-calculator', priority: '0.75', changefreq: 'monthly' },
  // Phase 2 — batch 1
  { url: '/calculators/hourly-to-salary-calculator', priority: '0.85', changefreq: 'monthly' },
  { url: '/calculators/overtime-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/wedding-budget-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/tank-volume-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/time-card-calculator', priority: '0.85', changefreq: 'monthly' },
  { url: '/calculators/gas-mileage-calculator', priority: '0.85', changefreq: 'monthly' },
  { url: '/calculators/tile-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/mulch-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/carbon-footprint-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/pizza-calculator', priority: '0.8', changefreq: 'monthly' },
  // Phase 2 — Cluster 1: Tax Power Hub
  { url: '/calculators/tax-refund-calculator', priority: '0.9', changefreq: 'monthly' },
  { url: '/calculators/1099-tax-calculator', priority: '0.9', changefreq: 'monthly' },
  { url: '/calculators/quarterly-tax-calculator', priority: '0.85', changefreq: 'monthly' },
  { url: '/calculators/self-employment-tax-calculator', priority: '0.85', changefreq: 'monthly' },
  { url: '/calculators/creator-tax-calculator', priority: '0.85', changefreq: 'monthly' },
  // Gap-fill from Search Console query report
  { url: '/calculators/army-body-fat-calculator', priority: '0.8', changefreq: 'monthly' },
  { url: '/calculators/basic-calculator', priority: '0.8', changefreq: 'monthly' },
]

export const GET: APIRoute = async () => {
  const today = new Date().toISOString().split('T')[0]
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages.map(p => `  <url>
    <loc>${siteUrl}${p.url}${p.url.endsWith('/') ? '' : '/'}</loc>
    <lastmod>${today}</lastmod>
    <changefreq>${p.changefreq}</changefreq>
    <priority>${p.priority}</priority>
  </url>`).join('\n')}
</urlset>`

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, max-age=86400',
    },
  })
}
