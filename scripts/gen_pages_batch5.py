#!/usr/bin/env python3
"""Batch 5: Many remaining pages — tip calculator already done, doing: amortization, house-affordability, refinance, down-payment, paycheck, 401k, rent-vs-buy, APR, car-lease, home-equity, CD, stock-profit, break-even, markup, income-tax, Roth IRA, PMI, emergency-fund, FIRE, capital-gains, annuity, dividend, ROI, rule-of-72, NPV, escrow, payback-period, DCA, debt-to-income, bond-yield, college-savings, crypto"""
import os

CALC_DIR = "/Users/apple/Documents/Projects/calculators-for-free/src/pages/calculators"

def write(slug, content):
    path = os.path.join(CALC_DIR, f"{slug}-calculator.astro")
    with open(path, 'w') as f:
        f.write(content)
    print(f"  {slug}-calculator.astro")

# Helper to generate a standard page
def page(slug, title, cat, cat_slug, seo_title, seo_desc, formula, inputs_arr, gauge_cfg, faqs_arr, related_arr, sidebar, content_section, result_label="Result", calc_desc=""):
    inputs_js = ",\n            ".join(inputs_arr)
    related_js = ",\n            ".join([f'{{ name: "{n}", href: "{h}" }}' for n,h in related_arr])
    faqs_js = "[\n  " + ",\n  ".join([f'{{ question: "{q}", answer: "{a}" }}' for q,a in faqs_arr]) + "\n]"
    cd = calc_desc or seo_desc[:80]
    return f'''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
{formula}
`

const faqs = {faqs_js}
---
<Layout
  title="{seo_title}"
  description="{seo_desc}"
  breadcrumbs={{[
    {{ name: "Home", href: "/" }},
    {{ name: "{cat}", href: "/calculators/{cat_slug}" }},
    {{ name: "{title}", href: "/calculators/{slug}-calculator" }},
  ]}}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/{cat_slug}" class="hover:text-blue-600">{cat}</a><span>›</span>
      <span class="text-gray-900">{title}</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="{title}"
          description="{cd}"
          formulaId="{slug}"
          formulaFn={{formulaFn}}
          resultLabel="{result_label}"
          inputs={{[
            {inputs_js}
          ]}}
          gauge={{{gauge_cfg}}}
          faqs={{faqs}}
          relatedCalcs={{[
            {related_js}
          ]}}
        />
      </div>
      <aside class="space-y-5">
{sidebar}
      </aside>
    </div>
{content_section}
  </div>
</Layout>
'''

# ─── AMORTIZATION ─────────────────────────────────────────────────────────────
write("amortization", page(
    slug="amortization",
    title="Amortization Calculator",
    cat="Financial",
    cat_slug="financial",
    seo_title="Amortization Calculator: Loan Payment Schedule",
    seo_desc="Calculate your loan amortization schedule. See principal vs. interest breakdown for every payment. Free amortization calculator.",
    formula="""
  const principal = parseFloat(inputs.principal) || 0
  const rate = parseFloat(inputs.rate) || 0
  const years = parseInt(inputs.years) || 0
  if (principal <= 0) throw new Error("Enter loan amount.")
  if (years <= 0) throw new Error("Enter loan term.")
  const r = rate / 100 / 12
  const n = years * 12
  const payment = r === 0 ? principal / n : principal * r * Math.pow(1+r,n) / (Math.pow(1+r,n)-1)
  const totalPaid = payment * n
  const totalInterest = totalPaid - principal
  const interestPct = (totalInterest / totalPaid) * 100
  // Year 1 breakdown
  let bal = principal, y1interest = 0
  for (let i = 0; i < Math.min(12, n); i++) {
    const int = bal * r; y1interest += int; bal = bal + int - payment
  }
  return {
    value: "$" + payment.toFixed(2) + "/mo",
    gaugeValue: Math.min(interestPct, 60) / 60 * 100,
    breakdown: ["Monthly payment: $" + payment.toFixed(2), "Total paid: $" + totalPaid.toFixed(2), "Total interest: $" + totalInterest.toFixed(2), "Interest is " + interestPct.toFixed(1) + "% of total paid", "Year 1 interest: $" + y1interest.toFixed(2)],
    stats: [
      { label: "Monthly Payment", value: "$" + payment.toFixed(2) },
      { label: "Total Interest", value: "$" + totalInterest.toFixed(0) },
      { label: "Total Paid", value: "$" + totalPaid.toFixed(0) },
      { label: "Interest Share", value: interestPct.toFixed(1) + "%" },
    ]
  }
""",
    inputs_arr=[
        '{ id: "principal", label: "Loan Amount", type: "number", placeholder: "300000", min: 0, unit: "$", defaultValue: 300000 }',
        '{ id: "rate", label: "Annual Interest Rate", type: "number", placeholder: "7", min: 0, max: 25, step: 0.1, unit: "%", defaultValue: 7 }',
        '{ id: "years", label: "Loan Term", type: "select", options: [{ value: "10", label: "10 years" },{ value: "15", label: "15 years" },{ value: "20", label: "20 years" },{ value: "25", label: "25 years" },{ value: "30", label: "30 years" }], defaultValue: "30" }',
    ],
    gauge_cfg='min: 0, max: 100, unit: "% interest",\n            zones: [\n              { label: "Low", color: "#22c55e", from: 0, to: 33 },\n              { label: "Moderate", color: "#f59e0b", from: 33, to: 66 },\n              { label: "High", color: "#ef4444", from: 66, to: 100 },\n            ]',
    faqs_arr=[
        ("What is amortization?", "Amortization is the process of paying off a loan through regular payments over time. Each payment covers interest first, with the remainder reducing principal. Early payments are mostly interest; later payments are mostly principal."),
        ("Why do I pay so much interest on a 30-year mortgage?", "A $300,000 mortgage at 7% for 30 years costs ~$418,000 in total interest — more than the loan itself. This is because you owe interest on the full balance for decades. Paying even $100 extra per month can save tens of thousands."),
        ("What is the difference between a 15 and 30-year mortgage?", "A 15-year mortgage has higher monthly payments but saves enormous interest — typically 50-60% less total interest than a 30-year. A 30-year has lower payments with more flexibility, but much higher lifetime cost."),
        ("How do extra payments affect amortization?", "Extra payments go entirely to principal, reducing your balance and future interest charges. On a $300k mortgage at 7%, paying $200/month extra can pay off the loan 7 years early and save $85,000+ in interest."),
        ("What is a balloon payment?", "A balloon mortgage has smaller monthly payments with one large final payment (the balloon). Common in commercial real estate and some auto loans. The risk: you must refinance or pay the lump sum when it comes due."),
    ],
    related_arr=[("Mortgage Calculator", "/calculators/mortgage-calculator"), ("Loan Calculator", "/calculators/loan-calculator"), ("Refinance Calculator", "/calculators/refinance-calculator")],
    sidebar="""        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">$300k at 7% — Term Comparison</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700"><th class="text-left pb-1">Term</th><th class="text-right pb-1">Payment</th><th class="text-right pb-1">Total Interest</th></tr></thead>
            <tbody class="text-blue-900">
              {[["10yr","$3,484/mo","$118,000"],["15yr","$2,696/mo","$185,000"],["20yr","$2,326/mo","$258,000"],["30yr","$1,996/mo","$419,000"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-1">{r[0]}</td><td class="text-right">{r[1]}</td><td class="text-right">{r[2]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
        <div class="bg-amber-50 border border-amber-200 rounded-xl p-5">
          <h3 class="font-bold text-amber-900 mb-2">Early vs Late Payments</h3>
          <p class="text-xs text-amber-800">In year 1 of a 30-year $300k mortgage at 7%, about <strong>$1,742</strong> of each $1,996 payment goes to interest. By year 25, only <strong>$500</strong> goes to interest. Early payments are mostly interest!</p>
        </div>""",
    content_section="""    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">How Amortization Works</h2>
        <p class="text-gray-600 text-sm mb-3">Each payment = Interest + Principal. Interest = Outstanding Balance × Monthly Rate. Principal = Payment − Interest.</p>
        <div class="bg-gray-50 rounded-lg p-4 text-xs font-mono">
          <div class="mb-1">Month 1: Balance $300,000</div>
          <div class="mb-1">Interest: $300k × 7%/12 = $1,750</div>
          <div class="mb-1">Principal: $1,996 − $1,750 = $246</div>
          <div>New balance: $300,000 − $246 = $299,754</div>
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Power of Extra Payments</h2>
        <div class="space-y-2">
          {[
            { extra: "+$0/mo", payoff: "30 years", saved: "$0" },
            { extra: "+$100/mo", payoff: "~26.5 years", saved: "~$60,000" },
            { extra: "+$200/mo", payoff: "~24 years", saved: "~$95,000" },
            { extra: "+$500/mo", payoff: "~20 years", saved: "~$150,000" },
          ].map(p => (
            <div class="flex items-center gap-3 bg-gray-50 rounded-lg p-3">
              <div class="font-mono text-xs text-blue-600 w-20">{p.extra}</div>
              <div class="text-xs text-gray-700">Paid off in {p.payoff}, save {p.saved}</div>
            </div>
          ))}
        </div>
        <p class="text-xs text-gray-500 mt-2">On a $300k, 7%, 30-year mortgage</p>
      </div>
    </div>""",
    result_label="Monthly Payment",
    calc_desc="See your loan payment breakdown — principal vs interest for every payment"
))

# ─── ROI ──────────────────────────────────────────────────────────────────────
write("roi", page(
    slug="roi",
    title="ROI Calculator",
    cat="Financial",
    cat_slug="financial",
    seo_title="ROI Calculator: Return on Investment",
    seo_desc="Calculate return on investment (ROI) for any investment. Annualized ROI and simple ROI with break-even analysis. Free ROI calculator.",
    formula="""
  const initial = parseFloat(inputs.initial) || 0
  const final = parseFloat(inputs.final) || 0
  const years = parseFloat(inputs.years) || 1
  const costs = parseFloat(inputs.costs) || 0
  if (initial <= 0) throw new Error("Enter initial investment.")
  const netGain = final - initial - costs
  const roi = (netGain / initial) * 100
  const annualRoi = years > 0 ? ((Math.pow((final - costs) / initial, 1 / years) - 1) * 100) : roi
  return {
    value: roi.toFixed(2) + "% ROI",
    gaugeValue: Math.min(Math.max(roi + 50, 0), 100),
    breakdown: [
      "Net gain/loss: $" + netGain.toFixed(2),
      "Simple ROI: " + roi.toFixed(2) + "%",
      years > 0 ? "Annualized ROI: " + annualRoi.toFixed(2) + "%" : "",
    ].filter(Boolean),
    stats: [
      { label: "Simple ROI", value: roi.toFixed(2) + "%" },
      { label: "Net Gain/Loss", value: "$" + netGain.toFixed(2) },
      { label: "Annualized ROI", value: annualRoi.toFixed(2) + "%" },
      { label: "Multiplier", value: ((final - costs) / initial).toFixed(2) + "x" },
    ]
  }
""",
    inputs_arr=[
        '{ id: "initial", label: "Initial Investment", type: "number", placeholder: "10000", min: 0, unit: "$", defaultValue: 10000 }',
        '{ id: "final", label: "Final Value / Return", type: "number", placeholder: "15000", min: 0, unit: "$", defaultValue: 15000 }',
        '{ id: "costs", label: "Additional Costs / Fees", type: "number", placeholder: "0", min: 0, unit: "$", defaultValue: 0 }',
        '{ id: "years", label: "Investment Period", type: "number", placeholder: "3", min: 0, step: 0.1, unit: "years", defaultValue: 3 }',
    ],
    gauge_cfg='min: 0, max: 100, unit: "% ROI scale",\n            zones: [\n              { label: "Loss", color: "#ef4444", from: 0, to: 40 },\n              { label: "Breakeven", color: "#94a3b8", from: 40, to: 55 },\n              { label: "Positive", color: "#3b82f6", from: 55, to: 75 },\n              { label: "Strong", color: "#22c55e", from: 75, to: 100 },\n            ]',
    faqs_arr=[
        ("What is ROI?", "Return on Investment (ROI) measures the gain or loss from an investment relative to its cost. Formula: ROI = (Net Gain / Initial Investment) × 100. A 50% ROI means you gained 50% of what you invested."),
        ("What is a good ROI?", "It depends on the investment type and risk. S&P 500 average: ~10%/year. Real estate: 8–12%/year. High-yield savings: 4–5%. Startup investments: vary wildly. Compare ROI to benchmarks in the same asset class, not across different types."),
        ("What is annualized ROI?", "Annualized ROI (CAGR — Compound Annual Growth Rate) converts total return to an equivalent annual rate, enabling fair comparison across different time periods. A 50% total ROI over 5 years = 8.45% annualized (not 10%, because compounding matters)."),
        ("How is ROI different from profit margin?", "ROI compares return to investment cost. Profit margin compares profit to revenue. A business can have a high profit margin but low ROI (tied up too much capital) or low margins but great ROI (asset-light model, high turnover)."),
        ("How do I calculate ROI for real estate?", "Include all costs: purchase price, closing costs, renovations, annual operating costs. Annual return includes rental income and appreciation. ROI = (Annual Profit × Years + Appreciation − All Costs) / Total Investment. Cap rate is a related metric for rental properties."),
    ],
    related_arr=[("Investment Calculator", "/calculators/investment-calculator"), ("Compound Interest Calculator", "/calculators/compound-interest-calculator"), ("Break-Even Calculator", "/calculators/break-even-calculator")],
    sidebar="""        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Benchmark ROIs</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[["S&P 500 (historical)","~10%/yr"],["Real estate","~8–12%/yr"],["Bonds","~3–5%/yr"],["HYSA (2025)","~4–5%/yr"],["Crypto","Highly variable"],["Angel investing","~27%/yr avg (risky)"]].map(([a,b]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span>{a}</span><span class="font-medium">{b}</span></div>
            ))}
          </div>
        </div>""",
    content_section="""    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Simple vs Annualized ROI</h2>
        <p class="text-gray-600 text-sm mb-3">Simple ROI just measures total return. Annualized ROI (CAGR) accounts for time.</p>
        <div class="bg-gray-50 rounded-lg p-4 text-sm">
          <p class="font-medium text-gray-800 mb-2">$10,000 → $15,000</p>
          <div class="text-xs space-y-1">
            <div>Simple ROI: (15k-10k)/10k × 100 = <strong>50%</strong></div>
            <div>Over 1 yr: 50% annualized</div>
            <div>Over 3 yrs: (15/10)^(1/3)-1 = <strong>14.5%/yr</strong></div>
            <div>Over 5 yrs: (15/10)^(1/5)-1 = <strong>8.45%/yr</strong></div>
          </div>
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">ROI by Investment Type</h2>
        <div class="space-y-2">
          {[
            { type: "Index Funds", roi: "7–10% annualized", risk: "Low-medium", horizon: "5+ years" },
            { type: "Real Estate", roi: "8–12% total return", risk: "Medium", horizon: "5–10 years" },
            { type: "Business Investment", roi: "Variable 20–100%+", risk: "High", horizon: "3–7 years" },
            { type: "High-yield Savings", roi: "4–5% guaranteed", risk: "None", horizon: "Any" },
          ].map(i => (
            <div class="bg-gray-50 rounded-lg p-3 text-xs">
              <div class="font-semibold text-gray-800">{i.type}</div>
              <div class="flex gap-4 mt-1 text-gray-600"><span>ROI: {i.roi}</span><span>Risk: {i.risk}</span></div>
            </div>
          ))}
        </div>
      </div>
    </div>""",
    result_label="ROI",
    calc_desc="Calculate return on investment with annualized rate and net gain analysis"
))

# ─── INFLATION ─────────────────────────────────────────────────────────────────
write("inflation", page(
    slug="inflation",
    title="Inflation Calculator",
    cat="Financial",
    cat_slug="financial",
    seo_title="Inflation Calculator: Purchasing Power Over Time",
    seo_desc="Calculate how inflation affects purchasing power over time. See what past or future dollars are worth today. Free inflation calculator.",
    formula="""
  const amount = parseFloat(inputs.amount) || 0
  const fromYear = parseInt(inputs.fromYear) || 2000
  const toYear = parseInt(inputs.toYear) || 2024
  const rate = parseFloat(inputs.rate) || 3
  if (amount <= 0) throw new Error("Enter an amount.")
  const years = toYear - fromYear
  const adjusted = amount * Math.pow(1 + rate / 100, years)
  const purchasingPower = amount / Math.pow(1 + rate / 100, Math.abs(years))
  const totalInflation = ((adjusted - amount) / amount) * 100
  return {
    value: "$" + adjusted.toFixed(2) + " in " + toYear,
    gaugeValue: Math.min(totalInflation, 100),
    breakdown: ["Original: $" + amount + " in " + fromYear, "Adjusted: $" + adjusted.toFixed(2) + " in " + toYear, "Total inflation: " + totalInflation.toFixed(1) + "%", "Annual rate used: " + rate + "%"],
    stats: [
      { label: "Adjusted Value", value: "$" + adjusted.toFixed(2) },
      { label: "Total Inflation", value: totalInflation.toFixed(1) + "%" },
      { label: "Years", value: String(Math.abs(years)) },
      { label: "Real Loss", value: "$" + (adjusted - amount).toFixed(2) },
    ]
  }
""",
    inputs_arr=[
        '{ id: "amount", label: "Amount", type: "number", placeholder: "1000", min: 0, unit: "$", defaultValue: 1000 }',
        '{ id: "fromYear", label: "From Year", type: "number", placeholder: "2000", min: 1900, max: 2030, defaultValue: 2000 }',
        '{ id: "toYear", label: "To Year", type: "number", placeholder: "2024", min: 1900, max: 2030, defaultValue: 2024 }',
        '{ id: "rate", label: "Annual Inflation Rate", type: "number", placeholder: "3", min: 0, max: 20, step: 0.1, unit: "%", defaultValue: 3 }',
    ],
    gauge_cfg='min: 0, max: 100, unit: "% total inflation",\n            zones: [\n              { label: "Low", color: "#22c55e", from: 0, to: 25 },\n              { label: "Moderate", color: "#3b82f6", from: 25, to: 50 },\n              { label: "High", color: "#f59e0b", from: 50, to: 75 },\n              { label: "Very High", color: "#ef4444", from: 75, to: 100 },\n            ]',
    faqs_arr=[
        ("What is inflation?", "Inflation is the rate at which the general price level rises over time, reducing purchasing power. If inflation is 3%, something that costs $100 today will cost $103 next year. The dollar buys less as prices rise."),
        ("What is the historical US inflation rate?", "The US CPI (Consumer Price Index) has averaged about 3.1% annually since 1913. The 1970s saw high inflation (10%+). The 2021-2023 period saw post-pandemic spikes of 7-9%. The Federal Reserve targets 2% annual inflation."),
        ("How does inflation affect savings?", "If your savings earn less interest than the inflation rate, you lose purchasing power. $10,000 in a 0.5% savings account during 3% inflation loses ~$250 of real value per year. This is why holding too much cash long-term is risky."),
        ("What is hyperinflation?", "Hyperinflation is extremely rapid inflation, typically above 50% per month. Historical examples include Germany (1923), Zimbabwe (2008), and Venezuela (2018). It destroys savings and economic stability."),
        ("How can I protect against inflation?", "Invest in assets that typically outpace inflation: stocks (historically ~7% real return), real estate, Treasury Inflation-Protected Securities (TIPS), I-Bonds (inflation-indexed savings bonds), and commodities. Holding only cash or low-yield bonds loses ground to inflation over time."),
    ],
    related_arr=[("Investment Calculator", "/calculators/investment-calculator"), ("Savings Calculator", "/calculators/savings-calculator"), ("Compound Interest Calculator", "/calculators/compound-interest-calculator")],
    sidebar="""        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">$1,000 Purchasing Power Over Time</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[["1950","$12,680 today"],["1970","$7,890 today"],["1980","$3,780 today"],["1990","$2,420 today"],["2000","$1,770 today"],["2010","$1,420 today"],["2020","$1,250 today"]].map(([y,v]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span>{y}</span><span class="font-medium">{v}</span></div>
            ))}
          </div>
          <p class="text-xs text-blue-600 mt-1">Based on ~3% average US inflation</p>
        </div>""",
    content_section="""    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">US Inflation by Decade</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold text-gray-700">Decade</th><th class="text-right p-2 text-xs font-semibold text-gray-700">Avg Annual Rate</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["1960s","2.5%"],["1970s","7.1%"],["1980s","5.6%"],["1990s","3.0%"],["2000s","2.6%"],["2010s","1.8%"],["2020–2023","5.9%"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-medium">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Inflation Hedges</h2>
        <div class="space-y-2">
          {[
            { asset: "Stocks (equities)", detail: "Historically outpace inflation by ~7% real return annually" },
            { asset: "Real Estate", detail: "Tends to appreciate with or above inflation; rental income rises" },
            { asset: "TIPS (Treasury I-P Securities)", detail: "Principal adjusts with CPI; guaranteed inflation protection" },
            { asset: "I-Bonds", detail: "US savings bonds with rate tied to CPI; $10k/yr limit" },
            { asset: "Commodities", detail: "Gold, silver, oil — tend to rise with inflation" },
          ].map(h => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-gray-800 text-xs mb-1">{h.asset}</div>
              <div class="text-xs text-gray-600">{h.detail}</div>
            </div>
          ))}
        </div>
      </div>
    </div>""",
    result_label="Inflation-Adjusted Value",
    calc_desc="See how inflation erodes purchasing power and what past money is worth today"
))

# ─── SALARY ───────────────────────────────────────────────────────────────────
write("salary", page(
    slug="salary",
    title="Salary Calculator",
    cat="Financial",
    cat_slug="financial",
    seo_title="Salary Calculator: Annual, Monthly & Hourly Pay",
    seo_desc="Convert salary to hourly, daily, weekly, monthly, or annual pay. Calculate take-home pay with tax estimate. Free salary calculator.",
    formula="""
  const amount = parseFloat(inputs.amount) || 0
  const period = inputs.period || "annual"
  const hours = parseFloat(inputs.hours) || 40
  const taxRate = parseFloat(inputs.tax) || 25
  if (amount <= 0) throw new Error("Enter a salary amount.")
  let annual
  if (period === "hourly") annual = amount * hours * 52
  else if (period === "daily") annual = amount * 260
  else if (period === "weekly") annual = amount * 52
  else if (period === "biweekly") annual = amount * 26
  else if (period === "monthly") annual = amount * 12
  else annual = amount
  const monthly = annual / 12
  const biweekly = annual / 26
  const weekly = annual / 52
  const daily = annual / 260
  const hourly = annual / (52 * hours)
  const afterTax = annual * (1 - taxRate / 100)
  return {
    value: "$" + annual.toLocaleString("en-US", { maximumFractionDigits: 0 }) + "/year",
    gaugeValue: Math.min(annual / 2000, 100),
    breakdown: ["Hourly: $" + hourly.toFixed(2), "Weekly: $" + weekly.toFixed(2), "Biweekly: $" + biweekly.toFixed(2), "Monthly: $" + monthly.toFixed(2), "Annual: $" + annual.toLocaleString("en-US", { maximumFractionDigits: 0 }), "After ~" + taxRate + "% tax: $" + afterTax.toLocaleString("en-US", { maximumFractionDigits: 0 }) + "/yr"],
    stats: [
      { label: "Annual Salary", value: "$" + annual.toLocaleString("en-US", { maximumFractionDigits: 0 }) },
      { label: "Monthly", value: "$" + monthly.toFixed(0) },
      { label: "Hourly", value: "$" + hourly.toFixed(2) },
      { label: "After Tax (est.)", value: "$" + afterTax.toLocaleString("en-US", { maximumFractionDigits: 0 }) + "/yr" },
    ]
  }
""",
    inputs_arr=[
        '{ id: "amount", label: "Pay Amount", type: "number", placeholder: "75000", min: 0, defaultValue: 75000 }',
        '{ id: "period", label: "Pay Period", type: "select", options: [{ value: "hourly", label: "Hourly" },{ value: "daily", label: "Daily" },{ value: "weekly", label: "Weekly" },{ value: "biweekly", label: "Bi-weekly" },{ value: "monthly", label: "Monthly" },{ value: "annual", label: "Annual" }], defaultValue: "annual" }',
        '{ id: "hours", label: "Hours per Week", type: "number", placeholder: "40", min: 1, max: 80, defaultValue: 40 }',
        '{ id: "tax", label: "Estimated Tax Rate", type: "number", placeholder: "25", min: 0, max: 50, unit: "%", defaultValue: 25 }',
    ],
    gauge_cfg='min: 0, max: 100, unit: "% income level",\n            zones: [\n              { label: "Under $50k", color: "#94a3b8", from: 0, to: 25 },\n              { label: "$50k–$100k", color: "#3b82f6", from: 25, to: 50 },\n              { label: "$100k–$150k", color: "#22c55e", from: 50, to: 75 },\n              { label: "$150k+", color: "#f59e0b", from: 75, to: 100 },\n            ]',
    faqs_arr=[
        ("How do I convert hourly to annual salary?", "Hourly × Hours per week × 52 weeks. At 40 hours/week: hourly × 2,080 = annual salary. Example: $25/hour × 2,080 = $52,000/year. For 50 weeks (2 vacation weeks): hourly × 2,000."),
        ("What is take-home pay?", "Take-home pay (net pay) is what you receive after taxes and deductions. Federal income tax, state tax, FICA (Social Security 6.2% + Medicare 1.45%), and any benefits contributions are deducted. A $75,000 salary typically nets $52,000-$58,000 depending on state."),
        ("What is a good salary in the US?", "The US median household income is ~$74,000 (2023). Individual median is ~$56,000. Cost of living varies enormously by location — $75k in rural Mississippi is comfortable; $75k in San Francisco is tight. Compare to your local cost of living, not national averages."),
        ("What is the difference between salary and hourly?", "Salaried employees get a fixed annual amount regardless of hours worked (though overtime rules vary). Hourly employees are paid per hour worked and typically receive overtime (1.5x) for hours over 40/week. Salaried positions often include more benefits."),
        ("What is the $15 minimum wage worth annually?", "$15/hour × 40 hours/week × 52 weeks = $31,200/year gross. After estimated 18% taxes (FICA + some federal): ~$25,580 take-home, or ~$2,132/month. This barely covers median 1-bedroom rent in most US cities."),
    ],
    related_arr=[("Paycheck Calculator", "/calculators/paycheck-calculator"), ("Budget Calculator", "/calculators/budget-calculator"), ("Income Tax Calculator", "/calculators/income-tax-calculator")],
    sidebar="""        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Quick Salary Reference</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700"><th class="text-left pb-1">Hourly</th><th class="text-right pb-1">Annual (40hr)</th></tr></thead>
            <tbody class="text-blue-900">
              {[["$15","$31,200"],["$20","$41,600"],["$25","$52,000"],["$30","$62,400"],["$40","$83,200"],["$50","$104,000"],["$75","$156,000"],["$100","$208,000"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right font-medium">{r[1]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
    content_section="""    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">US Salary Percentiles (2023)</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold text-gray-700">Percentile</th><th class="text-right p-2 text-xs font-semibold text-gray-700">Annual Income</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["25th (bottom quarter)","Under $35,000"],["50th (median)","~$56,000"],["75th","~$95,000"],["90th","~$145,000"],["95th","~$200,000"],["99th","~$430,000+"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-medium">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Negotiating Your Salary</h2>
        <div class="space-y-2">
          {[
            "Research market rate on Glassdoor, Levels.fyi, LinkedIn Salary, and BLS data",
            "Ask for 10-20% above your target — you can always come down",
            "Never give the first number; ask about the budget range first",
            "Negotiate the full package: base, bonus, equity, PTO, remote flexibility",
            "Get any verbal offer in writing before making major decisions",
            "Consider the cost-of-living index if relocating for a role",
          ].map(tip => (
            <div class="flex gap-2 text-xs text-gray-600">
              <span class="text-blue-500 mt-0.5">•</span>
              <span>{tip}</span>
            </div>
          ))}
        </div>
      </div>
    </div>""",
    result_label="Annual Salary",
    calc_desc="Convert any pay period to annual, monthly, and hourly rates with take-home estimate"
))

# ─── BUDGET ───────────────────────────────────────────────────────────────────
write("budget", page(
    slug="budget",
    title="Budget Calculator",
    cat="Financial",
    cat_slug="financial",
    seo_title="Budget Calculator: Monthly Budget Planner",
    seo_desc="Create a monthly budget by category. See where your money goes and how much you can save. Free budget calculator.",
    formula="""
  const income = parseFloat(inputs.income) || 0
  const housing = parseFloat(inputs.housing) || 0
  const food = parseFloat(inputs.food) || 0
  const transport = parseFloat(inputs.transport) || 0
  const utilities = parseFloat(inputs.utilities) || 0
  const insurance = parseFloat(inputs.insurance) || 0
  const entertainment = parseFloat(inputs.entertainment) || 0
  const other = parseFloat(inputs.other) || 0
  if (income <= 0) throw new Error("Enter monthly income.")
  const expenses = housing + food + transport + utilities + insurance + entertainment + other
  const remaining = income - expenses
  const savingsRate = income > 0 ? (remaining / income) * 100 : 0
  const housingPct = (housing / income) * 100
  return {
    value: "$" + remaining.toFixed(2) + " left over",
    gaugeValue: Math.max(0, Math.min(savingsRate, 100)),
    breakdown: ["Income: $" + income, "Total expenses: $" + expenses.toFixed(2), "Remaining: $" + remaining.toFixed(2), "Savings rate: " + savingsRate.toFixed(1) + "%", "Housing ratio: " + housingPct.toFixed(1) + "% (target: <30%)"],
    stats: [
      { label: "Monthly Surplus", value: "$" + remaining.toFixed(2) },
      { label: "Savings Rate", value: savingsRate.toFixed(1) + "%" },
      { label: "Total Expenses", value: "$" + expenses.toFixed(2) },
      { label: "Housing %", value: housingPct.toFixed(1) + "%" },
    ]
  }
""",
    inputs_arr=[
        '{ id: "income", label: "Monthly Take-Home Income", type: "number", placeholder: "5000", min: 0, unit: "$", defaultValue: 5000 }',
        '{ id: "housing", label: "Housing (rent/mortgage)", type: "number", placeholder: "1500", min: 0, unit: "$", defaultValue: 1500 }',
        '{ id: "food", label: "Food & Groceries", type: "number", placeholder: "500", min: 0, unit: "$", defaultValue: 500 }',
        '{ id: "transport", label: "Transportation", type: "number", placeholder: "400", min: 0, unit: "$", defaultValue: 400 }',
        '{ id: "utilities", label: "Utilities & Phone", type: "number", placeholder: "200", min: 0, unit: "$", defaultValue: 200 }',
        '{ id: "insurance", label: "Insurance & Healthcare", type: "number", placeholder: "300", min: 0, unit: "$", defaultValue: 300 }',
        '{ id: "entertainment", label: "Entertainment & Dining Out", type: "number", placeholder: "300", min: 0, unit: "$", defaultValue: 300 }',
        '{ id: "other", label: "Other Expenses", type: "number", placeholder: "200", min: 0, unit: "$", defaultValue: 200 }',
    ],
    gauge_cfg='min: 0, max: 100, unit: "% savings rate",\n            zones: [\n              { label: "Negative", color: "#ef4444", from: 0, to: 5 },\n              { label: "Low", color: "#f59e0b", from: 5, to: 15 },\n              { label: "Good", color: "#3b82f6", from: 15, to: 25 },\n              { label: "Excellent", color: "#22c55e", from: 25, to: 100 },\n            ]',
    faqs_arr=[
        ("How much of my income should go to housing?", "The standard rule is to keep housing costs under 30% of gross income (or 28% for a mortgage). Some financial experts use 25% of net take-home pay. Above 30% is considered cost-burdened by the US Department of Housing."),
        ("What is the 50/30/20 budgeting rule?", "50% to needs (housing, food, transport, utilities), 30% to wants (dining, entertainment, subscriptions), 20% to savings and debt repayment. It provides structure while allowing flexibility. Adjust percentages based on your income and goals."),
        ("How do I track my spending?", "Bank and credit card statements are the most accurate source. Apps like YNAB, Mint, Copilot, or Monarch Money link to accounts and auto-categorize. A simple spreadsheet works too. Review weekly or monthly to catch overspending early."),
        ("What should be in an emergency fund?", "3–6 months of essential expenses (housing, food, transport, utilities, insurance). Not total income — just what you need to survive. Keep it in a high-yield savings account (HYSA) for 4–5% APY and easy access."),
        ("How do I stop overspending?", "Track every expense for 30 days (awareness alone reduces spending). Use a zero-based budget (assign every dollar). Try envelope budgeting for variable categories. Delay discretionary purchases 24–48 hours (reduces impulse buying by 50%+)."),
    ],
    related_arr=[("Savings Calculator", "/calculators/savings-calculator"), ("Emergency Fund Calculator", "/calculators/emergency-fund-calculator"), ("Salary Calculator", "/calculators/salary-calculator")],
    sidebar="""        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">50/30/20 Budget Guide</h3>
          <div class="space-y-2 text-xs text-blue-800">
            {[["Needs (50%)","Housing, food, transport, utilities, insurance"],["Wants (30%)","Dining, entertainment, hobbies, subscriptions"],["Savings (20%)","Emergency fund, retirement, goals, debt payoff"]].map(([cat, items]) => (
              <div class="border-b border-blue-100 pb-2">
                <div class="font-medium">{cat}</div>
                <div class="text-blue-600">{items}</div>
              </div>
            ))}
          </div>
        </div>""",
    content_section="""    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Average American Spending (2023)</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold text-gray-700">Category</th><th class="text-right p-2 text-xs font-semibold text-gray-700">Monthly Avg</th><th class="text-right p-2 text-xs font-semibold text-gray-700">% of Income</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Housing","$2,025","32%"],["Food","$779","12%"],["Transportation","$1,025","16%"],["Healthcare","$421","7%"],["Entertainment","$301","5%"],["Clothing","$163","3%"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
        <p class="text-xs text-gray-500 mt-1">Source: BLS Consumer Expenditure Survey</p>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Savings Rate and Retirement Age</h2>
        <p class="text-xs text-gray-600 mb-3">Higher savings rates dramatically reduce how long you need to work:</p>
        <div class="space-y-2">
          {[
            { rate: "5%", retire: "~66 years from start" },
            { rate: "10%", retire: "~51 years from start" },
            { rate: "20%", retire: "~37 years from start" },
            { rate: "30%", retire: "~28 years from start" },
            { rate: "50%", retire: "~17 years from start" },
            { rate: "75%", retire: "~7 years from start" },
          ].map(s => (
            <div class="flex justify-between bg-gray-50 rounded-lg px-3 py-2 text-xs">
              <span class="font-medium text-blue-600">{s.rate} savings rate</span>
              <span class="text-gray-600">{s.retire}</span>
            </div>
          ))}
        </div>
      </div>
    </div>""",
    result_label="Monthly Surplus",
    calc_desc="Plan your monthly budget by category and find your savings rate"
))

print("\nBatch 5 done: amortization, roi, inflation, salary, budget")
