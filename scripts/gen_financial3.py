#!/usr/bin/env python3
"""Generate more financial calculator pages."""
import os
CALC_DIR = "/Users/apple/Documents/Projects/calculators-for-free/src/pages/calculators"
written = 0

def w(slug,title,cat,cat_slug,seo_title,seo_desc,formula,inputs_js,gauge_zones,gauge_unit,gauge_max,
      faqs_pairs,related_pairs,sidebar_html,content_html,result_label="Result",calc_desc=""):
    global written
    zones_js="\n".join(f'              {{ label: "{z[0]}", color: "{z[1]}", from: {z[2]}, to: {z[3]} }},' for z in gauge_zones)
    related_js="\n            ".join(f'{{ name: "{n}", href: "{h}" }},' for n,h in related_pairs)
    faqs_js="[\n"+",\n".join(f'  {{ question: "{q.replace(chr(34),chr(92)+chr(34))}", answer: "{a.replace(chr(34),chr(92)+chr(34))}" }}' for q,a in faqs_pairs)+"\n]"
    cd=calc_desc or seo_desc[:90]
    content=f'''---
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
            min: 0, max: {gauge_max}, unit: "{gauge_unit}",
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
    path=os.path.join(CALC_DIR,f"{slug}-calculator.astro")
    open(path,'w').write(content)
    written+=1
    print(f"  {slug}")

# ── COLLEGE SAVINGS ──────────────────────────────────────────────────────────
w("college-savings","College Savings Calculator","Financial","financial",
  "College Savings Calculator: How Much to Save for College",
  "Calculate how much you need to save monthly to fund your child education. Includes 529 plan growth. Free college savings calculator.",
  """
  const currentAge = parseInt(inputs.currentAge)||0
  const collegeAge = parseInt(inputs.collegeAge)||18
  const annualCost = parseFloat(inputs.annualCost)||40000
  const inflation = parseFloat(inputs.inflation)||5
  const returnRate = parseFloat(inputs.returnRate)||7
  const currentSaved = parseFloat(inputs.currentSaved)||0
  if(collegeAge<=currentAge) throw new Error("College age must be greater than current age.")
  const yearsToCollege = collegeAge-currentAge
  const inflatedCost = annualCost*Math.pow(1+inflation/100,yearsToCollege)
  const totalNeeded = inflatedCost*4
  const r = returnRate/100/12
  const n = yearsToCollege*12
  const fvCurrent = currentSaved*Math.pow(1+r,n)
  const stillNeeded = Math.max(0,totalNeeded-fvCurrent)
  const monthlyNeeded = stillNeeded/(((Math.pow(1+r,n)-1)/r))
  return {
    value:"$"+monthlyNeeded.toFixed(2)+"/mo",
    gaugeValue:Math.min((fvCurrent/totalNeeded)*100,100),
    breakdown:["Years until college: "+yearsToCollege,"Inflation-adjusted annual cost: $"+inflatedCost.toFixed(0),"Total 4-yr cost: $"+totalNeeded.toFixed(0),"Current savings at college: $"+fvCurrent.toFixed(0),"Still needed: $"+stillNeeded.toFixed(0),"Monthly savings needed: $"+monthlyNeeded.toFixed(2)],
    stats:[
      {label:"Total 4-yr Cost",value:"$"+totalNeeded.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Already Funded",value:"$"+fvCurrent.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Still Needed",value:"$"+stillNeeded.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Monthly Savings",value:"$"+monthlyNeeded.toFixed(2)},
    ]
  }
""",
  """{id:"currentAge",label:"Child Current Age",type:"number",placeholder:"5",min:0,max:17,unit:"years",defaultValue:5},
            {id:"collegeAge",label:"Age Starting College",type:"number",placeholder:"18",min:16,max:25,unit:"years",defaultValue:18},
            {id:"annualCost",label:"Annual College Cost (today)",type:"number",placeholder:"40000",min:0,unit:"$",defaultValue:40000},
            {id:"inflation",label:"College Cost Inflation Rate",type:"number",placeholder:"5",min:0,max:15,step:0.1,unit:"%",defaultValue:5},
            {id:"returnRate",label:"Investment Return Rate",type:"number",placeholder:"7",min:0,max:15,step:0.1,unit:"%",defaultValue:7},
            {id:"currentSaved",label:"Amount Already Saved",type:"number",placeholder:"0",min:0,unit:"$",defaultValue:0}""",
  [("Not started","#ef4444",0,10),("Building","#f59e0b",10,40),("On track","#3b82f6",40,75),("Well funded","#22c55e",75,100)],
  "% funded","100",
  [("What is a 529 plan?","A 529 plan is a tax-advantaged savings account designed for education expenses. Contributions grow tax-free, and withdrawals for qualified education expenses (tuition, room, board, books) are federal income tax-free. Many states offer additional state tax deductions. The 2025 annual gift-tax exclusion limit is $19,000/person."),
   ("How much does college actually cost in 2025?","Average annual costs (2024-25): Public 4-year in-state: ~$28,000 (tuition + room/board). Private nonprofit 4-year: ~$60,000. Costs typically increase 4-6% annually. Over 4 years, expect $120k-$250k+ depending on school type. Financial aid can significantly reduce actual cost for many families."),
   ("When should I start saving for college?","The earlier the better due to compounding. Starting at birth vs. age 10 can mean 2-3x more money at college age. Even small amounts invested early grow substantially. If starting late, maximize contributions and consider more aggressive investment allocation in the early years."),
   ("What can 529 funds be used for?","Qualified expenses: tuition, fees, room and board, books, supplies, computers required for school. Since 2024, up to $35,000 of unused 529 funds can be rolled into a Roth IRA (with some restrictions). K-12 tuition (up to $10,000/year) also qualifies."),
   ("What if my child does not go to college?","You can transfer the 529 to a sibling or other family member tax-free. Starting 2024, up to $35,000 can roll into a Roth IRA (must be 15+ year old account). Non-qualified withdrawals pay income tax + 10% penalty on earnings only — the principal comes out tax-free since it was already taxed.")],
  [("Savings Calculator","/calculators/savings-calculator"),("Investment Calculator","/calculators/investment-calculator"),("401k Calculator","/calculators/401k-calculator"),("Budget Calculator","/calculators/budget-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Average 4-Year College Costs</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[["Public in-state","$28k/yr ($112k total)"],["Public out-of-state","$45k/yr ($180k total)"],["Private nonprofit","$60k/yr ($240k total)"]].map(([t,c]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span>{t}</span><span class="font-medium">{c}</span></div>
            ))}
          </div>
          <p class="text-xs text-blue-600 mt-1">2024-25 estimates including room and board</p>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Monthly Savings Needed by Start Age</h2>
        <p class="text-xs text-gray-600 mb-3">Goal: $100,000 at age 18, 7% return, starting from $0</p>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Start Age</th><th class="text-right p-2 text-xs font-semibold">Years</th><th class="text-right p-2 text-xs font-semibold">Monthly</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Birth","18 years","$229"],["Age 5","13 years","$366"],["Age 10","8 years","$718"],["Age 14","4 years","$1,697"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right font-medium text-blue-700">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">529 Plan Benefits</h2>
        <div class="space-y-2">
          {["Tax-free growth — no federal tax on investment earnings","Tax-free withdrawals for qualified education expenses","Many states offer state income tax deductions on contributions","Flexible beneficiary — transfer to siblings, cousins, even yourself","No income limits to contribute (unlike Roth IRA)","New: up to $35k can roll to Roth IRA if unused (starting 2024)","Can be used for K-12 tuition up to $10k/year"].map(b => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-green-500 mt-0.5">✓</span><span>{b}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Monthly Savings Needed","Project college costs and calculate how much to save monthly")

# ── DCA ──────────────────────────────────────────────────────────────────────
w("dca","Dollar-Cost Averaging Calculator","Financial","financial",
  "Dollar-Cost Averaging Calculator: DCA Investment Returns",
  "Calculate returns from dollar-cost averaging (DCA) into stocks, ETFs, or Bitcoin over time. Free DCA investment calculator.",
  """
  const monthly = parseFloat(inputs.monthly)||0
  const years = parseInt(inputs.years)||10
  const annualReturn = parseFloat(inputs.annualReturn)||10
  const initialInvestment = parseFloat(inputs.initialInvestment)||0
  if(monthly<=0) throw new Error("Enter monthly investment amount.")
  const r = annualReturn/100/12
  const n = years*12
  const fvMonthly = monthly*((Math.pow(1+r,n)-1)/r)
  const fvInitial = initialInvestment*Math.pow(1+r,n)
  const totalFV = fvMonthly+fvInitial
  const totalInvested = monthly*n+initialInvestment
  const totalGains = totalFV-totalInvested
  const roi = (totalGains/totalInvested)*100
  return {
    value:"$"+totalFV.toLocaleString("en-US",{maximumFractionDigits:0}),
    gaugeValue:Math.min(roi,200)/2,
    breakdown:["Monthly investment: $"+monthly,"Years: "+years,"Annual return: "+annualReturn+"%","Total invested: $"+totalInvested.toLocaleString("en-US",{maximumFractionDigits:0}),"Investment gains: $"+totalGains.toLocaleString("en-US",{maximumFractionDigits:0}),"Final portfolio: $"+totalFV.toLocaleString("en-US",{maximumFractionDigits:0}),"ROI: "+roi.toFixed(1)+"%"],
    stats:[
      {label:"Final Portfolio",value:"$"+totalFV.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Total Invested",value:"$"+totalInvested.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Investment Gains",value:"$"+totalGains.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Total ROI",value:roi.toFixed(1)+"%"},
    ]
  }
""",
  """{id:"monthly",label:"Monthly Investment",type:"number",placeholder:"500",min:0,unit:"$",defaultValue:500},
            {id:"years",label:"Investment Duration",type:"number",placeholder:"10",min:1,max:50,unit:"years",defaultValue:10},
            {id:"annualReturn",label:"Expected Annual Return",type:"number",placeholder:"10",min:0,max:30,step:0.5,unit:"%",defaultValue:10},
            {id:"initialInvestment",label:"Initial Lump Sum (optional)",type:"number",placeholder:"0",min:0,unit:"$",defaultValue:0}""",
  [("Under 50%","#f59e0b",0,25),("50-100% ROI","#3b82f6",25,50),("100-200% ROI","#22c55e",50,75),("200%+ ROI","#22c55e",75,100)],
  "% ROI (of 200%)","100",
  [("What is dollar-cost averaging?","DCA means investing a fixed dollar amount at regular intervals (e.g., $500/month) regardless of price. When prices are high, you buy fewer shares. When prices are low, you buy more. Over time, this averages out your cost per share and removes the pressure of timing the market."),
   ("Does DCA outperform lump sum investing?","Studies show lump sum investing outperforms DCA about 2/3 of the time in rising markets — because money is invested sooner and earns more returns. However, DCA is psychologically easier, reduces timing risk, and is often the only practical option (you invest as you earn). Both beat not investing."),
   ("What is the S&P 500 average annual return for DCA?","Historical S&P 500 return: ~10% nominal, ~7% inflation-adjusted per year. Some years are down 30%, some up 30%. DCA into index funds over long periods has historically produced strong results because you buy more shares during downturns. Always use diversified index funds for DCA."),
   ("How often should I invest with DCA?","Monthly aligns with most paychecks and is most practical. Bi-weekly or weekly DCA statistically produces slightly lower average cost but the difference is small. Automate it — set up automatic investment on payday so the money is invested before you can spend it."),
   ("What are the best DCA investments?","Broad index funds work best for DCA: S&P 500 index (like VFIAX or VOO), total market index (like VTI), international index (like VXUS). Individual stocks add company-specific risk. Target-date funds simplify it further. Low expense ratios (under 0.1%) matter more over long time horizons.")],
  [("Investment Calculator","/calculators/investment-calculator"),("Compound Interest Calculator","/calculators/compound-interest-calculator"),("Retirement Calculator","/calculators/retirement-calculator"),("Stock Profit Calculator","/calculators/stock-profit-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">$500/Month at 10% Annual Return</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700 border-b border-blue-200"><th class="text-left pb-1">Years</th><th class="text-right pb-1">Invested</th><th class="text-right pb-1">Value</th></tr></thead>
            <tbody class="text-blue-900">
              {[["5","$30k","$39k"],["10","$60k","$103k"],["20","$120k","$382k"],["30","$180k","$1.13M"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right">{r[1]}</td><td class="text-right font-medium">{r[2]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">DCA in a Volatile Market</h2>
        <p class="text-xs text-gray-600 mb-3">Investing $1,000/month into a volatile fund:</p>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Month</th><th class="text-right p-2 text-xs font-semibold">Price</th><th class="text-right p-2 text-xs font-semibold">Shares Bought</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["1","$100","10.0"],["2","$80","12.5"],["3","$60","16.7"],["4","$100","10.0"],["5","$120","8.3"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right font-medium">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
        <p class="text-xs text-gray-500 mt-1">Average cost: $85.11 vs avg price: $92. DCA wins in volatility.</p>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">DCA Best Practices</h2>
        <div class="space-y-2">
          {["Automate — set recurring investments and do not watch the market daily","Stay consistent during downturns — they are when DCA works best (buy more shares)","Use tax-advantaged accounts: 401(k), IRA before taxable brokerage","Low-cost index funds over individual stocks for most investors","Increase contributions when income rises — a small % raises can compound significantly","Do not stop during crashes — the recovery is where you earn the most"].map(t => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{t}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Final Portfolio Value","Calculate your DCA investment returns over time")

# ── DEBT TO INCOME ──────────────────────────────────────────────────────────
w("debt-to-income","Debt-to-Income Ratio Calculator","Financial","financial",
  "Debt-to-Income Ratio Calculator: DTI for Mortgage Approval",
  "Calculate your debt-to-income ratio for mortgage qualification. Know your front-end and back-end DTI. Free DTI calculator.",
  """
  const grossIncome = parseFloat(inputs.grossIncome)||0
  const mortgage = parseFloat(inputs.mortgage)||0
  const carLoan = parseFloat(inputs.carLoan)||0
  const studentLoan = parseFloat(inputs.studentLoan)||0
  const creditCards = parseFloat(inputs.creditCards)||0
  const otherDebt = parseFloat(inputs.otherDebt)||0
  if(grossIncome<=0) throw new Error("Enter gross monthly income.")
  const housingDebt = mortgage
  const totalDebt = mortgage+carLoan+studentLoan+creditCards+otherDebt
  const frontEnd = (housingDebt/grossIncome)*100
  const backEnd = (totalDebt/grossIncome)*100
  let status = backEnd<=36?"Excellent":backEnd<=43?"Good — mortgage likely":backEnd<=50?"Borderline":"Too High for mortgage"
  return {
    value:"DTI: "+backEnd.toFixed(1)+"%",
    gaugeValue:Math.min(backEnd,60)/60*100,
    breakdown:["Gross monthly income: $"+grossIncome,"Housing debt: $"+housingDebt+" (front-end DTI: "+frontEnd.toFixed(1)+"%)","Total monthly debt: $"+totalDebt,"Back-end DTI: "+backEnd.toFixed(1)+"%","Status: "+status],
    stats:[
      {label:"Back-End DTI",value:backEnd.toFixed(1)+"%"},
      {label:"Front-End DTI",value:frontEnd.toFixed(1)+"%"},
      {label:"Total Monthly Debt",value:"$"+totalDebt},
      {label:"Mortgage Status",value:status.split(" ")[0]},
    ]
  }
""",
  """{id:"grossIncome",label:"Gross Monthly Income",type:"number",placeholder:"6000",min:0,unit:"$",defaultValue:6000},
            {id:"mortgage",label:"Housing Payment (PITI)",type:"number",placeholder:"1800",min:0,unit:"$",defaultValue:1800},
            {id:"carLoan",label:"Car Loan Payment",type:"number",placeholder:"400",min:0,unit:"$",defaultValue:400},
            {id:"studentLoan",label:"Student Loan Payment",type:"number",placeholder:"300",min:0,unit:"$",defaultValue:300},
            {id:"creditCards",label:"Minimum Credit Card Payments",type:"number",placeholder:"100",min:0,unit:"$",defaultValue:100},
            {id:"otherDebt",label:"Other Monthly Debt",type:"number",placeholder:"0",min:0,unit:"$",defaultValue:0}""",
  [("Excellent <36%","#22c55e",0,60),("Good 36-43%","#3b82f6",60,72),("Borderline 43-50%","#f59e0b",72,83),("Too High 50%+","#ef4444",83,100)],
  "% DTI (of 60%)","100",
  [("What is debt-to-income ratio?","DTI = Total monthly debt payments / Gross monthly income. Lenders use it to assess your ability to manage monthly payments. Front-end DTI includes only housing costs. Back-end DTI includes all debt. For mortgage approval, most lenders focus on back-end DTI."),
   ("What DTI do I need for a mortgage?","Conventional loans: ideally under 36%, maximum 45% (some up to 50% with strong compensating factors). FHA loans: maximum 43% (sometimes up to 57% with strong credit and reserves). VA loans: no official limit, but 41% is a benchmark. Lower is always better for getting approved and getting good rates."),
   ("What is front-end vs back-end DTI?","Front-end (housing ratio): just your PITI (Principal, Interest, Taxes, Insurance) divided by gross income. Most lenders want this under 28%. Back-end (total DTI): all monthly debt including housing, car loans, student loans, minimum credit card payments. Keep under 36-43%."),
   ("How can I lower my DTI?","Two approaches: reduce debt or increase income. Pay off small debts first to eliminate minimum payments. Pay down credit cards to lower minimums. Refinance student loans for lower payments. Consider a co-borrower with income. Increase income through raises, second job, or side income. Avoid taking on new debt before applying."),
   ("Does DTI affect my mortgage interest rate?","DTI does not directly set rates, but indirectly affects them. High DTI may push you toward FHA loans vs. conventional (which may have higher costs). Very high DTI can result in denial regardless of credit score. Lenders price risk holistically: DTI + credit score + down payment + reserves all factor in.")],
  [("Mortgage Calculator","/calculators/mortgage-calculator"),("Budget Calculator","/calculators/budget-calculator"),("Debt Payoff Calculator","/calculators/debt-payoff-calculator"),("Net Worth Calculator","/calculators/net-worth-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">DTI Guidelines by Loan Type</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[["Conventional","36% ideal / 45% max"],["FHA","43% / 57% with factors"],["VA Loan","41% benchmark"],["USDA","41% benchmark"],["Jumbo","36-43% typical"]].map(([t,d]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span class="font-medium">{t}</span><span>{d}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">DTI Benchmarks</h2>
        <div class="space-y-2">
          {[{range:"Under 20%",status:"Excellent",desc:"Very low debt load, strong financial position"},
            {range:"20–35%",status:"Good",desc:"Manageable debt, easy mortgage qualification"},
            {range:"36–43%",status:"Acceptable",desc:"May need to shop lenders for best rates"},
            {range:"44–50%",status:"High",desc:"Borderline — may need FHA or compensating factors"},
            {range:"Over 50%",status:"Too High",desc:"Most lenders will decline — reduce debt first"},
          ].map(d => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="flex justify-between items-start">
                <span class="font-semibold text-xs text-gray-800">{d.range}</span>
                <span class="text-xs font-medium text-blue-600">{d.status}</span>
              </div>
              <div class="text-xs text-gray-600 mt-0.5">{d.desc}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">What Counts as Debt for DTI?</h2>
        <div class="grid grid-cols-2 gap-4">
          <div class="bg-red-50 rounded-xl p-3">
            <div class="font-bold text-red-800 text-xs mb-2">INCLUDED in DTI</div>
            <ul class="text-xs text-red-700 space-y-1">
              <li>Mortgage / rent</li>
              <li>Car loans</li>
              <li>Student loans</li>
              <li>Credit card minimums</li>
              <li>Personal loans</li>
              <li>Child support / alimony</li>
            </ul>
          </div>
          <div class="bg-green-50 rounded-xl p-3">
            <div class="font-bold text-green-800 text-xs mb-2">NOT in DTI</div>
            <ul class="text-xs text-green-700 space-y-1">
              <li>Utilities</li>
              <li>Groceries</li>
              <li>Insurance</li>
              <li>Cell phone bill</li>
              <li>Subscriptions</li>
              <li>Variable expenses</li>
            </ul>
          </div>
        </div>
      </div>
    </div>""",
  "Debt-to-Income Ratio","Calculate your DTI for mortgage qualification")

# ── DIVIDEND ─────────────────────────────────────────────────────────────────
w("dividend","Dividend Calculator","Financial","financial",
  "Dividend Calculator: Dividend Income & DRIP Growth",
  "Calculate dividend income, DRIP (dividend reinvestment) growth, and yield on cost over time. Free dividend calculator.",
  """
  const shares = parseFloat(inputs.shares)||0
  const pricePerShare = parseFloat(inputs.pricePerShare)||0
  const annualDividend = parseFloat(inputs.annualDividend)||0
  const growthRate = parseFloat(inputs.growthRate)||5
  const years = parseInt(inputs.years)||10
  const drip = inputs.drip!=="false"
  if(shares<=0||pricePerShare<=0) throw new Error("Enter shares and price.")
  const investment = shares*pricePerShare
  const yield_ = (annualDividend/pricePerShare)*100
  let currentShares=shares, totalDiv=0, currentDiv=annualDividend
  for(let y=0;y<years;y++){
    const annualTotal=currentShares*currentDiv
    totalDiv+=annualTotal
    if(drip){ currentShares+=annualTotal/pricePerShare }
    currentDiv*=(1+growthRate/100)
  }
  const finalIncome = currentShares*currentDiv
  return {
    value:"$"+totalDiv.toLocaleString("en-US",{maximumFractionDigits:0})+" total",
    gaugeValue:Math.min(yield_*5,100),
    breakdown:["Initial investment: $"+investment.toLocaleString("en-US",{maximumFractionDigits:0}),"Dividend yield: "+yield_.toFixed(2)+"%","Annual income (yr 1): $"+(shares*annualDividend).toFixed(2),"Total dividends over "+years+"yr: $"+totalDiv.toLocaleString("en-US",{maximumFractionDigits:0}),"Annual income at end: $"+finalIncome.toLocaleString("en-US",{maximumFractionDigits:0})],
    stats:[
      {label:"Dividend Yield",value:yield_.toFixed(2)+"%"},
      {label:"Year 1 Income",value:"$"+(shares*annualDividend).toFixed(0)},
      {label:years+"yr Total Dividends",value:"$"+totalDiv.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Annual Income at End",value:"$"+finalIncome.toFixed(0)},
    ]
  }
""",
  """{id:"shares",label:"Number of Shares",type:"number",placeholder:"100",min:0,defaultValue:100},
            {id:"pricePerShare",label:"Price Per Share",type:"number",placeholder:"50",min:0,unit:"$",defaultValue:50},
            {id:"annualDividend",label:"Annual Dividend Per Share",type:"number",placeholder:"2",min:0,unit:"$",step:0.01,defaultValue:2},
            {id:"growthRate",label:"Dividend Growth Rate",type:"number",placeholder:"5",min:0,max:30,step:0.5,unit:"%",defaultValue:5},
            {id:"years",label:"Investment Horizon",type:"number",placeholder:"10",min:1,max:50,unit:"years",defaultValue:10},
            {id:"drip",label:"DRIP (Reinvest Dividends)?",type:"select",options:[{value:"true",label:"Yes — reinvest dividends"},{value:"false",label:"No — take as cash"}],defaultValue:"true"}""",
  [("Low yield <2%","#ef4444",0,10),("Moderate 2-3%","#f59e0b",10,15),("Good 3-5%","#3b82f6",15,25),("High yield 5%+","#22c55e",25,100)],
  "% yield (×5)","100",
  [("What is a good dividend yield?","2-4% is typical for quality dividend stocks. Over 5% may indicate risk (the price dropped, inflating the yield — investigate why). Under 2% but growing fast can be better than 5% with no growth. Focus on dividend growth rate and payout ratio as much as current yield."),
   ("What is DRIP and why does it matter?","DRIP = Dividend Reinvestment Plan. Instead of receiving cash, dividends automatically buy more shares. Over decades, this compounding accelerates wealth dramatically. A $10,000 investment with 3% yield, 5% dividend growth, and DRIP over 30 years generates far more than taking dividends as cash."),
   ("What is payout ratio and why does it matter?","Payout ratio = Dividends paid / Net income. Under 50%: sustainable, room to grow. 50-75%: moderate, still usually safe. Over 75-80%: may be unsustainable. Over 100%: the company is paying more than it earns — dividend cut likely. Always check payout ratio before buying dividend stocks."),
   ("What is yield on cost?","Yield on cost (YOC) = Current annual dividend / Original purchase price. If you bought a stock at $20/share and it now pays $2/year, your YOC is 10% even if current yield is only 3%. Long-term dividend growth investing is powerful because YOC compounds over time."),
   ("What are the best dividend-paying investments?","Individual dividend stocks: reits, utilities, consumer staples, financials with long dividend history. Dividend ETFs: VYM (Vanguard High Dividend), SCHD (Schwab Dividend), NOBL (Dividend Aristocrats). REITs offer high yields but pay as ordinary income. Dividend growth > high current yield for long-term investors.")],
  [("Investment Calculator","/calculators/investment-calculator"),("Stock Profit Calculator","/calculators/stock-profit-calculator"),("DCA Calculator","/calculators/dca-calculator"),("Compound Interest Calculator","/calculators/compound-interest-calculator")],
  """        <div class="bg-green-50 border border-green-200 rounded-xl p-5">
          <h3 class="font-bold text-green-900 mb-3">DRIP Power: 30-Year Example</h3>
          <p class="text-xs text-green-800 mb-2">$10,000 invested, 3% yield, 5% dividend growth:</p>
          <div class="space-y-1 text-xs text-green-800">
            {[["Without DRIP","~$17,000 total dividends"],["With DRIP","~$29,000 total dividends"],["Difference","+$12,000 (70% more)"]].map(([k,v]) => (
              <div class="flex justify-between border-b border-green-100 pb-0.5"><span>{k}</span><span class="font-medium">{v}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Dividend Safety Checklist</h2>
        <div class="space-y-2">
          {[
            {factor:"Payout Ratio",safe:"Under 60%",risky:"Over 80%"},
            {factor:"Dividend Growth",safe:"5+ consecutive years",risky:"Flat or cut history"},
            {factor:"Free Cash Flow",safe:"Covers dividend 1.5x+",risky:"Barely covers payout"},
            {factor:"Debt Level",safe:"Manageable debt/EBITDA",risky:"High leverage"},
            {factor:"Business Model",safe:"Recurring revenue",risky:"Cyclical or declining"},
          ].map(f => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-xs text-gray-800 mb-1">{f.factor}</div>
              <div class="flex gap-4 text-xs">
                <span class="text-green-700">✓ {f.safe}</span>
                <span class="text-red-600">✗ {f.risky}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Dividend Aristocrats — 25+ Year Growers</h2>
        <p class="text-xs text-gray-600 mb-2">Companies that have increased dividends for 25+ consecutive years (S&P 500 Dividend Aristocrats index):</p>
        <div class="bg-blue-50 rounded-xl p-4 text-xs text-blue-800 space-y-1">
          <div>Examples: Coca-Cola, Johnson & Johnson, Procter & Gamble, 3M, Colgate-Palmolive, McDonald&apos;s, Walmart</div>
          <div class="mt-2">Track via ETF: <strong>NOBL</strong> (ProShares S&P 500 Dividend Aristocrats)</div>
          <div class="mt-1">65 qualifying companies as of 2025</div>
        </div>
      </div>
    </div>""",
  "Total Dividend Income","Calculate dividend income and DRIP growth over time")

# ── DOWN PAYMENT ─────────────────────────────────────────────────────────────
w("down-payment","Down Payment Calculator","Financial","financial",
  "Down Payment Calculator: How Much to Save for a Home",
  "Calculate how much to save monthly to reach your home down payment goal. Includes PMI savings and timeline. Free down payment calculator.",
  """
  const homePrice = parseFloat(inputs.homePrice)||0
  const downPct = parseFloat(inputs.downPct)||20
  const currentSaved = parseFloat(inputs.currentSaved)||0
  const monthlySavings = parseFloat(inputs.monthlySavings)||500
  const returnRate = parseFloat(inputs.returnRate)||4
  if(homePrice<=0) throw new Error("Enter home price.")
  const downPaymentTarget = homePrice*(downPct/100)
  const stillNeeded = Math.max(0,downPaymentTarget-currentSaved)
  const r = returnRate/100/12
  let months=0, balance=currentSaved
  while(balance<downPaymentTarget&&months<600){
    balance=balance*(1+r)+monthlySavings; months++
  }
  const years = Math.floor(months/12), mo = months%12
  const loanAmount = homePrice-downPaymentTarget
  const pmiSavings = downPct>=20?0:loanAmount*0.008/12
  return {
    value:"$"+downPaymentTarget.toLocaleString("en-US",{maximumFractionDigits:0})+" needed",
    gaugeValue:Math.min((currentSaved/downPaymentTarget)*100,100),
    breakdown:["Home price: $"+homePrice.toLocaleString("en-US",{maximumFractionDigits:0}),"Down payment ("+downPct+"%): $"+downPaymentTarget.toLocaleString("en-US",{maximumFractionDigits:0}),"Currently saved: $"+currentSaved,"Time to goal: "+years+"y "+mo+"mo","PMI saved (20% down): $"+pmiSavings.toFixed(0)+"/mo"],
    stats:[
      {label:"Down Payment Goal",value:"$"+downPaymentTarget.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Currently Saved",value:"$"+currentSaved.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Time to Goal",value:years+"y "+mo+"mo"},
      {label:"Monthly PMI (if <20%)",value:"$"+pmiSavings.toFixed(0)},
    ]
  }
""",
  """{id:"homePrice",label:"Target Home Price",type:"number",placeholder:"400000",min:0,unit:"$",defaultValue:400000},
            {id:"downPct",label:"Down Payment Percentage",type:"select",options:[{value:"3",label:"3% (minimum conventional)"},{value:"5",label:"5%"},{value:"10",label:"10%"},{value:"20",label:"20% (no PMI)"},{value:"25",label:"25%"}],defaultValue:"20"},
            {id:"currentSaved",label:"Amount Already Saved",type:"number",placeholder:"10000",min:0,unit:"$",defaultValue:10000},
            {id:"monthlySavings",label:"Monthly Savings",type:"number",placeholder:"800",min:0,unit:"$",defaultValue:800},
            {id:"returnRate",label:"Savings Return Rate",type:"number",placeholder:"4",min:0,max:10,step:0.1,unit:"%",defaultValue:4}""",
  [("Not Started","#ef4444",0,10),("Building","#f59e0b",10,40),("Nearly There","#3b82f6",40,80),("Ready!","#22c55e",80,100)],
  "% funded","100",
  [("How much down payment do I need?","Minimum: 3% for conventional loans (Fannie/Freddie), 3.5% for FHA, 0% for VA and USDA loans. Recommended: 20% to avoid PMI and get the best rates. Reality: most first-time buyers put down 6-12%. A larger down payment means lower monthly payment, no PMI, and less total interest paid."),
   ("Is 20% down required to buy a house?","No. You can buy with as little as 3% down on conventional loans. However, under 20% typically means paying PMI (0.5-1.5% of loan annually). FHA loans require only 3.5% down. The tradeoff: smaller down payment = PMI + higher monthly payment + more total interest over the loan life."),
   ("What else do I need beyond the down payment?","Closing costs: 2-5% of loan amount ($8,000-$20,000 on a $400k home). Moving costs. Initial repairs or furnishings. Emergency fund (you do not want to deplete savings completely for the down payment). Also budget for ongoing homeownership costs: property tax, insurance, HOA, maintenance (~1% of home value/year)."),
   ("Should I use a HYSA or invest my down payment savings?","For timelines under 3 years: high-yield savings account (HYSA) or CDs — you need capital preservation. For 3-5 years: consider conservative bonds or CDs. Over 5 years: a mix of bonds and stocks may be reasonable. Never invest a near-term down payment in volatile assets — markets can drop 30-40% right when you need the money."),
   ("Can I use gift money for a down payment?","Yes, for most loan types. FHA allows 100% gifted down payment. Conventional allows gifts but usually requires some of your own funds for down payments over 20%. You need a gift letter stating the funds are not a loan. VA and USDA also allow gifts. The donor may need to document the source of funds.")],
  [("Mortgage Calculator","/calculators/mortgage-calculator"),("PMI Calculator","/calculators/pmi-calculator"),("House Affordability Calculator","/calculators/house-affordability-calculator"),("Savings Calculator","/calculators/savings-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Down Payment % Comparison</h3>
          <p class="text-xs text-blue-700 mb-2">$400,000 home, 7% rate, 30-yr:</p>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700 border-b border-blue-200"><th class="text-left pb-1">Down %</th><th class="text-right pb-1">Monthly</th><th class="text-right pb-1">PMI</th></tr></thead>
            <tbody class="text-blue-900">
              {[["3% ($12k)","$2,568","+$267"],["10% ($40k)","$2,395","+$200"],["20% ($80k)","$2,129","None"],["25% ($100k)","$1,996","None"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right">{r[1]}</td><td class="text-right">{r[2]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">First-Time Buyer Programs</h2>
        <div class="space-y-3">
          {[
            {prog:"FHA Loan",detail:"3.5% down with 580+ credit score. Government-backed. Lower credit requirements but requires mortgage insurance premium (MIP)."},
            {prog:"Fannie Mae HomeReady",detail:"3% down, income limits apply, homebuyer education required. Good for low-to-moderate income buyers."},
            {prog:"VA Loan",detail:"0% down for eligible veterans and active military. No PMI. Competitive rates. Best deal for those who qualify."},
            {prog:"USDA Loan",detail:"0% down for eligible rural/suburban properties. Income limits apply. Competitive rates."},
            {prog:"State/Local Programs",detail:"Many states offer down payment assistance grants or 0% second mortgages for first-time buyers. Check your state HFA."},
          ].map(p => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-xs text-gray-800 mb-0.5">{p.prog}</div>
              <div class="text-xs text-gray-600">{p.detail}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Full Home Buying Budget</h2>
        <div class="space-y-2">
          {[["Down payment (20%)","$80,000"],["Closing costs (3%)","$12,000"],["Home inspection","$400–800"],["Moving costs","$1,000–5,000"],["Initial repairs","$2,000–10,000"],["Emergency fund (keep!)","$15,000+"],["Total needed","$110,000+"]].map(([item,amount]) => (
            <div class="flex justify-between bg-gray-50 rounded px-3 py-1.5 text-xs">
              <span class="text-gray-700">{item}</span>
              <span class="font-medium">{amount}</span>
            </div>
          ))}
          <p class="text-xs text-gray-500 mt-1">Example for $400,000 home</p>
        </div>
      </div>
    </div>""",
  "Down Payment Goal","Calculate how long to save for your home down payment")

print(f"\nWritten: {written} pages (college-savings, dca, debt-to-income, dividend, down-payment)")
