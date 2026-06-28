#!/usr/bin/env python3
"""Generate more financial calculator pages — batch 4."""
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

# ── ESCROW ───────────────────────────────────────────────────────────────────
w("escrow","Escrow Calculator","Financial","financial",
  "Escrow Calculator: Monthly Escrow Payment for Property Tax & Insurance",
  "Calculate your monthly escrow payment for property taxes and homeowners insurance. Free mortgage escrow calculator.",
  """
  const propertyTax = parseFloat(inputs.propertyTax)||0
  const insurance = parseFloat(inputs.insurance)||0
  const pmi = parseFloat(inputs.pmi)||0
  const cushion = parseFloat(inputs.cushion)||2
  const monthlyEscrow = (propertyTax+insurance+pmi)/12
  const cushionAmount = monthlyEscrow*(cushion/12)*12
  const minBalance = monthlyEscrow*2
  const annualTotal = propertyTax+insurance+pmi
  return {
    value:"$"+monthlyEscrow.toFixed(2)+"/mo",
    gaugeValue:Math.min(monthlyEscrow/500*100,100),
    breakdown:["Property tax (annual): $"+propertyTax,"Insurance (annual): $"+insurance,"PMI (annual): $"+pmi,"Monthly escrow: $"+monthlyEscrow.toFixed(2),"Required cushion: $"+cushionAmount.toFixed(2),"Min escrow balance: $"+minBalance.toFixed(2)],
    stats:[
      {label:"Monthly Escrow",value:"$"+monthlyEscrow.toFixed(2)},
      {label:"Annual Total",value:"$"+annualTotal.toFixed(0)},
      {label:"Required Cushion",value:"$"+cushionAmount.toFixed(0)},
      {label:"Min Balance",value:"$"+minBalance.toFixed(0)},
    ]
  }
""",
  """{id:"propertyTax",label:"Annual Property Tax",type:"number",placeholder:"4800",min:0,unit:"$",defaultValue:4800},
            {id:"insurance",label:"Annual Homeowners Insurance",type:"number",placeholder:"1800",min:0,unit:"$",defaultValue:1800},
            {id:"pmi",label:"Annual PMI (if applicable)",type:"number",placeholder:"0",min:0,unit:"$",defaultValue:0},
            {id:"cushion",label:"Escrow Cushion (months)",type:"select",options:[{value:"1",label:"1 month"},{value:"2",label:"2 months (standard)"},{value:"3",label:"3 months"}],defaultValue:"2"}""",
  [("Low (<$200/mo)","#22c55e",0,40),("Moderate ($200-400)","#3b82f6",40,80),("High ($400-600)","#f59e0b",80,100)],
  "% of $500","100",
  [("What is an escrow account for a mortgage?","An escrow account is managed by your lender. Each month, you pay a portion of your annual property tax and homeowners insurance into it. When those bills come due, the lender pays them from the escrow account. It ensures taxes and insurance are always paid."),
   ("Is escrow required?","Most lenders require escrow for conventional loans with less than 20% down payment. FHA and VA loans almost always require escrow. If you have 20%+ equity, you may be able to waive escrow, though some lenders charge a fee for this."),
   ("What is an escrow cushion?","By law (RESPA), lenders can require you to maintain a cushion of up to 2 months of escrow payments as a buffer. This protects against unexpected increases in taxes or insurance. If your escrow is over-funded by more than the allowed cushion, the lender must refund the excess."),
   ("What is an escrow analysis?","Lenders perform an annual escrow analysis to review actual costs vs. estimates. If they underestimated (taxes increased), your monthly payment goes up. If overestimated, you get a refund or credit. Expect your escrow payment to change slightly each year as costs change."),
   ("Can I pay property taxes myself instead of through escrow?","If you have significant equity (usually 20%+) and request to waive escrow, some lenders allow it. You would then be responsible for saving and paying property taxes directly. However, the discipline required is high — many homeowners prefer escrow to avoid a large tax bill surprise.")],
  [("Mortgage Calculator","/calculators/mortgage-calculator"),("PMI Calculator","/calculators/pmi-calculator"),("House Affordability Calculator","/calculators/house-affordability-calculator"),("Down Payment Calculator","/calculators/down-payment-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Typical Escrow Costs</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[["Property tax","1-2% of home value/yr"],["Homeowners insurance","$1,200-2,400/yr avg"],["PMI (if < 20% down)","0.5-1.5% of loan/yr"],["Flood insurance","$700-1,500/yr if req."]].map(([item,cost]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span>{item}</span><span class="font-medium">{cost}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Your Full PITI Monthly Payment</h2>
      <div class="grid md:grid-cols-4 gap-4">
        {[
          {letter:"P",label:"Principal",desc:"Reduces your loan balance"},
          {letter:"I",label:"Interest",desc:"Cost of borrowing"},
          {letter:"T",label:"Taxes",desc:"Property tax via escrow"},
          {letter:"I",label:"Insurance",desc:"Homeowners + PMI via escrow"},
        ].map(c => (
          <div class="bg-gray-50 rounded-xl p-4 text-center">
            <div class="text-2xl font-bold text-blue-600 mb-1">{c.letter}</div>
            <div class="font-semibold text-sm text-gray-800">{c.label}</div>
            <div class="text-xs text-gray-600">{c.desc}</div>
          </div>
        ))}
      </div>
    </div>""",
  "Monthly Escrow","Calculate your monthly escrow for taxes and insurance")

# ── FIRE ──────────────────────────────────────────────────────────────────────
w("fire","FIRE Calculator","Financial","financial",
  "FIRE Calculator: Financial Independence Retire Early Number",
  "Calculate your FIRE number and how long until financial independence. Supports lean FIRE, regular FIRE, and fat FIRE. Free FIRE calculator.",
  """
  const annualExpenses = parseFloat(inputs.annualExpenses)||0
  const currentSavings = parseFloat(inputs.currentSavings)||0
  const annualSavings = parseFloat(inputs.annualSavings)||0
  const returnRate = parseFloat(inputs.returnRate)||7
  const withdrawalRate = parseFloat(inputs.withdrawalRate)||4
  if(annualExpenses<=0) throw new Error("Enter annual expenses.")
  const fireNumber = annualExpenses/(withdrawalRate/100)
  const r = returnRate/100
  let years=0, balance=currentSavings
  while(balance<fireNumber&&years<100){
    balance=balance*(1+r)+annualSavings; years++
  }
  const progress = Math.min((currentSavings/fireNumber)*100,100)
  const lean = annualExpenses*0.75/(withdrawalRate/100)
  const fat = annualExpenses*1.5/(withdrawalRate/100)
  return {
    value:"$"+fireNumber.toLocaleString("en-US",{maximumFractionDigits:0})+" FIRE number",
    gaugeValue:progress,
    breakdown:["Annual expenses: $"+annualExpenses,"FIRE number ("+withdrawalRate+"% rule): $"+fireNumber.toLocaleString("en-US",{maximumFractionDigits:0}),"Current savings: $"+currentSavings.toLocaleString("en-US",{maximumFractionDigits:0}),"Years to FIRE: "+years,"Progress: "+progress.toFixed(1)+"%"],
    stats:[
      {label:"FIRE Number",value:"$"+fireNumber.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Years to FIRE",value:years+" years"},
      {label:"Progress",value:progress.toFixed(1)+"%"},
      {label:"Lean FIRE Number",value:"$"+lean.toLocaleString("en-US",{maximumFractionDigits:0})},
    ]
  }
""",
  """{id:"annualExpenses",label:"Annual Living Expenses",type:"number",placeholder:"60000",min:0,unit:"$",defaultValue:60000},
            {id:"currentSavings",label:"Current Invested Savings",type:"number",placeholder:"100000",min:0,unit:"$",defaultValue:100000},
            {id:"annualSavings",label:"Annual Savings (net, after expenses)",type:"number",placeholder:"30000",min:0,unit:"$",defaultValue:30000},
            {id:"returnRate",label:"Expected Annual Return",type:"number",placeholder:"7",min:0,max:20,step:0.5,unit:"%",defaultValue:7},
            {id:"withdrawalRate",label:"Safe Withdrawal Rate",type:"number",placeholder:"4",min:2,max:6,step:0.25,unit:"%",defaultValue:4}""",
  [("Just Starting","#ef4444",0,10),("Building","#f59e0b",10,40),("Halfway There","#3b82f6",40,75),("FIRE Ready","#22c55e",75,100)],
  "% to FIRE","100",
  [("What is FIRE?","FIRE = Financial Independence, Retire Early. The goal: accumulate enough invested assets so that investment returns cover living expenses indefinitely. The most common approach: save 25x your annual expenses (the 4% rule), then withdraw 4% per year — historically sufficient to last 30+ years without depleting the portfolio."),
   ("What is the 4% rule?","Based on the Trinity Study (1998), withdrawing 4% of a balanced stock/bond portfolio annually has historically sustained portfolios for 30+ years in most historical market scenarios. This gives a FIRE number of 25x annual expenses. Some use 3.5% (28.5x expenses) for more conservative early retirement."),
   ("What is lean FIRE vs fat FIRE?","Lean FIRE: retiring with a minimalist budget (typically $25-40k/year, ~$625k-$1M FIRE number). Regular FIRE: middle-ground lifestyle. Fat FIRE: retiring with a generous budget ($100k+/year, $2.5M+ FIRE number). Coast FIRE: having enough that compound growth alone will reach your number. Barista FIRE: partially FI, working part-time."),
   ("How do I increase my savings rate for FIRE?","Savings rate is the #1 driver of time to FIRE. Going from 10% to 50% savings rate cuts time to FIRE from ~40 years to ~17 years. Focus on the big three: housing (rent/buy cheaper), transportation (drive older car), food (cook at home). Reduce these and you can save 50%+ of income."),
   ("Is the 4% rule still valid?","It remains widely used, but some researchers suggest 3.5% may be safer for very long retirements (40-50 years) given current market valuations. Flexibility helps — if portfolio drops 30%, cut spending 10-20%. Many early retirees also have some part-time income in early retirement years, making the rule more sustainable.")],
  [("Retirement Calculator","/calculators/retirement-calculator"),("Investment Calculator","/calculators/investment-calculator"),("Savings Calculator","/calculators/savings-calculator"),("Budget Calculator","/calculators/budget-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">FIRE Numbers by Spending</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[["$30k/yr (lean)","$750,000"],["$50k/yr","$1,250,000"],["$75k/yr","$1,875,000"],["$100k/yr","$2,500,000"],["$150k/yr (fat)","$3,750,000"]].map(([e,n]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span>{e}</span><span class="font-medium">{n}</span></div>
            ))}
          </div>
          <p class="text-xs text-blue-600 mt-1">Based on 4% safe withdrawal rate (25x rule)</p>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Years to FIRE by Savings Rate</h2>
        <p class="text-xs text-gray-600 mb-3">Assumes 7% return, 4% withdrawal rate, starting from $0:</p>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Savings Rate</th><th class="text-right p-2 text-xs font-semibold">Years to FIRE</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["10%","43 years"],["20%","37 years"],["30%","28 years"],["50%","17 years"],["70%","8.5 years"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-medium text-blue-700">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">FIRE Variants</h2>
        <div class="space-y-3">
          {[
            {t:"Lean FIRE",d:"Minimalist lifestyle. Very low spending. Often requires flexibility or geographic arbitrage (relocating to lower cost areas)."},
            {t:"Regular FIRE",d:"Middle-class lifestyle maintained. Average spending. Most common FIRE goal in the community."},
            {t:"Fat FIRE",d:"Luxury retirement. High spending budget. Requires significantly larger portfolio but offers maximum lifestyle freedom."},
            {t:"Coast FIRE",d:"Invested enough that compound growth alone reaches target by traditional retirement age. Can relax savings and coast."},
            {t:"Barista FIRE",d:"Portfolio covers most expenses. Part-time work covers remainder and benefits. Less accumulation needed."},
          ].map(f => (
            <div class="bg-gray-50 rounded-lg p-2.5">
              <div class="font-semibold text-xs text-blue-700 mb-0.5">{f.t}</div>
              <div class="text-xs text-gray-600">{f.d}</div>
            </div>
          ))}
        </div>
      </div>
    </div>""",
  "FIRE Number","Calculate your financial independence number and years to FIRE")

# ── HOME EQUITY ──────────────────────────────────────────────────────────────
w("home-equity","Home Equity Calculator","Financial","financial",
  "Home Equity Calculator: HELOC & Home Equity Loan Eligibility",
  "Calculate your home equity, loan-to-value ratio, and HELOC borrowing limit. Free home equity calculator.",
  """
  const homeValue = parseFloat(inputs.homeValue)||0
  const mortgageBalance = parseFloat(inputs.mortgageBalance)||0
  const secondMortgage = parseFloat(inputs.secondMortgage)||0
  const maxLtv = parseFloat(inputs.maxLtv)||80
  if(homeValue<=0) throw new Error("Enter home value.")
  const equity = homeValue-mortgageBalance-secondMortgage
  const ltv = ((mortgageBalance+secondMortgage)/homeValue)*100
  const maxBorrow = homeValue*(maxLtv/100)-(mortgageBalance+secondMortgage)
  const availableCredit = Math.max(0,maxBorrow)
  const equityPct = (equity/homeValue)*100
  return {
    value:"$"+equity.toLocaleString("en-US",{maximumFractionDigits:0})+" equity",
    gaugeValue:Math.min(equityPct,100),
    breakdown:["Home value: $"+homeValue.toLocaleString("en-US",{maximumFractionDigits:0}),"Mortgage balance: $"+mortgageBalance.toLocaleString("en-US",{maximumFractionDigits:0}),"Home equity: $"+equity.toLocaleString("en-US",{maximumFractionDigits:0}),"LTV ratio: "+ltv.toFixed(1)+"%","Max HELOC (at "+maxLtv+"% LTV): $"+availableCredit.toLocaleString("en-US",{maximumFractionDigits:0})],
    stats:[
      {label:"Home Equity",value:"$"+equity.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Equity %",value:equityPct.toFixed(1)+"%"},
      {label:"LTV Ratio",value:ltv.toFixed(1)+"%"},
      {label:"Available HELOC",value:"$"+availableCredit.toLocaleString("en-US",{maximumFractionDigits:0})},
    ]
  }
""",
  """{id:"homeValue",label:"Current Home Value",type:"number",placeholder:"450000",min:0,unit:"$",defaultValue:450000},
            {id:"mortgageBalance",label:"First Mortgage Balance",type:"number",placeholder:"280000",min:0,unit:"$",defaultValue:280000},
            {id:"secondMortgage",label:"Second Mortgage Balance",type:"number",placeholder:"0",min:0,unit:"$",defaultValue:0},
            {id:"maxLtv",label:"Max Combined LTV",type:"select",options:[{value:"75",label:"75% (conservative)"},{value:"80",label:"80% (standard)"},{value:"85",label:"85% (some lenders)"},{value:"90",label:"90% (maximum)"}],defaultValue:"80"}""",
  [("Under 20% equity","#ef4444",0,20),("20-40% equity","#f59e0b",20,40),("40-60% equity","#3b82f6",40,60),("60%+ equity","#22c55e",60,100)],
  "% equity","100",
  [("What is home equity?","Home equity = Current home value - All mortgage balances. If your home is worth $450,000 and you owe $280,000, you have $170,000 in equity. Equity grows as you pay down the mortgage and as home values appreciate. It is your ownership stake in the property."),
   ("What is a HELOC and how does it work?","A HELOC (Home Equity Line of Credit) is a revolving credit line secured by your home, similar to a credit card. You draw from it during the draw period (5-10 years), then repay during the repayment period (10-20 years). Interest is variable. Rates are typically much lower than personal loans or credit cards."),
   ("How much can I borrow against my home equity?","Most lenders allow combined LTV (your mortgage + HELOC) up to 80-85% of home value. If your home is worth $450k and you owe $280k, and the lender allows 80% CLTV: $450k x 80% = $360k max combined. $360k - $280k mortgage = $80k available HELOC."),
   ("HELOC vs home equity loan: which is better?","HELOC: variable rate, flexible draw (use only what you need), better for ongoing projects. Home equity loan: fixed rate, lump sum, predictable payments, better for one-time expenses. HELOC is more common. Both use your home as collateral — default risks foreclosure."),
   ("What can I use home equity for?","Home improvements (often tax-deductible interest), debt consolidation (caution: converts unsecured to secured debt), college, emergencies. Not recommended: vacations, luxury purchases, investing in stocks (double risk — if market drops, home could be at risk too). Use equity loans for value-adding purposes only.")],
  [("Mortgage Calculator","/calculators/mortgage-calculator"),("Refinance Calculator","/calculators/refinance-calculator"),("PMI Calculator","/calculators/pmi-calculator"),("Net Worth Calculator","/calculators/net-worth-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">HELOC vs Home Equity Loan</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[["Rate","Variable","Fixed"],["Structure","Line of credit","Lump sum"],["Payments","Interest-only (draw)","Fixed P+I"],["Flexibility","Draw what you need","Set amount"],["Best for","Ongoing projects","One-time expense"]].map(([f,h,he]) => (
              <div class="grid grid-cols-3 gap-1 border-b border-blue-100 pb-1">
                <span class="font-medium">{f}</span><span>{h} (HELOC)</span><span>{he} (HEL)</span>
              </div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Home Equity Growth Over Time</h2>
        <p class="text-xs text-gray-600 mb-3">$400k home, $320k mortgage (7%, 30yr), 4% annual appreciation:</p>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Year</th><th class="text-right p-2 text-xs font-semibold">Home Value</th><th class="text-right p-2 text-xs font-semibold">Equity</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Now","$400k","$80k"],["5 yrs","$486k","$174k"],["10 yrs","$592k","$305k"],["15 yrs","$720k","$487k"],["20 yrs","$876k","$720k"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right font-medium text-green-700">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Ways to Build Equity Faster</h2>
        <div class="space-y-2">
          {["Make bi-weekly mortgage payments (one extra payment per year)","Apply windfalls (bonuses, tax refunds) to principal","Choose a 15-year mortgage for faster equity build","Make extra principal-only payments whenever possible","Buy in an appreciating area (location is the biggest driver)","Improve the property to increase appraised value"].map(t => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{t}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Home Equity","Calculate your home equity and available HELOC credit")

# ── HOUSE AFFORDABILITY ──────────────────────────────────────────────────────
w("house-affordability","House Affordability Calculator","Financial","financial",
  "House Affordability Calculator: How Much Home Can I Afford?",
  "Calculate how much house you can afford based on income, debt, and down payment. Uses DTI guidelines. Free home affordability calculator.",
  """
  const grossIncome = parseFloat(inputs.grossIncome)||0
  const monthlyDebt = parseFloat(inputs.monthlyDebt)||0
  const downPayment = parseFloat(inputs.downPayment)||40000
  const rate = parseFloat(inputs.rate)||7
  const term = parseInt(inputs.term)||30
  const propertyTax = parseFloat(inputs.propertyTax)||1.2
  const insurance = parseFloat(inputs.insurance)||1200
  if(grossIncome<=0) throw new Error("Enter annual income.")
  const monthlyIncome = grossIncome/12
  const maxDti = 0.43
  const maxHousingDti = 0.28
  const maxTotalPayment = monthlyIncome*maxDti-monthlyDebt
  const maxHousingPayment = Math.min(maxTotalPayment,monthlyIncome*maxHousingDti)
  const r=rate/100/12, n=term*12
  const monthlyInsurance=insurance/12
  const pAndI = maxHousingPayment-monthlyInsurance
  const loanAmount = pAndI*(Math.pow(1+r,n)-1)/(r*Math.pow(1+r,n))
  const maxHomePrice = loanAmount+downPayment
  const taxMonthly = maxHomePrice*(propertyTax/100)/12
  const adjustedPandI = maxHousingPayment-monthlyInsurance-taxMonthly
  const adjustedLoan = adjustedPandI*(Math.pow(1+r,n)-1)/(r*Math.pow(1+r,n))
  const finalPrice = Math.max(0,adjustedLoan+downPayment)
  return {
    value:"$"+finalPrice.toLocaleString("en-US",{maximumFractionDigits:0}),
    gaugeValue:Math.min(finalPrice/1000000*100,100),
    breakdown:["Annual income: $"+grossIncome,"Monthly income: $"+monthlyIncome.toFixed(0),"Max DTI payment: $"+maxHousingPayment.toFixed(0),"Down payment: $"+downPayment,"Estimated home price: $"+finalPrice.toLocaleString("en-US",{maximumFractionDigits:0})],
    stats:[
      {label:"Affordable Home Price",value:"$"+finalPrice.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Down Payment",value:"$"+downPayment.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Max Housing Payment",value:"$"+maxHousingPayment.toFixed(0)+"/mo"},
      {label:"Loan Amount",value:"$"+adjustedLoan.toLocaleString("en-US",{maximumFractionDigits:0})},
    ]
  }
""",
  """{id:"grossIncome",label:"Annual Gross Income",type:"number",placeholder:"100000",min:0,unit:"$",defaultValue:100000},
            {id:"monthlyDebt",label:"Existing Monthly Debt Payments",type:"number",placeholder:"500",min:0,unit:"$",defaultValue:500},
            {id:"downPayment",label:"Down Payment Available",type:"number",placeholder:"40000",min:0,unit:"$",defaultValue:40000},
            {id:"rate",label:"Mortgage Rate",type:"number",placeholder:"7",min:0,max:15,step:0.1,unit:"%",defaultValue:7},
            {id:"term",label:"Loan Term",type:"select",options:[{value:"15",label:"15 years"},{value:"20",label:"20 years"},{value:"30",label:"30 years"}],defaultValue:"30"},
            {id:"propertyTax",label:"Property Tax Rate",type:"number",placeholder:"1.2",min:0,max:3,step:0.1,unit:"%",defaultValue:1.2},
            {id:"insurance",label:"Annual Homeowners Insurance",type:"number",placeholder:"1200",min:0,unit:"$",defaultValue:1200}""",
  [("Starter (<$250k)","#3b82f6",0,25),("Mid-range ($250-600k)","#22c55e",25,60),("Luxury ($600k-$1M)","#f59e0b",60,100)],
  "% of $1M","100",
  [("How much house can I afford on my income?","The standard guideline: your total housing payment (PITI) should not exceed 28% of gross monthly income (front-end DTI). All debt payments combined should not exceed 36-43% (back-end DTI). On $100k salary: max housing payment ~$2,333/month, which supports roughly a $350-400k home with 10% down at 7%."),
   ("What is the 28/36 rule for home buying?","The 28/36 rule: spend no more than 28% of gross monthly income on housing (principal, interest, taxes, insurance), and no more than 36% on all debt combined. More generous modern guidelines use 28/43 or 36/50 for well-qualified buyers. The rule is a starting point — actual affordability depends on your full financial picture."),
   ("What income do I need for a $400,000 house?","At 7% rate, 30-year loan, 20% down on a $400k home: monthly PITI ~$2,500-2,700. Using 28% rule: need ~$9,300/month ($112k/year) gross income. Using the 43% back-end with no other debt: could qualify on ~$6,300/month ($75k/year), but it would be tight. Higher down payment reduces income needed."),
   ("How does debt affect home buying power?","Existing debt directly reduces how much house you can afford. $500/month in car and student loan payments removes roughly $60-80k from your affordable home price. Paying off debt before buying can dramatically increase your budget. This is why mortgage lenders look at back-end DTI carefully."),
   ("Should I stretch my budget to buy more house?","Generally no. Being house-poor — spending 40%+ of income on housing — creates financial stress and prevents savings and investing. A smaller home you can comfortably afford is better than a larger one that keeps you from building wealth. Leave room for emergency savings, retirement contributions, and life expenses.")],
  [("Mortgage Calculator","/calculators/mortgage-calculator"),("Debt-to-Income Calculator","/calculators/debt-to-income-calculator"),("Down Payment Calculator","/calculators/down-payment-calculator"),("Budget Calculator","/calculators/budget-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Affordability by Income (7% rate, 30yr, 20% down)</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700 border-b border-blue-200"><th class="text-left pb-1">Annual Income</th><th class="text-right pb-1">Affordable Home</th></tr></thead>
            <tbody class="text-blue-900">
              {[["$60,000","~$200,000"],["$80,000","~$275,000"],["$100,000","~$340,000"],["$150,000","~$510,000"],["$200,000","~$680,000"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right font-medium">{r[1]}</td></tr>
              ))}
            </tbody>
          </table>
          <p class="text-xs text-blue-600 mt-1">Assumes no other debt, 28% front-end DTI</p>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">What Impacts Your Buying Power?</h2>
        <div class="space-y-3">
          {[
            {factor:"Income",impact:"Every $10k more income adds ~$35-50k buying power"},
            {factor:"Down Payment",impact:"$10k more down = ~$10k more home (less = more loan)"},
            {factor:"Interest Rate",impact:"1% higher rate cuts buying power by ~10%"},
            {factor:"Existing Debt",impact:"$500/mo more debt = ~$60k less home"},
            {factor:"Loan Term",impact:"15yr vs 30yr: higher payment, 20% more buying power vs same payment"},
          ].map(f => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-xs text-blue-700">{f.factor}</div>
              <div class="text-xs text-gray-600 mt-0.5">{f.impact}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Hidden Costs of Homeownership</h2>
        <div class="space-y-2">
          {[["Property taxes","1-2% of home value/year"],["Homeowners insurance","$1,500-3,000/year"],["HOA fees","$0-500+/month"],["Maintenance","1% of home value/year"],["Utilities","$200-400+/month more than renting"],["PMI (< 20% down)","$100-400/month"]].map(([cost,amount]) => (
            <div class="flex justify-between bg-gray-50 rounded px-3 py-1.5 text-xs">
              <span class="text-gray-700">{cost}</span>
              <span class="font-medium text-gray-800">{amount}</span>
            </div>
          ))}
        </div>
      </div>
    </div>""",
  "Affordable Home Price","Calculate how much house you can afford based on income and DTI")

# ── INCOME TAX ────────────────────────────────────────────────────────────────
w("income-tax","Income Tax Calculator","Financial","financial",
  "Income Tax Calculator 2025: Federal Tax Estimate",
  "Estimate your 2025 federal income tax liability based on taxable income and filing status. Includes brackets and effective rate. Free income tax calculator.",
  """
  const income = parseFloat(inputs.income)||0
  const deductions = parseFloat(inputs.deductions)||0
  const filing = inputs.filing||"single"
  const credits = parseFloat(inputs.credits)||0
  if(income<=0) throw new Error("Enter annual income.")
  const standardDeduction = filing==="married"?30000:15000
  const deductionUsed = Math.max(deductions||0,standardDeduction)
  const taxableIncome = Math.max(0,income-deductionUsed)
  const brackets = filing==="married"
    ?[[0,23200,0.10],[23200,94300,0.12],[94300,201050,0.22],[201050,383900,0.24],[383900,487450,0.32],[487450,731200,0.35],[731200,Infinity,0.37]]
    :[[0,11600,0.10],[11600,47150,0.12],[47150,100525,0.22],[100525,191950,0.24],[191950,243725,0.32],[243725,609350,0.35],[609350,Infinity,0.37]]
  let tax=0, remaining=taxableIncome
  for(const [low,high,rate] of brackets){
    if(remaining<=0) break
    const taxable=Math.min(remaining,(high===Infinity?remaining:high)-low)
    tax+=taxable*rate; remaining-=taxable
  }
  tax=Math.max(0,tax-credits)
  const effectiveRate = income>0?(tax/income)*100:0
  const marginalRate = brackets.find(([l,h])=>taxableIncome>=l&&taxableIncome<h)?.[2]*100||37
  const afterTaxIncome = income-tax
  return {
    value:"$"+tax.toLocaleString("en-US",{maximumFractionDigits:0})+" tax",
    gaugeValue:Math.min(effectiveRate*2,100),
    breakdown:["Gross income: $"+income.toLocaleString("en-US",{maximumFractionDigits:0}),"Deductions: $"+deductionUsed,"Taxable income: $"+taxableIncome.toLocaleString("en-US",{maximumFractionDigits:0}),"Federal tax: $"+tax.toLocaleString("en-US",{maximumFractionDigits:0}),"Effective rate: "+effectiveRate.toFixed(2)+"%","Marginal rate: "+marginalRate+"%"],
    stats:[
      {label:"Federal Tax",value:"$"+tax.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Effective Rate",value:effectiveRate.toFixed(2)+"%"},
      {label:"Marginal Rate",value:marginalRate+"%"},
      {label:"After-Tax Income",value:"$"+afterTaxIncome.toLocaleString("en-US",{maximumFractionDigits:0})},
    ]
  }
""",
  """{id:"income",label:"Annual Gross Income",type:"number",placeholder:"75000",min:0,unit:"$",defaultValue:75000},
            {id:"filing",label:"Filing Status",type:"select",options:[{value:"single",label:"Single"},{value:"married",label:"Married Filing Jointly"}],defaultValue:"single"},
            {id:"deductions",label:"Itemized Deductions (leave 0 for standard)",type:"number",placeholder:"0",min:0,unit:"$",defaultValue:0},
            {id:"credits",label:"Tax Credits",type:"number",placeholder:"0",min:0,unit:"$",defaultValue:0}""",
  [("10-12% effective","#22c55e",0,25),("22-24% effective","#3b82f6",25,50),("32-35% effective","#f59e0b",50,70),("37%+ effective","#ef4444",70,100)],
  "% effective rate (×2)","100",
  [("What is the difference between marginal and effective tax rate?","Marginal rate is the rate on your last dollar of income (your tax bracket). Effective rate is total taxes paid divided by total income. Example: $75k income (single) pays ~$10,000 in taxes. Marginal rate = 22%, but effective rate = ~13.3%. The US uses a progressive system — lower income is taxed at lower rates first."),
   ("What is the 2025 standard deduction?","$15,000 for single filers, $30,000 for married filing jointly, $22,500 for head of household. If your itemized deductions (mortgage interest, state taxes, charity, medical) exceed these amounts, itemize. Otherwise, take the standard deduction — about 90% of taxpayers do."),
   ("What are the 2025 tax brackets for single filers?","10% on income up to $11,600; 12% on $11,600-$47,150; 22% on $47,150-$100,525; 24% on $100,525-$191,950; 32% on $191,950-$243,725; 35% on $243,725-$609,350; 37% above $609,350. Note: these brackets are indexed for inflation annually."),
   ("How can I legally reduce my tax bill?","Maximize 401(k) contributions (up to $23,500 in 2025, pre-tax reduces taxable income). Contribute to HSA ($4,300 single, $8,550 family). Harvest tax losses in investment accounts. Bunch charitable deductions into alternating years to itemize. Use FSA for healthcare and dependent care. Business owners have additional options."),
   ("Does this calculator include state income tax?","No — this calculator estimates federal income tax only. State income taxes vary: from 0% (TX, FL, WA, NV, WY, SD, AK) to over 13% (CA). Add your state income tax to get your total tax burden. Most people also pay 7.65% in FICA taxes (Social Security + Medicare) on earned income.")],
  [("Capital Gains Calculator","/calculators/capital-gains-calculator"),("Paycheck Calculator","/calculators/paycheck-calculator"),("Salary Calculator","/calculators/salary-calculator"),("Budget Calculator","/calculators/budget-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">2025 Federal Brackets (Single)</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700 border-b border-blue-200"><th class="text-left pb-1">Taxable Income</th><th class="text-right pb-1">Rate</th></tr></thead>
            <tbody class="text-blue-900">
              {[["$0–$11,600","10%"],["$11,601–$47,150","12%"],["$47,151–$100,525","22%"],["$100,526–$191,950","24%"],["$191,951–$243,725","32%"],["$243,726–$609,350","35%"],["Over $609,350","37%"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right font-medium">{r[1]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Effective Tax Rate by Income (Single, 2025)</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Income</th><th class="text-right p-2 text-xs font-semibold">Federal Tax</th><th class="text-right p-2 text-xs font-semibold">Effective Rate</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["$40,000","$3,524","8.8%"],["$75,000","$9,900","13.2%"],["$100,000","$15,432","15.4%"],["$150,000","$27,432","18.3%"],["$250,000","$56,124","22.4%"],["$500,000","$148,574","29.7%"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right font-medium text-red-600">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
        <p class="text-xs text-gray-500 mt-1">Standard deduction applied. Federal only — excludes state and FICA.</p>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Top Tax Reduction Strategies</h2>
        <div class="space-y-2">
          {[["401(k) / 403(b)","Up to $23,500 pre-tax reduces AGI"],["Traditional IRA","Up to $7,000 if eligible"],["HSA","$4,300 individual — triple tax advantage"],["Itemize deductions","If mortgage interest + SALT + charity > $15k"],["Business deductions","Home office, vehicle, equipment if self-employed"],["Tax-loss harvesting","Sell losing investments to offset gains"]].map(([s,d]) => (
            <div class="bg-gray-50 rounded-lg p-2.5">
              <div class="font-semibold text-xs text-gray-800">{s}</div>
              <div class="text-xs text-gray-600">{d}</div>
            </div>
          ))}
        </div>
      </div>
    </div>""",
  "Federal Tax Owed","Estimate your 2025 federal income tax and effective tax rate")

print(f"\nWritten: {written} pages")
