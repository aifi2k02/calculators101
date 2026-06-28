#!/usr/bin/env python3
"""Batch 2: Financial calculators — credit card, debt payoff, interest, salary, budget, net-worth, amortization, house-affordability, refinance, down-payment, paycheck, 401k, rent-vs-buy, APR, car-lease, home-equity, CD, stock-profit, break-even, markup, income-tax, Roth IRA, PMI, emergency-fund, FIRE, capital-gains, annuity, dividend, ROI, rule-of-72"""
import os

CALC_DIR = "/Users/apple/Documents/Projects/calculators-for-free/src/pages/calculators"

def write(slug, content):
    path = os.path.join(CALC_DIR, f"{slug}-calculator.astro")
    with open(path, 'w') as f:
        f.write(content)
    print(f"✅ {slug}-calculator.astro")

TEMPLATE = '''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `{formula}`

const faqs = {faqs}
---
<Layout
  title="{seo_title}"
  description="{seo_desc}"
  breadcrumbs={{[
    {{ name: 'Home', href: '/' }},
    {{ name: '{category}', href: '/calculators/{cat_slug}' }},
    {{ name: '{title}', href: '/calculators/{slug}-calculator' }},
  ]}}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/{cat_slug}" class="hover:text-blue-600">{category}</a><span>›</span>
      <span class="text-gray-900">{title}</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="{title}"
          description="{calc_desc}"
          formulaId="{slug}"
          formulaFn={{formulaFn}}
          resultLabel="{result_label}"
          inputs={{{inputs}}}
          gauge={{{gauge}}}
          faqs={{faqs}}
          relatedCalcs={{{related}}}
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

# ─── CREDIT CARD ─────────────────────────────────────────────────────────────
write("credit-card", '''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const balance = parseFloat(inputs.balance) || 0
  const rate = parseFloat(inputs.rate) || 0
  const payment = parseFloat(inputs.payment) || 0
  if (balance <= 0) throw new Error('Enter a balance.')
  if (payment <= 0) throw new Error('Enter a monthly payment.')
  const r = rate / 100 / 12
  const minPayment = Math.max(balance * 0.02, 25)
  if (payment < minPayment && payment < balance) throw new Error('Payment too low — minimum is ~2% of balance or $25.')
  let months = 0, totalInterest = 0, bal = balance
  while (bal > 0 && months < 600) {
    const interest = bal * r
    totalInterest += interest
    bal = bal + interest - payment
    if (bal < 0) bal = 0
    months++
  }
  const score = Math.max(0, Math.min(100, 100 - (months / 6)))
  return {
    value: months >= 600 ? 'Never (increase payment)' : months + ' months to pay off',
    gaugeValue: score,
    breakdown: [
      'Payoff time: ' + Math.floor(months/12) + 'y ' + (months%12) + 'm',
      'Total interest paid: $' + totalInterest.toFixed(2),
      'Total paid: $' + (balance + totalInterest).toFixed(2),
    ],
    stats: [
      { label: 'Months to Payoff', value: String(months) },
      { label: 'Total Interest', value: '$' + totalInterest.toFixed(2) },
      { label: 'Total Paid', value: '$' + (balance + totalInterest).toFixed(2) },
      { label: 'Interest %', value: ((totalInterest/balance)*100).toFixed(0) + '% extra' },
    ]
  }
`

const faqs = [
  { question: 'What is the minimum credit card payment?', answer: 'Most cards require a minimum payment of 1–2% of the balance or $25–35, whichever is greater. Paying only the minimum on a $5,000 balance at 20% APR could take 27+ years and cost over $7,000 in interest.' },
  { question: 'How does credit card interest work?', answer: 'Credit card APR is divided by 365 (daily periodic rate). Interest accrues on your average daily balance. If you pay in full each month, you pay zero interest. If you carry a balance, interest compounds daily.' },
  { question: 'What is a good credit card APR?', answer: 'The average credit card APR in 2025 is ~21%. Cards for excellent credit may offer 15–18%. Store cards can reach 25–30%. If you carry a balance, look for cards with low APRs or 0% promotional periods.' },
  { question: 'Avalanche vs snowball: which debt payoff method is better?', answer: 'Avalanche (highest rate first) saves more money in interest. Snowball (smallest balance first) provides psychological wins and motivation. Studies show snowball leads to higher completion rates despite costing slightly more.' },
  { question: 'Does paying more than the minimum really help?', answer: 'Dramatically. On a $5,000 balance at 20% APR, paying $100/month takes 94 months and $4,311 in interest. Paying $200/month takes 32 months and $1,163 in interest. Double the payment, save 3× the interest.' },
]
---
<Layout
  title="Credit Card Payoff Calculator: Time & Interest to Pay Off Debt"
  description="See how long it takes to pay off your credit card debt and how much interest you'll pay. Free credit card payoff calculator."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Financial', href: '/calculators/financial' },
    { name: 'Credit Card Calculator', href: '/calculators/credit-card-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/financial" class="hover:text-blue-600">Financial</a><span>›</span>
      <span class="text-gray-900">Credit Card Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Credit Card Payoff Calculator"
          description="Find out how long it takes to pay off your credit card and how much interest you'll pay"
          formulaId="credit-card"
          formulaFn={formulaFn}
          resultLabel="Payoff Time"
          inputs={[
            { id: 'balance', label: 'Current Balance', type: 'number', placeholder: '5000', min: 0, unit: '$', defaultValue: 5000 },
            { id: 'rate', label: 'Annual Interest Rate (APR)', type: 'number', placeholder: '20', min: 0, max: 50, step: 0.1, unit: '%', defaultValue: 20 },
            { id: 'payment', label: 'Monthly Payment', type: 'number', placeholder: '200', min: 0, unit: '$', defaultValue: 200 },
          ]}
          gauge={{
            min: 0, max: 100, unit: '% speed score',
            zones: [
              { label: 'Very Slow', color: '#ef4444', from: 0, to: 25 },
              { label: 'Slow', color: '#f59e0b', from: 25, to: 50 },
              { label: 'Good Pace', color: '#3b82f6', from: 50, to: 75 },
              { label: 'Fast', color: '#22c55e', from: 75, to: 100 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'Debt Payoff Calculator', href: '/calculators/debt-payoff-calculator' },
            { name: 'Loan Calculator', href: '/calculators/loan-calculator' },
            { name: 'Budget Calculator', href: '/calculators/budget-calculator' },
            { name: 'APR Calculator', href: '/calculators/apr-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-red-50 border border-red-200 rounded-xl p-5">
          <h3 class="font-bold text-red-900 mb-3">$5,000 Balance at 20% APR</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-red-700"><th class="text-left pb-1">Payment</th><th class="text-right pb-1">Months</th><th class="text-right pb-1">Interest</th></tr></thead>
            <tbody class="text-red-900">
              {[['Min (~$100)','94','$4,311'],['$150','50','$2,264'],['$200','32','$1,163'],['$500','11','$285']].map(r => (
                <tr class="border-t border-red-100"><td class="py-1">{r[0]}</td><td class="text-right">{r[1]}</td><td class="text-right">{r[2]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-2">Payoff Strategies</h3>
          <div class="space-y-2 text-xs text-blue-800">
            <div><strong>Avalanche:</strong> Pay highest APR first. Saves most interest.</div>
            <div><strong>Snowball:</strong> Pay smallest balance first. Best for motivation.</div>
            <div><strong>Balance Transfer:</strong> Move to 0% promo card. Pay aggressively during promo.</div>
          </div>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">How Credit Card Interest Works</h2>
        <p class="text-gray-600 text-sm mb-3">Credit card APR is applied daily. Your average daily balance × (APR ÷ 365) = daily interest. This compounds throughout the month. If you pay your full statement balance by the due date, you pay zero interest (the grace period).</p>
        <div class="grid grid-cols-2 gap-3">
          {[
            { label: 'Grace Period', detail: 'Pay in full by due date = no interest charged' },
            { label: 'Daily Rate', detail: 'APR ÷ 365. At 20% APR: 0.0548%/day' },
            { label: 'Min Payment Trap', detail: 'Minimum keeps you in debt for decades' },
            { label: '0% Promo', detail: 'Balance transfers buy time — pay off before promo ends' },
          ].map(c => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-gray-800 text-xs mb-1">{c.label}</div>
              <div class="text-xs text-gray-600">{c.detail}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Average Credit Card APRs (2025)</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr>
            <th class="text-left p-3 text-xs font-semibold text-gray-700">Credit Score</th>
            <th class="text-right p-3 text-xs font-semibold text-gray-700">Typical APR</th>
          </tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[['Excellent (750+)','15–18%'],['Good (700–749)','18–22%'],['Fair (650–699)','22–26%'],['Poor (below 650)','26–30%+'],['Store cards (any)','25–35%']].map(r => (
              <tr><td class="p-3 text-xs">{r[0]}</td><td class="p-3 text-xs text-right font-medium">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</Layout>
''')

# ─── DEBT PAYOFF ─────────────────────────────────────────────────────────────
write("debt-payoff", '''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const balance = parseFloat(inputs.balance) || 0
  const rate = parseFloat(inputs.rate) || 0
  const payment = parseFloat(inputs.payment) || 0
  const extra = parseFloat(inputs.extra) || 0
  if (balance <= 0) throw new Error('Enter a debt balance.')
  if (payment <= 0) throw new Error('Enter a monthly payment.')
  const r = rate / 100 / 12
  const totalPayment = payment + extra
  let months = 0, interest = 0, bal = balance
  while (bal > 0.01 && months < 600) {
    const int = bal * r
    interest += int
    bal = bal + int - totalPayment
    if (bal < 0) bal = 0
    months++
  }
  let monthsBase = 0, interestBase = 0, balBase = balance
  while (balBase > 0.01 && monthsBase < 600) {
    const int = balBase * r
    interestBase += int
    balBase = balBase + int - payment
    if (balBase < 0) balBase = 0
    monthsBase++
  }
  const saved = interestBase - interest
  const timeSaved = monthsBase - months
  return {
    value: months + ' months to debt-free',
    gaugeValue: Math.max(0, Math.min(100, 100 - months / 3)),
    breakdown: [
      'Payoff: ' + Math.floor(months/12) + 'y ' + (months%12) + 'm',
      'Total interest: $' + interest.toFixed(2),
      extra > 0 ? 'Interest saved vs base: $' + saved.toFixed(2) : '',
      extra > 0 ? 'Time saved: ' + timeSaved + ' months' : '',
    ].filter(Boolean),
    stats: [
      { label: 'Payoff Time', value: Math.floor(months/12) + 'y ' + (months%12) + 'm' },
      { label: 'Total Interest', value: '$' + interest.toFixed(0) },
      { label: 'Interest Saved', value: extra > 0 ? '$' + saved.toFixed(0) : 'N/A' },
      { label: 'Months Saved', value: extra > 0 ? String(timeSaved) : 'N/A' },
    ]
  }
`

const faqs = [
  { question: 'What is the debt avalanche method?', answer: 'Pay minimum payments on all debts, then put every extra dollar toward the highest-interest debt first. Once paid off, roll that payment into the next highest. This minimizes total interest paid.' },
  { question: 'What is the debt snowball method?', answer: 'Pay minimum payments on all debts, then put extra money toward the smallest balance first. Once paid, roll that payment into the next smallest. Provides psychological wins that improve follow-through.' },
  { question: 'How much extra should I pay toward debt?', answer: 'Even $50–$100 extra per month makes a significant difference. On a $10,000 loan at 8%, adding $100/month extra cuts payoff time from 10 years to 7 years and saves ~$2,000 in interest.' },
  { question: 'Should I use savings to pay off debt?', answer: 'If debt interest > savings return, yes. Using a 5% savings account to pay off 20% credit card debt is a guaranteed 15% return. Keep a $1,000 emergency fund minimum before aggressively paying debt.' },
  { question: 'What is debt consolidation?', answer: 'Combining multiple debts into a single loan, ideally at a lower interest rate. Options include personal loans, balance transfer cards (0% promo), home equity loans (HELOC), and debt management plans. Compare total cost, not just monthly payment.' },
]
---
<Layout
  title="Debt Payoff Calculator: Time & Interest with Extra Payments"
  description="Calculate how long it takes to pay off debt and how much extra payments save. Free debt payoff calculator with avalanche and snowball support."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Financial', href: '/calculators/financial' },
    { name: 'Debt Payoff Calculator', href: '/calculators/debt-payoff-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/financial" class="hover:text-blue-600">Financial</a><span>›</span>
      <span class="text-gray-900">Debt Payoff Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Debt Payoff Calculator"
          description="See how extra payments eliminate debt faster and save you money"
          formulaId="debt-payoff"
          formulaFn={formulaFn}
          resultLabel="Payoff Time"
          inputs={[
            { id: 'balance', label: 'Current Balance', type: 'number', placeholder: '10000', min: 0, unit: '$', defaultValue: 10000 },
            { id: 'rate', label: 'Annual Interest Rate', type: 'number', placeholder: '18', min: 0, max: 50, step: 0.1, unit: '%', defaultValue: 18 },
            { id: 'payment', label: 'Monthly Payment', type: 'number', placeholder: '250', min: 0, unit: '$', defaultValue: 250 },
            { id: 'extra', label: 'Extra Monthly Payment', type: 'number', placeholder: '100', min: 0, unit: '$', defaultValue: 100 },
          ]}
          gauge={{
            min: 0, max: 100, unit: '% speed score',
            zones: [
              { label: 'Very Slow', color: '#ef4444', from: 0, to: 25 },
              { label: 'Slow', color: '#f59e0b', from: 25, to: 50 },
              { label: 'Good', color: '#3b82f6', from: 50, to: 75 },
              { label: 'Fast', color: '#22c55e', from: 75, to: 100 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'Credit Card Calculator', href: '/calculators/credit-card-calculator' },
            { name: 'Loan Calculator', href: '/calculators/loan-calculator' },
            { name: 'Budget Calculator', href: '/calculators/budget-calculator' },
            { name: 'Net Worth Calculator', href: '/calculators/net-worth-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-red-50 border border-red-200 rounded-xl p-5">
          <h3 class="font-bold text-red-900 mb-3">Power of Extra Payments</h3>
          <p class="text-xs text-red-700 mb-2">$10,000 at 18% APR, $250 base payment:</p>
          <table class="w-full text-xs">
            <thead><tr class="text-red-700"><th class="text-left pb-1">Extra/mo</th><th class="text-right pb-1">Payoff</th><th class="text-right pb-1">Saved</th></tr></thead>
            <tbody class="text-red-900">
              {[['$0','63 mo','—'],['$50','51 mo','$781'],['$100','43 mo','$1,321'],['$250','31 mo','$2,287']].map(r => (
                <tr class="border-t border-red-100"><td class="py-1">{r[0]}</td><td class="text-right">{r[1]}</td><td class="text-right">{r[2]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-2">Avalanche vs Snowball</h3>
          <div class="text-xs text-blue-800 space-y-2">
            <div><strong>Avalanche:</strong> Highest rate first → saves most money</div>
            <div><strong>Snowball:</strong> Smallest balance first → most motivating</div>
            <div class="text-blue-600 mt-1">Studies show snowball has higher completion rates</div>
          </div>
        </div>
      </aside>
    </div>
    <div class="mt-12">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Debt Payoff Strategies Compared</h2>
      <div class="grid md:grid-cols-3 gap-4">
        {[
          { name: 'Avalanche Method', desc: 'Pay highest interest rate first', pros: 'Saves the most money in interest over time', cons: 'Can feel slow if high-rate debt has a large balance', best: 'Mathematically optimal' },
          { name: 'Snowball Method', desc: 'Pay smallest balance first', pros: 'Quick wins keep you motivated', cons: 'May pay more total interest', best: 'Best for motivation' },
          { name: 'Consolidation', desc: 'Combine debts at lower rate', pros: 'Simplifies payments, may lower rate', cons: 'Requires good credit; may extend term', best: 'Good for multiple high-rate debts' },
        ].map(s => (
          <div class="bg-gray-50 rounded-xl p-5">
            <div class="font-bold text-gray-900 mb-1">{s.name}</div>
            <div class="text-xs text-gray-500 mb-2">{s.desc}</div>
            <div class="text-xs text-green-700 mb-1">✓ {s.pros}</div>
            <div class="text-xs text-red-600 mb-1">✗ {s.cons}</div>
            <div class="text-xs font-medium text-blue-600 mt-2">{s.best}</div>
          </div>
        ))}
      </div>
    </div>
  </div>
</Layout>
''')

# ─── INTEREST ─────────────────────────────────────────────────────────────────
write("interest", '''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const principal = parseFloat(inputs.principal) || 0
  const rate = parseFloat(inputs.rate) || 0
  const time = parseFloat(inputs.time) || 0
  const type = inputs.type || 'simple'
  if (principal <= 0) throw new Error('Enter a principal amount.')
  if (rate < 0) throw new Error('Rate must be positive.')
  if (time <= 0) throw new Error('Time must be positive.')
  let interest, total
  if (type === 'simple') {
    interest = principal * (rate / 100) * time
    total = principal + interest
  } else {
    total = principal * Math.pow(1 + rate / 100, time)
    interest = total - principal
  }
  return {
    value: '$' + interest.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
    gaugeValue: Math.min((interest / principal) * 100, 200),
    breakdown: [
      'Principal: $' + principal.toLocaleString(),
      'Interest earned: $' + interest.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
      'Total amount: $' + total.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
      'Return: ' + ((interest / principal) * 100).toFixed(2) + '%',
    ],
    stats: [
      { label: 'Interest Earned', value: '$' + interest.toFixed(2) },
      { label: 'Total Amount', value: '$' + total.toFixed(2) },
      { label: 'Return', value: ((interest / principal) * 100).toFixed(2) + '%' },
      { label: 'Type', value: type === 'simple' ? 'Simple' : 'Compound' },
    ]
  }
`

const faqs = [
  { question: 'What is the difference between simple and compound interest?', answer: 'Simple interest is calculated only on the principal. Compound interest is calculated on the principal plus any previously earned interest. Compound interest grows exponentially while simple interest grows linearly.' },
  { question: 'When is simple interest used?', answer: 'Simple interest is used for short-term loans, some auto loans, and savings bonds. Most mortgages technically use simple interest daily but compound monthly. Credit cards use compound interest daily.' },
  { question: 'How do I calculate interest manually?', answer: 'Simple interest: I = P × r × t (where r is decimal rate and t is years). Compound interest: A = P(1 + r)^t for annual compounding, where A is the total amount including principal.' },
  { question: 'What is APR vs APY?', answer: 'APR (Annual Percentage Rate) is the simple interest rate. APY (Annual Percentage Yield) includes compounding and shows the true annual return. A 5% APR compounded monthly equals 5.12% APY. Use APY to compare accounts accurately.' },
  { question: 'Does more frequent compounding matter?', answer: 'Yes, but modestly for typical rates. $10,000 at 5% for 1 year: annual compounding = $10,500; monthly = $10,511.62; daily = $10,512.67. The difference grows over longer time periods.' },
]
---
<Layout
  title="Interest Calculator: Simple vs Compound Interest"
  description="Calculate simple or compound interest on any amount. Compare how much interest you earn or pay with our free interest calculator."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Financial', href: '/calculators/financial' },
    { name: 'Interest Calculator', href: '/calculators/interest-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/financial" class="hover:text-blue-600">Financial</a><span>›</span>
      <span class="text-gray-900">Interest Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Interest Calculator"
          description="Calculate simple or compound interest on any principal amount"
          formulaId="interest"
          formulaFn={formulaFn}
          resultLabel="Interest Earned"
          inputs={[
            { id: 'principal', label: 'Principal Amount', type: 'number', placeholder: '10000', min: 0, unit: '$', defaultValue: 10000 },
            { id: 'rate', label: 'Annual Interest Rate', type: 'number', placeholder: '5', min: 0, max: 100, step: 0.1, unit: '%', defaultValue: 5 },
            { id: 'time', label: 'Time Period', type: 'number', placeholder: '5', min: 0.1, max: 100, step: 0.1, unit: 'years', defaultValue: 5 },
            { id: 'type', label: 'Interest Type', type: 'select', options: [
              { value: 'simple', label: 'Simple Interest' },
              { value: 'compound', label: 'Compound Interest (annual)' },
            ], defaultValue: 'simple' },
          ]}
          gauge={{
            min: 0, max: 200, unit: '% return',
            zones: [
              { label: 'Low', color: '#94a3b8', from: 0, to: 25 },
              { label: 'Moderate', color: '#3b82f6', from: 25, to: 75 },
              { label: 'High', color: '#22c55e', from: 75, to: 150 },
              { label: 'Very High', color: '#f59e0b', from: 150, to: 200 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'Compound Interest Calculator', href: '/calculators/compound-interest-calculator' },
            { name: 'Savings Calculator', href: '/calculators/savings-calculator' },
            { name: 'APR Calculator', href: '/calculators/apr-calculator' },
            { name: 'CD Calculator', href: '/calculators/cd-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">$10,000 at 5% for 10 Years</h3>
          <div class="space-y-2 text-xs text-blue-800">
            <div class="flex justify-between border-b border-blue-100 pb-1"><span>Simple interest</span><span class="font-medium">$5,000 interest</span></div>
            <div class="flex justify-between border-b border-blue-100 pb-1"><span>Compound (annual)</span><span class="font-medium">$6,289 interest</span></div>
            <div class="flex justify-between"><span>Compound (monthly)</span><span class="font-medium">$6,470 interest</span></div>
          </div>
        </div>
        <div class="bg-white border border-gray-200 rounded-xl p-5">
          <h3 class="font-bold text-gray-900 mb-2">Formulas</h3>
          <div class="text-xs space-y-2">
            <div><span class="font-medium text-gray-700">Simple:</span> <code class="bg-gray-100 px-1 rounded">I = P × r × t</code></div>
            <div><span class="font-medium text-gray-700">Compound:</span> <code class="bg-gray-100 px-1 rounded">A = P(1+r)^t</code></div>
          </div>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">APR vs APY Explained</h2>
        <p class="text-gray-600 text-sm mb-3">APR (Annual Percentage Rate) is the nominal rate without compounding. APY (Annual Percentage Yield) includes compounding effects and reflects the true annual return. When comparing savings accounts, always compare APY.</p>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold text-gray-700">APR</th><th class="text-right p-2 text-xs font-semibold text-gray-700">APY (monthly compounding)</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[['4.00%','4.07%'],['5.00%','5.12%'],['6.00%','6.17%'],['8.00%','8.30%'],['10.00%','10.47%']].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-medium text-green-600">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Where Each Type Is Used</h2>
        <div class="space-y-3">
          {[
            { type: 'Simple Interest', uses: 'Short-term loans, some auto loans, savings bonds, car title loans' },
            { type: 'Compound Interest', uses: 'Savings accounts, CDs, mortgages (daily simple, monthly compound), credit cards, student loans, investments' },
          ].map(i => (
            <div class="bg-gray-50 rounded-lg p-4">
              <div class="font-semibold text-gray-800 text-sm mb-1">{i.type}</div>
              <div class="text-xs text-gray-600">{i.uses}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
</Layout>
''')

# ─── PERCENTAGE ─────────────────────────────────────────────────────────────
write("percentage", '''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const type = inputs.type || 'of'
  const a = parseFloat(inputs.a) || 0
  const b = parseFloat(inputs.b) || 0
  let result, label, gaugeVal
  if (type === 'of') {
    result = (a / 100) * b
    label = a + '% of ' + b + ' = ' + result.toLocaleString('en-US', { maximumFractionDigits: 4 })
    gaugeVal = a
  } else if (type === 'what') {
    result = b === 0 ? 0 : (a / b) * 100
    label = a + ' is ' + result.toFixed(2) + '% of ' + b
    gaugeVal = result
  } else if (type === 'change') {
    result = b === 0 ? 0 : ((b - a) / Math.abs(a)) * 100
    label = (result >= 0 ? '+' : '') + result.toFixed(2) + '% change from ' + a + ' to ' + b
    gaugeVal = Math.abs(result)
  } else {
    result = a * (1 + b / 100)
    label = a + ' increased by ' + b + '% = ' + result.toLocaleString('en-US', { maximumFractionDigits: 4 })
    gaugeVal = b
  }
  return {
    value: label,
    gaugeValue: Math.min(Math.abs(gaugeVal), 100),
    stats: [
      { label: 'Result', value: typeof result === 'number' ? result.toLocaleString('en-US', { maximumFractionDigits: 4 }) : result },
      { label: 'Calculation Type', value: type === 'of' ? '% of number' : type === 'what' ? 'what % is' : type === 'change' ? '% change' : '% increase/decrease' },
      { label: 'Input A', value: String(a) },
      { label: 'Input B', value: String(b) },
    ]
  }
`

const faqs = [
  { question: 'How do I calculate what percent one number is of another?', answer: 'Divide the part by the whole, then multiply by 100. Example: 45 out of 180 = (45 ÷ 180) × 100 = 25%. This is the most common percentage calculation in everyday life.' },
  { question: 'How do I calculate percent change?', answer: 'Percent change = ((New Value − Old Value) ÷ |Old Value|) × 100. Example: from $50 to $65 = ((65 − 50) ÷ 50) × 100 = +30% increase. From $65 to $50 = −23.1% decrease.' },
  { question: 'How do I find a percentage of a number?', answer: 'Multiply the percentage (as a decimal) by the number. Example: 15% of $200 = 0.15 × 200 = $30. Or multiply the number by the percentage and divide by 100: 200 × 15 ÷ 100 = $30.' },
  { question: 'What is the difference between percentage and percentage points?', answer: 'Percentage points measure the arithmetic difference between two percentages. If interest rates go from 3% to 5%, that is a 2 percentage-point increase, but a 66.7% relative increase. These are very different and often confused.' },
  { question: 'How do I calculate a discount or sale price?', answer: 'Sale price = Original price × (1 − discount%). Example: $80 item with 25% off = $80 × (1 − 0.25) = $80 × 0.75 = $60. Or: find 25% of $80 ($20) and subtract: $80 − $20 = $60.' },
]
---
<Layout
  title="Percentage Calculator: % of Number, % Change, What % Is"
  description="Calculate percentages instantly — find what percent one number is of another, percent change, or a percentage of a number. Free percentage calculator."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Math', href: '/calculators/math' },
    { name: 'Percentage Calculator', href: '/calculators/percentage-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/math" class="hover:text-blue-600">Math</a><span>›</span>
      <span class="text-gray-900">Percentage Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Percentage Calculator"
          description="Calculate any type of percentage problem instantly"
          formulaId="percentage"
          formulaFn={formulaFn}
          resultLabel="Result"
          inputs={[
            { id: 'type', label: 'Calculation Type', type: 'select', options: [
              { value: 'of', label: 'What is X% of Y?' },
              { value: 'what', label: 'X is what % of Y?' },
              { value: 'change', label: '% change from X to Y' },
              { value: 'increase', label: 'Increase/decrease X by Y%' },
            ], defaultValue: 'of' },
            { id: 'a', label: 'Value A (X)', type: 'number', placeholder: '15', defaultValue: 15 },
            { id: 'b', label: 'Value B (Y)', type: 'number', placeholder: '200', defaultValue: 200 },
          ]}
          gauge={{
            min: 0, max: 100, unit: '%',
            zones: [
              { label: '0–25%', color: '#3b82f6', from: 0, to: 25 },
              { label: '25–50%', color: '#22c55e', from: 25, to: 50 },
              { label: '50–75%', color: '#f59e0b', from: 50, to: 75 },
              { label: '75–100%', color: '#8b5cf6', from: 75, to: 100 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'Discount Calculator', href: '/calculators/discount-calculator' },
            { name: 'Sales Tax Calculator', href: '/calculators/sales-tax-calculator' },
            { name: 'Tip Calculator', href: '/calculators/tip-calculator' },
            { name: 'Percentage Error Calculator', href: '/calculators/percentage-error-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Quick Reference</h3>
          <div class="space-y-2 text-xs text-blue-800">
            {[['10% of X','Divide X by 10'],['25% of X','Divide X by 4'],['50% of X','Divide X by 2'],['75% of X','Multiply X by 0.75'],['1% of X','Divide X by 100']].map(([pct, trick]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span class="font-medium">{pct}</span><span>{trick}</span></div>
            ))}
          </div>
        </div>
        <div class="bg-green-50 border border-green-200 rounded-xl p-5">
          <h3 class="font-bold text-green-900 mb-2">Common Uses</h3>
          <ul class="text-xs text-green-800 space-y-1">
            <li>• Sale discounts and markups</li>
            <li>• Tax calculations</li>
            <li>• Grade and test score percentages</li>
            <li>• Investment returns</li>
            <li>• Survey and data analysis</li>
          </ul>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Four Types of Percentage Problems</h2>
        <div class="space-y-3">
          {[
            { type: 'P% of N = ?', example: '15% of 200 = 30', formula: '(15 ÷ 100) × 200 = 30' },
            { type: 'X is ?% of N', example: '30 is ?% of 200 = 15%', formula: '(30 ÷ 200) × 100 = 15' },
            { type: '% Change', example: '50 → 65 = +30% change', formula: '((65−50)÷50) × 100 = 30' },
            { type: 'Increase/Decrease', example: '200 + 15% = 230', formula: '200 × (1 + 0.15) = 230' },
          ].map(p => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-gray-800 text-xs mb-1">{p.type}</div>
              <div class="text-xs text-gray-500 mb-1">Example: {p.example}</div>
              <div class="text-xs font-mono text-blue-600">{p.formula}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Common Percentage Conversions</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr>
            <th class="text-left p-2 text-xs font-semibold text-gray-700">Fraction</th>
            <th class="text-right p-2 text-xs font-semibold text-gray-700">Decimal</th>
            <th class="text-right p-2 text-xs font-semibold text-gray-700">Percentage</th>
          </tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[['1/4','0.25','25%'],['1/3','0.333','33.3%'],['1/2','0.5','50%'],['2/3','0.667','66.7%'],['3/4','0.75','75%'],['1/8','0.125','12.5%']].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right font-medium">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</Layout>
''')

# ─── TIP ─────────────────────────────────────────────────────────────────────
write("tip", '''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const bill = parseFloat(inputs.bill) || 0
  const tipPct = parseFloat(inputs.tip) || 18
  const people = parseInt(inputs.people) || 1
  if (bill <= 0) throw new Error('Enter a bill amount.')
  if (people < 1) throw new Error('Enter at least 1 person.')
  const tipAmount = bill * (tipPct / 100)
  const total = bill + tipAmount
  const perPerson = total / people
  const tipPerPerson = tipAmount / people
  return {
    value: '$' + tipAmount.toFixed(2) + ' tip',
    gaugeValue: tipPct,
    breakdown: [
      'Bill: $' + bill.toFixed(2),
      'Tip (' + tipPct + '%): $' + tipAmount.toFixed(2),
      'Total: $' + total.toFixed(2),
      people > 1 ? 'Per person: $' + perPerson.toFixed(2) : '',
    ].filter(Boolean),
    stats: [
      { label: 'Tip Amount', value: '$' + tipAmount.toFixed(2) },
      { label: 'Total Bill', value: '$' + total.toFixed(2) },
      { label: 'Per Person', value: '$' + perPerson.toFixed(2) },
      { label: 'Tip Per Person', value: '$' + tipPerPerson.toFixed(2) },
    ]
  }
`

const faqs = [
  { question: 'How much should I tip at a restaurant?', answer: 'Standard restaurant tipping in the US: 15% for adequate service, 18–20% for good service, 20–25% for excellent service. Pre-pandemic the standard was 15–18%; post-pandemic, 20% has become the new standard.' },
  { question: 'Should I tip on pre-tax or post-tax amount?', answer: 'Tipping on the pre-tax amount is technically correct and slightly cheaper. However, many people tip on the post-tax total for simplicity. The difference is small — on a $100 bill with 8% tax, it\'s $1.60 at 20% tip.' },
  { question: 'Do I need to tip at counter service or coffee shops?', answer: 'Not traditionally required, but common. For cafes and counter service, 10–15% is appreciated for more complex orders or good service. For simple orders like a drip coffee, spare change or no tip is fine.' },
  { question: 'How do I split the bill fairly when people order differently?', answer: 'For fairness, have each person pay their portion plus the tip percentage. Apps like Splitwise or Venmo make this easy. Alternatively, have the server split the check — most restaurants accommodate this request.' },
  { question: 'What services typically expect tips?', answer: 'Restaurants (15–20%), food delivery (10–15%), bartenders ($1–2/drink or 15–20%), hair/nail services (15–20%), taxi/rideshare (15–20%), hotel housekeeping ($2–5/night), spa services (15–20%). Tips are discretionary but important income for service workers.' },
]
---
<Layout
  title="Tip Calculator: Split the Bill & Calculate Gratuity"
  description="Calculate tip amount and total bill instantly. Split between any number of people. Free tip calculator with customizable tip percentage."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Other', href: '/calculators/other' },
    { name: 'Tip Calculator', href: '/calculators/tip-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/other" class="hover:text-blue-600">Other</a><span>›</span>
      <span class="text-gray-900">Tip Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Tip Calculator"
          description="Calculate tip and split the bill between any number of people"
          formulaId="tip"
          formulaFn={formulaFn}
          resultLabel="Tip Amount"
          inputs={[
            { id: 'bill', label: 'Bill Amount', type: 'number', placeholder: '85.00', min: 0, step: 0.01, unit: '$', defaultValue: 85 },
            { id: 'tip', label: 'Tip Percentage', type: 'select', options: [
              { value: '10', label: '10% — Below average' },
              { value: '15', label: '15% — Adequate' },
              { value: '18', label: '18% — Good' },
              { value: '20', label: '20% — Great' },
              { value: '25', label: '25% — Excellent' },
              { value: '30', label: '30% — Exceptional' },
            ], defaultValue: '18' },
            { id: 'people', label: 'Split Between', type: 'number', placeholder: '2', min: 1, max: 20, unit: 'people', defaultValue: 2 },
          ]}
          gauge={{
            min: 0, max: 30, unit: '% tip',
            zones: [
              { label: 'Low', color: '#ef4444', from: 0, to: 12 },
              { label: 'Standard', color: '#f59e0b', from: 12, to: 18 },
              { label: 'Good', color: '#22c55e', from: 18, to: 25 },
              { label: 'Generous', color: '#8b5cf6', from: 25, to: 30 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'Sales Tax Calculator', href: '/calculators/sales-tax-calculator' },
            { name: 'Percentage Calculator', href: '/calculators/percentage-calculator' },
            { name: 'Discount Calculator', href: '/calculators/discount-calculator' },
            { name: 'Budget Calculator', href: '/calculators/budget-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-green-50 border border-green-200 rounded-xl p-5">
          <h3 class="font-bold text-green-900 mb-3">Tip Guide by Service</h3>
          <div class="space-y-2 text-xs text-green-800">
            {[['Restaurant (full service)','15–20%'],['Food delivery','10–15%'],['Bar / bartender','15–20%'],['Hair / nail salon','15–20%'],['Rideshare / taxi','15–20%'],['Hotel housekeeping','$2–5/night'],['Spa services','15–20%']].map(([s,t]) => (
              <div class="flex justify-between border-b border-green-100 pb-1"><span>{s}</span><span class="font-medium">{t}</span></div>
            ))}
          </div>
        </div>
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-2">Quick Tip Math</h3>
          <p class="text-xs text-blue-800">To tip 20%: move the decimal left one place (10%) then double it. $85 → $8.50 (10%) → $17.00 (20%). Easy mental math!</p>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">$100 Bill — Tip Comparison</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr>
            <th class="text-left p-3 text-xs font-semibold text-gray-700">Tip %</th>
            <th class="text-right p-3 text-xs font-semibold text-gray-700">Tip Amount</th>
            <th class="text-right p-3 text-xs font-semibold text-gray-700">Total</th>
          </tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[['10%','$10.00','$110.00'],['15%','$15.00','$115.00'],['18%','$18.00','$118.00'],['20%','$20.00','$120.00'],['25%','$25.00','$125.00']].map(r => (
              <tr><td class="p-3 text-xs">{r[0]}</td><td class="p-3 text-xs text-right">{r[1]}</td><td class="p-3 text-xs text-right font-medium">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Splitting the Bill (18% Tip)</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr>
            <th class="text-left p-3 text-xs font-semibold text-gray-700">Bill Total</th>
            <th class="text-right p-3 text-xs font-semibold text-gray-700">2 People</th>
            <th class="text-right p-3 text-xs font-semibold text-gray-700">4 People</th>
          </tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[['$40','$23.60','$11.80'],['$80','$47.20','$23.60'],['$120','$70.80','$35.40'],['$200','$118.00','$59.00']].map(r => (
              <tr><td class="p-3 text-xs">{r[0]}</td><td class="p-3 text-xs text-right">{r[1]}</td><td class="p-3 text-xs text-right">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</Layout>
''')

# ─── GPA ─────────────────────────────────────────────────────────────────────
write("gpa", '''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const grades = []
  const letters = ['A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F']
  const points = [4.0,4.0,3.7,3.3,3.0,2.7,2.3,2.0,1.7,1.3,1.0,0.7,0.0]
  const letter = inputs.grade1 || 'A'
  const credits1 = parseFloat(inputs.credits1) || 3
  const letter2 = inputs.grade2 || 'B+'
  const credits2 = parseFloat(inputs.credits2) || 3
  const letter3 = inputs.grade3 || 'A-'
  const credits3 = parseFloat(inputs.credits3) || 3
  const letter4 = inputs.grade4 || 'B'
  const credits4 = parseFloat(inputs.credits4) || 3
  const letter5 = inputs.grade5 || ''
  const credits5 = parseFloat(inputs.credits5) || 0
  const parseGPA = (g) => { const i = letters.indexOf(g); return i >= 0 ? points[i] : 0 }
  const courses = [
    [parseGPA(letter), credits1], [parseGPA(letter2), credits2],
    [parseGPA(letter3), credits3], [parseGPA(letter4), credits4],
  ]
  if (letter5 && credits5 > 0) courses.push([parseGPA(letter5), credits5])
  const totalCredits = courses.reduce((s, c) => s + c[1], 0)
  const weightedPoints = courses.reduce((s, c) => s + c[0] * c[1], 0)
  if (totalCredits === 0) throw new Error('Enter at least one course with credits.')
  const gpa = weightedPoints / totalCredits
  const honor = gpa >= 3.9 ? 'Summa Cum Laude' : gpa >= 3.7 ? 'Magna Cum Laude' : gpa >= 3.5 ? 'Cum Laude' : gpa >= 3.0 ? 'Good Standing' : gpa >= 2.0 ? 'Satisfactory' : 'Academic Probation Risk'
  return {
    value: gpa.toFixed(2) + ' GPA',
    gaugeValue: (gpa / 4.0) * 100,
    breakdown: [
      'Total credits: ' + totalCredits,
      'Weighted points: ' + weightedPoints.toFixed(1),
      'GPA: ' + gpa.toFixed(3),
      'Standing: ' + honor,
    ],
    stats: [
      { label: 'GPA', value: gpa.toFixed(2) },
      { label: 'Total Credits', value: String(totalCredits) },
      { label: 'Academic Standing', value: honor },
      { label: 'Out of 4.0', value: (gpa / 4.0 * 100).toFixed(1) + '%' },
    ]
  }
`

const faqs = [
  { question: 'How is GPA calculated?', answer: 'GPA = (Sum of grade points × credit hours) ÷ Total credit hours. Each letter grade converts to grade points (A=4.0, B=3.0, C=2.0, D=1.0, F=0). Weight each by the course\'s credit hours, sum them, divide by total credits.' },
  { question: 'What is a good GPA?', answer: '3.5+ is considered excellent and qualifies for most academic honors. 3.0–3.5 is good and competitive for grad school. 2.5–3.0 is average. Below 2.0 may put you on academic probation at many schools.' },
  { question: 'What are the Latin honors thresholds?', answer: 'Thresholds vary by institution: Cum Laude typically 3.5–3.7, Magna Cum Laude 3.7–3.9, Summa Cum Laude 3.9–4.0. Some schools use class rank instead of GPA for honors designation.' },
  { question: 'Does GPA matter after graduation?', answer: 'It matters most for grad school (most programs require 3.0+) and first jobs in competitive fields. After 2–3 years of work experience, employers care far more about your work history than GPA. Many employers stop asking after your first job.' },
  { question: 'Can I raise my GPA significantly?', answer: 'It becomes harder as you accumulate credits. Early in college, each grade has more weight. A sophomore with 60 credits raising a 2.5 GPA to 3.0 would need roughly a 3.5 average for the remaining 60 credits. Use our grade calculator for precise projections.' },
]
---
<Layout
  title="GPA Calculator: Weighted Grade Point Average"
  description="Calculate your GPA with weighted credits. Find your academic standing and see Latin honors thresholds. Free GPA calculator."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Other', href: '/calculators/other' },
    { name: 'GPA Calculator', href: '/calculators/gpa-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/other" class="hover:text-blue-600">Other</a><span>›</span>
      <span class="text-gray-900">GPA Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="GPA Calculator"
          description="Calculate your weighted GPA for up to 5 courses"
          formulaId="gpa"
          formulaFn={formulaFn}
          resultLabel="GPA"
          inputs={[
            { id: 'grade1', label: 'Course 1 Grade', type: 'select', options: ['A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F'].map(g => ({ value: g, label: g })), defaultValue: 'A' },
            { id: 'credits1', label: 'Course 1 Credits', type: 'number', placeholder: '3', min: 1, max: 6, defaultValue: 3 },
            { id: 'grade2', label: 'Course 2 Grade', type: 'select', options: ['A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F'].map(g => ({ value: g, label: g })), defaultValue: 'B+' },
            { id: 'credits2', label: 'Course 2 Credits', type: 'number', placeholder: '3', min: 1, max: 6, defaultValue: 3 },
            { id: 'grade3', label: 'Course 3 Grade', type: 'select', options: ['A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F'].map(g => ({ value: g, label: g })), defaultValue: 'A-' },
            { id: 'credits3', label: 'Course 3 Credits', type: 'number', placeholder: '3', min: 1, max: 6, defaultValue: 3 },
            { id: 'grade4', label: 'Course 4 Grade', type: 'select', options: ['A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F'].map(g => ({ value: g, label: g })), defaultValue: 'B' },
            { id: 'credits4', label: 'Course 4 Credits', type: 'number', placeholder: '3', min: 1, max: 6, defaultValue: 3 },
          ]}
          gauge={{
            min: 0, max: 100, unit: '% of 4.0',
            zones: [
              { label: 'Probation Risk', color: '#ef4444', from: 0, to: 50 },
              { label: 'Satisfactory', color: '#f59e0b', from: 50, to: 75 },
              { label: 'Good', color: '#3b82f6', from: 75, to: 87.5 },
              { label: 'Honors', color: '#22c55e', from: 87.5, to: 100 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'Grade Calculator', href: '/calculators/grade-calculator' },
            { name: 'Final Grade Calculator', href: '/calculators/final-grade-calculator' },
            { name: 'Percentage Calculator', href: '/calculators/percentage-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Grade Point Scale</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700"><th class="text-left pb-1">Grade</th><th class="text-right pb-1">Points</th><th class="text-right pb-1">%</th></tr></thead>
            <tbody class="text-blue-900">
              {[['A / A+','4.0','93–100'],['A-','3.7','90–92'],['B+','3.3','87–89'],['B','3.0','83–86'],['B-','2.7','80–82'],['C+','2.3','77–79'],['C','2.0','73–76'],['D','1.0','60–69'],['F','0.0','<60']].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right">{r[1]}</td><td class="text-right">{r[2]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
        <div class="bg-purple-50 border border-purple-200 rounded-xl p-5">
          <h3 class="font-bold text-purple-900 mb-2">Latin Honors</h3>
          <ul class="text-xs text-purple-800 space-y-1">
            <li><strong>Summa Cum Laude:</strong> 3.9+</li>
            <li><strong>Magna Cum Laude:</strong> 3.7–3.9</li>
            <li><strong>Cum Laude:</strong> 3.5–3.7</li>
          </ul>
          <p class="text-xs text-purple-600 mt-2">Thresholds vary by school</p>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">GPA for Graduate School Admissions</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr>
            <th class="text-left p-3 text-xs font-semibold text-gray-700">Program Type</th>
            <th class="text-right p-3 text-xs font-semibold text-gray-700">Typical Minimum</th>
          </tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[['Medical School (MD)','3.7+'],['Law School (top 20)','3.7+'],['MBA (top programs)','3.5+'],['PhD Programs','3.5+'],['Master\'s Programs','3.0+'],['Most Graduate Schools','2.5–3.0']].map(r => (
              <tr><td class="p-3 text-xs">{r[0]}</td><td class="p-3 text-xs text-right font-medium">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">How to Improve Your GPA</h2>
        <div class="space-y-2">
          {[
            'Retake failed or low-grade courses if your school allows grade replacement',
            'Take more credit hours — larger credit load means each course affects GPA less',
            'Prioritize high-credit courses (4–5 credits affect GPA more than 1-credit courses)',
            'Attend office hours and use tutoring centers early in the semester',
            'Drop courses before the deadline rather than earning a failing grade',
            'Consider a lighter course load to focus on grade quality over quantity',
          ].map(tip => (
            <div class="flex gap-2 text-xs text-gray-600">
              <span class="text-blue-500 mt-0.5">•</span>
              <span>{tip}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
</Layout>
''')

# ─── DISCOUNT ─────────────────────────────────────────────────────────────────
write("discount", '''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const original = parseFloat(inputs.original) || 0
  const discount = parseFloat(inputs.discount) || 0
  const taxRate = parseFloat(inputs.tax) || 0
  if (original <= 0) throw new Error('Enter original price.')
  if (discount < 0 || discount > 100) throw new Error('Discount must be 0–100%.')
  const savings = original * (discount / 100)
  const afterDiscount = original - savings
  const tax = afterDiscount * (taxRate / 100)
  const finalPrice = afterDiscount + tax
  return {
    value: '$' + finalPrice.toFixed(2),
    gaugeValue: discount,
    breakdown: [
      'Original price: $' + original.toFixed(2),
      'Discount (' + discount + '%): -$' + savings.toFixed(2),
      'Price after discount: $' + afterDiscount.toFixed(2),
      taxRate > 0 ? 'Tax (' + taxRate + '%): +$' + tax.toFixed(2) : '',
      'Final price: $' + finalPrice.toFixed(2),
    ].filter(Boolean),
    stats: [
      { label: 'Final Price', value: '$' + finalPrice.toFixed(2) },
      { label: 'You Save', value: '$' + savings.toFixed(2) },
      { label: 'Savings %', value: discount + '%' },
      { label: 'Tax Added', value: taxRate > 0 ? '$' + tax.toFixed(2) : '$0.00' },
    ]
  }
`

const faqs = [
  { question: 'How do I calculate a discount?', answer: 'Multiply the original price by the discount percentage, then subtract. Example: $120 with 25% off → $120 × 0.25 = $30 discount → $120 − $30 = $90 final price. Or multiply by (1 − discount%): $120 × 0.75 = $90.' },
  { question: 'Is tax applied before or after discount?', answer: 'Sales tax is applied after the discount in all US states. You pay tax on the discounted price, not the original price. This is beneficial — a $100 item with 20% off and 8% tax = ($100 × 0.80) × 1.08 = $86.40.' },
  { question: 'How do I stack multiple discounts?', answer: 'Multiply them consecutively, not together. Two 20% discounts off a $100 item = $100 × 0.80 = $80, then $80 × 0.80 = $64. NOT 40% off ($60). The effective combined discount is 36%, not 40%.' },
  { question: 'What is BOGO and how does it work?', answer: 'Buy One Get One (BOGO) free is equivalent to 50% off both items. BOGO 50% off means each item is 25% off. When comparing sales, convert to an equivalent single-item discount percentage for fair comparison.' },
  { question: 'How do I calculate original price from discounted price?', answer: 'Divide the sale price by (1 − discount%). If something costs $75 after a 25% discount, original price = $75 ÷ 0.75 = $100. This is useful when you only see the sale tag.' },
]
---
<Layout
  title="Discount Calculator: Sale Price & Savings Calculator"
  description="Calculate sale price, discount amount, and savings percentage instantly. Includes sales tax. Free discount calculator."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Other', href: '/calculators/other' },
    { name: 'Discount Calculator', href: '/calculators/discount-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/other" class="hover:text-blue-600">Other</a><span>›</span>
      <span class="text-gray-900">Discount Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Discount Calculator"
          description="Find sale price, savings amount, and final cost with tax"
          formulaId="discount"
          formulaFn={formulaFn}
          resultLabel="Final Price"
          inputs={[
            { id: 'original', label: 'Original Price', type: 'number', placeholder: '120', min: 0, step: 0.01, unit: '$', defaultValue: 120 },
            { id: 'discount', label: 'Discount', type: 'number', placeholder: '25', min: 0, max: 100, step: 0.1, unit: '%', defaultValue: 25 },
            { id: 'tax', label: 'Sales Tax Rate', type: 'number', placeholder: '8', min: 0, max: 20, step: 0.1, unit: '%', defaultValue: 0 },
          ]}
          gauge={{
            min: 0, max: 75, unit: '% discount',
            zones: [
              { label: 'Small', color: '#94a3b8', from: 0, to: 15 },
              { label: 'Good', color: '#3b82f6', from: 15, to: 30 },
              { label: 'Great', color: '#22c55e', from: 30, to: 50 },
              { label: 'Huge', color: '#f59e0b', from: 50, to: 75 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'Sales Tax Calculator', href: '/calculators/sales-tax-calculator' },
            { name: 'Percentage Calculator', href: '/calculators/percentage-calculator' },
            { name: 'Markup Calculator', href: '/calculators/markup-calculator' },
            { name: 'Tip Calculator', href: '/calculators/tip-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-green-50 border border-green-200 rounded-xl p-5">
          <h3 class="font-bold text-green-900 mb-3">$100 Item — Discount Savings</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-green-700"><th class="text-left pb-1">Discount</th><th class="text-right pb-1">You Pay</th><th class="text-right pb-1">Save</th></tr></thead>
            <tbody class="text-green-900">
              {[['10%','$90','$10'],['20%','$80','$20'],['30%','$70','$30'],['50%','$50','$50'],['70%','$30','$70']].map(r => (
                <tr class="border-t border-green-100"><td class="py-0.5">{r[0]}</td><td class="text-right">{r[1]}</td><td class="text-right font-medium">{r[2]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
        <div class="bg-amber-50 border border-amber-200 rounded-xl p-5">
          <h3 class="font-bold text-amber-900 mb-2">Stacked Discounts</h3>
          <p class="text-xs text-amber-800">Two 20% discounts ≠ 40% off. Actual: 36% off. Calculate by multiplying: 0.80 × 0.80 = 0.64 → 36% off.</p>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">How to Calculate Discounts</h2>
        <div class="space-y-3">
          {[
            { step: '1', label: 'Find the discount amount', detail: 'Multiply: $120 × 25% = $30 savings' },
            { step: '2', label: 'Subtract from original', detail: '$120 − $30 = $90 after discount' },
            { step: '3', label: 'Add sales tax (if any)', detail: '$90 × 1.08 = $97.20 final price' },
          ].map(s => (
            <div class="flex gap-3 bg-gray-50 rounded-lg p-3">
              <div class="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">{s.step}</div>
              <div>
                <div class="font-semibold text-gray-800 text-xs mb-1">{s.label}</div>
                <div class="text-xs text-gray-600">{s.detail}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Finding Original Price from Sale Price</h2>
        <p class="text-gray-600 text-sm mb-3">If you only see the sale price and discount, work backwards:</p>
        <div class="bg-gray-50 rounded-lg p-4 text-sm">
          <p class="text-gray-700 mb-2"><strong>Formula:</strong> Original = Sale Price ÷ (1 − Discount%)</p>
          <p class="text-gray-600 text-xs mb-2">Example: $75 sale price, 25% off</p>
          <p class="text-blue-600 text-xs font-mono">$75 ÷ 0.75 = $100 original price</p>
        </div>
        <p class="text-xs text-gray-500 mt-3">Useful when comparing "was $X, now $Y" vs just the sale price tag.</p>
      </div>
    </div>
  </div>
</Layout>
''')

# ─── SALES TAX ─────────────────────────────────────────────────────────────────
write("sales-tax", '''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const price = parseFloat(inputs.price) || 0
  const rate = parseFloat(inputs.rate) || 0
  if (price <= 0) throw new Error('Enter a price.')
  const tax = price * (rate / 100)
  const total = price + tax
  return {
    value: '$' + total.toFixed(2),
    gaugeValue: rate,
    breakdown: [
      'Pre-tax price: $' + price.toFixed(2),
      'Tax rate: ' + rate + '%',
      'Tax amount: $' + tax.toFixed(2),
      'Total with tax: $' + total.toFixed(2),
    ],
    stats: [
      { label: 'Total Price', value: '$' + total.toFixed(2) },
      { label: 'Tax Amount', value: '$' + tax.toFixed(2) },
      { label: 'Tax Rate', value: rate + '%' },
      { label: 'Pre-Tax Price', value: '$' + price.toFixed(2) },
    ]
  }
`

const faqs = [
  { question: 'How do I calculate sales tax?', answer: 'Multiply the price by the tax rate (as a decimal). Example: $50 item with 8% sales tax → $50 × 0.08 = $4.00 tax → $54.00 total. Or multiply the price by (1 + rate): $50 × 1.08 = $54.00.' },
  { question: 'What states have no sales tax?', answer: 'Oregon, Montana, New Hampshire, Delaware, and Alaska have no statewide sales tax (though Alaska allows local taxes). These 5 states are popular for large purchases. Most states range from 4–10%.' },
  { question: 'What is the highest sales tax in the US?', answer: 'Combined state + local rates can exceed 12% in some areas. Louisiana, Tennessee, Arkansas, Alabama, and Oklahoma regularly top the combined rate rankings. California has the highest base state rate at 7.25%.' },
  { question: 'Do online purchases require sales tax?', answer: 'Yes, since the 2018 South Dakota v. Wayfair Supreme Court decision. Online retailers are now required to collect sales tax in states where they have economic nexus (usually $100,000+ in sales or 200+ transactions per year).' },
  { question: 'Are groceries taxed?', answer: 'It depends on the state. Many states exempt food for home consumption (groceries). However, prepared food (restaurants, hot deli items) is usually taxable. About 37 states exempt most grocery items from sales tax.' },
]
---
<Layout
  title="Sales Tax Calculator: Price After Tax"
  description="Calculate total price after sales tax for any state. Add tax to any purchase amount instantly. Free sales tax calculator."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Other', href: '/calculators/other' },
    { name: 'Sales Tax Calculator', href: '/calculators/sales-tax-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/other" class="hover:text-blue-600">Other</a><span>›</span>
      <span class="text-gray-900">Sales Tax Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Sales Tax Calculator"
          description="Calculate the total price of any purchase including sales tax"
          formulaId="sales-tax"
          formulaFn={formulaFn}
          resultLabel="Total with Tax"
          inputs={[
            { id: 'price', label: 'Purchase Price', type: 'number', placeholder: '100', min: 0, step: 0.01, unit: '$', defaultValue: 100 },
            { id: 'rate', label: 'Sales Tax Rate', type: 'number', placeholder: '8', min: 0, max: 15, step: 0.1, unit: '%', defaultValue: 8 },
          ]}
          gauge={{
            min: 0, max: 15, unit: '% tax rate',
            zones: [
              { label: 'Low', color: '#22c55e', from: 0, to: 4 },
              { label: 'Average', color: '#3b82f6', from: 4, to: 8 },
              { label: 'High', color: '#f59e0b', from: 8, to: 10 },
              { label: 'Very High', color: '#ef4444', from: 10, to: 15 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'Discount Calculator', href: '/calculators/discount-calculator' },
            { name: 'Tip Calculator', href: '/calculators/tip-calculator' },
            { name: 'Percentage Calculator', href: '/calculators/percentage-calculator' },
            { name: 'GST/VAT Calculator', href: '/calculators/gst-vat-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">US State Sales Tax Rates</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[['Oregon, Montana, NH, DE','0%'],['Colorado','2.9%'],['New York','4%'],['Florida','6%'],['California','7.25%'],['Tennessee','7%'],['Local taxes can add','0–5%+']].map(([s,r]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span>{s}</span><span class="font-medium">{r}</span></div>
            ))}
          </div>
        </div>
        <div class="bg-amber-50 border border-amber-200 rounded-xl p-5">
          <h3 class="font-bold text-amber-900 mb-2">Tax on $1,000 Purchase</h3>
          <div class="space-y-1 text-xs text-amber-800">
            {[['5% rate','$1,050 total'],['8% rate','$1,080 total'],['10% rate','$1,100 total'],['12% rate','$1,120 total']].map(([r,t]) => (
              <div class="flex justify-between"><span>{r}</span><span class="font-medium">{t}</span></div>
            ))}
          </div>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Reverse Sales Tax Calculation</h2>
        <p class="text-gray-600 text-sm mb-3">If you know the total paid (with tax) and want to find the pre-tax price:</p>
        <div class="bg-gray-50 rounded-lg p-4 text-sm mb-3">
          <p class="font-medium text-gray-800 mb-1">Pre-tax price = Total ÷ (1 + tax rate)</p>
          <p class="text-xs text-gray-600">Example: $108 total with 8% tax → $108 ÷ 1.08 = $100 pre-tax</p>
        </div>
        <p class="text-xs text-gray-500">Useful when a receipt shows the total and you need to separate the tax for expense reports or accounting.</p>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">What Is and Isn't Taxed</h2>
        <div class="space-y-2">
          {[
            { label: 'Usually Taxable', items: 'Electronics, clothing (most states), furniture, cars, prepared food, alcohol' },
            { label: 'Often Exempt', items: 'Groceries (37 states), prescription drugs (most states), medical devices, some services' },
            { label: 'Varies by State', items: 'Clothing (NY/PA exempt, others tax), digital downloads, SaaS software' },
          ].map(c => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-gray-800 text-xs mb-1">{c.label}</div>
              <div class="text-xs text-gray-600">{c.items}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
</Layout>
''')

# ─── DATE CALCULATOR ─────────────────────────────────────────────────────────
write("date", '''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const type = inputs.type || 'diff'
  const date1 = inputs.date1 ? new Date(inputs.date1) : new Date()
  const date2 = inputs.date2 ? new Date(inputs.date2) : new Date()
  const days = parseInt(inputs.days) || 0
  if (type === 'diff') {
    if (!inputs.date1 || !inputs.date2) throw new Error('Select both dates.')
    const diffMs = Math.abs(date2 - date1)
    const diffDays = Math.floor(diffMs / 86400000)
    const diffWeeks = Math.floor(diffDays / 7)
    const years = Math.floor(diffDays / 365.25)
    const months = Math.floor(diffDays / 30.44)
    const hours = Math.floor(diffMs / 3600000)
    return {
      value: diffDays + ' days between dates',
      gaugeValue: Math.min(diffDays / 3.65, 100),
      breakdown: ['Days: ' + diffDays, 'Weeks: ' + diffWeeks, 'Months: ~' + months, 'Years: ~' + years, 'Hours: ' + hours.toLocaleString()],
      stats: [
        { label: 'Days', value: diffDays.toLocaleString() },
        { label: 'Weeks', value: diffWeeks.toLocaleString() },
        { label: 'Months', value: '~' + months },
        { label: 'Years', value: '~' + years },
      ]
    }
  } else {
    if (!inputs.date1) throw new Error('Select a start date.')
    const result = new Date(date1.getTime() + days * 86400000)
    const formatted = result.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
    return {
      value: formatted,
      gaugeValue: 50,
      breakdown: ['Start: ' + date1.toLocaleDateString(), 'Days added: ' + days, 'Result: ' + formatted],
      stats: [
        { label: 'Result Date', value: result.toLocaleDateString() },
        { label: 'Day of Week', value: result.toLocaleDateString('en-US', { weekday: 'long' }) },
        { label: 'Days Added', value: String(days) },
        { label: 'Week Number', value: String(Math.ceil((result - new Date(result.getFullYear(), 0, 1)) / 604800000 + 1)) },
      ]
    }
  }
`

const faqs = [
  { question: 'How do I calculate the number of days between two dates?', answer: 'Subtract the earlier date from the later date in milliseconds, then divide by 86,400,000 (ms per day). Our calculator handles leap years, different month lengths, and daylight saving time automatically.' },
  { question: 'What is the difference between business days and calendar days?', answer: 'Calendar days count all 7 days per week. Business days count only weekdays (Monday–Friday), excluding weekends and sometimes public holidays. Shipping estimates and legal deadlines often use business days.' },
  { question: 'How do I add or subtract days from a date?', answer: 'Add or subtract the number of days in milliseconds (1 day = 86,400,000 ms). The result will cross month and year boundaries automatically. Use our calculator to instantly find the date 30, 60, or 90 days from any date.' },
  { question: 'How many days until a specific date?', answer: 'Subtract today\'s date from the target date. Our calculator does this automatically when you enter today as date 1 and your target as date 2. Use the Age Calculator for birthdays and the Days Until calculator for countdowns.' },
  { question: 'Why do date calculations get complicated near month ends?', answer: 'Months have 28–31 days, and leap years affect February. Adding "one month" to January 31 is ambiguous — does it become February 28 or March 3? Our calculator adds exact calendar days to avoid ambiguity.' },
]
---
<Layout
  title="Date Calculator: Days Between Dates & Date Math"
  description="Calculate the number of days between two dates, or add/subtract days from a date. Free date calculator with weeks, months, and years breakdown."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Other', href: '/calculators/other' },
    { name: 'Date Calculator', href: '/calculators/date-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/other" class="hover:text-blue-600">Other</a><span>›</span>
      <span class="text-gray-900">Date Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Date Calculator"
          description="Find days between dates, or calculate a new date by adding or subtracting days"
          formulaId="date"
          formulaFn={formulaFn}
          resultLabel="Result"
          inputs={[
            { id: 'type', label: 'Calculation Type', type: 'select', options: [
              { value: 'diff', label: 'Days between two dates' },
              { value: 'add', label: 'Add/subtract days from date' },
            ], defaultValue: 'diff' },
            { id: 'date1', label: 'Start Date', type: 'date', defaultValue: new Date().toISOString().split('T')[0] },
            { id: 'date2', label: 'End Date (for difference)', type: 'date', defaultValue: new Date(Date.now() + 30*86400000).toISOString().split('T')[0] },
            { id: 'days', label: 'Days to Add/Subtract (for date math)', type: 'number', placeholder: '30', defaultValue: 30 },
          ]}
          gauge={{
            min: 0, max: 100, unit: '% of year',
            zones: [
              { label: '< 1 month', color: '#22c55e', from: 0, to: 8 },
              { label: '1–3 months', color: '#3b82f6', from: 8, to: 25 },
              { label: '3–6 months', color: '#f59e0b', from: 25, to: 50 },
              { label: '6–12 months', color: '#8b5cf6', from: 50, to: 100 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'Age Calculator', href: '/calculators/age-calculator' },
            { name: 'Days Until Calculator', href: '/calculators/days-until-calculator' },
            { name: 'Time Calculator', href: '/calculators/time-calculator' },
            { name: 'Due Date Calculator', href: '/calculators/due-date-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Common Date Intervals</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[['1 week','7 days'],['1 month','~30 days'],['90 days','~3 months'],['1 quarter','91–92 days'],['6 months','~182 days'],['1 year','365 or 366 days']].map(([l,r]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span>{l}</span><span class="font-medium">{r}</span></div>
            ))}
          </div>
        </div>
        <div class="bg-green-50 border border-green-200 rounded-xl p-5">
          <h3 class="font-bold text-green-900 mb-2">Leap Years</h3>
          <p class="text-xs text-green-800">Leap years occur every 4 years (e.g., 2024, 2028), except centuries not divisible by 400 (1900 was not a leap year; 2000 was). February has 29 days in a leap year.</p>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Days in Each Month</h2>
        <div class="grid grid-cols-3 gap-2">
          {[['January','31'],['February','28/29'],['March','31'],['April','30'],['May','31'],['June','30'],['July','31'],['August','31'],['September','30'],['October','31'],['November','30'],['December','31']].map(([m,d]) => (
            <div class="bg-gray-50 rounded-lg p-2 text-center">
              <div class="text-xs font-medium text-gray-700">{m}</div>
              <div class="text-sm font-bold text-blue-600">{d}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Useful Date Facts</h2>
        <div class="space-y-2">
          {[
            { fact: 'Days in a year', value: '365 (or 366 in a leap year)' },
            { fact: 'Weeks in a year', value: '52 weeks + 1 day (or 2 in leap year)' },
            { fact: 'Days in a quarter', value: '90–92 days' },
            { fact: '100 days from Jan 1', value: 'April 10 (or 11 in leap year)' },
            { fact: '10,000 days', value: '~27.4 years' },
            { fact: '1 million seconds', value: '~11.6 days' },
          ].map(f => (
            <div class="flex justify-between bg-gray-50 rounded-lg p-2 text-xs">
              <span class="text-gray-600">{f.fact}</span>
              <span class="font-medium text-gray-800">{f.value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
</Layout>
''')

print("\\n✅ Batch 2 done. Written: credit-card, debt-payoff, interest, percentage, tip, gpa, discount, sales-tax, date")
