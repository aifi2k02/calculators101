#!/usr/bin/env python3
"""Generate full enhanced pages for all remaining 101 calculators at once.
Each page gets: formulaFn with stats+gaugeValue, gauge, faqs, relatedCalcs, breadcrumbs, sidebar, content sections."""
import os

CALC_DIR = "/Users/apple/Documents/Projects/calculators-for-free/src/pages/calculators"

written = 0

def w(slug, title, cat, cat_slug, seo_title, seo_desc, formula, inputs_js, gauge_zones, gauge_unit, gauge_max,
      faqs_pairs, related_pairs, sidebar_html, content_html, result_label="Result", calc_desc=""):
    global written
    gauge_min = 0
    zones_js = "\n".join(
        f'              {{ label: "{z[0]}", color: "{z[1]}", from: {z[2]}, to: {z[3]} }},'
        for z in gauge_zones
    )
    related_js = "\n            ".join(
        f'{{ name: "{n}", href: "{h}" }},'
        for n, h in related_pairs
    )
    # Build faqs as JS array using double quotes to avoid apostrophe issues
    faqs_items = []
    for q, a in faqs_pairs:
        # Escape double quotes in q and a
        q2 = q.replace('"', '\\"')
        a2 = a.replace('"', '\\"')
        faqs_items.append(f'  {{ question: "{q2}", answer: "{a2}" }}')
    faqs_js = "[\n" + ",\n".join(faqs_items) + "\n]"

    cd = calc_desc or seo_desc[:90]

    content = f'''---
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
          gauge={{{{
            min: {gauge_min}, max: {gauge_max}, unit: "{gauge_unit}",
            zones: [
{zones_js}
            ]
          }}}}
          faqs={{faqs}}
          relatedCalcs={{[
            {related_js}
          ]}}
        />
      </div>
      <aside class="space-y-5">
{sidebar_html}
      </aside>
    </div>
{content_html}
  </div>
</Layout>
'''
    path = os.path.join(CALC_DIR, f"{slug}-calculator.astro")
    with open(path, 'w') as f:
        f.write(content)
    written += 1
    print(f"  {slug}")

# ── 401K ────────────────────────────────────────────────────────────────────
w("401k","401(k) Calculator","Financial","financial",
  "401(k) Calculator: Retirement Savings Projection",
  "Project your 401(k) balance at retirement with employer match and compound growth. Free 401k calculator.",
  """
  const salary = parseFloat(inputs.salary)||0
  const contrib = parseFloat(inputs.contrib)||0
  const match = parseFloat(inputs.match)||0
  const matchLimit = parseFloat(inputs.matchLimit)||0
  const rate = parseFloat(inputs.rate)||7
  const years = parseInt(inputs.years)||30
  const current = parseFloat(inputs.current)||0
  if(salary<=0||years<=0) throw new Error("Enter salary and years.")
  const annual = salary*(contrib/100)
  const employerMatch = salary*(Math.min(contrib,matchLimit)/100)*(match/100)
  const totalAnnual = annual+employerMatch
  const r=rate/100
  const fv = current*Math.pow(1+r,years) + totalAnnual*((Math.pow(1+r,years)-1)/r)
  const totalContrib = current + totalAnnual*years
  const gains = fv-totalContrib
  return {
    value:"$"+fv.toLocaleString("en-US",{maximumFractionDigits:0}),
    gaugeValue:Math.min((fv/1000000)*100,100),
    breakdown:["Your annual contrib: $"+annual.toFixed(0),"Employer match: $"+employerMatch.toFixed(0),"Total annual: $"+totalAnnual.toFixed(0),"Balance at retirement: $"+fv.toLocaleString("en-US",{maximumFractionDigits:0})],
    stats:[
      {label:"Final Balance",value:"$"+fv.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Employer Match/yr",value:"$"+employerMatch.toFixed(0)},
      {label:"Investment Gains",value:"$"+gains.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Total Contributed",value:"$"+totalContrib.toLocaleString("en-US",{maximumFractionDigits:0})},
    ]
  }
""",
  """{id:"salary",label:"Annual Salary",type:"number",placeholder:"75000",min:0,unit:"$",defaultValue:75000},
            {id:"contrib",label:"Your Contribution %",type:"number",placeholder:"10",min:0,max:100,step:0.5,unit:"%",defaultValue:10},
            {id:"match",label:"Employer Match %",type:"number",placeholder:"100",min:0,max:200,unit:"%",defaultValue:100},
            {id:"matchLimit",label:"Match Limit (% of salary)",type:"number",placeholder:"5",min:0,max:20,step:0.5,unit:"%",defaultValue:5},
            {id:"current",label:"Current 401(k) Balance",type:"number",placeholder:"0",min:0,unit:"$",defaultValue:0},
            {id:"rate",label:"Annual Return Rate",type:"number",placeholder:"7",min:0,max:20,step:0.1,unit:"%",defaultValue:7},
            {id:"years",label:"Years Until Retirement",type:"number",placeholder:"30",min:1,max:50,unit:"years",defaultValue:30}""",
  [("Under $250k","#ef4444",0,25),("$250k–$500k","#f59e0b",25,50),("$500k–$1M","#3b82f6",50,75),("$1M+","#22c55e",75,100)],
  "% to $1M","100",
  [("Always get the full employer match first — it is a 50-100% instant return","If your employer matches 100% up to 5% of salary, contribute at least 5%. That is a guaranteed 100% return on that money before any investment gains. No investment can reliably beat free money."),
   ("What is the 2025 401(k) contribution limit?","$23,500 for employees under 50. If you are 50 or older, you can contribute an additional $7,500 catch-up contribution for a total of $31,000. Employer contributions do not count toward your personal limit."),
   ("What happens to my 401(k) if I leave my job?","You have several options: leave it in the old plan, roll it over to your new employer plan, roll it over to an IRA (often best for investment flexibility), or cash it out (not recommended — 10% penalty + income taxes if under 59.5)."),
   ("Roth 401(k) vs traditional 401(k): which is better?","Traditional: pre-tax contributions now, pay taxes in retirement. Roth: after-tax now, tax-free in retirement. If you expect higher taxes in retirement, Roth wins. Many financial advisors suggest contributing to both for tax diversification."),
   ("What investment funds should I choose in my 401(k)?","For most people: low-cost index funds (S&P 500 or total market). Target-date funds are simple one-decision options — pick your retirement year and the fund automatically adjusts allocation. Avoid high-fee actively managed funds (expense ratio above 0.5%).")],
  [("Retirement Calculator","/calculators/retirement-calculator"),("Roth IRA Calculator","/calculators/roth-ira-calculator"),("Investment Calculator","/calculators/investment-calculator"),("FIRE Calculator","/calculators/fire-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">2025 401(k) Limits</h3>
          <div class="space-y-1 text-xs text-blue-800">
            <div class="flex justify-between border-b border-blue-100 pb-1"><span>Employee limit</span><span class="font-medium">$23,500</span></div>
            <div class="flex justify-between border-b border-blue-100 pb-1"><span>Catch-up (50+)</span><span class="font-medium">+$7,500</span></div>
            <div class="flex justify-between border-b border-blue-100 pb-1"><span>Total (50+)</span><span class="font-medium">$31,000</span></div>
            <div class="flex justify-between"><span>Total w/ employer</span><span class="font-medium">$70,000</span></div>
          </div>
        </div>
        <div class="bg-green-50 border border-green-200 rounded-xl p-5">
          <h3 class="font-bold text-green-900 mb-2">Why Employer Match Matters</h3>
          <p class="text-xs text-green-800">A 100% match up to 5% is a guaranteed 100% return. A $75k salary at 5% = $3,750/yr free money from employer + your $3,750 = $7,500/yr total. Over 30 years at 7%: the match alone contributes ~$350,000 to your retirement.</p>
        </div>""",
  """    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">$75k Salary — Balance Projections</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-3 text-xs font-semibold text-gray-700">Contrib %</th><th class="text-right p-3 text-xs font-semibold text-gray-700">At 20 yrs</th><th class="text-right p-3 text-xs font-semibold text-gray-700">At 30 yrs</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["5% + 5% match","$211k","$521k"],["10% + 5% match","$316k","$781k"],["15% + 5% match","$422k","$1.04M"],["Max ($23,500)","$640k","$1.58M"]].map(r => (
              <tr><td class="p-3 text-xs">{r[0]}</td><td class="p-3 text-xs text-right">{r[1]}</td><td class="p-3 text-xs text-right text-green-600 font-medium">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
        <p class="text-xs text-gray-500 mt-1">Assumes 7% annual return, starting from $0</p>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">401(k) Contribution Strategy</h2>
        <div class="space-y-2">
          {[
            {step:"1",text:"Contribute at least enough to get the full employer match (free 50-100% return)"},
            {step:"2",text:"Max out HSA contributions if eligible ($8,550 family in 2025) — triple tax advantage"},
            {step:"3",text:"Consider maxing Roth IRA ($7,000) for tax diversification"},
            {step:"4",text:"Return to 401(k) and contribute up to the $23,500 limit"},
            {step:"5",text:"Use taxable brokerage accounts for additional savings beyond tax-advantaged limits"},
          ].map(s => (
            <div class="flex gap-3 bg-gray-50 rounded-lg p-3">
              <div class="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">{s.step}</div>
              <div class="text-xs text-gray-600">{s.text}</div>
            </div>
          ))}
        </div>
      </div>
    </div>""",
  "Retirement Balance","Project your 401(k) balance with employer match and compound growth")

# ── NET WORTH ────────────────────────────────────────────────────────────────
w("net-worth","Net Worth Calculator","Financial","financial",
  "Net Worth Calculator: Total Assets Minus Liabilities",
  "Calculate your net worth by subtracting total debts from total assets. Track your financial progress. Free net worth calculator.",
  """
  const cash = parseFloat(inputs.cash)||0
  const investments = parseFloat(inputs.investments)||0
  const retirement = parseFloat(inputs.retirement)||0
  const realEstate = parseFloat(inputs.realEstate)||0
  const vehicles = parseFloat(inputs.vehicles)||0
  const otherAssets = parseFloat(inputs.otherAssets)||0
  const mortgage = parseFloat(inputs.mortgage)||0
  const carLoans = parseFloat(inputs.carLoans)||0
  const studentLoans = parseFloat(inputs.studentLoans)||0
  const creditCards = parseFloat(inputs.creditCards)||0
  const otherDebt = parseFloat(inputs.otherDebt)||0
  const assets = cash+investments+retirement+realEstate+vehicles+otherAssets
  const liabilities = mortgage+carLoans+studentLoans+creditCards+otherDebt
  const netWorth = assets-liabilities
  const debtRatio = assets>0?(liabilities/assets)*100:0
  return {
    value:"$"+netWorth.toLocaleString("en-US",{maximumFractionDigits:0}),
    gaugeValue:Math.min(Math.max((netWorth/500000)*100,0),100),
    breakdown:["Total assets: $"+assets.toLocaleString("en-US",{maximumFractionDigits:0}),"Total liabilities: $"+liabilities.toLocaleString("en-US",{maximumFractionDigits:0}),"Net worth: $"+netWorth.toLocaleString("en-US",{maximumFractionDigits:0}),"Debt-to-asset ratio: "+debtRatio.toFixed(1)+"%"],
    stats:[
      {label:"Net Worth",value:"$"+netWorth.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Total Assets",value:"$"+assets.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Total Debt",value:"$"+liabilities.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Debt-to-Asset %",value:debtRatio.toFixed(1)+"%"},
    ]
  }
""",
  """{id:"cash",label:"Cash & Savings",type:"number",placeholder:"10000",min:0,unit:"$",defaultValue:10000},
            {id:"investments",label:"Investments & Brokerage",type:"number",placeholder:"50000",min:0,unit:"$",defaultValue:50000},
            {id:"retirement",label:"401(k) / IRA / Pension",type:"number",placeholder:"80000",min:0,unit:"$",defaultValue:80000},
            {id:"realEstate",label:"Real Estate Value",type:"number",placeholder:"0",min:0,unit:"$",defaultValue:0},
            {id:"vehicles",label:"Vehicles",type:"number",placeholder:"20000",min:0,unit:"$",defaultValue:20000},
            {id:"otherAssets",label:"Other Assets",type:"number",placeholder:"0",min:0,unit:"$",defaultValue:0},
            {id:"mortgage",label:"Mortgage Balance",type:"number",placeholder:"0",min:0,unit:"$",defaultValue:0},
            {id:"carLoans",label:"Car Loans",type:"number",placeholder:"15000",min:0,unit:"$",defaultValue:15000},
            {id:"studentLoans",label:"Student Loans",type:"number",placeholder:"30000",min:0,unit:"$",defaultValue:30000},
            {id:"creditCards",label:"Credit Card Debt",type:"number",placeholder:"5000",min:0,unit:"$",defaultValue:5000},
            {id:"otherDebt",label:"Other Debt",type:"number",placeholder:"0",min:0,unit:"$",defaultValue:0}""",
  [("Negative","#ef4444",0,10),("Under $100k","#f59e0b",10,30),("$100k–$300k","#3b82f6",30,60),("$300k–$500k+","#22c55e",60,100)],
  "% to $500k","100",
  [("What is net worth?","Net worth = Total Assets - Total Liabilities. It is the most comprehensive snapshot of your financial health. Positive net worth means you own more than you owe. Tracking it over time shows whether your financial position is improving."),
   ("What is the average net worth in the US?","US median net worth is ~$192,700 (2022 Federal Reserve SCF). Mean net worth is ~$1.06 million, heavily skewed by the ultra-wealthy. Median is more representative. At age 35, median net worth is ~$76k; at 55-64, ~$364k."),
   ("How do I grow my net worth?","Two levers: increase assets (invest, save, appreciate real estate) and decrease liabilities (pay off debt). Investing consistently over time has the biggest impact due to compounding. Eliminating high-interest debt also rapidly improves net worth."),
   ("Should I include home equity in net worth?","Yes. Home equity (market value minus mortgage balance) is an asset. However, it is illiquid — you cannot easily spend it. Some financial planners separate liquid net worth (excludes home) from total net worth for this reason."),
   ("What is a good net worth for my age?","Rough benchmark: net worth = Annual Income x Age / 10 (from The Millionaire Next Door). At 35 with $70k income: target ~$245k. This varies enormously by income, cost of living, and career stage. Focus on trajectory (improving year over year) more than absolute numbers.")],
  [("Investment Calculator","/calculators/investment-calculator"),("Budget Calculator","/calculators/budget-calculator"),("Retirement Calculator","/calculators/retirement-calculator"),("Debt Payoff Calculator","/calculators/debt-payoff-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Median Net Worth by Age (US)</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[["Under 35","$39,000"],["35–44","$135,000"],["45–54","$247,000"],["55–64","$364,000"],["65–74","$410,000"],["75+","$335,000"]].map(([a,v]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span>{a}</span><span class="font-medium">{v}</span></div>
            ))}
          </div>
          <p class="text-xs text-blue-600 mt-1">Source: Federal Reserve SCF 2022</p>
        </div>""",
  """    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Assets vs Liabilities</h2>
        <div class="grid grid-cols-2 gap-4">
          <div class="bg-green-50 rounded-xl p-4">
            <h3 class="font-bold text-green-800 text-sm mb-2">Assets (+)</h3>
            <ul class="text-xs text-green-700 space-y-1">
              <li>Cash & checking accounts</li>
              <li>Investment accounts</li>
              <li>401(k), IRA, pension</li>
              <li>Home equity</li>
              <li>Vehicle value</li>
              <li>Business equity</li>
              <li>Valuables (art, jewelry)</li>
            </ul>
          </div>
          <div class="bg-red-50 rounded-xl p-4">
            <h3 class="font-bold text-red-800 text-sm mb-2">Liabilities (-)</h3>
            <ul class="text-xs text-red-700 space-y-1">
              <li>Mortgage balance</li>
              <li>Car loan balances</li>
              <li>Student loan debt</li>
              <li>Credit card balances</li>
              <li>Personal loans</li>
              <li>Medical debt</li>
              <li>Any other debt owed</li>
            </ul>
          </div>
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">How to Grow Net Worth Faster</h2>
        <div class="space-y-2">
          {["Invest consistently — even $200/month compounds to $200k+ over 25 years at 7%","Pay off high-interest debt aggressively — guaranteed return equal to the interest rate","Avoid depreciating debt — car loans and consumer debt reduce net worth","Increase income through skills, raises, or side income — invest the difference","Review and rebalance investments annually","Avoid lifestyle inflation as income grows — save the raise"].map(tip => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{tip}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Net Worth","Calculate your total net worth from all assets and liabilities")

# ── EMERGENCY FUND ──────────────────────────────────────────────────────────
w("emergency-fund","Emergency Fund Calculator","Financial","financial",
  "Emergency Fund Calculator: How Much Should You Save?",
  "Calculate your ideal emergency fund size based on monthly expenses and job stability. Free emergency fund calculator.",
  """
  const monthly = parseFloat(inputs.monthly)||0
  const months = parseInt(inputs.months)||6
  const current = parseFloat(inputs.current)||0
  if(monthly<=0) throw new Error("Enter monthly expenses.")
  const target = monthly*months
  const needed = Math.max(0,target-current)
  const funded = Math.min((current/target)*100,100)
  const monthsToFull = needed>0&&inputs.savingRate?(needed/parseFloat(inputs.savingRate)):0
  return {
    value:"$"+target.toLocaleString("en-US",{maximumFractionDigits:0})+" target",
    gaugeValue:funded,
    breakdown:["Monthly expenses: $"+monthly,"Months coverage: "+months,"Target fund: $"+target.toLocaleString("en-US",{maximumFractionDigits:0}),"Current saved: $"+current,"Still needed: $"+needed.toLocaleString("en-US",{maximumFractionDigits:0}),"Funded: "+funded.toFixed(1)+"%"],
    stats:[
      {label:"Target Fund",value:"$"+target.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Currently Saved",value:"$"+current.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Still Needed",value:"$"+needed.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"% Funded",value:funded.toFixed(1)+"%"},
    ]
  }
""",
  """{id:"monthly",label:"Monthly Essential Expenses",type:"number",placeholder:"3500",min:0,unit:"$",defaultValue:3500},
            {id:"months",label:"Months of Coverage",type:"select",options:[{value:"3",label:"3 months (minimum)"},{value:"6",label:"6 months (standard)"},{value:"9",label:"9 months (cautious)"},{value:"12",label:"12 months (very safe)"}],defaultValue:"6"},
            {id:"current",label:"Current Emergency Savings",type:"number",placeholder:"0",min:0,unit:"$",defaultValue:0},
            {id:"savingRate",label:"Monthly Savings Rate (for timeline)",type:"number",placeholder:"500",min:0,unit:"$",defaultValue:500}""",
  [("Not Started","#ef4444",0,10),("Building","#f59e0b",10,50),("Nearly There","#3b82f6",50,90),("Fully Funded","#22c55e",90,100)],
  "% funded","100",
  [("How many months of expenses should I save?","3 months: absolute minimum for stable employment. 6 months: standard recommendation for most people. 9-12 months: recommended for self-employed, freelancers, commission-based income, single-income households, or those with health issues."),
   ("What counts as monthly expenses for an emergency fund?","Only essential expenses: rent/mortgage, food, utilities, transportation, minimum debt payments, insurance, and basic healthcare. Do NOT include entertainment, dining out, or discretionary spending. This makes your fund go further."),
   ("Where should I keep my emergency fund?","High-yield savings account (HYSA): 4-5% APY, FDIC insured, easy access. Money market accounts are also good. Avoid investing emergency funds in stocks — they can drop 30-50% when you need the money most (job loss often correlates with market downturns)."),
   ("Should I build an emergency fund or pay off debt first?","Build a small $1,000 starter emergency fund first, then focus on high-interest debt (credit cards). Once high-interest debt is gone, build full 3-6 month fund. The exception: if debt interest is lower than HYSA rate, build fund first."),
   ("Can I use a credit card instead of an emergency fund?","Credit cards are a backstop, not a substitute. During true emergencies (job loss), issuers sometimes reduce limits or close accounts — exactly when you need them most. Also, credit card debt at 20% APR turns a $3,000 emergency into an ongoing financial burden.")],
  [("Savings Calculator","/calculators/savings-calculator"),("Budget Calculator","/calculators/budget-calculator"),("Net Worth Calculator","/calculators/net-worth-calculator"),("Debt Payoff Calculator","/calculators/debt-payoff-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Emergency Fund by Situation</h3>
          <div class="space-y-2 text-xs text-blue-800">
            {[["Stable job, dual income","3 months"],["Single income household","6 months"],["Self-employed / freelance","9–12 months"],["Commission-based income","9–12 months"],["Health conditions","9–12 months"],["Near retirement","12+ months"]].map(([s,m]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span>{s}</span><span class="font-medium">{m}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Emergency Fund Timeline</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold text-gray-700">Monthly Savings</th><th class="text-right p-2 text-xs font-semibold text-gray-700">3 mo ($10,500)</th><th class="text-right p-2 text-xs font-semibold text-gray-700">6 mo ($21,000)</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["$200","4.4 yrs","8.75 yrs"],["$500","1.75 yrs","3.5 yrs"],["$1,000","10.5 mo","1.75 yrs"],["$2,000","5.25 mo","10.5 mo"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
        <p class="text-xs text-gray-500 mt-1">Based on $3,500/month in expenses</p>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Building Your Emergency Fund Faster</h2>
        <div class="space-y-2">
          {["Set up automatic transfer on payday — treat it like a bill","Use a separate high-yield savings account (out of sight, out of mind)","Direct any windfall (tax refund, bonus, gift) straight to the fund","Sell unused items and deposit the proceeds","Cut one recurring subscription per month and redirect the savings","Consider a temporary side gig to accelerate the timeline"].map(tip => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-green-500 mt-0.5">•</span><span>{tip}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Emergency Fund Target","Find your ideal emergency fund size and track your progress")

# ── PMI ──────────────────────────────────────────────────────────────────────
w("pmi","PMI Calculator","Financial","financial",
  "PMI Calculator: Private Mortgage Insurance Cost",
  "Calculate your monthly PMI payment and find out when you can cancel it. Free private mortgage insurance calculator.",
  """
  const homePrice = parseFloat(inputs.homePrice)||0
  const downPayment = parseFloat(inputs.downPayment)||0
  const loanRate = parseFloat(inputs.loanRate)||7
  const pmiRate = parseFloat(inputs.pmiRate)||0.8
  if(homePrice<=0) throw new Error("Enter home price.")
  const ltv = ((homePrice-downPayment)/homePrice)*100
  const loanAmount = homePrice-downPayment
  const pmiAnnual = loanAmount*(pmiRate/100)
  const pmiMonthly = pmiAnnual/12
  const r = loanRate/100/12
  const n = 360
  const payment = r===0?loanAmount/n:loanAmount*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1)
  let bal=loanAmount,monthsToRemove=0
  const targetBalance = homePrice*0.80
  while(bal>targetBalance&&monthsToRemove<360){
    const int=bal*r; bal=bal+int-payment; monthsToRemove++
  }
  const yearsToRemove = Math.floor(monthsToRemove/12)
  const pmiSaved = pmiMonthly*monthsToRemove
  return {
    value:"$"+pmiMonthly.toFixed(2)+"/mo",
    gaugeValue:Math.max(0,Math.min(ltv,100)),
    breakdown:["LTV ratio: "+ltv.toFixed(1)+"%","PMI monthly: $"+pmiMonthly.toFixed(2),"PMI annual: $"+pmiAnnual.toFixed(2),"PMI removed at: ~"+yearsToRemove+"y "+monthsToRemove%12+"m","Total PMI paid: $"+pmiSaved.toFixed(2)],
    stats:[
      {label:"Monthly PMI",value:"$"+pmiMonthly.toFixed(2)},
      {label:"LTV Ratio",value:ltv.toFixed(1)+"%"},
      {label:"PMI Removed",value:"~"+yearsToRemove+" yrs"},
      {label:"Total PMI Cost",value:"$"+pmiSaved.toFixed(0)},
    ]
  }
""",
  """{id:"homePrice",label:"Home Price",type:"number",placeholder:"400000",min:0,unit:"$",defaultValue:400000},
            {id:"downPayment",label:"Down Payment",type:"number",placeholder:"40000",min:0,unit:"$",defaultValue:40000},
            {id:"loanRate",label:"Mortgage Interest Rate",type:"number",placeholder:"7",min:0,max:20,step:0.1,unit:"%",defaultValue:7},
            {id:"pmiRate",label:"PMI Rate",type:"number",placeholder:"0.8",min:0.1,max:3,step:0.1,unit:"%",defaultValue:0.8}""",
  [("20%+ down (no PMI)","#22c55e",0,80),("15–20% down","#3b82f6",80,85),("10–15% down","#f59e0b",85,90),("Less than 10%","#ef4444",90,100)],
  "% LTV","100",
  [("What is PMI?","Private Mortgage Insurance (PMI) protects the lender (not you) if you default on a loan with less than 20% down. It typically costs 0.5-1.5% of the loan amount annually. On a $320,000 loan at 0.8% PMI, that is $2,560/year ($213/month)."),
   ("When can I cancel PMI?","By law (Homeowners Protection Act), you can request PMI cancellation when your loan-to-value ratio reaches 80% (20% equity). Lenders must automatically cancel it at 78% LTV based on original value. You can also refinance once you have 20% equity."),
   ("How do I get rid of PMI faster?","Make extra principal payments to reach 80% LTV sooner. Pay for a new appraisal once your home appreciates — if the current LTV is under 80% of current value, you can request cancellation. Some lenders accept appreciation within 2+ years of ownership."),
   ("Is PMI tax deductible?","PMI deductibility has varied by tax year and income level. Check the current IRS guidelines — it was deductible for eligible taxpayers through 2021 and has been extended at various times. Consult a tax professional for your specific situation."),
   ("What is a piggyback loan to avoid PMI?","An 80/10/10 loan: 80% first mortgage, 10% second mortgage (home equity loan), and 10% down payment. This avoids PMI entirely. The second mortgage typically has a higher rate, but may cost less than PMI over time if rates are favorable.")],
  [("Mortgage Calculator","/calculators/mortgage-calculator"),("House Affordability Calculator","/calculators/house-affordability-calculator"),("Down Payment Calculator","/calculators/down-payment-calculator"),("Refinance Calculator","/calculators/refinance-calculator")],
  """        <div class="bg-red-50 border border-red-200 rounded-xl p-5">
          <h3 class="font-bold text-red-900 mb-3">PMI Cost by Loan Amount</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-red-700"><th class="text-left pb-1">Loan Amount</th><th class="text-right pb-1">0.5% PMI</th><th class="text-right pb-1">1.0% PMI</th></tr></thead>
            <tbody class="text-red-900">
              {[["$200k","$83/mo","$167/mo"],["$320k","$133/mo","$267/mo"],["$400k","$167/mo","$333/mo"],["$500k","$208/mo","$417/mo"]].map(r => (
                <tr class="border-t border-red-100"><td class="py-0.5">{r[0]}</td><td class="text-right">{r[1]}</td><td class="text-right">{r[2]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Ways to Avoid PMI</h2>
        <div class="space-y-3">
          {[
            {opt:"20% Down Payment",desc:"The simplest way — save 20% of home price and avoid PMI entirely from day one"},
            {opt:"Piggyback Loan (80/10/10)",desc:"Take a second mortgage for 10%, put 10% down, avoid PMI on the primary 80% loan"},
            {opt:"Lender-Paid PMI (LPMI)",desc:"Lender pays PMI in exchange for a higher interest rate — better if you plan to sell soon"},
            {opt:"VA or USDA Loans",desc:"Veterans and rural buyers may qualify for no-down-payment loans with no PMI requirement"},
          ].map(o => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-gray-800 text-xs mb-1">{o.opt}</div>
              <div class="text-xs text-gray-600">{o.desc}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">LTV and PMI Rate Reference</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold text-gray-700">Down Payment</th><th class="text-right p-2 text-xs font-semibold text-gray-700">LTV</th><th class="text-right p-2 text-xs font-semibold text-gray-700">Typical PMI Rate</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["20%+","80% or less","No PMI"],["15%","85%","0.3–0.5%"],["10%","90%","0.5–0.8%"],["5%","95%","0.8–1.2%"],["3%","97%","1.0–1.5%"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right font-medium">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "Monthly PMI","Calculate your PMI payment and find out when you can cancel it")

print(f"\nWritten so far: {written} pages (401k, net-worth, emergency-fund, pmi)")
