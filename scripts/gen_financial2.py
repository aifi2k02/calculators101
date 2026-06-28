#!/usr/bin/env python3
"""Generate remaining financial calculator pages."""
import os

CALC_DIR = "/Users/apple/Documents/Projects/calculators-for-free/src/pages/calculators"
written = 0

def w(slug, title, cat, cat_slug, seo_title, seo_desc, formula, inputs_js, gauge_zones, gauge_unit, gauge_max,
      faqs_pairs, related_pairs, sidebar_html, content_html, result_label="Result", calc_desc=""):
    global written
    zones_js = "\n".join(
        f'              {{ label: "{z[0]}", color: "{z[1]}", from: {z[2]}, to: {z[3]} }},'
        for z in gauge_zones
    )
    related_js = "\n            ".join(
        f'{{ name: "{n}", href: "{h}" }},'
        for n, h in related_pairs
    )
    faqs_items = []
    for q, a in faqs_pairs:
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
    path = os.path.join(CALC_DIR, f"{slug}-calculator.astro")
    with open(path, 'w') as f:
        f.write(content)
    written += 1
    print(f"  {slug}")

# ── APR ──────────────────────────────────────────────────────────────────────
w("apr","APR Calculator","Financial","financial",
  "APR Calculator: Annual Percentage Rate Calculator",
  "Calculate the true annual percentage rate (APR) of a loan including fees. Compare loan costs accurately with our free APR calculator.",
  """
  const principal = parseFloat(inputs.principal)||0
  const rate = parseFloat(inputs.rate)||0
  const term = parseInt(inputs.term)||12
  const fees = parseFloat(inputs.fees)||0
  if(principal<=0) throw new Error("Enter loan amount.")
  const r = rate/100/12
  const payment = r===0?(principal/term):principal*r*Math.pow(1+r,term)/(Math.pow(1+r,term)-1)
  const totalPaid = payment*term
  const totalInterest = totalPaid-principal
  const effectivePrincipal = principal-fees
  let aprGuess=rate/100, step=0.001
  for(let i=0;i<1000;i++){
    const rm=aprGuess/12
    const pv=rm===0?effectivePrincipal/term:payment*(1-Math.pow(1+rm,-term))/rm
    if(Math.abs(pv-effectivePrincipal)<0.01) break
    if(pv>effectivePrincipal) aprGuess+=step; else aprGuess-=step; step*=0.99
  }
  const apr = aprGuess*100
  const diff = apr-rate
  return {
    value:apr.toFixed(3)+"%",
    gaugeValue:Math.min(apr,30)/30*100,
    breakdown:["Stated rate: "+rate+"%","APR (with fees): "+apr.toFixed(3)+"%","Monthly payment: $"+payment.toFixed(2),"Total interest: $"+totalInterest.toFixed(2),"Fees added: $"+fees],
    stats:[
      {label:"APR",value:apr.toFixed(3)+"%"},
      {label:"Stated Rate",value:rate+"%"},
      {label:"Rate Difference",value:"+"+diff.toFixed(3)+"%"},
      {label:"Monthly Payment",value:"$"+payment.toFixed(2)},
    ]
  }
""",
  """{id:"principal",label:"Loan Amount",type:"number",placeholder:"20000",min:0,unit:"$",defaultValue:20000},
            {id:"rate",label:"Stated Interest Rate",type:"number",placeholder:"6.5",min:0,max:50,step:0.1,unit:"%",defaultValue:6.5},
            {id:"term",label:"Loan Term",type:"number",placeholder:"60",min:1,unit:"months",defaultValue:60},
            {id:"fees",label:"Total Upfront Fees",type:"number",placeholder:"500",min:0,unit:"$",defaultValue:500}""",
  [("Excellent <7%","#22c55e",0,23),("Good 7-12%","#3b82f6",23,40),("Fair 12-20%","#f59e0b",40,67),("High 20%+","#ef4444",67,100)],
  "% of 30%","100",
  [("What is APR and how is it different from interest rate?","The interest rate is the base cost of borrowing. APR (Annual Percentage Rate) includes the interest rate PLUS fees and other costs, expressed as a yearly rate. APR is always equal to or higher than the stated rate. It is the true cost of the loan."),
   ("Why is APR important when comparing loans?","Two loans with the same interest rate can have very different APRs if one has high origination fees. Always compare APR, not just interest rate. A 6% loan with $2,000 in fees may cost more than a 6.5% loan with no fees on a short-term loan."),
   ("What fees are typically included in APR?","Origination fees, underwriting fees, broker fees, mortgage points (for home loans), and other mandatory closing costs. NOT included: appraisal, title insurance, escrow, and other third-party fees that vary by provider."),
   ("What is a good APR for a personal loan?","Under 10% is excellent. 10-15% is good. 15-20% is fair. Above 20% is high. Credit cards average 21-24% APR. Payday loans can exceed 400% APR. Your rate depends heavily on credit score, income, and loan term."),
   ("Does APR account for compounding?","Standard APR does not account for compounding. APY (Annual Percentage Yield) does. When comparing savings accounts, use APY. When comparing loans, APR is the standard. For credit cards, APR divided by 365 gives daily periodic rate, which compounds monthly.")],
  [("Mortgage Calculator","/calculators/mortgage-calculator"),("Loan Calculator","/calculators/loan-calculator"),("Auto Loan Calculator","/calculators/auto-loan-calculator"),("Interest Calculator","/calculators/interest-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">APR vs Interest Rate</h3>
          <div class="text-xs text-blue-800 space-y-2">
            <div><strong>Interest Rate:</strong> Base cost of borrowing money, expressed as annual %</div>
            <div><strong>APR:</strong> Total cost including fees. Always &ge; interest rate.</div>
            <div class="bg-blue-100 rounded p-2 mt-2">Example: 6% rate + $1,000 fee on $20k/5yr loan = <strong>6.8% APR</strong></div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Typical APR Ranges by Loan Type</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold text-gray-700">Loan Type</th><th class="text-right p-2 text-xs font-semibold text-gray-700">Good Credit APR</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["30-yr Mortgage","6-8%"],["15-yr Mortgage","5.5-7%"],["Auto Loan","5-9%"],["Personal Loan","8-15%"],["Student Loan","5-8%"],["Credit Card","18-25%"],["Payday Loan","300-400%+"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-medium">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">How Fees Impact APR</h2>
        <p class="text-xs text-gray-600 mb-3">$20,000 loan at 6%, 60 months. Fee impact:</p>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Fees</th><th class="text-right p-2 text-xs font-semibold">APR</th><th class="text-right p-2 text-xs font-semibold">Extra Cost</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["$0","6.00%","$0"],["$250","6.26%","$250"],["$500","6.52%","$500"],["$1,000","7.04%","$1,000"],["$2,000","8.07%","$2,000"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right text-red-600">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "APR","Calculate the true annual percentage rate including fees")

# ── ANNUITY ──────────────────────────────────────────────────────────────────
w("annuity","Annuity Calculator","Financial","financial",
  "Annuity Calculator: Present & Future Value of Annuity Payments",
  "Calculate the present value, future value, or monthly payment of an annuity. Supports ordinary annuity and annuity due. Free annuity calculator.",
  """
  const payment = parseFloat(inputs.payment)||0
  const rate = parseFloat(inputs.rate)||5
  const periods = parseInt(inputs.periods)||120
  const type = inputs.type||"ordinary"
  if(payment<=0) throw new Error("Enter payment amount.")
  const r = rate/100/12
  const n = periods
  const due = type==="due"?1:0
  const pv = r===0?payment*n:payment*((1-Math.pow(1+r,-n))/r)*Math.pow(1+r,due)
  const fv = r===0?payment*n:payment*((Math.pow(1+r,n)-1)/r)*Math.pow(1+r,due)
  const totalPaid = payment*n
  return {
    value:"PV: $"+pv.toLocaleString("en-US",{maximumFractionDigits:0}),
    gaugeValue:Math.min(pv/500000*100,100),
    breakdown:["Payment: $"+payment+"/period","Rate: "+rate+"% annual","Periods: "+periods,"Present Value: $"+pv.toLocaleString("en-US",{maximumFractionDigits:0}),"Future Value: $"+fv.toLocaleString("en-US",{maximumFractionDigits:0}),"Total Payments: $"+totalPaid.toLocaleString("en-US",{maximumFractionDigits:0})],
    stats:[
      {label:"Present Value",value:"$"+pv.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Future Value",value:"$"+fv.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Total Payments",value:"$"+totalPaid.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Interest Earned",value:"$"+(fv-totalPaid).toLocaleString("en-US",{maximumFractionDigits:0})},
    ]
  }
""",
  """{id:"payment",label:"Payment Amount",type:"number",placeholder:"1000",min:0,unit:"$",defaultValue:1000},
            {id:"rate",label:"Annual Interest Rate",type:"number",placeholder:"5",min:0,max:30,step:0.1,unit:"%",defaultValue:5},
            {id:"periods",label:"Number of Periods (months)",type:"number",placeholder:"120",min:1,unit:"months",defaultValue:120},
            {id:"type",label:"Annuity Type",type:"select",options:[{value:"ordinary",label:"Ordinary Annuity (end of period)"},{value:"due",label:"Annuity Due (beginning of period)"}],defaultValue:"ordinary"}""",
  [("Under $100k","#f59e0b",0,20),("$100k–$250k","#3b82f6",20,50),("$250k–$500k","#22c55e",50,100)],
  "% of $500k","100",
  [("What is an annuity?","An annuity is a series of equal payments made at regular intervals. Present value (PV) is what a future series of payments is worth today. Future value (FV) is what regular payments grow to over time with interest. Annuities are used for mortgages, pensions, savings plans, and insurance products."),
   ("What is the difference between ordinary annuity and annuity due?","Ordinary annuity (most common): payments at the END of each period (mortgages, car loans). Annuity due: payments at the BEGINNING (rent, lease). Annuity due payments are worth slightly more because each payment earns interest for one extra period."),
   ("How is an annuity different from a lump sum?","A lump sum is a single payment. An annuity spreads payments over time. The time value of money means $1,000/month for 10 years is NOT the same as $120,000 today — the lump sum today is worth more because it can be invested. Present value calculates the lump-sum equivalent."),
   ("What is a good annuity interest rate?","For insurance annuities, rates depend on market conditions — typically 3-6% for fixed annuities. Variable annuities depend on investment performance. For calculating NPV of business cash flows, use your discount rate or WACC. For personal finance, compare to what you could earn investing the money."),
   ("How do I calculate annuity payments for retirement?","If you want $3,000/month for 25 years with 5% return: PV = $3,000 x ((1 - (1.05/12)^-300) / (0.05/12)) = ~$511,000 needed at retirement. This is how pension obligations and retirement nest egg requirements are calculated.")],
  [("Retirement Calculator","/calculators/retirement-calculator"),("NPV Calculator","/calculators/npv-calculator"),("Loan Calculator","/calculators/loan-calculator"),("Investment Calculator","/calculators/investment-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Annuity Quick Reference</h3>
          <div class="text-xs text-blue-800 space-y-1">
            <div><strong>PV:</strong> What is this stream worth TODAY?</div>
            <div><strong>FV:</strong> What will this stream be worth in the FUTURE?</div>
            <div><strong>Ordinary:</strong> Payment at END of period</div>
            <div><strong>Due:</strong> Payment at START of period</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Annuity Types Comparison</h2>
        <div class="space-y-3">
          {[
            {t:"Fixed Annuity",d:"Guaranteed fixed payments. Insurance product. Safe but limited upside. Good for predictable retirement income."},
            {t:"Variable Annuity",d:"Payments vary based on investment performance. Higher risk, higher potential. Typically higher fees."},
            {t:"Immediate Annuity",d:"Start payments immediately. Buy with lump sum. Good for converting retirement savings to income."},
            {t:"Deferred Annuity",d:"Accumulate value now, receive payments later. Tax-deferred growth. Good for long-term retirement planning."},
          ].map(a => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-xs text-gray-800 mb-1">{a.t}</div>
              <div class="text-xs text-gray-600">{a.d}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">$1,000/Month Annuity — Present Value</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Duration</th><th class="text-right p-2 text-xs font-semibold">3% rate</th><th class="text-right p-2 text-xs font-semibold">6% rate</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["5 years","$55,797","$50,504"],["10 years","$103,797","$90,073"],["20 years","$180,455","$139,581"],["30 years","$237,189","$166,792"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "Present Value","Calculate present and future value of annuity payments")

# ── CAR LEASE ────────────────────────────────────────────────────────────────
w("car-lease","Car Lease Calculator","Financial","financial",
  "Car Lease Calculator: Monthly Payment & Total Cost",
  "Calculate your car lease monthly payment, total cost, and compare leasing vs buying. Free car lease calculator.",
  """
  const msrp = parseFloat(inputs.msrp)||0
  const capCost = parseFloat(inputs.capCost)||msrp
  const residual = parseFloat(inputs.residual)||60
  const moneyFactor = parseFloat(inputs.moneyFactor)||0.002
  const term = parseInt(inputs.term)||36
  const downPayment = parseFloat(inputs.downPayment)||0
  const taxes = parseFloat(inputs.taxes)||8
  if(msrp<=0) throw new Error("Enter MSRP.")
  const adjCap = capCost-downPayment
  const residualValue = msrp*(residual/100)
  const depreciation = (adjCap-residualValue)/term
  const finance = (adjCap+residualValue)*moneyFactor
  const basePayment = depreciation+finance
  const totalPayment = basePayment*(1+taxes/100)
  const totalCost = totalPayment*term+downPayment
  const apr = moneyFactor*2400
  return {
    value:"$"+totalPayment.toFixed(2)+"/mo",
    gaugeValue:Math.min(totalPayment/1000*100,100),
    breakdown:["Base payment: $"+basePayment.toFixed(2),"Tax: "+taxes+"%","Total monthly: $"+totalPayment.toFixed(2),"Residual value: $"+residualValue.toFixed(0),"Effective APR: "+apr.toFixed(2)+"%","Total lease cost: $"+totalCost.toFixed(0)],
    stats:[
      {label:"Monthly Payment",value:"$"+totalPayment.toFixed(2)},
      {label:"Residual Value",value:"$"+residualValue.toFixed(0)},
      {label:"Effective APR",value:apr.toFixed(2)+"%"},
      {label:"Total Lease Cost",value:"$"+totalCost.toFixed(0)},
    ]
  }
""",
  """{id:"msrp",label:"Vehicle MSRP",type:"number",placeholder:"40000",min:0,unit:"$",defaultValue:40000},
            {id:"capCost",label:"Negotiated Price (Cap Cost)",type:"number",placeholder:"38000",min:0,unit:"$",defaultValue:38000},
            {id:"residual",label:"Residual Value %",type:"number",placeholder:"55",min:0,max:90,step:1,unit:"%",defaultValue:55},
            {id:"moneyFactor",label:"Money Factor",type:"number",placeholder:"0.002",min:0,max:0.01,step:0.0001,defaultValue:0.002},
            {id:"term",label:"Lease Term",type:"select",options:[{value:"24",label:"24 months"},{value:"36",label:"36 months"},{value:"48",label:"48 months"}],defaultValue:"36"},
            {id:"downPayment",label:"Down Payment / Cap Reduction",type:"number",placeholder:"0",min:0,unit:"$",defaultValue:0},
            {id:"taxes",label:"Sales Tax Rate",type:"number",placeholder:"8",min:0,max:15,step:0.1,unit:"%",defaultValue:8}""",
  [("Low (<$300/mo)","#22c55e",0,30),("Moderate ($300-500)","#3b82f6",30,50),("High ($500-800)","#f59e0b",50,80),("Very High (>$800)","#ef4444",80,100)],
  "% of $1k","100",
  [("What is money factor in a car lease?","Money factor is the financing rate, similar to APR but expressed differently. To convert: Money Factor x 2400 = APR. A money factor of 0.002 = 4.8% APR. Lower money factor = cheaper financing. Dealers may not reveal this — you can calculate it from the payment breakdown."),
   ("What is residual value?","The residual value is the car's predicted worth at lease end, set by the leasing company as a percentage of MSRP. Higher residual = lower monthly payment (less depreciation to cover). SUVs and luxury brands often have strong residuals. This is NOT negotiable — it is set by the manufacturer."),
   ("Should I put money down on a lease?","Generally no. A down payment reduces monthly payments but provides zero benefit if the car is totaled or stolen — the insurance pays the leasing company, not you. This money is lost. Instead, keep cash and invest it; let the lease run at its natural monthly payment."),
   ("What is cap cost (capitalized cost)?","Cap cost is the negotiated selling price of the vehicle — it IS negotiable. Lower cap cost = lower monthly payment. Always negotiate the sale price down before discussing lease terms. Never agree to a lease without knowing the cap cost — dealers may hide inflated prices."),
   ("Leasing vs buying: which is better?","Leasing: lower monthly payments, always in a new car, no resale hassle, but no equity built and mileage limits. Buying: builds equity, no mileage limits, better long-term value if you keep the car 7-10 years. If you drive more than 15k miles/year or want to keep the car long-term, buying usually wins.")],
  [("Auto Loan Calculator","/calculators/auto-loan-calculator"),("Loan Calculator","/calculators/loan-calculator"),("Budget Calculator","/calculators/budget-calculator"),("Depreciation Calculator","/calculators/investment-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Lease vs Buy — Quick Look</h3>
          <div class="text-xs text-blue-800 space-y-2">
            <div class="grid grid-cols-2 gap-2">
              <div class="bg-blue-100 rounded p-2"><strong>Lease Pros</strong><br/>Lower payments<br/>New car every 3 yrs<br/>Less maintenance</div>
              <div class="bg-blue-100 rounded p-2"><strong>Buy Pros</strong><br/>Build equity<br/>No mileage limit<br/>Lower total cost</div>
            </div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Lease vs Finance Comparison</h2>
        <p class="text-xs text-gray-600 mb-3">$40,000 vehicle, 36-month example</p>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold"></th><th class="text-right p-2 text-xs font-semibold">Lease</th><th class="text-right p-2 text-xs font-semibold">Finance (60mo)</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Monthly","~$450","~$720"],["Down","$0","$0"],["3-yr cost","$16,200","$25,920"],["End of 3 yrs","No car","Own car (~$24k)"]].map(r => (
              <tr><td class="p-2 text-xs font-medium">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Lease Negotiation Tips</h2>
        <div class="space-y-2">
          {["Always negotiate the cap cost (selling price) — treat it like a purchase","Research money factor and residual on sites like Edmunds MF before visiting dealer","Avoid rolling fees into the lease — pay them upfront or shop elsewhere","Know your mileage needs — excess mileage fees run $0.15-0.25/mile","Multiple security deposit (MSD) programs can lower the money factor at some brands","Get multiple quotes — same car, different dealers can have different fees"].map(t => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{t}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Monthly Payment","Calculate your car lease payment and total lease cost")

# ── CD (Certificate of Deposit) ─────────────────────────────────────────────
w("cd","CD Calculator","Financial","financial",
  "CD Calculator: Certificate of Deposit Interest Calculator",
  "Calculate how much you earn with a certificate of deposit. Compare CD terms and APY rates. Free CD interest calculator.",
  """
  const principal = parseFloat(inputs.principal)||0
  const apy = parseFloat(inputs.apy)||5
  const term = parseInt(inputs.term)||12
  if(principal<=0) throw new Error("Enter deposit amount.")
  const years = term/12
  const finalBalance = principal*Math.pow(1+apy/100,years)
  const interest = finalBalance-principal
  const effectiveDaily = Math.pow(1+apy/100,1/365)-1
  const dailyInterest = principal*effectiveDaily
  return {
    value:"$"+finalBalance.toLocaleString("en-US",{maximumFractionDigits:2}),
    gaugeValue:Math.min((interest/principal)*100*2,100),
    breakdown:["Principal: $"+principal.toLocaleString("en-US"),"APY: "+apy+"%","Term: "+term+" months","Interest earned: $"+interest.toFixed(2),"Final balance: $"+finalBalance.toFixed(2),"Daily interest: $"+dailyInterest.toFixed(2)],
    stats:[
      {label:"Final Balance",value:"$"+finalBalance.toFixed(2)},
      {label:"Interest Earned",value:"$"+interest.toFixed(2)},
      {label:"Return %",value:((interest/principal)*100).toFixed(2)+"%"},
      {label:"Daily Interest",value:"$"+dailyInterest.toFixed(2)},
    ]
  }
""",
  """{id:"principal",label:"Deposit Amount",type:"number",placeholder:"10000",min:0,unit:"$",defaultValue:10000},
            {id:"apy",label:"APY (Annual Percentage Yield)",type:"number",placeholder:"5",min:0,max:15,step:0.05,unit:"%",defaultValue:5},
            {id:"term",label:"Term",type:"select",options:[{value:"3",label:"3 months"},{value:"6",label:"6 months"},{value:"12",label:"1 year"},{value:"18",label:"18 months"},{value:"24",label:"2 years"},{value:"36",label:"3 years"},{value:"60",label:"5 years"}],defaultValue:"12"}""",
  [("Low (< 2%)","#ef4444",0,4),("Fair (2-4%)","#f59e0b",4,8),("Good (4-5.5%)","#3b82f6",8,11),("Excellent (5.5%+)","#22c55e",11,100)],
  "% return (50% of actual)","100",
  [("What is a CD (Certificate of Deposit)?","A CD is a savings account that holds a fixed amount of money for a fixed term (months to years) and earns interest at a higher rate than regular savings. At maturity, you get your principal plus interest back. If you withdraw early, you pay a penalty (typically 3-6 months of interest)."),
   ("What is a good CD rate right now?","In 2024-2025, competitive CD rates range from 4.5-5.5% APY for 6-12 month CDs. Rates vary by institution — online banks and credit unions typically offer significantly higher rates than traditional big banks. Always compare rates before committing."),
   ("What is the early withdrawal penalty for CDs?","Common penalties: 3 months interest (CDs under 1 year), 6 months interest (1-2 year CDs), 12 months interest (2-5 year CDs). Some banks have more severe penalties. Calculate the penalty before breaking a CD early — it can eat into your principal."),
   ("What is a CD ladder strategy?","Instead of locking all money in one CD, split it into multiple CDs with staggered maturities. Example: $20,000 split into four $5,000 CDs maturing in 6, 12, 18, and 24 months. As each matures, reinvest at the current rate. You get liquidity every 6 months."),
   ("CD vs high-yield savings account: which is better?","HYSAs offer flexibility — no maturity date, can add/withdraw money, competitive rates. CDs offer higher rates in exchange for locking money away. If rates are rising, prefer HYSAs (you can move money as rates improve). If rates are falling, lock in CDs at the current higher rate.")],
  [("Savings Calculator","/calculators/savings-calculator"),("Investment Calculator","/calculators/investment-calculator"),("Compound Interest Calculator","/calculators/compound-interest-calculator"),("Interest Calculator","/calculators/interest-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">$10,000 CD at 5% APY</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700 border-b border-blue-200"><th class="text-left pb-1">Term</th><th class="text-right pb-1">Interest</th><th class="text-right pb-1">Balance</th></tr></thead>
            <tbody class="text-blue-900">
              {[["6 months","$247","$10,247"],["1 year","$500","$10,500"],["2 years","$1,025","$11,025"],["5 years","$2,763","$12,763"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right">{r[1]}</td><td class="text-right font-medium">{r[2]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">CD Ladder Example</h2>
        <p class="text-xs text-gray-600 mb-3">$20,000 split into 4 CDs at 5% APY:</p>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">CD</th><th class="text-right p-2 text-xs font-semibold">Amount</th><th class="text-right p-2 text-xs font-semibold">Matures</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["CD #1","$5,000","6 months"],["CD #2","$5,000","12 months"],["CD #3","$5,000","18 months"],["CD #4","$5,000","24 months"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
        <p class="text-xs text-gray-500 mt-1">Access $5,000 every 6 months. Reinvest at current rates.</p>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">CD vs Alternatives</h2>
        <div class="space-y-3">
          {[
            {opt:"CD",pros:"Guaranteed rate, FDIC insured",cons:"Lock-up period, early withdrawal penalty"},
            {opt:"HYSA",pros:"Flexible, no lock-in, competitive rates",cons:"Rate can drop anytime, no rate guarantee"},
            {opt:"T-Bills",pros:"No state tax on interest, very safe",cons:"Rates vary, less accessible"},
            {opt:"I-Bonds",pros:"Inflation-protected, tax advantages",cons:"$10k limit/year, 12-month lock-up"},
          ].map(c => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-gray-800 text-xs">{c.opt}</div>
              <div class="text-xs text-green-700">+ {c.pros}</div>
              <div class="text-xs text-red-600">- {c.cons}</div>
            </div>
          ))}
        </div>
      </div>
    </div>""",
  "Final Balance","Calculate your CD earnings and compare term options")

# ── CAPITAL GAINS ───────────────────────────────────────────────────────────
w("capital-gains","Capital Gains Tax Calculator","Financial","financial",
  "Capital Gains Tax Calculator: Short & Long Term Rates",
  "Calculate your capital gains tax on investments, stocks, and real estate. Includes federal short-term and long-term rates. Free capital gains calculator.",
  """
  const purchase = parseFloat(inputs.purchase)||0
  const salePrice = parseFloat(inputs.salePrice)||0
  const held = inputs.held||"long"
  const income = parseFloat(inputs.income)||75000
  const filingStatus = inputs.filingStatus||"single"
  if(salePrice<=0) throw new Error("Enter sale price.")
  const gain = salePrice-purchase
  if(gain<=0){
    return {value:"No taxable gain",gaugeValue:0,stats:[{label:"Loss",value:"$"+Math.abs(gain).toFixed(0)},{label:"Tax Owed",value:"$0"},{label:"After-Tax Proceeds",value:"$"+salePrice.toFixed(0)},{label:"Return %",value:((gain/purchase)*100).toFixed(1)+"%"}]}
  }
  let taxRate
  if(held==="short"){
    if(income<=11600) taxRate=0.10
    else if(income<=47150) taxRate=0.12
    else if(income<=100525) taxRate=0.22
    else if(income<=191950) taxRate=0.24
    else taxRate=0.32
  } else {
    const brackets = filingStatus==="married"?[94050,583750]:[47025,518900]
    if(income<=brackets[0]) taxRate=0
    else if(income<=brackets[1]) taxRate=0.15
    else taxRate=0.20
  }
  const tax = gain*taxRate
  const afterTax = salePrice-tax
  return {
    value:"$"+tax.toFixed(2)+" tax",
    gaugeValue:taxRate*100,
    breakdown:["Purchase price: $"+purchase,"Sale price: $"+salePrice,"Capital gain: $"+gain.toFixed(2),"Holding period: "+held+"-term","Tax rate: "+(taxRate*100)+"%","Tax owed: $"+tax.toFixed(2),"After-tax: $"+afterTax.toFixed(2)],
    stats:[
      {label:"Capital Gain",value:"$"+gain.toFixed(0)},
      {label:"Tax Rate",value:(taxRate*100)+"%"},
      {label:"Tax Owed",value:"$"+tax.toFixed(0)},
      {label:"After-Tax Proceeds",value:"$"+afterTax.toFixed(0)},
    ]
  }
""",
  """{id:"purchase",label:"Purchase Price (Cost Basis)",type:"number",placeholder:"10000",min:0,unit:"$",defaultValue:10000},
            {id:"salePrice",label:"Sale Price",type:"number",placeholder:"25000",min:0,unit:"$",defaultValue:25000},
            {id:"held",label:"Holding Period",type:"select",options:[{value:"long",label:"Long-term (over 1 year)"},{value:"short",label:"Short-term (1 year or less)"}],defaultValue:"long"},
            {id:"income",label:"Annual Taxable Income",type:"number",placeholder:"75000",min:0,unit:"$",defaultValue:75000},
            {id:"filingStatus",label:"Filing Status",type:"select",options:[{value:"single",label:"Single"},{value:"married",label:"Married Filing Jointly"}],defaultValue:"single"}""",
  [("0% rate","#22c55e",0,1),("10-15% rate","#3b82f6",1,16),("20-24% rate","#f59e0b",16,25),("High rate 25%+","#ef4444",25,100)],
  "% tax rate","100",
  [("What is the capital gains tax rate for 2025?","Long-term capital gains (held over 1 year) rates for 2025: 0% if taxable income under $47,025 (single) or $94,050 (MFJ); 15% for most taxpayers; 20% for high earners. Short-term gains are taxed as ordinary income at your marginal tax bracket (10-37%)."),
   ("How long must I hold an asset for long-term capital gains?","More than one year (at least 366 days). If you sell on day 365 or sooner, the gain is short-term and taxed at ordinary income rates — which can be dramatically higher. For someone in the 22% bracket, waiting one more day can cut the tax rate from 22% to 15%."),
   ("What is cost basis?","Cost basis is your original purchase price plus any commissions, fees, or improvements. For inherited assets, basis is usually the fair market value at the date of death (stepped-up basis). For gifted assets, it depends on whether the recipient sells at a gain or loss."),
   ("Can capital losses offset capital gains?","Yes. Capital losses directly offset capital gains, dollar for dollar. If losses exceed gains, you can deduct up to $3,000 against ordinary income per year. Remaining losses carry forward indefinitely. This is called tax-loss harvesting when done strategically."),
   ("Does the home sale exclusion apply?","Yes! If you owned and lived in your home for at least 2 of the past 5 years, you can exclude up to $250,000 in gains (single) or $500,000 (married) from capital gains tax. This exclusion applies once every 2 years. Most primary home sales are tax-free because of this rule.")],
  [("Income Tax Calculator","/calculators/income-tax-calculator"),("Investment Calculator","/calculators/investment-calculator"),("Stock Profit Calculator","/calculators/stock-profit-calculator"),("ROI Calculator","/calculators/roi-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">2025 Long-Term Rates (Single)</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700 border-b border-blue-200"><th class="text-left pb-1">Taxable Income</th><th class="text-right pb-1">Rate</th></tr></thead>
            <tbody class="text-blue-900">
              {[["$0–$47,025","0%"],["$47,025–$518,900","15%"],["Over $518,900","20%"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right font-medium">{r[1]}</td></tr>
              ))}
            </tbody>
          </table>
          <p class="text-xs text-blue-600 mt-1">Net Investment Income Tax (3.8%) may apply at higher incomes</p>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Short vs Long Term Tax Impact</h2>
        <p class="text-xs text-gray-600 mb-3">$50,000 gain, $100,000 income (single):</p>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Holding Period</th><th class="text-right p-2 text-xs font-semibold">Rate</th><th class="text-right p-2 text-xs font-semibold">Tax Owed</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["< 1 year (short)","22%","$11,000"],["> 1 year (long)","15%","$7,500"],["Savings by waiting","—","$3,500"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right font-medium">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Tax-Loss Harvesting Strategies</h2>
        <div class="space-y-2">
          {["Sell losing positions before year end to offset gains","Capital losses offset capital gains dollar for dollar","Up to $3,000 excess loss deductible against ordinary income","Remaining losses carry forward to future tax years","Beware wash-sale rule: no repurchase within 30 days of selling at a loss","Harvest losses in taxable accounts; keep winners in tax-advantaged accounts"].map(t => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{t}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Capital Gains Tax","Calculate your capital gains tax on investments and real estate")

# ── BOND YIELD ───────────────────────────────────────────────────────────────
w("bond-yield","Bond Yield Calculator","Financial","financial",
  "Bond Yield Calculator: Current Yield & Yield to Maturity (YTM)",
  "Calculate current yield, yield to maturity (YTM), and yield to call for bonds. Free bond yield calculator.",
  """
  const face = parseFloat(inputs.face)||1000
  const price = parseFloat(inputs.price)||950
  const couponRate = parseFloat(inputs.couponRate)||5
  const years = parseFloat(inputs.years)||10
  const freq = parseInt(inputs.freq)||2
  if(face<=0||price<=0) throw new Error("Enter face value and price.")
  const coupon = face*(couponRate/100)/freq
  const n = years*freq
  const currentYield = (face*(couponRate/100)/price)*100
  let ytm=couponRate/100/freq, step=0.001
  for(let i=0;i<2000;i++){
    const pv = coupon*((1-Math.pow(1+ytm,-n))/ytm)+face*Math.pow(1+ytm,-n)
    if(Math.abs(pv-price)<0.01) break
    if(pv>price) ytm+=step; else ytm-=step; step*=0.99
  }
  const ytmAnnual = ytm*freq*100
  const premium = price>face?"premium":price<face?"discount":"par"
  return {
    value:"YTM: "+ytmAnnual.toFixed(3)+"%",
    gaugeValue:Math.min(ytmAnnual/15*100,100),
    breakdown:["Face value: $"+face,"Price: $"+price+" ("+premium+")","Coupon: "+couponRate+"% ($"+(face*couponRate/100).toFixed(2)+"/yr)","Current yield: "+currentYield.toFixed(3)+"%","YTM: "+ytmAnnual.toFixed(3)+"%","Payments/yr: "+freq],
    stats:[
      {label:"YTM",value:ytmAnnual.toFixed(3)+"%"},
      {label:"Current Yield",value:currentYield.toFixed(3)+"%"},
      {label:"Annual Coupon",value:"$"+(face*couponRate/100).toFixed(2)},
      {label:"Price vs Par",value:premium.charAt(0).toUpperCase()+premium.slice(1)},
    ]
  }
""",
  """{id:"face",label:"Face Value",type:"number",placeholder:"1000",min:0,unit:"$",defaultValue:1000},
            {id:"price",label:"Current Market Price",type:"number",placeholder:"950",min:0,unit:"$",defaultValue:950},
            {id:"couponRate",label:"Coupon Rate",type:"number",placeholder:"5",min:0,max:30,step:0.1,unit:"%",defaultValue:5},
            {id:"years",label:"Years to Maturity",type:"number",placeholder:"10",min:0.5,max:50,step:0.5,defaultValue:10},
            {id:"freq",label:"Coupon Frequency",type:"select",options:[{value:"1",label:"Annual"},{value:"2",label:"Semi-annual"},{value:"4",label:"Quarterly"}],defaultValue:"2"}""",
  [("Very Low (<2%)","#ef4444",0,13),("Low (2-4%)","#f59e0b",13,27),("Moderate (4-7%)","#3b82f6",27,47),("High (7%+)","#22c55e",47,100)],
  "% of 15%","100",
  [("What is yield to maturity (YTM)?","YTM is the total return anticipated if you hold the bond until it matures, accounting for current price, coupon payments, and the difference between price and face value. It is the most comprehensive bond yield measure and allows apples-to-apples comparison between different bonds."),
   ("What is the difference between current yield and YTM?","Current yield = Annual coupon / Market price. Simple but ignores price appreciation/depreciation. YTM accounts for the gain/loss from buying at a discount/premium plus all coupon payments. When comparing bonds, always use YTM."),
   ("Why do bond prices move opposite to interest rates?","If rates rise, newly issued bonds offer higher coupons. Your existing bond with a lower coupon becomes less attractive, so its price falls to compensate. If rates fall, your higher-coupon bond becomes more valuable and its price rises. This inverse relationship is fundamental to bond investing."),
   ("What is bond duration?","Duration measures how sensitive a bond price is to interest rate changes. A 10-year duration bond drops ~10% in price if rates rise 1%. Longer maturity and lower coupon = higher duration = more rate sensitivity. Duration helps investors manage interest rate risk."),
   ("What is a bond premium vs discount?","Discount bond: price below face value (market rate > coupon rate). Premium bond: price above face value (market rate < coupon rate). At maturity, you always receive the face value, so discount bonds have built-in capital gains and premium bonds have built-in losses — both reflected in YTM.")],
  [("NPV Calculator","/calculators/npv-calculator"),("Investment Calculator","/calculators/investment-calculator"),("Annuity Calculator","/calculators/annuity-calculator"),("Interest Calculator","/calculators/interest-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Bond Price vs Yield Relationship</h3>
          <div class="text-xs text-blue-800 space-y-1">
            <div class="font-medium">Price ↑ → Yield ↓</div>
            <div class="font-medium">Price ↓ → Yield ↑</div>
            <div class="mt-2 text-blue-700">$1,000 face, 5% coupon bond:</div>
            {[["$950 (discount)","5.53% YTM"],["$1,000 (par)","5.00% YTM"],["$1,050 (premium)","4.50% YTM"]].map(r => (
              <div class="flex justify-between border-b border-blue-100 pb-0.5"><span>{r[0]}</span><span class="font-medium">{r[1]}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Types of Bond Yield</h2>
        <div class="space-y-3">
          {[
            {t:"Current Yield",f:"Annual coupon ÷ Price",d:"Simple but ignores capital gain/loss at maturity"},
            {t:"Yield to Maturity (YTM)",f:"Complex IRR calculation",d:"Total return if held to maturity — the standard for comparison"},
            {t:"Yield to Call (YTC)",f:"Like YTM but to call date",d:"For callable bonds that may be redeemed early by the issuer"},
            {t:"Tax-Equivalent Yield",f:"Muni yield ÷ (1 - tax rate)",d:"Compares tax-free muni bonds to taxable bonds"},
          ].map(y => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-xs text-gray-800">{y.t}</div>
              <div class="text-xs text-blue-600 font-mono">{y.f}</div>
              <div class="text-xs text-gray-600 mt-0.5">{y.d}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Interest Rate Sensitivity (Duration)</h2>
        <p class="text-xs text-gray-600 mb-3">If interest rates rise 1%, approximate price change:</p>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Bond</th><th class="text-right p-2 text-xs font-semibold">Duration</th><th class="text-right p-2 text-xs font-semibold">Price Change</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["2-yr Treasury","~1.9 yrs","−1.9%"],["10-yr Treasury","~8.5 yrs","−8.5%"],["30-yr Treasury","~18 yrs","−18%"],["Zero-coupon 20yr","20 yrs","−20%"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right text-red-600">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "Yield to Maturity","Calculate bond yield, current yield, and yield to maturity")

# ── BREAK EVEN ───────────────────────────────────────────────────────────────
w("break-even","Break-Even Calculator","Financial","financial",
  "Break-Even Calculator: Break-Even Point for Business & Products",
  "Calculate your break-even point in units and revenue. Understand fixed vs variable costs and target profit. Free break-even analysis calculator.",
  """
  const fixedCosts = parseFloat(inputs.fixedCosts)||0
  const pricePerUnit = parseFloat(inputs.pricePerUnit)||0
  const varCostPerUnit = parseFloat(inputs.varCostPerUnit)||0
  const targetProfit = parseFloat(inputs.targetProfit)||0
  if(pricePerUnit<=0) throw new Error("Enter price per unit.")
  if(pricePerUnit<=varCostPerUnit) throw new Error("Price must be higher than variable cost.")
  const contributionMargin = pricePerUnit-varCostPerUnit
  const cmRatio = (contributionMargin/pricePerUnit)*100
  const beUnits = Math.ceil(fixedCosts/contributionMargin)
  const beRevenue = beUnits*pricePerUnit
  const targetUnits = Math.ceil((fixedCosts+targetProfit)/contributionMargin)
  const targetRevenue = targetUnits*pricePerUnit
  return {
    value:beUnits.toLocaleString()+" units",
    gaugeValue:Math.min(cmRatio,100),
    breakdown:["Fixed costs: $"+fixedCosts,"Contribution margin: $"+contributionMargin.toFixed(2)+" ("+cmRatio.toFixed(1)+"%)","Break-even units: "+beUnits,"Break-even revenue: $"+beRevenue.toLocaleString(),"For $"+targetProfit+" profit: "+targetUnits+" units"],
    stats:[
      {label:"Break-Even Units",value:beUnits.toLocaleString()},
      {label:"Break-Even Revenue",value:"$"+beRevenue.toLocaleString()},
      {label:"Contribution Margin",value:cmRatio.toFixed(1)+"%"},
      {label:"Units for Target Profit",value:targetUnits.toLocaleString()},
    ]
  }
""",
  """{id:"fixedCosts",label:"Fixed Costs (monthly)",type:"number",placeholder:"5000",min:0,unit:"$",defaultValue:5000},
            {id:"pricePerUnit",label:"Price Per Unit",type:"number",placeholder:"50",min:0,unit:"$",defaultValue:50},
            {id:"varCostPerUnit",label:"Variable Cost Per Unit",type:"number",placeholder:"20",min:0,unit:"$",defaultValue:20},
            {id:"targetProfit",label:"Target Monthly Profit",type:"number",placeholder:"3000",min:0,unit:"$",defaultValue:3000}""",
  [("High margin (>50%)","#22c55e",50,100),("Good (30-50%)","#3b82f6",30,50),("Moderate (15-30%)","#f59e0b",15,30),("Low (<15%)","#ef4444",0,15)],
  "% margin","100",
  [("What is the break-even point?","The break-even point is the number of units you must sell (or revenue you must generate) to cover all costs — fixed and variable. At this point, profit = $0. Selling more generates profit; selling less generates a loss. It is a fundamental business planning tool."),
   ("What is contribution margin?","Contribution margin = Price - Variable Cost per unit. It is the amount each unit sold contributes toward covering fixed costs and then generating profit. Example: $50 price - $20 variable cost = $30 contribution margin. After covering fixed costs, each additional unit generates $30 profit."),
   ("What are fixed vs variable costs?","Fixed costs stay constant regardless of production volume: rent, insurance, salaries, software subscriptions. Variable costs change with each unit produced: raw materials, packaging, direct labor, shipping. Most businesses have both. Understanding this split is essential for pricing and forecasting."),
   ("How do I reduce my break-even point?","Three approaches: (1) Increase selling price — most powerful but may reduce demand. (2) Reduce variable costs — negotiate better supplier prices, improve processes. (3) Reduce fixed costs — smaller space, fewer subscriptions, automation. Combination approaches work best."),
   ("What is a good contribution margin ratio?","Software: often 70-90% (low variable costs). Manufacturing: 20-40% typical. Retail: 10-30%. Service businesses: 40-70%. There is no universal benchmark — compare within your industry. Higher is better because each dollar of revenue contributes more to covering fixed costs and profit.")],
  [("ROI Calculator","/calculators/roi-calculator"),("Markup Calculator","/calculators/markup-calculator"),("Budget Calculator","/calculators/budget-calculator"),("NPV Calculator","/calculators/npv-calculator")],
  """        <div class="bg-green-50 border border-green-200 rounded-xl p-5">
          <h3 class="font-bold text-green-900 mb-2">Break-Even Formula</h3>
          <div class="text-xs text-green-800 font-mono bg-green-100 rounded p-2 mb-2">BEP = Fixed Costs ÷ (Price - Variable Cost)</div>
          <div class="text-xs text-green-800">Contribution Margin = Price - Variable Cost<br/>CM Ratio = CM ÷ Price × 100</div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Break-Even Sensitivity</h2>
        <p class="text-xs text-gray-600 mb-3">$5,000 fixed costs, $20 variable cost, various prices:</p>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Price</th><th class="text-right p-2 text-xs font-semibold">CM</th><th class="text-right p-2 text-xs font-semibold">BEP Units</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["$30","$10","500"],["$40","$20","250"],["$50","$30","167"],["$75","$55","91"],["$100","$80","63"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right font-medium text-blue-700">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Typical Margin Benchmarks by Industry</h2>
        <div class="space-y-2">
          {[["Software / SaaS","70–90%"],["Professional Services","50–70%"],["Food & Beverage","20–35%"],["Retail","20–40%"],["Manufacturing","20–40%"],["Grocery","1–5%"]].map(([ind,cm]) => (
            <div class="flex justify-between bg-gray-50 rounded px-3 py-1.5 text-xs">
              <span class="text-gray-700">{ind}</span>
              <span class="font-medium text-green-700">{cm} CM ratio</span>
            </div>
          ))}
        </div>
      </div>
    </div>""",
  "Break-Even Units","Calculate break-even point, contribution margin, and target profit units")

print(f"\nWritten: {written} financial pages (apr, annuity, car-lease, cd, capital-gains, bond-yield, break-even)")
