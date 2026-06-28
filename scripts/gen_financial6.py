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

# ── REFINANCE ─────────────────────────────────────────────────────────────────
w("refinance","Refinance Calculator","Financial","financial",
  "Refinance Calculator: Should I Refinance My Mortgage?",
  "Calculate your monthly savings, break-even period, and lifetime savings from refinancing your mortgage. Free refinance calculator.",
  """
  const currentBalance = parseFloat(inputs.currentBalance)||0
  const currentRate = parseFloat(inputs.currentRate)||7
  const currentPayment = parseFloat(inputs.currentPayment)||0
  const newRate = parseFloat(inputs.newRate)||6
  const term = parseInt(inputs.term)||30
  const closingCosts = parseFloat(inputs.closingCosts)||5000
  if(currentBalance<=0) throw new Error("Enter remaining loan balance.")
  const r=newRate/100/12, n=term*12
  const newPayment = currentBalance*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1)
  const cp = currentPayment||currentBalance*(currentRate/100/12)
  const monthlySavings = cp-newPayment
  const breakEvenMonths = monthlySavings>0?Math.ceil(closingCosts/monthlySavings):Infinity
  const beYears=Math.floor(breakEvenMonths/12), beMo=breakEvenMonths%12
  const lifetimeSavings = monthlySavings*n-closingCosts
  return {
    value:"$"+monthlySavings.toFixed(2)+"/mo savings",
    gaugeValue:Math.min(monthlySavings/500*100,100),
    breakdown:["New monthly payment: $"+newPayment.toFixed(2),"Monthly savings: $"+monthlySavings.toFixed(2),"Closing costs: $"+closingCosts,"Break-even: "+beYears+"y "+beMo+"mo","Lifetime savings: $"+lifetimeSavings.toLocaleString("en-US",{maximumFractionDigits:0})],
    stats:[
      {label:"Monthly Savings",value:"$"+monthlySavings.toFixed(2)},
      {label:"New Payment",value:"$"+newPayment.toFixed(2)},
      {label:"Break-Even",value:beYears+"y "+beMo+"mo"},
      {label:"Lifetime Net Savings",value:"$"+lifetimeSavings.toLocaleString("en-US",{maximumFractionDigits:0})},
    ]
  }
""",
  """{id:"currentBalance",label:"Remaining Loan Balance",type:"number",placeholder:"280000",min:0,unit:"$",defaultValue:280000},
            {id:"currentRate",label:"Current Interest Rate",type:"number",placeholder:"7.5",min:0,max:20,step:0.1,unit:"%",defaultValue:7.5},
            {id:"currentPayment",label:"Current Monthly Payment (P+I)",type:"number",placeholder:"0",min:0,unit:"$",defaultValue:0},
            {id:"newRate",label:"New Interest Rate",type:"number",placeholder:"6.5",min:0,max:20,step:0.1,unit:"%",defaultValue:6.5},
            {id:"term",label:"New Loan Term",type:"select",options:[{value:"10",label:"10 years"},{value:"15",label:"15 years"},{value:"20",label:"20 years"},{value:"30",label:"30 years"}],defaultValue:"30"},
            {id:"closingCosts",label:"Estimated Closing Costs",type:"number",placeholder:"5000",min:0,unit:"$",defaultValue:5000}""",
  [("Great savings (>$400/mo)","#22c55e",75,100),("Good ($200-400/mo)","#3b82f6",40,75),("Modest ($100-200/mo)","#f59e0b",20,40),("Minimal (<$100/mo)","#ef4444",0,20)],
  "% savings","100",
  [("When does it make sense to refinance?","Key factors: 1) Rate reduction: at least 0.5-1% lower rate typically needed. 2) Break-even period: under 3-5 years ideally — if you sell or move before break-even, you lose money on closing costs. 3) Time remaining: refinancing deep into a loan may not make sense (most interest already paid in early years)."),
   ("What are typical refinancing closing costs?","Usually 2-5% of the loan amount: $4,000-$14,000 on a $280k loan. Includes: origination fee (0.5-1%), appraisal ($300-500), title insurance ($700-2,000), attorney fees, recording fees, and prepaid items (insurance, taxes). Some lenders offer no-closing-cost refis with slightly higher rates."),
   ("What is a no-closing-cost refinance?","The lender pays closing costs in exchange for a higher interest rate (usually 0.125-0.25% higher). This makes sense if: you plan to sell/refinance again within a few years, you lack cash for closing costs, or the rate is still significantly lower than your current rate. Calculate both options."),
   ("Should I reset to a 30-year mortgage when refinancing?","Resetting extends your payoff date. Example: 20 years left on original, refinancing into another 30-year means 30 more years instead of 20. Consider a 15 or 20-year term to maintain payoff timeline while getting a lower rate. Or keep making the same payment on the new loan to pay it off faster."),
   ("How often can you refinance?","Technically, you can refinance as soon as the math makes sense. Most lenders require 6 months of seasoning (payments) before refinancing. Repeat refinancing can cost you long-term if closing costs eat the savings. Focus on lifetime savings, not just monthly payment reduction.")],
  [("Mortgage Calculator","/calculators/mortgage-calculator"),("Mortgage Points Calculator","/calculators/mortgage-points-calculator"),("House Affordability Calculator","/calculators/house-affordability-calculator"),("APR Calculator","/calculators/apr-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Refinance Decision Checklist</h3>
          <div class="space-y-1 text-xs text-blue-800">
            <div>✓ Rate reduction of 0.5%+ from current</div>
            <div>✓ Break-even under 3-5 years</div>
            <div>✓ Plan to stay past break-even</div>
            <div>✓ Good credit score (740+ for best rates)</div>
            <div>✓ Sufficient home equity (20%+ avoids PMI)</div>
            <div>✗ Skip if moving within 2 years</div>
          </div>
        </div>""",
  """    <div class="mt-10">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Rate Reduction vs Monthly Savings ($280k balance)</h2>
      <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
        <thead class="bg-gray-50"><tr><th class="text-left p-3 text-xs font-semibold">Rate Drop</th><th class="text-right p-3 text-xs font-semibold">Monthly Savings</th><th class="text-right p-3 text-xs font-semibold">Annual Savings</th><th class="text-right p-3 text-xs font-semibold">Break-Even ($5k costs)</th></tr></thead>
        <tbody class="divide-y divide-gray-100">
          {[["0.25%","~$44","-$533","~9.4 years"],["0.5%","~$88","$1,059","~4.7 years"],["0.75%","~$132","$1,584","~3.2 years"],["1.0%","~$175","$2,104","~2.4 years"],["1.5%","~$262","$3,144","~1.6 years"]].map(r => (
            <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right text-green-600 font-medium">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td><td class="p-2 text-xs text-right">{r[3]}</td></tr>
          ))}
        </tbody>
      </table>
    </div>""",
  "Monthly Savings","Calculate monthly savings and break-even for mortgage refinancing")

# ── RENT VS BUY ───────────────────────────────────────────────────────────────
w("rent-vs-buy","Rent vs Buy Calculator","Financial","financial",
  "Rent vs Buy Calculator: Is It Better to Rent or Buy?",
  "Compare the true cost of renting vs buying a home over time, including opportunity cost and home appreciation. Free rent vs buy calculator.",
  """
  const homePrice = parseFloat(inputs.homePrice)||400000
  const downPct = parseFloat(inputs.downPct)||20
  const mortgageRate = parseFloat(inputs.mortgageRate)||7
  const monthlyRent = parseFloat(inputs.monthlyRent)||2000
  const rentIncrease = parseFloat(inputs.rentIncrease)||3
  const homeAppreciation = parseFloat(inputs.homeAppreciation)||4
  const investReturn = parseFloat(inputs.investReturn)||7
  const years = parseInt(inputs.years)||10
  if(homePrice<=0||monthlyRent<=0) throw new Error("Enter home price and rent.")
  const downPayment = homePrice*(downPct/100)
  const loanAmount = homePrice-downPayment
  const r=mortgageRate/100/12, n=360
  const payment = loanAmount*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1)
  const propTaxMonthly = homePrice*0.012/12
  const insuranceMonthly = 150
  const maintenanceMonthly = homePrice*0.01/12
  const totalBuyCost = (payment+propTaxMonthly+insuranceMonthly+maintenanceMonthly)*years*12
  const futureHomeValue = homePrice*Math.pow(1+homeAppreciation/100,years)
  let bal=loanAmount
  for(let m=0;m<years*12;m++){const int=bal*r;const prin=payment-int;bal-=prin}
  const buyEquity = futureHomeValue-Math.max(0,bal)
  const totalRentPaid = monthlyRent*((Math.pow(1+rentIncrease/100/12,years*12)-1)/(rentIncrease/100/12))*((rentIncrease/100/12)?1:years*12)
  const downInvested = downPayment*Math.pow(1+investReturn/100,years)
  const netRent = totalRentPaid+downPayment-downInvested
  const buyWins = buyEquity-totalBuyCost>0
  return {
    value:buyEquity>totalRentPaid?"Buying builds more wealth":"Renting may be better short-term",
    gaugeValue:Math.min((buyEquity/(homePrice))*100,100),
    breakdown:["Monthly buy cost: $"+(payment+propTaxMonthly+insuranceMonthly+maintenanceMonthly).toFixed(0),"Monthly rent: $"+monthlyRent,"Future home value: $"+futureHomeValue.toLocaleString("en-US",{maximumFractionDigits:0}),"Equity after "+years+"yr: $"+buyEquity.toLocaleString("en-US",{maximumFractionDigits:0}),"Total rent paid: $"+totalRentPaid.toLocaleString("en-US",{maximumFractionDigits:0})],
    stats:[
      {label:"Monthly Buy Cost",value:"$"+(payment+propTaxMonthly+insuranceMonthly+maintenanceMonthly).toFixed(0)},
      {label:"Future Home Value",value:"$"+futureHomeValue.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Home Equity at "+years+"yr",value:"$"+buyEquity.toLocaleString("en-US",{maximumFractionDigits:0})},
      {label:"Total Rent Paid",value:"$"+totalRentPaid.toLocaleString("en-US",{maximumFractionDigits:0})},
    ]
  }
""",
  """{id:"homePrice",label:"Home Purchase Price",type:"number",placeholder:"400000",min:0,unit:"$",defaultValue:400000},
            {id:"downPct",label:"Down Payment %",type:"select",options:[{value:"5",label:"5%"},{value:"10",label:"10%"},{value:"20",label:"20%"},{value:"25",label:"25%"}],defaultValue:"20"},
            {id:"mortgageRate",label:"Mortgage Rate",type:"number",placeholder:"7",min:0,max:15,step:0.1,unit:"%",defaultValue:7},
            {id:"monthlyRent",label:"Current Monthly Rent",type:"number",placeholder:"2000",min:0,unit:"$",defaultValue:2000},
            {id:"rentIncrease",label:"Annual Rent Increase",type:"number",placeholder:"3",min:0,max:10,step:0.5,unit:"%",defaultValue:3},
            {id:"homeAppreciation",label:"Annual Home Appreciation",type:"number",placeholder:"4",min:0,max:15,step:0.5,unit:"%",defaultValue:4},
            {id:"investReturn",label:"Investment Return (if renting)",type:"number",placeholder:"7",min:0,max:15,step:0.5,unit:"%",defaultValue:7},
            {id:"years",label:"Years to Compare",type:"number",placeholder:"10",min:1,max:30,unit:"years",defaultValue:10}""",
  [("Strong buy case","#22c55e",75,100),("Moderate buy","#3b82f6",50,75),("Moderate rent","#f59e0b",25,50),("Strong rent case","#ef4444",0,25)],
  "% equity/price","100",
  [("Is it always better to buy than rent?","No. The answer depends on: how long you stay (buying wins with longer holds), your market (high price-to-rent ratio cities favor renting), opportunity cost of the down payment, home appreciation, transaction costs, and lifestyle flexibility. In very expensive markets, renting and investing the difference can beat buying."),
   ("What is the price-to-rent ratio?","Price-to-rent ratio = Home price / Annual rent. Under 15: strongly favors buying. 15-20: leans toward buying. 20-25: could go either way. Over 25: often favors renting. In San Francisco or NYC, ratios of 40-50+ are common — renting and investing the savings may be financially smarter in those markets."),
   ("How long do I need to stay for buying to make sense?","Transaction costs (closing costs 2-5% when buying, 6-8% when selling) are the main hurdle. You typically need to stay at least 3-5 years to offset these costs and build enough equity. The longer you stay, the more buying makes sense. If you might move in 2-3 years, renting is often better."),
   ("What is the true cost of homeownership?","Mortgage payment is just the start. Add: property taxes (1-2% of value annually), homeowners insurance ($1,500+/year), maintenance and repairs (1-2% of value annually), HOA fees if applicable, and opportunity cost of the down payment. True ownership cost is often 40-50% more than the mortgage payment alone."),
   ("Should I rent and invest the difference?","If monthly rent is significantly less than buying costs, invest the difference in index funds. The math depends on home appreciation vs. stock market returns. Historically, stocks have returned more than real estate long-term, but a home provides leverage, tax benefits, forced savings, and housing stability that pure investments do not.")],
  [("Mortgage Calculator","/calculators/mortgage-calculator"),("House Affordability Calculator","/calculators/house-affordability-calculator"),("Investment Calculator","/calculators/investment-calculator"),("Net Worth Calculator","/calculators/net-worth-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Price-to-Rent Ratio Guide</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[["Under 15","Strongly favors buying"],["15–20","Leans toward buying"],["20–25","Could go either way"],["Over 25","Leans toward renting"],["Over 35","Strongly favors renting"]].map(([r,d]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span class="font-medium">{r}</span><span>{d}</span></div>
            ))}
          </div>
          <p class="text-xs text-blue-600 mt-1">Price/Annual Rent = Ratio</p>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">True Monthly Cost of Ownership</h2>
        <p class="text-xs text-gray-600 mb-3">$400,000 home, 7% rate, 20% down:</p>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Cost Component</th><th class="text-right p-2 text-xs font-semibold">Monthly</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Mortgage (P+I)","$2,129"],["Property tax (1.2%)","$400"],["Homeowners insurance","$125"],["Maintenance (1%)","$333"],["Total","$2,987"]].map(([c,a]) => (
              <tr class={c==="Total"?"bg-blue-50 font-semibold":""}><td class="p-2 text-xs">{c}</td><td class="p-2 text-xs text-right">{a}</td></tr>
            ))}
          </tbody>
        </table>
        <p class="text-xs text-gray-500 mt-1">Not including HOA or PMI</p>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Factors Favoring Renting</h2>
        <div class="space-y-2">
          {["High price-to-rent ratio (over 25) in your market","Planning to move within 3-5 years","Career or life changes likely in the near term","No emergency fund beyond down payment","Real estate prices appear at a cyclical peak","The flexibility of renting fits your lifestyle better","You can invest the rent/buy payment difference at better returns"].map(t => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-orange-500 mt-0.5">•</span><span>{t}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Rent vs Buy Analysis","Compare long-term cost of renting vs buying a home")

# ── RULE OF 72 ────────────────────────────────────────────────────────────────
w("rule-of-72","Rule of 72 Calculator","Financial","financial",
  "Rule of 72 Calculator: Doubling Time for Investments",
  "Calculate how long to double your investment using the Rule of 72. Find required rate for any doubling time. Free Rule of 72 calculator.",
  """
  const rate = parseFloat(inputs.rate)||0
  const years = parseFloat(inputs.years)||0
  if(rate>0){
    const doublingYears = 72/rate
    const exact = Math.log(2)/Math.log(1+rate/100)
    const error = Math.abs(doublingYears-exact)/exact*100
    return {
      value:doublingYears.toFixed(1)+" years to double",
      gaugeValue:Math.min(100-doublingYears*2,100),
      breakdown:["Rate: "+rate+"%","Rule of 72 estimate: "+doublingYears.toFixed(2)+" years","Exact calculation: "+exact.toFixed(2)+" years","Approximation error: "+error.toFixed(2)+"%","At 20yr: $10k → $"+(10000*Math.pow(2,20/doublingYears)).toFixed(0)],
      stats:[
        {label:"Years to Double",value:doublingYears.toFixed(1)},
        {label:"Exact Answer",value:exact.toFixed(2)+" yrs"},
        {label:"Approximation Error",value:error.toFixed(2)+"%"},
        {label:"Doubles in 20yr",value:(20/doublingYears).toFixed(1)+"x"},
      ]
    }
  } else if(years>0){
    const reqRate = 72/years
    return {
      value:reqRate.toFixed(2)+"% rate needed",
      gaugeValue:Math.min(reqRate*3,100),
      breakdown:["Desired doubling time: "+years+" years","Required rate (Rule of 72): "+reqRate.toFixed(2)+"%"],
      stats:[
        {label:"Required Rate",value:reqRate.toFixed(2)+"%"},
        {label:"Target Years",value:years},
        {label:"Est. Quadruple",value:(years*2)+" years"},
        {label:"Est. 8x growth",value:(years*3)+" years"},
      ]
    }
  }
  throw new Error("Enter either rate or desired years.")
""",
  """{id:"rate",label:"Annual Return Rate (leave 0 to find required rate)",type:"number",placeholder:"7",min:0,max:50,step:0.5,unit:"%",defaultValue:7},
            {id:"years",label:"Desired Years to Double (leave 0 if entering rate)",type:"number",placeholder:"0",min:0,max:100,unit:"years",defaultValue:0}""",
  [("Doubles quickly <5yr","#22c55e",0,30),("5-10 year double","#3b82f6",30,60),("10-20 year double","#f59e0b",60,85),("Slow double >20yr","#ef4444",85,100)],
  "% speed","100",
  [("What is the Rule of 72?","The Rule of 72 is a simple formula to estimate doubling time: Years to Double = 72 / Annual Return Rate. At 8% return, money doubles in 72/8 = 9 years. At 6%, it doubles in 12 years. At 3%, in 24 years. It works because 72 is close to the mathematical constant needed for continuous compounding."),
   ("How accurate is the Rule of 72?","Very accurate for rates between 5-12%. At 8%, Rule of 72 gives 9 years; exact answer is 9.01 years (0.1% error). At 4%, it gives 18 years vs. exact 17.67 (1.9% error). At 25%, error is about 2.5%. More accurate alternatives: Rule of 70 (lower rates), Rule of 69.3 (continuous compounding)."),
   ("How can I use the Rule of 72 to understand debt?","Works for debt too. A credit card at 18% APR doubles your debt in 72/18 = 4 years if you make no payments. Payday loan at 400% APR: debt doubles in 72/400 = 0.18 years (about 66 days). This mental math is powerful for understanding the cost of high-interest debt."),
   ("What is the Rule of 69 and when should I use it?","Rule of 69.3 is more mathematically precise for continuous compounding. For comparing very different rates or for precise calculations, use the exact formula: Years = ln(2) / ln(1 + r). The Rule of 72 is for quick mental math. Rule of 69 is for precise calculations. Both give the same approximate result."),
   ("How does the Rule of 72 apply to inflation?","Inflation erodes purchasing power at the same rate math applies. At 3% inflation, prices double in 72/3 = 24 years. At 7% inflation, prices double in just 10.3 years. This is why high inflation is dangerous: a 7% inflation rate halves your purchasing power in a decade.")],
  [("Compound Interest Calculator","/calculators/compound-interest-calculator"),("Investment Calculator","/calculators/investment-calculator"),("DCA Calculator","/calculators/dca-calculator"),("Inflation Calculator","/calculators/inflation-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Rule of 72 Quick Reference</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700 border-b border-blue-200"><th class="text-left pb-1">Rate</th><th class="text-right pb-1">Doubles In</th></tr></thead>
            <tbody class="text-blue-900">
              {[["2% (savings)","36 yrs"],["4% (bonds)","18 yrs"],["6% (conservative)","12 yrs"],["8% (balanced)","9 yrs"],["10% (aggressive)","7.2 yrs"],["18% (credit card)","4 yrs"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right font-medium">{r[1]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Power of Compounding: $10,000 at 8%</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Years</th><th class="text-right p-2 text-xs font-semibold">Doublings</th><th class="text-right p-2 text-xs font-semibold">Value</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["9 (1st)","1x","$20,000"],["18 (2nd)","2x","$40,000"],["27 (3rd)","3x","$80,000"],["36 (4th)","4x","$160,000"],["45 (5th)","5x","$320,000"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right font-medium text-green-700">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
        <p class="text-xs text-gray-500 mt-1">Each doubling period adds as much as ALL previous periods combined.</p>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Rule of 72 Uses Beyond Investing</h2>
        <div class="space-y-3">
          {[
            {use:"Credit Card Debt",eg:"18% APR → debt doubles in 4 years without payments"},
            {use:"Inflation Erosion",eg:"7% inflation → purchasing power halves in ~10 years"},
            {use:"Population Growth",eg:"2% growth → population doubles in 36 years"},
            {use:"Company Revenue",eg:"25% growth → revenue doubles in ~3 years"},
            {use:"Economic GDP",eg:"3.5% growth → GDP doubles in ~20 years"},
          ].map(u => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-xs text-blue-700 mb-0.5">{u.use}</div>
              <div class="text-xs text-gray-600">{u.eg}</div>
            </div>
          ))}
        </div>
      </div>
    </div>""",
  "Years to Double","Calculate doubling time using the Rule of 72")

# ── STOCK PROFIT ──────────────────────────────────────────────────────────────
w("stock-profit","Stock Profit Calculator","Financial","financial",
  "Stock Profit Calculator: Investment Return & Capital Gains",
  "Calculate your profit, loss, and return percentage from buying and selling stocks. Includes commission costs. Free stock profit calculator.",
  """
  const shares = parseFloat(inputs.shares)||0
  const buyPrice = parseFloat(inputs.buyPrice)||0
  const sellPrice = parseFloat(inputs.sellPrice)||0
  const buyCommission = parseFloat(inputs.buyCommission)||0
  const sellCommission = parseFloat(inputs.sellCommission)||0
  if(shares<=0||buyPrice<=0) throw new Error("Enter shares and buy price.")
  const totalCost = shares*buyPrice+buyCommission
  const totalProceeds = shares*sellPrice-sellCommission
  const profit = totalProceeds-totalCost
  const returnPct = (profit/totalCost)*100
  const dividends = parseFloat(inputs.dividends)||0
  const totalReturn = profit+dividends
  const totalReturnPct = (totalReturn/totalCost)*100
  return {
    value:"$"+profit.toFixed(2)+" ("+(returnPct>0?"+":"")+returnPct.toFixed(2)+"%)",
    gaugeValue:Math.min(Math.max(returnPct+50,0),100),
    breakdown:["Shares: "+shares,"Buy: $"+buyPrice+" × "+shares+" = $"+totalCost.toFixed(2),"Sell: $"+sellPrice+" × "+shares+" = $"+totalProceeds.toFixed(2),"Profit/Loss: $"+profit.toFixed(2),"Return: "+returnPct.toFixed(2)+"%","Total return (with dividends): $"+totalReturn.toFixed(2)],
    stats:[
      {label:"Profit / Loss",value:"$"+profit.toFixed(2)},
      {label:"Return %",value:(returnPct>0?"+":"")+returnPct.toFixed(2)+"%"},
      {label:"Total Invested",value:"$"+totalCost.toFixed(2)},
      {label:"Net Proceeds",value:"$"+totalProceeds.toFixed(2)},
    ]
  }
""",
  """{id:"shares",label:"Number of Shares",type:"number",placeholder:"100",min:0,defaultValue:100},
            {id:"buyPrice",label:"Buy Price Per Share",type:"number",placeholder:"50",min:0,unit:"$",step:0.01,defaultValue:50},
            {id:"sellPrice",label:"Sell Price Per Share",type:"number",placeholder:"75",min:0,unit:"$",step:0.01,defaultValue:75},
            {id:"buyCommission",label:"Buy Commission",type:"number",placeholder:"0",min:0,unit:"$",step:0.01,defaultValue:0},
            {id:"sellCommission",label:"Sell Commission",type:"number",placeholder:"0",min:0,unit:"$",step:0.01,defaultValue:0},
            {id:"dividends",label:"Total Dividends Received",type:"number",placeholder:"0",min:0,unit:"$",defaultValue:0}""",
  [("Big loss (>-25%)","#ef4444",0,25),("Small loss/flat","#f59e0b",25,50),("Gain (0-50%)","#3b82f6",50,75),("Big gain (>50%)","#22c55e",75,100)],
  "% (50=breakeven)","100",
  [("How is stock profit calculated?","Stock Profit = (Sell Price × Shares) - (Buy Price × Shares) - Commissions. Return % = Profit / Total Cost × 100. If you received dividends, add those to get total return. Most modern brokers charge $0 commissions, so cost basis is simply purchase price × shares."),
   ("What is cost basis and why does it matter for taxes?","Cost basis = total amount paid for shares including commissions. Capital gains = Sale proceeds - Cost basis. This determines your taxable gain. Keep records of all purchases, reinvested dividends, and stock splits, as they adjust your cost basis. Wrong cost basis can mean overpaying taxes."),
   ("How are stock gains taxed?","Short-term gains (held under 1 year): taxed as ordinary income (10-37%). Long-term gains (over 1 year): 0%, 15%, or 20% depending on income. Most middle-income investors pay 15% long-term capital gains tax. Always know your holding period before selling."),
   ("What is a wash sale and how does it affect stock losses?","If you sell a stock at a loss and buy the same or substantially identical stock within 30 days before or after the sale, it is a wash sale. You cannot deduct that loss — it is added to the new stock cost basis instead. Wait 31 days before rebuying the same stock to preserve the tax loss."),
   ("How do I track multiple purchases of the same stock?","For tax purposes, you must identify which shares you are selling. Methods: FIFO (first in, first out — default), LIFO (last in, first out), specific identification (choose which shares to sell for tax optimization), or average cost basis (common for mutual funds). Specific identification gives most control over tax outcomes.")],
  [("Capital Gains Calculator","/calculators/capital-gains-calculator"),("Investment Calculator","/calculators/investment-calculator"),("DCA Calculator","/calculators/dca-calculator"),("Dividend Calculator","/calculators/dividend-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Stock Return Calculation</h3>
          <div class="text-xs text-blue-800 space-y-1 font-mono">
            <div>Profit = (Sell - Buy) × Shares</div>
            <div>Return % = Profit / Cost × 100</div>
            <div class="mt-2 font-sans">Example: Buy 100 shares at $50, sell at $75</div>
            <div>Profit = ($75-$50) × 100 = $2,500</div>
            <div>Return = $2,500 / $5,000 = 50%</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Return Required to Break Even After Loss</h2>
        <p class="text-xs text-gray-600 mb-3">This is why avoiding large losses matters more than big gains:</p>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Loss</th><th class="text-right p-2 text-xs font-semibold">Gain to Break Even</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["−10%","+11.1%"],["−20%","+25%"],["−33%","+50%"],["−50%","+100%"],["−75%","+300%"]].map(r => (
              <tr><td class="p-2 text-xs text-red-600">{r[0]}</td><td class="p-2 text-xs text-right font-medium text-blue-700">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Tax Optimization Strategies</h2>
        <div class="space-y-2">
          {["Hold shares 366+ days to qualify for lower long-term capital gains rate","Harvest losses in December to offset gains taken earlier in the year","Use tax-advantaged accounts (IRA, 401k) for most active trading","Donate appreciated stock to charity — avoid capital gains entirely","Gift appreciated stock to family members in lower tax brackets","Specify tax lots when selling to choose highest-basis shares first"].map(t => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{t}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Stock Profit / Loss","Calculate your stock investment profit, return %, and total return")

print(f"\nWritten: {written} pages (refinance, rent-vs-buy, rule-of-72, stock-profit)")
