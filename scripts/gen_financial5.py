#!/usr/bin/env python3
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

# ── MARKUP ───────────────────────────────────────────────────────────────────
w("markup","Markup Calculator","Financial","financial",
  "Markup Calculator: Markup Percentage & Selling Price",
  "Calculate selling price, markup percentage, gross profit margin, and profit. Free markup and margin calculator.",
  """
  const cost = parseFloat(inputs.cost)||0
  const markup = parseFloat(inputs.markup)||0
  if(cost<=0) throw new Error("Enter cost.")
  const sellingPrice = cost*(1+markup/100)
  const profit = sellingPrice-cost
  const margin = (profit/sellingPrice)*100
  return {
    value:"$"+sellingPrice.toFixed(2),
    gaugeValue:Math.min(markup,100),
    breakdown:["Cost: $"+cost.toFixed(2),"Markup: "+markup+"%","Selling price: $"+sellingPrice.toFixed(2),"Gross profit: $"+profit.toFixed(2),"Profit margin: "+margin.toFixed(2)+"%"],
    stats:[
      {label:"Selling Price",value:"$"+sellingPrice.toFixed(2)},
      {label:"Gross Profit",value:"$"+profit.toFixed(2)},
      {label:"Profit Margin",value:margin.toFixed(2)+"%"},
      {label:"Markup %",value:markup+"%"},
    ]
  }
""",
  """{id:"cost",label:"Cost Price",type:"number",placeholder:"50",min:0,unit:"$",step:0.01,defaultValue:50},
            {id:"markup",label:"Markup Percentage",type:"number",placeholder:"40",min:0,unit:"%",step:0.5,defaultValue:40}""",
  [("Low <20%","#ef4444",0,20),("Fair 20-40%","#f59e0b",20,40),("Good 40-60%","#3b82f6",40,60),("High 60%+","#22c55e",60,100)],
  "% markup","100",
  [("What is the difference between markup and margin?","Markup is profit divided by COST. Margin is profit divided by SELLING PRICE. A 50% markup does NOT equal 50% margin. Example: $10 cost, $15 price. Markup = ($5/$10) = 50%. Margin = ($5/$15) = 33.3%. Businesses often confuse these — always clarify which you mean."),
   ("How do I convert markup to margin?","Margin = Markup / (1 + Markup). Example: 50% markup = 50/150 = 33.3% margin. To convert margin to markup: Markup = Margin / (1 - Margin). 33.3% margin = 0.333/0.667 = 50% markup. Use this conversion when comparing prices with suppliers vs. customers."),
   ("What is a good markup percentage?","It varies enormously by industry. Grocery stores: 5-25%. Retail clothing: 50-100%+. Jewelry: 100-300%. Restaurants: 200-400% on food. Software: often infinite (cost of goods is near zero). The right markup depends on: industry norms, competition, customer willingness to pay, and your overhead costs."),
   ("Why is markup different from margin in practice?","When you tell a customer your price includes a 50% margin, they expect $1 to become $1.50 (50% of $1). When a supplier offers a product with 50% markup, they mean cost $1, sell at $1.50. The confusion is real and costly — businesses have lost money quoting the wrong metric to partners."),
   ("How do overhead costs factor into pricing?","Markup must cover not just profit but also overhead: rent, salaries, utilities, marketing, insurance. If overhead is 30% of revenue, you need at least 30% margin (43% markup) just to break even. A common formula: Price = (Cost + Overhead Allocation) / (1 - Desired Profit Margin).")],
  [("Break-Even Calculator","/calculators/break-even-calculator"),("ROI Calculator","/calculators/roi-calculator"),("Discount Calculator","/calculators/discount-calculator"),("Percentage Calculator","/calculators/percentage-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Markup vs Margin Quick Reference</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700 border-b border-blue-200"><th class="text-left pb-1">Markup</th><th class="text-right pb-1">Margin</th></tr></thead>
            <tbody class="text-blue-900">
              {[["10%","9.1%"],["20%","16.7%"],["33%","25%"],["50%","33.3%"],["100%","50%"],["200%","66.7%"]].map(r => (
                <tr class="border-t border-blue-100"><td>{r[0]}</td><td class="text-right">{r[1]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Industry Markup Benchmarks</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Industry</th><th class="text-right p-2 text-xs font-semibold">Typical Markup</th><th class="text-right p-2 text-xs font-semibold">Margin</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Grocery","5–25%","5–20%"],["Retail Clothing","50–100%","33–50%"],["Electronics","5–25%","5–20%"],["Jewelry","100–300%","50–75%"],["Restaurant","200–400%","67–80%"],["Software/SaaS","Very high","70–90%"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right font-medium">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Pricing Formula</h2>
        <div class="bg-gray-50 rounded-xl p-4 font-mono text-xs text-gray-700 space-y-2">
          <div>Selling Price = Cost × (1 + Markup%/100)</div>
          <div>Profit = Selling Price - Cost</div>
          <div>Margin = (Profit / Selling Price) × 100</div>
          <div class="mt-3 font-sans text-gray-600">Example: cost $10, 50% markup</div>
          <div>Price = $10 × 1.50 = $15</div>
          <div>Profit = $15 - $10 = $5</div>
          <div>Margin = ($5 / $15) × 100 = 33.3%</div>
        </div>
      </div>
    </div>""",
  "Selling Price","Calculate selling price, markup percentage, and profit margin")

# ── MORTGAGE POINTS ───────────────────────────────────────────────────────────
w("mortgage-points","Mortgage Points Calculator","Financial","financial",
  "Mortgage Points Calculator: Should You Buy Down Your Rate?",
  "Calculate if buying mortgage discount points makes financial sense. Find your break-even period. Free mortgage points calculator.",
  """
  const loanAmount = parseFloat(inputs.loanAmount)||0
  const currentRate = parseFloat(inputs.currentRate)||7
  const points = parseFloat(inputs.points)||1
  const rateReduction = parseFloat(inputs.rateReduction)||0.25
  if(loanAmount<=0) throw new Error("Enter loan amount.")
  const n=360, r1=currentRate/100/12
  const payment1 = loanAmount*r1*Math.pow(1+r1,n)/(Math.pow(1+r1,n)-1)
  const newRate = currentRate-rateReduction
  const r2 = newRate/100/12
  const payment2 = loanAmount*r2*Math.pow(1+r2,n)/(Math.pow(1+r2,n)-1)
  const pointsCost = loanAmount*(points/100)
  const monthlySavings = payment1-payment2
  const breakEvenMonths = Math.ceil(pointsCost/monthlySavings)
  const breakEvenYears = Math.floor(breakEvenMonths/12)
  const breakEvenMo = breakEvenMonths%12
  const savingsOver30yr = monthlySavings*360-pointsCost
  return {
    value:"Break-even: "+breakEvenYears+"y "+breakEvenMo+"mo",
    gaugeValue:Math.min(breakEvenMonths/360*100,100),
    breakdown:["Points cost: $"+pointsCost.toFixed(0)+" ("+points+" pt)","Rate: "+currentRate+"% → "+newRate+"%","Monthly savings: $"+monthlySavings.toFixed(2),"Break-even: "+breakEvenMonths+" months","30yr net savings: $"+savingsOver30yr.toFixed(0)],
    stats:[
      {label:"Points Cost",value:"$"+pointsCost.toFixed(0)},
      {label:"Monthly Savings",value:"$"+monthlySavings.toFixed(2)},
      {label:"Break-Even",value:breakEvenYears+"y "+breakEvenMo+"mo"},
      {label:"30yr Net Savings",value:"$"+savingsOver30yr.toFixed(0)},
    ]
  }
""",
  """{id:"loanAmount",label:"Loan Amount",type:"number",placeholder:"350000",min:0,unit:"$",defaultValue:350000},
            {id:"currentRate",label:"Current Interest Rate",type:"number",placeholder:"7",min:0,max:15,step:0.1,unit:"%",defaultValue:7},
            {id:"points",label:"Number of Discount Points",type:"number",placeholder:"1",min:0.25,max:4,step:0.25,defaultValue:1},
            {id:"rateReduction",label:"Rate Reduction Per Point",type:"number",placeholder:"0.25",min:0.1,max:0.5,step:0.05,unit:"%",defaultValue:0.25}""",
  [("Quick break-even <3yr","#22c55e",0,10),("Good 3-5yr","#3b82f6",10,17),("Moderate 5-7yr","#f59e0b",17,23),("Long >7yr","#ef4444",23,100)],
  "% of 30yr","100",
  [("What are mortgage discount points?","One discount point costs 1% of the loan amount and typically reduces your interest rate by 0.125-0.25%. On a $350,000 loan, 1 point = $3,500. The rate reduction varies by lender and market conditions. Points are paid at closing and may be tax-deductible as prepaid mortgage interest."),
   ("Should I buy mortgage points?","The key question: how long will you stay in the home? If you sell or refinance before the break-even period, you lose money. If you stay longer, you save money. Rule of thumb: only buy points if you plan to stay in the home for at least 5-7 years AND you have cash for closing costs plus points."),
   ("Are mortgage points tax-deductible?","Yes, for primary residences. Discount points paid on a purchase mortgage are typically fully deductible in the year paid. Points on a refinance must be deducted over the life of the loan (amortized). Consult a tax advisor for your specific situation, as rules can be complex."),
   ("What is the break-even period for points?","Break-even = Points cost / Monthly payment savings. Example: 1 point on $350k loan = $3,500 cost; reduces rate 0.25%, saving $57/month. Break-even = $3,500 / $57 = 61 months (~5.1 years). If you stay longer than 5 years, points pay off. Shorter? Skip them."),
   ("Can I negotiate points with the lender?","Yes. You can often negotiate the rate-to-point relationship. Some lenders offer better rate reductions per point. Get quotes from multiple lenders. You can also ask for lender credits (negative points) to reduce closing costs in exchange for a higher rate — the opposite tradeoff if you plan to move soon.")],
  [("Mortgage Calculator","/calculators/mortgage-calculator"),("Refinance Calculator","/calculators/refinance-calculator"),("APR Calculator","/calculators/apr-calculator"),("House Affordability Calculator","/calculators/house-affordability-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Points Decision Framework</h3>
          <div class="space-y-2 text-xs text-blue-800">
            <div class="font-medium">Buy points if:</div>
            <div>✓ Staying 7+ years in the home</div>
            <div>✓ Have cash beyond closing costs</div>
            <div>✓ Break-even is under 5 years</div>
            <div class="font-medium mt-2">Skip points if:</div>
            <div>✗ May sell or refinance within 5 years</div>
            <div>✗ Need cash for other purposes</div>
          </div>
        </div>""",
  """    <div class="mt-10">
      <h2 class="text-xl font-bold text-gray-900 mb-4">$350,000 Loan — Points vs Rate Savings</h2>
      <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
        <thead class="bg-gray-50"><tr><th class="text-left p-3 text-xs font-semibold">Points Paid</th><th class="text-right p-3 text-xs font-semibold">Cost</th><th class="text-right p-3 text-xs font-semibold">Rate Reduction</th><th class="text-right p-3 text-xs font-semibold">Monthly Savings</th><th class="text-right p-3 text-xs font-semibold">Break-Even</th></tr></thead>
        <tbody class="divide-y divide-gray-100">
          {[["0 points","$0","0%","$0","N/A"],["0.5 points","$1,750","0.125%","$28","62 months"],["1 point","$3,500","0.25%","$57","61 months"],["2 points","$7,000","0.5%","$114","61 months"],["3 points","$10,500","0.75%","$170","62 months"]].map(r => (
            <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td><td class="p-2 text-xs text-right text-green-600">{r[3]}</td><td class="p-2 text-xs text-right font-medium">{r[4]}</td></tr>
          ))}
        </tbody>
      </table>
      <p class="text-xs text-gray-500 mt-2">Assumes 0.25% rate reduction per point. Actual reductions vary by lender and market conditions.</p>
    </div>""",
  "Break-Even Period","Find out if buying mortgage discount points makes financial sense")

# ── NPV ──────────────────────────────────────────────────────────────────────
w("npv","NPV Calculator","Financial","financial",
  "NPV Calculator: Net Present Value of Cash Flows",
  "Calculate the net present value (NPV) and IRR of an investment or project. Free NPV and IRR calculator.",
  """
  const rate = parseFloat(inputs.rate)||8
  const initial = parseFloat(inputs.initial)||0
  const cashFlows = (inputs.cashFlows||"").split(/[,\\n]+/).map(s=>parseFloat(s.trim())).filter(n=>!isNaN(n))
  if(cashFlows.length===0) throw new Error("Enter cash flows (comma or newline separated).")
  const r = rate/100
  let npv = -initial
  for(let i=0;i<cashFlows.length;i++){
    npv += cashFlows[i]/Math.pow(1+r,i+1)
  }
  const totalCash = cashFlows.reduce((a,b)=>a+b,0)
  let irr=0.1, step=0.01
  for(let attempt=0;attempt<2000;attempt++){
    let npvTest=-initial
    for(let i=0;i<cashFlows.length;i++) npvTest+=cashFlows[i]/Math.pow(1+irr,i+1)
    if(Math.abs(npvTest)<1) break
    if(npvTest>0) irr+=step; else irr-=step; step*=0.99
  }
  return {
    value:"NPV: $"+npv.toLocaleString("en-US",{maximumFractionDigits:0}),
    gaugeValue:npv>0?Math.min((npv/initial)*100,100):0,
    breakdown:["Initial investment: $"+initial,"Discount rate: "+rate+"%","Cash flows: "+cashFlows.length+" periods","Total undiscounted: $"+totalCash.toLocaleString("en-US",{maximumFractionDigits:0}),"NPV: $"+npv.toLocaleString("en-US",{maximumFractionDigits:0}),"IRR: "+(irr*100).toFixed(2)+"%"],
    stats:[
      {label:"NPV",value:"$"+npv.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"IRR",value:(irr*100).toFixed(2)+"%"},
      {label:"Total Cash Flows",value:"$"+totalCash.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Decision",value:npv>0?"Invest":"Reject"},
    ]
  }
""",
  """{id:"initial",label:"Initial Investment",type:"number",placeholder:"100000",min:0,unit:"$",defaultValue:100000},
            {id:"rate",label:"Discount Rate (WACC or required return)",type:"number",placeholder:"8",min:0,max:50,step:0.5,unit:"%",defaultValue:8},
            {id:"cashFlows",label:"Annual Cash Flows (comma-separated)",type:"text",placeholder:"20000, 30000, 40000, 40000, 30000",defaultValue:"20000, 30000, 40000, 40000, 30000"}""",
  [("Negative NPV","#ef4444",0,5),("Marginal NPV","#f59e0b",5,20),("Positive NPV","#3b82f6",20,60),("Strong NPV","#22c55e",60,100)],
  "% return","100",
  [("What is NPV?","Net Present Value (NPV) = Present value of all future cash flows minus the initial investment. Positive NPV means the investment creates value above the required return. Negative NPV means it destroys value. NPV is the gold standard for capital budgeting decisions."),
   ("What discount rate should I use for NPV?","Use your WACC (Weighted Average Cost of Capital) for corporate projects, or your required rate of return for personal investments. If your business requires 12% return on investments, use 12%. Higher discount rates make future cash flows worth less — important for long-term projects."),
   ("What is IRR and how is it related to NPV?","IRR (Internal Rate of Return) is the discount rate at which NPV = 0. If IRR > your cost of capital/required return, the investment is worthwhile. If IRR < required return, reject it. NPV and IRR usually agree on accept/reject decisions but can conflict when comparing mutually exclusive projects (use NPV in that case)."),
   ("When should I choose NPV over IRR?","Always trust NPV when they conflict. IRR can give misleading results for: non-conventional cash flows (multiple sign changes), mutually exclusive projects of different sizes or timing, projects with interim cash flows that must be reinvested. NPV directly measures value creation in dollar terms."),
   ("What are the limitations of NPV?","NPV requires accurately estimating discount rate and future cash flows — both are uncertain. It does not account for real options (ability to expand or abandon). It can favor larger projects over smaller, more efficient ones. It assumes cash flows are reinvested at the discount rate. Despite limitations, NPV remains the most rigorous investment metric.")],
  [("ROI Calculator","/calculators/roi-calculator"),("IRR Calculator","/calculators/investment-calculator"),("Payback Period Calculator","/calculators/payback-period-calculator"),("Annuity Calculator","/calculators/annuity-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">NPV Decision Rule</h3>
          <div class="space-y-2 text-xs text-blue-800">
            <div class="bg-green-100 rounded p-2"><strong>NPV &gt; 0:</strong> Accept — investment creates value above the required return</div>
            <div class="bg-red-100 rounded p-2"><strong>NPV &lt; 0:</strong> Reject — investment destroys value relative to the required return</div>
            <div class="bg-yellow-100 rounded p-2"><strong>NPV = 0:</strong> Indifferent — earns exactly the required return</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">NPV Example Calculation</h2>
        <p class="text-xs text-gray-600 mb-3">$100,000 investment, 8% rate, 5 years of cash flows:</p>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Year</th><th class="text-right p-2 text-xs font-semibold">Cash Flow</th><th class="text-right p-2 text-xs font-semibold">PV Factor</th><th class="text-right p-2 text-xs font-semibold">Present Value</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["0","−$100,000","1.000","−$100,000"],["1","$20,000","0.926","$18,519"],["2","$30,000","0.857","$25,720"],["3","$40,000","0.794","$31,752"],["4","$40,000","0.735","$29,400"],["5","$30,000","0.681","$20,420"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td><td class="p-2 text-xs text-right font-medium">{r[3]}</td></tr>
            ))}
          </tbody>
        </table>
        <p class="text-xs text-gray-700 font-semibold mt-2">NPV = $25,811 (positive — invest!)</p>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">NPV vs Payback Period vs ROI</h2>
        <div class="space-y-3">
          {[
            {m:"NPV",pros:"Measures actual $ value created, accounts for time value",cons:"Requires accurate discount rate, harder to compare projects of diff size"},
            {m:"IRR",pros:"Intuitive % return, easy to compare to cost of capital",cons:"Can mislead with unconventional flows, multiple IRRs possible"},
            {m:"Payback Period",pros:"Simple, quick liquidity test",cons:"Ignores time value of money, ignores cash flows after payback"},
            {m:"ROI",pros:"Simple ratio, easy to compare",cons:"Ignores timing of cash flows, can be manipulated"},
          ].map(m => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-xs text-gray-800">{m.m}</div>
              <div class="text-xs text-green-700">+ {m.pros}</div>
              <div class="text-xs text-red-600">- {m.cons}</div>
            </div>
          ))}
        </div>
      </div>
    </div>""",
  "NPV","Calculate net present value and IRR of any investment")

# ── PAYBACK PERIOD ────────────────────────────────────────────────────────────
w("payback-period","Payback Period Calculator","Financial","financial",
  "Payback Period Calculator: Investment Break-Even Timeline",
  "Calculate how long until your investment pays back its initial cost. Includes discounted payback period. Free payback period calculator.",
  """
  const initial = parseFloat(inputs.initial)||0
  const cashFlow = parseFloat(inputs.cashFlow)||0
  const rate = parseFloat(inputs.rate)||0
  if(initial<=0||cashFlow<=0) throw new Error("Enter investment amount and annual cash flow.")
  const simplePayback = initial/cashFlow
  const simpleYears = Math.floor(simplePayback)
  const simpleMo = Math.round((simplePayback-simpleYears)*12)
  let discountedPayback=0, balance=initial, year=0
  while(balance>0&&year<100){
    year++
    const discountedFlow = cashFlow/Math.pow(1+(rate||0)/100,year)
    balance-=discountedFlow
    if(balance<=0){
      discountedPayback=year+(balance/(cashFlow/Math.pow(1+(rate||0)/100,year)))
      break
    }
  }
  const roi5 = (cashFlow*5-initial)/initial*100
  return {
    value:simpleYears+"y "+simpleMo+"mo payback",
    gaugeValue:Math.min(100/simplePayback*10,100),
    breakdown:["Initial investment: $"+initial.toLocaleString("en-US",{maximumFractionDigits:0}),"Annual cash flow: $"+cashFlow.toLocaleString("en-US",{maximumFractionDigits:0}),"Simple payback: "+simpleYears+"y "+simpleMo+"mo","Discounted payback: "+(rate>0?discountedPayback.toFixed(1)+" years":"N/A (rate = 0)"),"5-year ROI: "+roi5.toFixed(1)+"%"],
    stats:[
      {label:"Simple Payback",value:simpleYears+"y "+simpleMo+"mo"},
      {label:"Annual Cash Flow",value:"$"+cashFlow.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"5-Year ROI",value:roi5.toFixed(1)+"%"},
      {label:"Discounted Payback",value:rate>0?discountedPayback.toFixed(1)+" yrs":"N/A"},
    ]
  }
""",
  """{id:"initial",label:"Initial Investment",type:"number",placeholder:"50000",min:0,unit:"$",defaultValue:50000},
            {id:"cashFlow",label:"Annual Cash Flow / Savings",type:"number",placeholder:"15000",min:0,unit:"$",defaultValue:15000},
            {id:"rate",label:"Discount Rate (for discounted payback)",type:"number",placeholder:"8",min:0,max:30,step:0.5,unit:"%",defaultValue:8}""",
  [("Under 2yr","#22c55e",0,10),("2-5 years","#3b82f6",10,50),("5-10 years","#f59e0b",50,100)],
  "% of 10yr","100",
  [("What is the payback period?","The payback period is how long it takes for an investment to recover its initial cost from generated cash flows. Simple payback = Initial Investment / Annual Cash Flow. A 3-year payback means the investment pays for itself in 3 years. After that, all cash flows are profit."),
   ("What is a good payback period?","It depends on industry and investment type. Solar panels: 6-10 years (with 25yr lifespan = great). Equipment: typically under 3-5 years. Real estate: 5-15 years common. Software: often 1-3 years. The shorter the better, but context matters — a 10-year payback is fine if the asset lasts 30 years."),
   ("What is discounted payback period?","Discounted payback accounts for the time value of money — future cash flows are worth less than present ones. Divide each future cash flow by (1 + rate)^year before tallying. The discounted payback period is always longer than simple payback, giving a more realistic picture of true break-even."),
   ("What are the limitations of payback period?","It ignores cash flows after the payback period (a 3-year payback project that generates $1 billion afterward looks the same as one that generates $0 after). It ignores the time value of money (unless using discounted version). It does not measure profitability, only liquidity/speed of recovery."),
   ("Should I use payback period or NPV?","Use both: NPV measures value creation (the right answer for investment decisions); payback period measures liquidity risk (how quickly can you recover the capital). A project with 8-year payback but hugely positive NPV is still worth doing. Short payback is especially important for small businesses with limited capital.")],
  [("NPV Calculator","/calculators/npv-calculator"),("ROI Calculator","/calculators/roi-calculator"),("Break-Even Calculator","/calculators/break-even-calculator"),("Investment Calculator","/calculators/investment-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Payback Formula</h3>
          <div class="font-mono text-xs text-blue-800 bg-blue-100 rounded p-2 mb-2">Payback = Investment ÷ Annual Cash Flow</div>
          <div class="text-xs text-blue-700">Example: $50,000 investment, $15,000/year cash flows<br/>Payback = $50,000 ÷ $15,000 = 3.33 years (3y 4mo)</div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Simple vs Discounted Payback</h2>
        <p class="text-xs text-gray-600 mb-3">$50,000 investment, $15,000/year, 8% rate:</p>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Year</th><th class="text-right p-2 text-xs font-semibold">Simple Balance</th><th class="text-right p-2 text-xs font-semibold">Discounted Balance</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["0","−$50,000","−$50,000"],["1","−$35,000","−$36,111"],["2","−$20,000","−$23,079"],["3","−$5,000","−$10,987"],["4","$10,000","$0,120"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
        <p class="text-xs text-gray-500 mt-1">Simple: 3.33yr | Discounted: ~3.85yr</p>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Investment Evaluation Framework</h2>
        <div class="space-y-3">
          {[
            {q:"Will it pay back quickly?",tool:"Payback Period",use:"Liquidity assessment"},
            {q:"Does it create value?",tool:"NPV",use:"Value creation"},
            {q:"What is the % return?",tool:"IRR or ROI",use:"Profitability"},
            {q:"Is revenue > costs?",tool:"Break-Even",use:"Viability"},
            {q:"Worth it vs. alternatives?",tool:"Compare NPVs",use:"Selection"},
          ].map(f => (
            <div class="flex gap-3 bg-gray-50 rounded-lg p-2.5">
              <div class="flex-1 text-xs text-gray-600">{f.q}</div>
              <div class="text-xs font-medium text-blue-700 text-right">{f.tool}</div>
            </div>
          ))}
        </div>
      </div>
    </div>""",
  "Payback Period","Calculate how quickly your investment pays back its initial cost")

# ── PAYCHECK ──────────────────────────────────────────────────────────────────
w("paycheck","Paycheck Calculator","Financial","financial",
  "Paycheck Calculator: Take-Home Pay After Taxes",
  "Calculate your take-home pay after federal taxes, Social Security, Medicare, and state taxes. Free paycheck calculator.",
  """
  const gross = parseFloat(inputs.gross)||0
  const freq = inputs.freq||"biweekly"
  const filing = inputs.filing||"single"
  const allowances = parseInt(inputs.allowances)||1
  const stateRate = parseFloat(inputs.stateRate)||5
  const k401 = parseFloat(inputs.k401)||0
  if(gross<=0) throw new Error("Enter gross pay.")
  const perPaycheck = gross
  const annual = freq==="weekly"?gross*52:freq==="biweekly"?gross*26:freq==="semimonthly"?gross*24:gross*12
  const pre401k = perPaycheck*(k401/100)
  const taxableGross = perPaycheck-pre401k
  const annualTaxable = annual-annual*(k401/100)
  const stdDed = filing==="married"?30000:15000
  const federalTaxable = Math.max(0,annualTaxable-stdDed)
  const brackets = filing==="married"
    ?[[0,23200,0.10],[23200,94300,0.12],[94300,201050,0.22],[201050,383900,0.24],[383900,487450,0.32],[487450,731200,0.35],[731200,Infinity,0.37]]
    :[[0,11600,0.10],[11600,47150,0.12],[47150,100525,0.22],[100525,191950,0.24],[191950,243725,0.32],[243725,609350,0.35],[609350,Infinity,0.37]]
  let annualFed=0, rem=federalTaxable
  for(const [lo,hi,r] of brackets){
    if(rem<=0) break
    const t=Math.min(rem,(hi===Infinity?rem:hi)-lo)
    annualFed+=t*r; rem-=t
  }
  const periods = freq==="weekly"?52:freq==="biweekly"?26:freq==="semimonthly"?24:12
  const federalWithholding = annualFed/periods
  const fica = taxableGross*0.0765
  const medicare = taxableGross*0.0145
  const socialSecurity = taxableGross*0.062
  const state = taxableGross*(stateRate/100)
  const totalDeductions = pre401k+federalWithholding+fica+state
  const netPay = perPaycheck-totalDeductions
  return {
    value:"$"+netPay.toFixed(2)+"/paycheck",
    gaugeValue:(netPay/perPaycheck)*100,
    breakdown:["Gross pay: $"+perPaycheck.toFixed(2),"Federal tax: $"+federalWithholding.toFixed(2),"Social Security: $"+socialSecurity.toFixed(2),"Medicare: $"+medicare.toFixed(2),"State tax: $"+state.toFixed(2),"401k contrib: $"+pre401k.toFixed(2),"Take-home: $"+netPay.toFixed(2)],
    stats:[
      {label:"Take-Home Pay",value:"$"+netPay.toFixed(2)},
      {label:"Federal Tax",value:"$"+federalWithholding.toFixed(2)},
      {label:"FICA (SS+Medicare)",value:"$"+fica.toFixed(2)},
      {label:"State Tax",value:"$"+state.toFixed(2)},
    ]
  }
""",
  """{id:"gross",label:"Gross Pay Per Paycheck",type:"number",placeholder:"3000",min:0,unit:"$",defaultValue:3000},
            {id:"freq",label:"Pay Frequency",type:"select",options:[{value:"weekly",label:"Weekly (52x)"},{value:"biweekly",label:"Bi-weekly (26x)"},{value:"semimonthly",label:"Semi-monthly (24x)"},{value:"monthly",label:"Monthly (12x)"}],defaultValue:"biweekly"},
            {id:"filing",label:"Federal Filing Status",type:"select",options:[{value:"single",label:"Single"},{value:"married",label:"Married Filing Jointly"}],defaultValue:"single"},
            {id:"k401",label:"401(k) Contribution %",type:"number",placeholder:"5",min:0,max:50,step:0.5,unit:"%",defaultValue:5},
            {id:"stateRate",label:"State Income Tax Rate",type:"number",placeholder:"5",min:0,max:15,step:0.1,unit:"%",defaultValue:5}""",
  [("Under 60% take-home","#ef4444",0,60),("60-70% take-home","#f59e0b",60,70),("70-80% take-home","#3b82f6",70,80),("80%+ take-home","#22c55e",80,100)],
  "% take-home","100",
  [("What deductions come out of a paycheck?","Federal income tax (based on brackets and W-4), Social Security tax (6.2% up to $176,100 wage base in 2025), Medicare tax (1.45%), state income tax (0-13% depending on state), local taxes (in some cities), and voluntary deductions like 401k, health insurance, FSA/HSA contributions."),
   ("How much should I expect in federal withholding?","It depends on your income and W-4 allowances. At $78k/year (single): ~$7,000 federal tax annually ($269/biweekly paycheck). At $100k/year: ~$13,000 annually ($500/biweekly). Submit a new W-4 if your life circumstances change — marriage, children, second job — to avoid under- or over-withholding."),
   ("What is FICA and how much is it?","FICA = Federal Insurance Contributions Act. It covers Social Security (6.2%) + Medicare (1.45%) = 7.65% of your gross pay. Your employer pays a matching 7.65%. For self-employed, you pay both halves (15.3%) as self-employment tax. Social Security only applies up to $176,100 in wages (2025)."),
   ("Why is my take-home pay different from what I calculated?","Possible reasons: employer-paid health, dental, vision premiums deducted pre-tax. HSA or FSA contributions. Union dues. Garnishments. Local/city taxes. Life insurance. Rounding in withholding tables. Your employer may also be withholding extra if you requested it on your W-4 to avoid underpayment."),
   ("How do I get a bigger paycheck?","Increase 401k contributions (reduces taxable income now). Contribute to FSA/HSA (pre-tax). Ensure W-4 reflects correct filing status and dependents. If you consistently get a large tax refund, you are over-withholding — adjust W-4 to increase take-home pay throughout the year instead.")],
  [("Income Tax Calculator","/calculators/income-tax-calculator"),("Salary Calculator","/calculators/salary-calculator"),("Budget Calculator","/calculators/budget-calculator"),("401k Calculator","/calculators/401k-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Paycheck Deduction Summary</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[["Federal income tax","Based on brackets"],["Social Security","6.2% (up to $176,100)"],["Medicare","1.45% (no limit)"],["State income tax","0–13%"],["401(k) contribution","Your elected %"]].map(([item,rate]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span>{item}</span><span class="font-medium">{rate}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Take-Home Pay by Salary (Single, Biweekly)</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Annual Salary</th><th class="text-right p-2 text-xs font-semibold">Gross/Check</th><th class="text-right p-2 text-xs font-semibold">Take-Home</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["$50,000","$1,923","~$1,450"],["$75,000","$2,885","~$2,100"],["$100,000","$3,846","~$2,700"],["$150,000","$5,769","~$3,800"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right font-medium text-green-700">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
        <p class="text-xs text-gray-500 mt-1">Approximate. Assumes 5% state tax, no 401k, standard deduction.</p>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">States With No Income Tax</h2>
        <div class="bg-green-50 rounded-xl p-4 text-xs text-green-800">
          <p class="font-semibold mb-2">No state income tax (as of 2025):</p>
          <div class="grid grid-cols-2 gap-1">
            {["Alaska","Florida","Nevada","New Hampshire","South Dakota","Tennessee","Texas","Washington","Wyoming"].map(s => (
              <div class="flex items-center gap-1"><span class="text-green-500">✓</span>{s}</div>
            ))}
          </div>
          <p class="mt-2 text-green-700">Moving to a no-tax state on $100k salary saves ~$3,000-6,000/year vs. high-tax states.</p>
        </div>
      </div>
    </div>""",
  "Take-Home Pay","Calculate your net paycheck after all taxes and deductions")

# ── ROTH IRA ──────────────────────────────────────────────────────────────────
w("roth-ira","Roth IRA Calculator","Financial","financial",
  "Roth IRA Calculator: Tax-Free Retirement Growth",
  "Calculate how much your Roth IRA will grow tax-free by retirement. Compare Roth vs traditional IRA. Free Roth IRA calculator.",
  """
  const annual = parseFloat(inputs.annual)||7000
  const currentBalance = parseFloat(inputs.currentBalance)||0
  const rate = parseFloat(inputs.rate)||7
  const years = parseInt(inputs.years)||30
  const taxRate = parseFloat(inputs.taxRate)||22
  if(years<=0) throw new Error("Enter years.")
  const r=rate/100/12, n=years*12
  const fvContrib = annual*(Math.pow(1+r,n)-1)/r/12
  const fvBalance = currentBalance*Math.pow(1+r,n)
  const totalFV = fvContrib+fvBalance
  const totalContrib = annual*years+currentBalance
  const gains = totalFV-totalContrib
  const taxSaved = gains*(taxRate/100)
  const traditionalAfterTax = totalFV*(1-taxRate/100)
  return {
    value:"$"+totalFV.toLocaleString("en-US",{maximumFractionDigits:0})+" tax-free",
    gaugeValue:Math.min(totalFV/1000000*100,100),
    breakdown:["Annual contribution: $"+annual,"Years: "+years,"Rate: "+rate+"%","Total contributed: $"+totalContrib.toLocaleString("en-US",{maximumFractionDigits:0}),"Tax-free gains: $"+gains.toLocaleString("en-US",{maximumFractionDigits:0}),"Tax savings vs taxable: $"+taxSaved.toLocaleString("en-US",{maximumFractionDigits:0}),"Final tax-free balance: $"+totalFV.toLocaleString("en-US",{maximumFractionDigits:0})],
    stats:[
      {label:"Final Balance (Tax-Free)",value:"$"+totalFV.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Total Contributed",value:"$"+totalContrib.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Tax-Free Gains",value:"$"+gains.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Tax Savings",value:"$"+taxSaved.toLocaleString("en-US",{maximumFractionDigits:0})},
    ]
  }
""",
  """{id:"annual",label:"Annual Roth IRA Contribution",type:"number",placeholder:"7000",min:0,max:8000,unit:"$",defaultValue:7000},
            {id:"currentBalance",label:"Current Roth IRA Balance",type:"number",placeholder:"0",min:0,unit:"$",defaultValue:0},
            {id:"rate",label:"Expected Annual Return",type:"number",placeholder:"7",min:0,max:20,step:0.5,unit:"%",defaultValue:7},
            {id:"years",label:"Years Until Retirement",type:"number",placeholder:"30",min:1,max:50,unit:"years",defaultValue:30},
            {id:"taxRate",label:"Expected Tax Rate in Retirement",type:"number",placeholder:"22",min:0,max:50,step:1,unit:"%",defaultValue:22}""",
  [("Under $250k","#f59e0b",0,25),("$250k–$500k","#3b82f6",25,50),("$500k–$1M","#22c55e",50,100)],
  "% to $1M","100",
  [("What makes the Roth IRA special?","Contributions are made with after-tax dollars, but all growth and qualified withdrawals are completely tax-free. No required minimum distributions (RMDs) in retirement. This makes Roth IRAs ideal if you expect to be in a higher tax bracket in retirement, or if you want tax flexibility."),
   ("What are the 2025 Roth IRA contribution limits?","$7,000 per person ($8,000 if age 50+). However, income limits apply. Single: full contribution under $150,000 MAGI, phases out to $165,000. Married jointly: full under $236,000, phases out to $246,000. Over these limits: consider the backdoor Roth strategy."),
   ("Roth IRA vs Traditional IRA: which is better?","Roth: pay taxes now, withdraw tax-free later. Best if you expect higher taxes in retirement or are in a low bracket now. Traditional: deduct now, pay taxes later. Best if you expect lower taxes in retirement or need the deduction now. Both are valuable — many financial advisors recommend contributing to both for tax diversification."),
   ("What is the backdoor Roth IRA?","If your income exceeds Roth IRA limits, you can contribute to a non-deductible traditional IRA (no income limits) and immediately convert it to a Roth IRA. This is legal and widely used. Beware the pro-rata rule if you have other traditional IRA balances — consult a tax advisor."),
   ("When can I withdraw from a Roth IRA?","Contributions (not earnings) can be withdrawn any time, tax-free and penalty-free — they were already taxed. Earnings can be withdrawn tax-free and penalty-free after age 59.5 AND the account is 5+ years old. The flexibility to access contributions without penalty is an advantage over 401(k)s.")],
  [("401k Calculator","/calculators/401k-calculator"),("Retirement Calculator","/calculators/retirement-calculator"),("Investment Calculator","/calculators/investment-calculator"),("FIRE Calculator","/calculators/fire-calculator")],
  """        <div class="bg-green-50 border border-green-200 rounded-xl p-5">
          <h3 class="font-bold text-green-900 mb-3">2025 Roth IRA Limits</h3>
          <div class="space-y-1 text-xs text-green-800">
            {[["Contribution (under 50)","$7,000"],["Contribution (50+)","$8,000"],["Phase-out starts (single)","$150,000 MAGI"],["Phase-out ends (single)","$165,000 MAGI"],["Phase-out starts (MFJ)","$236,000 MAGI"],["Phase-out ends (MFJ)","$246,000 MAGI"]].map(([k,v]) => (
              <div class="flex justify-between border-b border-green-100 pb-1"><span>{k}</span><span class="font-medium">{v}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Roth IRA Growth — Max Contribution</h2>
        <p class="text-xs text-gray-600 mb-3">$7,000/year, 7% return, starting from $0:</p>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Years</th><th class="text-right p-2 text-xs font-semibold">Contributed</th><th class="text-right p-2 text-xs font-semibold">Balance (Tax-Free)</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["10","$70k","$97k"],["20","$140k","$288k"],["30","$210k","$661k"],["40","$280k","$1.48M"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right font-medium text-green-700">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Roth vs Traditional IRA Comparison</h2>
        <div class="space-y-2">
          {[
            {factor:"Tax on contributions",roth:"After-tax (no deduction)",trad:"Pre-tax (deductible if eligible)"},
            {factor:"Tax on withdrawals",roth:"Tax-free",trad:"Taxed as ordinary income"},
            {factor:"Required withdrawals (RMDs)",roth:"None",trad:"Required at age 73"},
            {factor:"Early withdrawal",roth:"Contributions anytime (free)",trad:"10% penalty + taxes before 59.5"},
            {factor:"Best for",roth:"Lower bracket now, higher later",trad:"Higher bracket now, lower later"},
          ].map(f => (
            <div class="bg-gray-50 rounded-lg p-2.5 text-xs">
              <div class="font-semibold text-gray-800 mb-1">{f.factor}</div>
              <div class="grid grid-cols-2 gap-2">
                <div class="text-green-700"><span class="font-medium">Roth:</span> {f.roth}</div>
                <div class="text-blue-700"><span class="font-medium">Trad:</span> {f.trad}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>""",
  "Tax-Free Balance at Retirement","Calculate your Roth IRA tax-free growth and compare Roth vs traditional")

print(f"\nWritten: {written} pages (markup, mortgage-points, npv, payback-period, paycheck, roth-ira)")
