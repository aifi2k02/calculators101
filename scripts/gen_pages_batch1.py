#!/usr/bin/env python3
"""Generate enhanced calculator pages - Batch 1: Financial calculators"""
import os

CALC_DIR = "/Users/apple/Documents/Projects/calculators-for-free/src/pages/calculators"

def write(slug, content):
    path = os.path.join(CALC_DIR, f"{slug}-calculator.astro")
    with open(path, 'w') as f:
        f.write(content)
    print(f"✅ {slug}-calculator.astro")

# ─── SAVINGS ─────────────────────────────────────────────────────────────────
write("savings", """---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const goal = parseFloat(inputs.goal) || 0
  const initial = parseFloat(inputs.initial) || 0
  const monthly = parseFloat(inputs.monthly) || 0
  const rate = parseFloat(inputs.rate) || 0
  const r = rate / 100 / 12
  if (monthly <= 0) throw new Error('Enter a monthly saving amount.')
  const need = goal - initial
  if (need <= 0) return { value: 'Goal already met!', stats: [{ label: 'Status', value: 'Done ✓' }] }
  let months = 0
  if (r === 0) {
    months = Math.ceil(need / monthly)
  } else {
    months = Math.ceil(Math.log(1 + (need * r) / monthly) / Math.log(1 + r))
  }
  const years = Math.floor(months / 12)
  const remMonths = months % 12
  const totalSaved = initial + monthly * months
  const interest = totalSaved > goal ? totalSaved - goal : 0
  const pct = Math.min((goal / Math.max(totalSaved, 1)) * 100, 100)
  return {
    value: years + 'y ' + remMonths + 'm to reach goal',
    gaugeValue: pct,
    breakdown: [
      'Months to goal: ' + months,
      'Total deposited: $' + totalSaved.toLocaleString('en-US', { maximumFractionDigits: 0 }),
      'Interest earned: $' + interest.toLocaleString('en-US', { maximumFractionDigits: 0 }),
    ],
    stats: [
      { label: 'Time to Goal', value: years + 'y ' + remMonths + 'm' },
      { label: 'Total Deposited', value: '$' + totalSaved.toLocaleString('en-US', { maximumFractionDigits: 0 }) },
      { label: 'Interest Earned', value: '$' + interest.toLocaleString('en-US', { maximumFractionDigits: 0 }) },
      { label: 'Months', value: String(months) },
    ]
  }
`

const faqs = [
  { question: 'How much should I save each month?', answer: 'The standard guideline is to save at least 20% of your income (the 50/30/20 rule). For a specific goal, divide the amount needed by the months available. Emergency funds typically need 3–6 months of expenses.' },
  { question: 'Does interest rate matter for short-term savings?', answer: 'For short-term goals (under 2 years), rate matters less. On $500/month for 1 year, the difference between 0% and 5% APY is only about $135. For longer goals, higher-yield accounts make a significant difference.' },
  { question: 'What is a high-yield savings account?', answer: 'A high-yield savings account (HYSA) pays significantly more interest than a standard savings account. As of 2024–2025, top HYSAs pay 4–5% APY vs. the national average of ~0.46%. They are FDIC-insured and safe.' },
  { question: 'Should I save or pay off debt first?', answer: "If debt interest > savings interest, paying debt first wins mathematically. But most experts recommend keeping a small emergency fund ($1,000–$3,000) while aggressively paying high-interest debt, then building 3–6 months after debt is paid." },
  { question: 'How do I automate my savings?', answer: 'Set up automatic transfers from your checking to savings account on payday. Treat savings like a bill. Many banks let you split direct deposits — send 20% straight to savings before it even hits your checking account.' },
]
---
<Layout
  title="Savings Calculator: How Long to Reach Your Goal?"
  description="Calculate how long it takes to reach your savings goal with monthly contributions. Free savings calculator with interest rate support."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Financial', href: '/calculators/financial' },
    { name: 'Savings Calculator', href: '/calculators/savings-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/financial" class="hover:text-blue-600">Financial</a><span>›</span>
      <span class="text-gray-900">Savings Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Savings Calculator"
          description="Find out how long it takes to reach your savings goal"
          formulaId="savings"
          formulaFn={formulaFn}
          resultLabel="Time to Goal"
          inputs={[
            { id: 'goal', label: 'Savings Goal', type: 'number', placeholder: '10000', min: 0, unit: '$', defaultValue: 10000 },
            { id: 'initial', label: 'Initial Amount', type: 'number', placeholder: '0', min: 0, unit: '$', defaultValue: 0 },
            { id: 'monthly', label: 'Monthly Savings', type: 'number', placeholder: '500', min: 0, unit: '$', defaultValue: 500 },
            { id: 'rate', label: 'Annual Interest Rate (APY)', type: 'number', placeholder: '4.5', min: 0, max: 20, step: 0.1, unit: '%', defaultValue: 4.5 },
          ]}
          gauge={{
            min: 0, max: 100, unit: '% funded',
            zones: [
              { label: 'Just Starting', color: '#ef4444', from: 0, to: 25 },
              { label: 'Building', color: '#f59e0b', from: 25, to: 60 },
              { label: 'Almost There', color: '#3b82f6', from: 60, to: 90 },
              { label: 'Goal Met', color: '#22c55e', from: 90, to: 100 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'Compound Interest Calculator', href: '/calculators/compound-interest-calculator' },
            { name: 'Emergency Fund Calculator', href: '/calculators/emergency-fund-calculator' },
            { name: 'Budget Calculator', href: '/calculators/budget-calculator' },
            { name: 'Retirement Calculator', href: '/calculators/retirement-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Savings Rate Guide</h3>
          <div class="space-y-2 text-xs text-blue-800">
            {[['Emergency fund', '3–6 months expenses'], ['Retirement', '15% of gross income'], ['Home down payment', '20% of home price'], ['Vacation', 'Monthly cost ÷ months left']].map(([g, t]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1">
                <span>{g}</span><span class="font-medium">{t}</span>
              </div>
            ))}
          </div>
        </div>
        <div class="bg-green-50 border border-green-200 rounded-xl p-5">
          <h3 class="font-bold text-green-900 mb-2">Best Savings Accounts 2025</h3>
          <ul class="text-xs text-green-800 space-y-1">
            <li>• High-yield savings: 4–5% APY</li>
            <li>• Money market: 4–5% APY</li>
            <li>• 12-month CD: 4.5–5% APY</li>
            <li>• Standard savings: 0.4–0.6% APY</li>
          </ul>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">The 50/30/20 Savings Rule</h2>
        <p class="text-gray-600 text-sm mb-3">Allocate your after-tax income: 50% to needs (rent, food, utilities), 30% to wants (dining, entertainment), and 20% to savings and debt repayment. This creates a sustainable balance between enjoying life today and securing tomorrow.</p>
        <div class="grid grid-cols-3 gap-3">
          {[['50%', 'Needs', 'Housing, food, transport, utilities'], ['30%', 'Wants', 'Dining, hobbies, subscriptions'], ['20%', 'Savings', 'Emergency fund, retirement, goals']].map(([pct, label, detail]) => (
            <div class="bg-gray-50 rounded-lg p-3 text-center">
              <div class="text-2xl font-bold text-blue-600 mb-1">{pct}</div>
              <div class="font-semibold text-gray-800 text-xs mb-1">{label}</div>
              <div class="text-xs text-gray-500">{detail}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Time to Save $10,000</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr>
            <th class="text-left p-3 text-xs font-semibold text-gray-700">Monthly Savings</th>
            <th class="text-right p-3 text-xs font-semibold text-gray-700">At 0% APY</th>
            <th class="text-right p-3 text-xs font-semibold text-gray-700">At 4.5% APY</th>
          </tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[['$100','100 mo','88 mo'],['$200','50 mo','46 mo'],['$500','20 mo','19 mo'],['$1,000','10 mo','10 mo']].map(r => (
              <tr><td class="p-3 text-xs">{r[0]}</td><td class="p-3 text-xs text-right">{r[1]}</td><td class="p-3 text-xs text-right text-green-600">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</Layout>
""")

# ─── RETIREMENT ───────────────────────────────────────────────────────────────
write("retirement", """---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const currentAge = parseInt(inputs.currentAge) || 30
  const retireAge = parseInt(inputs.retireAge) || 65
  const savings = parseFloat(inputs.savings) || 0
  const monthly = parseFloat(inputs.monthly) || 0
  const rate = parseFloat(inputs.rate) || 7
  const withdrawalRate = parseFloat(inputs.withdrawal) || 4
  if (retireAge <= currentAge) throw new Error('Retirement age must be greater than current age.')
  const years = retireAge - currentAge
  const r = rate / 100 / 12
  const months = years * 12
  const fv = savings * Math.pow(1 + r, months) + monthly * (Math.pow(1 + r, months) - 1) / r
  const annualWithdrawal = fv * (withdrawalRate / 100)
  const monthlyIncome = annualWithdrawal / 12
  const readiness = Math.min((fv / Math.max(monthlyIncome * 12 * 25, 1)) * 100, 100)
  return {
    value: '$' + fv.toLocaleString('en-US', { maximumFractionDigits: 0 }),
    gaugeValue: Math.min(readiness, 100),
    breakdown: [
      'Years to retirement: ' + years,
      'Monthly retirement income: $' + monthlyIncome.toLocaleString('en-US', { maximumFractionDigits: 0 }),
      'Annual withdrawal (' + withdrawalRate + '%): $' + annualWithdrawal.toLocaleString('en-US', { maximumFractionDigits: 0 }),
    ],
    stats: [
      { label: 'Nest Egg at Retirement', value: '$' + fv.toLocaleString('en-US', { maximumFractionDigits: 0 }) },
      { label: 'Monthly Income', value: '$' + monthlyIncome.toLocaleString('en-US', { maximumFractionDigits: 0 }) },
      { label: 'Years to Retire', value: String(years) },
      { label: 'Withdrawal Rate', value: withdrawalRate + '%' },
    ]
  }
`

const faqs = [
  { question: 'How much do I need to retire?', answer: 'A common rule: multiply your desired annual retirement income by 25 (the "4% rule"). To spend $60,000/year in retirement, you need $1.5 million. This assumes a 4% annual withdrawal rate and a 30-year retirement.' },
  { question: 'What is the 4% rule?', answer: 'Research (the "Trinity Study") found that withdrawing 4% of your portfolio in year one, then adjusting for inflation, has historically lasted 30+ years in almost all market conditions. It is a starting point, not a guarantee.' },
  { question: 'How much should I contribute to my 401(k)?', answer: 'At minimum, contribute enough to get your full employer match — that is free money. Ideally, save 15% of gross income for retirement. Max 401(k) contribution in 2025 is $23,500 ($31,000 if age 50+).' },
  { question: 'Roth vs traditional 401(k): which is better?', answer: 'Roth = pay taxes now, withdrawals tax-free. Traditional = tax deduction now, pay taxes in retirement. If you expect to be in a higher tax bracket in retirement, Roth wins. Most experts suggest using both to diversify tax risk.' },
  { question: 'Can I retire early?', answer: 'Yes. The FIRE (Financial Independence, Retire Early) movement targets 25× annual expenses. With a 3.5% withdrawal rate for longer retirements, you may need 28–30× expenses. Retiring early means more years of withdrawals and less time to save.' },
]
---
<Layout
  title="Retirement Calculator: How Much Do You Need to Retire?"
  description="Calculate your retirement nest egg and monthly income. Plan how much to save each month to retire comfortably with our free retirement calculator."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Financial', href: '/calculators/financial' },
    { name: 'Retirement Calculator', href: '/calculators/retirement-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/financial" class="hover:text-blue-600">Financial</a><span>›</span>
      <span class="text-gray-900">Retirement Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Retirement Calculator"
          description="Project your retirement savings and estimate monthly income"
          formulaId="retirement"
          formulaFn={formulaFn}
          resultLabel="Retirement Nest Egg"
          inputs={[
            { id: 'currentAge', label: 'Current Age', type: 'number', placeholder: '30', min: 18, max: 80, unit: 'years', defaultValue: 30 },
            { id: 'retireAge', label: 'Retirement Age', type: 'number', placeholder: '65', min: 30, max: 90, unit: 'years', defaultValue: 65 },
            { id: 'savings', label: 'Current Savings', type: 'number', placeholder: '50000', min: 0, unit: '$', defaultValue: 50000 },
            { id: 'monthly', label: 'Monthly Contribution', type: 'number', placeholder: '500', min: 0, unit: '$', defaultValue: 500 },
            { id: 'rate', label: 'Annual Return Rate', type: 'number', placeholder: '7', min: 0, max: 20, step: 0.1, unit: '%', defaultValue: 7 },
            { id: 'withdrawal', label: 'Withdrawal Rate', type: 'number', placeholder: '4', min: 1, max: 10, step: 0.1, unit: '%', defaultValue: 4 },
          ]}
          gauge={{
            min: 0, max: 100, unit: '% readiness',
            zones: [
              { label: 'Off Track', color: '#ef4444', from: 0, to: 40 },
              { label: 'Behind', color: '#f59e0b', from: 40, to: 70 },
              { label: 'On Track', color: '#3b82f6', from: 70, to: 90 },
              { label: 'Ahead', color: '#22c55e', from: 90, to: 100 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: '401(k) Calculator', href: '/calculators/401k-calculator' },
            { name: 'Roth IRA Calculator', href: '/calculators/roth-ira-calculator' },
            { name: 'FIRE Calculator', href: '/calculators/fire-calculator' },
            { name: 'Investment Calculator', href: '/calculators/investment-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Retirement Benchmarks by Age</h3>
          <div class="space-y-2 text-xs text-blue-800">
            {[['Age 30', '1× annual salary'],['Age 40', '3× annual salary'],['Age 50', '6× annual salary'],['Age 60', '8× annual salary'],['Age 67', '10× annual salary']].map(([a, b]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span>{a}</span><span class="font-medium">{b}</span></div>
            ))}
          </div>
          <p class="text-xs text-blue-700 mt-2">Source: Fidelity Investments guidelines</p>
        </div>
        <div class="bg-amber-50 border border-amber-200 rounded-xl p-5">
          <h3 class="font-bold text-amber-900 mb-2">2025 Contribution Limits</h3>
          <ul class="text-xs text-amber-800 space-y-1">
            <li>• 401(k): $23,500 ($31,000 if 50+)</li>
            <li>• IRA: $7,000 ($8,000 if 50+)</li>
            <li>• HSA (family): $8,550</li>
            <li>• Roth IRA phases out at $150k–$165k (single)</li>
          </ul>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">The 4% Rule Explained</h2>
        <p class="text-gray-600 text-sm mb-3">The 4% rule states you can safely withdraw 4% of your portfolio in year one, then adjust for inflation each year, for a 30-year retirement. A $1M portfolio supports $40,000/year ($3,333/month) in this model.</p>
        <div class="grid grid-cols-2 gap-3">
          {[['$500k','$20,000/yr'],['$1M','$40,000/yr'],['$1.5M','$60,000/yr'],['$2M','$80,000/yr']].map(([nest, income]) => (
            <div class="bg-gray-50 rounded-lg p-3 text-center">
              <div class="font-bold text-blue-600 text-sm">{nest}</div>
              <div class="text-xs text-gray-500">nest egg</div>
              <div class="font-semibold text-gray-800 text-xs mt-1">{income}/yr income</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Account Types Comparison</h2>
        <table class="w-full text-xs border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr>
            <th class="text-left p-2 font-semibold text-gray-700">Account</th>
            <th class="text-left p-2 font-semibold text-gray-700">Tax Now</th>
            <th class="text-left p-2 font-semibold text-gray-700">Tax Later</th>
          </tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[['Traditional 401k','No deduction','Yes, on withdrawal'],['Roth 401k','Yes (after-tax)','No (tax-free)'],['Traditional IRA','Deductible','Yes, on withdrawal'],['Roth IRA','Yes (after-tax)','No (tax-free)']].map(r => (
              <tr><td class="p-2">{r[0]}</td><td class="p-2">{r[1]}</td><td class="p-2">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</Layout>
""")

# ─── INVESTMENT ───────────────────────────────────────────────────────────────
write("investment", """---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const initial = parseFloat(inputs.initial) || 0
  const monthly = parseFloat(inputs.monthly) || 0
  const rate = parseFloat(inputs.rate) || 0
  const years = parseFloat(inputs.years) || 0
  const inflation = parseFloat(inputs.inflation) || 0
  if (years <= 0) throw new Error('Investment period must be greater than 0.')
  const r = rate / 100 / 12
  const months = years * 12
  const fv = initial * Math.pow(1 + r, months) + (monthly > 0 && r > 0 ? monthly * (Math.pow(1 + r, months) - 1) / r : monthly * months)
  const totalInvested = initial + monthly * months
  const gains = fv - totalInvested
  const realRate = ((1 + rate / 100) / (1 + inflation / 100) - 1) * 100
  const realFv = initial * Math.pow(1 + realRate / 100 / 12, months) + (monthly > 0 ? monthly * (Math.pow(1 + realRate / 100 / 12, months) - 1) / (realRate / 100 / 12) : 0)
  const roi = totalInvested > 0 ? (gains / totalInvested) * 100 : 0
  return {
    value: '$' + fv.toLocaleString('en-US', { maximumFractionDigits: 0 }),
    gaugeValue: Math.min(roi, 500),
    breakdown: [
      'Total invested: $' + totalInvested.toLocaleString('en-US', { maximumFractionDigits: 0 }),
      'Investment gains: $' + gains.toLocaleString('en-US', { maximumFractionDigits: 0 }),
      'ROI: ' + roi.toFixed(1) + '%',
      'Inflation-adjusted value: $' + realFv.toLocaleString('en-US', { maximumFractionDigits: 0 }),
    ],
    stats: [
      { label: 'Final Value', value: '$' + fv.toLocaleString('en-US', { maximumFractionDigits: 0 }) },
      { label: 'Total Gains', value: '$' + gains.toLocaleString('en-US', { maximumFractionDigits: 0 }) },
      { label: 'ROI', value: roi.toFixed(1) + '%' },
      { label: 'Real Value (adj.)', value: '$' + realFv.toLocaleString('en-US', { maximumFractionDigits: 0 }) },
    ]
  }
`

const faqs = [
  { question: 'What is a good ROI for investments?', answer: 'The S&P 500 has averaged ~10% annually since 1926 (~7% after inflation). Bonds average 2–5%. Real estate varies widely. For retirement planning, 6–8% is a conservative assumption for diversified stock portfolios.' },
  { question: 'How does inflation affect investment returns?', answer: 'Inflation erodes purchasing power. A 10% nominal return with 3% inflation gives a real return of ~6.8%. Always consider real returns for long-term planning — $1M in 30 years is worth far less than $1M today.' },
  { question: 'What is dollar-cost averaging (DCA)?', answer: 'DCA means investing a fixed amount at regular intervals (e.g., $500/month) regardless of market price. This reduces the impact of volatility — you buy more shares when prices are low and fewer when high, averaging out your cost basis.' },
  { question: 'How much should I invest monthly?', answer: 'Financial advisors recommend investing 15% of gross income for retirement. If you cannot reach 15% immediately, start with whatever you can (even $50/month) and increase by 1% each year.' },
  { question: 'When should I start investing?', answer: 'As soon as possible. Thanks to compounding, $10,000 invested at age 25 grows to ~$217,000 by age 65 at 8% annual returns. The same $10,000 invested at 45 only grows to ~$46,600. Every year of delay costs significantly.' },
]
---
<Layout
  title="Investment Calculator: Project Your Portfolio Growth"
  description="Calculate how your investments grow over time with compounding returns. Includes inflation adjustment and monthly contribution support."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Financial', href: '/calculators/financial' },
    { name: 'Investment Calculator', href: '/calculators/investment-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/financial" class="hover:text-blue-600">Financial</a><span>›</span>
      <span class="text-gray-900">Investment Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Investment Calculator"
          description="Project investment growth with compounding and inflation adjustment"
          formulaId="investment"
          formulaFn={formulaFn}
          resultLabel="Portfolio Value"
          inputs={[
            { id: 'initial', label: 'Initial Investment', type: 'number', placeholder: '10000', min: 0, unit: '$', defaultValue: 10000 },
            { id: 'monthly', label: 'Monthly Contribution', type: 'number', placeholder: '500', min: 0, unit: '$', defaultValue: 500 },
            { id: 'rate', label: 'Annual Return Rate', type: 'number', placeholder: '8', min: 0, max: 30, step: 0.1, unit: '%', defaultValue: 8 },
            { id: 'years', label: 'Investment Period', type: 'number', placeholder: '20', min: 1, max: 50, unit: 'years', defaultValue: 20 },
            { id: 'inflation', label: 'Inflation Rate', type: 'number', placeholder: '3', min: 0, max: 15, step: 0.1, unit: '%', defaultValue: 3 },
          ]}
          gauge={{
            min: 0, max: 500, clampMax: 500, unit: '% ROI',
            zones: [
              { label: 'Low', color: '#94a3b8', from: 0, to: 50 },
              { label: 'Moderate', color: '#3b82f6', from: 50, to: 150 },
              { label: 'Strong', color: '#22c55e', from: 150, to: 300 },
              { label: 'Exceptional', color: '#f59e0b', from: 300, to: 500 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'Compound Interest Calculator', href: '/calculators/compound-interest-calculator' },
            { name: 'Retirement Calculator', href: '/calculators/retirement-calculator' },
            { name: 'DCA Calculator', href: '/calculators/dca-calculator' },
            { name: 'ROI Calculator', href: '/calculators/roi-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Historical Returns by Asset Class</h3>
          <div class="space-y-2 text-xs text-blue-800">
            {[['US Stocks (S&P 500)','~10%/yr'],['International Stocks','~7–8%/yr'],['Bonds (10-yr Treasury)','~3–5%/yr'],['Real Estate (REITs)','~8–10%/yr'],['Cash / HYSA','~4–5%/yr (2025)']].map(([a,b]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span>{a}</span><span class="font-medium">{b}</span></div>
            ))}
          </div>
        </div>
        <div class="bg-amber-50 border border-amber-200 rounded-xl p-5">
          <h3 class="font-bold text-amber-900 mb-2">Rule of 72</h3>
          <p class="text-xs text-amber-800">Divide 72 by your return rate to find years to double your money:</p>
          <ul class="text-xs text-amber-900 mt-2 space-y-1 font-medium">
            <li>• 6% → doubles in 12 years</li>
            <li>• 8% → doubles in 9 years</li>
            <li>• 10% → doubles in 7.2 years</li>
          </ul>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">$500/Month Investment Over Time</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr>
            <th class="text-left p-3 text-xs font-semibold text-gray-700">Years</th>
            <th class="text-right p-3 text-xs font-semibold text-gray-700">Total Invested</th>
            <th class="text-right p-3 text-xs font-semibold text-gray-700">At 8% Return</th>
          </tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[['10','$60,000','$91,473'],['20','$120,000','$294,510'],['30','$180,000','$745,180'],['40','$240,000','$1,750,202']].map(r => (
              <tr><td class="p-3 text-xs">{r[0]}</td><td class="p-3 text-xs text-right">{r[1]}</td><td class="p-3 text-xs text-right text-green-600 font-medium">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Diversification Basics</h2>
        <p class="text-gray-600 text-sm mb-3">Don't put all eggs in one basket. A diversified portfolio reduces risk without proportionally reducing returns.</p>
        <div class="space-y-2">
          {[
            { label: 'Aggressive (25–35)', pct: '90% stocks / 10% bonds' },
            { label: 'Moderate (35–50)', pct: '70% stocks / 30% bonds' },
            { label: 'Conservative (50–65)', pct: '50% stocks / 50% bonds' },
            { label: 'Income (65+)', pct: '30% stocks / 70% bonds' },
          ].map(p => (
            <div class="flex items-center gap-3 bg-gray-50 rounded-lg p-3">
              <div class="text-xs font-medium text-gray-700 w-36">{p.label}</div>
              <div class="text-xs text-gray-600">{p.pct}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
</Layout>
""")

# ─── AUTO LOAN ────────────────────────────────────────────────────────────────
write("auto-loan", """---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const price = parseFloat(inputs.price) || 0
  const down = parseFloat(inputs.down) || 0
  const rate = parseFloat(inputs.rate) || 0
  const term = parseInt(inputs.term) || 60
  const tradeIn = parseFloat(inputs.tradeIn) || 0
  const principal = price - down - tradeIn
  if (principal <= 0) throw new Error('Down payment exceeds vehicle price.')
  if (rate < 0) throw new Error('Interest rate must be positive.')
  const r = rate / 100 / 12
  const payment = r === 0 ? principal / term : principal * r * Math.pow(1 + r, term) / (Math.pow(1 + r, term) - 1)
  const totalCost = payment * term + down + tradeIn * 0
  const totalInterest = payment * term - principal
  const affordabilityScore = Math.max(0, Math.min(100, 100 - (payment / Math.max(price * 0.02, 1)) * 10))
  return {
    value: '$' + payment.toFixed(2) + '/mo',
    gaugeValue: affordabilityScore,
    breakdown: [
      'Loan amount: $' + principal.toLocaleString('en-US', { maximumFractionDigits: 0 }),
      'Total interest: $' + totalInterest.toLocaleString('en-US', { maximumFractionDigits: 0 }),
      'Total cost: $' + (payment * term + down).toLocaleString('en-US', { maximumFractionDigits: 0 }),
    ],
    stats: [
      { label: 'Monthly Payment', value: '$' + payment.toFixed(2) },
      { label: 'Total Interest', value: '$' + totalInterest.toLocaleString('en-US', { maximumFractionDigits: 0 }) },
      { label: 'Loan Amount', value: '$' + principal.toLocaleString('en-US', { maximumFractionDigits: 0 }) },
      { label: 'Total Cost', value: '$' + (payment * term + down).toLocaleString('en-US', { maximumFractionDigits: 0 }) },
    ]
  }
`

const faqs = [
  { question: 'What is a good car loan interest rate?', answer: 'As of 2025, excellent credit (720+) typically qualifies for 5–7% APR on new cars. Average credit (660–720) sees 7–10%. Below 660 may face 10–20%+. Credit unions often offer lower rates than dealerships.' },
  { question: 'How much car can I afford?', answer: "The 20/4/10 rule: put 20% down, finance for no more than 4 years, and keep total vehicle costs (payment + insurance) under 10% of monthly gross income. For a $5,000/mo income, total auto costs should be under $500/mo." },
  { question: 'Should I choose a shorter or longer loan term?', answer: 'Shorter terms (36–48 months) save significant interest but have higher payments. Longer terms (72–84 months) lower payments but cost more overall and risk being underwater (owing more than the car is worth).' },
  { question: 'What is a trade-in and how does it help?', answer: "A trade-in is your old vehicle's value applied to the new purchase. It reduces the loan amount needed and can save on sales tax in many states (you pay tax only on the price difference, not the full price)." },
  { question: 'Is 0% financing really free?', answer: '0% APR promotions from dealers often come with a catch: you may give up a cash rebate worth more than the interest saved, or need excellent credit (750+) to qualify. Always compare 0% financing vs. taking a rebate and getting a low-rate loan.' },
]
---
<Layout
  title="Auto Loan Calculator: Monthly Car Payment Estimator"
  description="Calculate your monthly car payment, total interest, and total cost. Supports down payment and trade-in. Free auto loan calculator."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Financial', href: '/calculators/financial' },
    { name: 'Auto Loan Calculator', href: '/calculators/auto-loan-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/financial" class="hover:text-blue-600">Financial</a><span>›</span>
      <span class="text-gray-900">Auto Loan Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Auto Loan Calculator"
          description="Calculate your monthly car payment and total cost of financing"
          formulaId="auto-loan"
          formulaFn={formulaFn}
          resultLabel="Monthly Payment"
          inputs={[
            { id: 'price', label: 'Vehicle Price', type: 'number', placeholder: '30000', min: 0, unit: '$', defaultValue: 30000 },
            { id: 'down', label: 'Down Payment', type: 'number', placeholder: '6000', min: 0, unit: '$', defaultValue: 6000 },
            { id: 'tradeIn', label: 'Trade-In Value', type: 'number', placeholder: '0', min: 0, unit: '$', defaultValue: 0 },
            { id: 'rate', label: 'Interest Rate (APR)', type: 'number', placeholder: '6.5', min: 0, max: 30, step: 0.1, unit: '%', defaultValue: 6.5 },
            { id: 'term', label: 'Loan Term', type: 'select', options: [
              { value: '24', label: '24 months (2 yr)' },
              { value: '36', label: '36 months (3 yr)' },
              { value: '48', label: '48 months (4 yr)' },
              { value: '60', label: '60 months (5 yr)' },
              { value: '72', label: '72 months (6 yr)' },
              { value: '84', label: '84 months (7 yr)' },
            ], defaultValue: '60' },
          ]}
          gauge={{
            min: 0, max: 100, unit: '% affordability',
            zones: [
              { label: 'Stretch', color: '#ef4444', from: 0, to: 30 },
              { label: 'Manageable', color: '#f59e0b', from: 30, to: 60 },
              { label: 'Comfortable', color: '#22c55e', from: 60, to: 100 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'Loan Calculator', href: '/calculators/loan-calculator' },
            { name: 'Car Lease Calculator', href: '/calculators/car-lease-calculator' },
            { name: 'APR Calculator', href: '/calculators/apr-calculator' },
            { name: 'Budget Calculator', href: '/calculators/budget-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">$25,000 Loan Payment by Term</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700"><th class="text-left pb-1">Term</th><th class="text-right pb-1">Payment</th><th class="text-right pb-1">Total Interest</th></tr></thead>
            <tbody class="text-blue-900">
              {[['36 mo','$760/mo','$1,376'],['48 mo','$583/mo','$1,985'],['60 mo','$475/mo','$2,509'],['72 mo','$402/mo','$3,087']].map(r => (
                <tr class="border-t border-blue-100"><td class="py-1">{r[0]}</td><td class="text-right">{r[1]}</td><td class="text-right">{r[2]}</td></tr>
              ))}
            </tbody>
          </table>
          <p class="text-xs text-blue-600 mt-1">At 6.5% APR</p>
        </div>
        <div class="bg-amber-50 border border-amber-200 rounded-xl p-5">
          <h3 class="font-bold text-amber-900 mb-2">20/4/10 Rule</h3>
          <ul class="text-xs text-amber-800 space-y-1">
            <li>• <strong>20%</strong> down payment minimum</li>
            <li>• <strong>4 years</strong> max loan term</li>
            <li>• <strong>10%</strong> of income max for auto costs</li>
          </ul>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Loan vs Lease: Which Is Better?</h2>
        <div class="space-y-3">
          {[
            { opt: 'Buy (Loan)', pros: 'Build equity, no mileage limits, eventually payment-free', cons: 'Higher monthly payment, responsible for all repairs' },
            { opt: 'Lease', pros: 'Lower monthly payment, always drive a new car, covered by warranty', cons: 'No equity, mileage limits (~12k/yr), fees for wear and tear' },
          ].map(o => (
            <div class="bg-gray-50 rounded-lg p-4">
              <div class="font-semibold text-gray-800 text-sm mb-2">{o.opt}</div>
              <div class="text-xs text-green-700 mb-1">✓ {o.pros}</div>
              <div class="text-xs text-red-600">✗ {o.cons}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Tips to Get a Lower Rate</h2>
        <div class="space-y-2">
          {[
            'Check your credit score before shopping — above 720 gets the best rates',
            'Get pre-approved by your bank or credit union first',
            'Negotiate the car price separately from financing',
            'Avoid dealer add-ons (GAP insurance, extended warranties) rolled into the loan',
            'Make a larger down payment to reduce principal and improve loan-to-value ratio',
            'Consider a shorter term — lenders offer lower rates for 36 vs. 72-month loans',
          ].map(tip => (
            <div class="flex gap-2 text-xs text-gray-600">
              <span class="text-blue-500 mt-0.5 flex-shrink-0">•</span>
              <span>{tip}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
</Layout>
""")

print("\\n✅ Batch 1 financial pages complete (compound-interest already done separately).")
print("Pages written: savings, retirement, investment, auto-loan")
