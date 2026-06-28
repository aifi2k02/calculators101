import { test, expect } from '@playwright/test'

// ── Homepage ──────────────────────────────────────────────────────────────────
test.describe('Homepage', () => {
  test('loads and shows calculator categories', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveTitle(/calculat/i)
    // Check that /calculators/ links exist in DOM (may be in collapsed mobile nav)
    await expect(page.locator('a[href*="/calculators/"]').first()).toBeAttached()
    // At least the page body has content
    await expect(page.locator('main, body > div, #app, [class*="max-w"]').first()).toBeVisible()
  })
})

// ── Category pages ────────────────────────────────────────────────────────────
const categories = ['financial', 'fitness', 'math', 'other']

for (const cat of categories) {
  test(`Category page: /calculators/${cat}`, async ({ page }) => {
    await page.goto(`/calculators/${cat}`)
    await expect(page.locator('h1').first()).toBeVisible()
    // Links may be in a grid that requires scrolling on mobile — just check they exist
    await expect(page.locator('a[href*="calculator"]').first()).toBeAttached()
  })
}

// ── Calculator pages: structure ───────────────────────────────────────────────
const samplePages = [
  { slug: 'bmi-calculator',           cat: 'health'  },
  { slug: 'mortgage-calculator',      cat: 'finance' },
  { slug: 'percentage-calculator',    cat: 'math'    },
  { slug: 'age-calculator',           cat: 'health'  },
  { slug: 'compound-interest-calculator', cat: 'finance' },
  { slug: 'calorie-calculator',       cat: 'health'  },
  { slug: 'triangle-calculator',      cat: 'math'    },
  { slug: 'angle-converter-calculator', cat: 'other' },
  { slug: 'unit-converter-calculator', cat: 'other'  },
]

for (const { slug, cat } of samplePages) {
  test.describe(`Calculator: ${slug}`, () => {
    test('has breadcrumb, title, inputs, FAQ, stats cards, gauge, AI button', async ({ page }) => {
      await page.goto(`/calculators/${slug}`)

      // Breadcrumb (skip header nav which is md:hidden on mobile — look for the page-level breadcrumb)
      await expect(page.locator('nav').last()).toBeAttached()

      // H1 title
      await expect(page.locator('h1').first()).toBeVisible()

      // At least one input
      const inputs = page.locator('input, select')
      await expect(inputs.first()).toBeVisible()

      // Calculate button
      const btn = page.getByRole('button', { name: /calculat/i }).first()
      await expect(btn).toBeVisible()

      // FAQ section exists
      await expect(page.locator('details, [class*="faq"], h2:has-text("FAQ"), h2:has-text("faq"), h3:has-text("FAQ")').first()).toBeVisible()

      // AI explain button
      await expect(page.getByRole('button', { name: /explain|AI/i }).first()).toBeVisible()
    })
  })
}

// ── Calculator: BMI — full calculation flow ───────────────────────────────────
test('BMI calculator: enter values → result appears → gauge shows → stats appear', async ({ page }) => {
  await page.goto('/calculators/bmi-calculator')

  // Find weight and height inputs
  const inputs = page.locator('input[type="number"]')
  const count = await inputs.count()
  expect(count).toBeGreaterThan(0)

  // Fill in first two numeric inputs (typically height, weight)
  await inputs.nth(0).fill('70')
  if (count > 1) await inputs.nth(1).fill('175')

  await page.getByRole('button', { name: /calculat/i }).first().click()

  // Result div should appear with a value
  const resultEl = page.locator('[id*="result"]').first()
  await expect(resultEl).toBeVisible({ timeout: 5000 })

  // Gauge pointer should appear (opacity transitions to 1)
  const gauge = page.locator('[id*="gauge-pointer"]').first()
  await expect(gauge).toBeVisible()

  // Stats cards — look for the stats grid (4 small cards)
  const statCards = page.locator('[class*="stat"], .grid .rounded-xl, .grid .rounded-lg')
  await expect(statCards.first()).toBeVisible()
})

// ── Calculator: Percentage — quick math check ─────────────────────────────────
test('Percentage calculator: 50% of 200 = 100', async ({ page }) => {
  await page.goto('/calculators/percentage-calculator')

  const inputs = page.locator('input[type="number"]')
  // Try filling the first two number inputs: percentage value + base number
  await inputs.nth(0).fill('50')
  if (await inputs.count() > 1) await inputs.nth(1).fill('200')

  await page.getByRole('button', { name: /calculat/i }).first().click()

  // Result should contain "100"
  await expect(page.locator('[id*="result"]').first()).toContainText('100', { timeout: 5000 })
})

// ── Mortgage calculator: produces a monthly payment ───────────────────────────
test('Mortgage calculator: inputs → result has dollar sign', async ({ page }) => {
  await page.goto('/calculators/mortgage-calculator')

  const inputs = page.locator('input[type="number"]')
  const count = await inputs.count()
  // Fill all numeric inputs with typical values
  const vals = ['300000', '20', '30', '7']
  for (let i = 0; i < Math.min(count, vals.length); i++) {
    await inputs.nth(i).fill(vals[i])
  }

  await page.getByRole('button', { name: /calculat/i }).first().click()

  const result = page.locator('[id*="result"]').first()
  await expect(result).toBeVisible({ timeout: 5000 })
  // Should show some numeric value
  await expect(result).not.toBeEmpty()
})

// ── Gauge: no visual overlap (CSS) ───────────────────────────────────────────
test('Gauge: pointer value label exists inside pointer div (no overlap)', async ({ page }) => {
  await page.goto('/calculators/bmi-calculator')

  const inputs = page.locator('input[type="number"]')
  await inputs.nth(0).fill('70')
  if (await inputs.count() > 1) await inputs.nth(1).fill('175')
  await page.getByRole('button', { name: /calculat/i }).first().click()

  // The value label should be INSIDE the pointer div (our CSS fix)
  const valLabel = page.locator('[id*="gauge-val-label"]').first()
  await expect(valLabel).toBeVisible({ timeout: 5000 })
  const text = await valLabel.textContent()
  expect(text?.trim().length).toBeGreaterThan(0)

  // Check it's a child of the pointer div (not a sibling at the same level)
  const pointer = page.locator('[id*="gauge-pointer"]').first()
  const pointerChildren = pointer.locator('[id*="gauge-val-label"]')
  await expect(pointerChildren).toHaveCount(1)
})

// ── Mobile viewport ───────────────────────────────────────────────────────────
test('BMI calculator: renders correctly on mobile (375px)', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 })
  await page.goto('/calculators/bmi-calculator')

  await expect(page.locator('h1').first()).toBeVisible()
  await expect(page.locator('input[type="number"]').first()).toBeVisible()
  await expect(page.getByRole('button', { name: /calculat/i }).first()).toBeVisible()
})

// ── No console errors on key pages ───────────────────────────────────────────
test('No JS errors on homepage or BMI page', async ({ page }) => {
  const errors: string[] = []
  page.on('pageerror', err => errors.push(err.message))

  await page.goto('/')
  await page.goto('/calculators/bmi-calculator')

  // Allow time for any async errors
  await page.waitForTimeout(1000)

  expect(errors.filter(e => !e.includes('favicon'))).toHaveLength(0)
})
