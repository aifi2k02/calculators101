import { test, expect } from '@playwright/test'

const ALL_CALCULATORS = [
  '401k-calculator','age-calculator','amortization-calculator','angle-converter-calculator',
  'annuity-calculator','apr-calculator','area-calculator','auto-loan-calculator',
  'average-calculator','bac-calculator','binary-calculator','bmi-calculator',
  'bmr-calculator','body-fat-calculator','body-surface-area-calculator','bond-yield-calculator',
  'break-even-calculator','budget-calculator','caloric-deficit-calculator','calorie-calculator',
  'calories-burned-calculator','capital-gains-calculator','car-lease-calculator','cd-calculator',
  'circle-calculator','college-savings-calculator','color-converter-calculator','combination-calculator',
  'compound-interest-calculator','concrete-calculator','cooking-calculator','credit-card-calculator',
  'crypto-calculator','currency-calculator','date-calculator','days-until-calculator',
  'dca-calculator','debt-payoff-calculator','debt-to-income-calculator','discount-calculator',
  'distance-calculator','dividend-calculator','dog-age-calculator','down-payment-calculator',
  'due-date-calculator','electricity-calculator','emergency-fund-calculator','escrow-calculator',
  'exponent-calculator','factorial-calculator','final-grade-calculator','fire-calculator',
  'fraction-calculator','fuel-cost-calculator','gpa-calculator','grade-calculator',
  'gst-vat-calculator','heart-rate-calculator','height-converter-calculator','home-equity-calculator',
  'house-affordability-calculator','ideal-weight-calculator','income-tax-calculator','inflation-calculator',
  'interest-calculator','intermittent-fasting-calculator','investment-calculator','keto-calculator',
  'law-of-cosines-calculator','lcm-gcd-calculator','lean-body-mass-calculator','loan-calculator',
  'logarithm-calculator','love-calculator','macro-calculator','markup-calculator',
  'military-time-calculator','modulo-calculator','mortgage-calculator','mortgage-points-calculator',
  'net-worth-calculator','npv-calculator','number-base-calculator','number-to-words-calculator',
  'numerology-calculator','one-rep-max-calculator','ovulation-calculator','pace-calculator',
  'paint-calculator','password-calculator','payback-period-calculator','paycheck-calculator',
  'percentage-calculator','percentage-error-calculator','pmi-calculator','pregnancy-weight-calculator',
  'prime-calculator','protein-calculator','quadratic-calculator','random-number-calculator',
  'ratio-calculator','refinance-calculator','rent-vs-buy-calculator','retirement-calculator',
  'roi-calculator','roman-numeral-calculator','roof-pitch-calculator','roth-ira-calculator',
  'rounding-calculator','rule-of-72-calculator','running-calorie-calculator','salary-calculator',
  'sales-tax-calculator','savings-calculator','scientific-notation-calculator','shoe-size-calculator',
  'sig-figs-calculator','sleep-calculator','slope-calculator','speed-calculator',
  'square-root-calculator','steps-to-miles-calculator','stock-profit-calculator','tdee-calculator',
  'time-calculator','tip-calculator','triangle-calculator','unit-converter-calculator',
  'vo2max-calculator','volume-calculator','waist-hip-calculator','water-intake-calculator',
  'word-count-calculator','z-score-calculator','zodiac-calculator',
]

for (const slug of ALL_CALCULATORS) {
  test(`${slug}: loads, has button, clicks without JS error`, async ({ page }) => {
    const errors: string[] = []
    page.on('pageerror', err => errors.push(err.message))

    await page.goto(`/calculators/${slug}`)

    // Page must load (not 404)
    await expect(page.locator('h1').first()).toBeVisible({ timeout: 10000 })

    // Must have a Calculate button
    const btn = page.locator('button[id^="calc-btn"]')
    await expect(btn).toBeVisible()

    // Click calculate
    await btn.click()

    // Wait briefly for JS to run
    await page.waitForTimeout(500)

    // Result OR error box must be visible (not both hidden)
    const resultVisible = await page.locator('[id^="calc-result"]').first().isVisible()
    const errorVisible = await page.locator('[id^="calc-error"]').first().isVisible()
    expect(resultVisible || errorVisible).toBe(true)

    // No JS crashes
    const hardErrors = errors.filter(e =>
      !e.includes('favicon') &&
      !e.includes('manifest') &&
      !e.includes('ResizeObserver')
    )
    expect(hardErrors).toHaveLength(0)
  })
}
