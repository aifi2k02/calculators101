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

# ── FACTORIAL ─────────────────────────────────────────────────────────────────
w("factorial","Factorial Calculator","Math","math",
  "Factorial Calculator: n! with Steps",
  "Calculate the factorial of any number (n!) with step-by-step breakdown. Supports large factorials. Free factorial calculator.",
  """
  const n = parseInt(inputs.n)
  if(isNaN(n)||n<0) throw new Error("Enter a non-negative integer.")
  if(n>20) throw new Error("n must be 20 or less (larger values exceed safe integers).")
  let result=1
  const steps=["0! = 1 (by definition)"]
  if(n>0){
    steps.length=0
    for(let i=1;i<=n;i++){result*=i;steps.push(i+"! = "+result.toLocaleString())}
  }
  return {
    value:n+"! = "+result.toLocaleString(),
    gaugeValue:Math.min(n/20*100,100),
    breakdown:["n = "+n,"n! = "+result.toLocaleString(),"Digits: "+result.toLocaleString().replace(/,/g,"").length,...steps.slice(-5)],
    stats:[
      {label:"Result n!",value:result.toLocaleString()},
      {label:"Input n",value:String(n)},
      {label:"Number of digits",value:String(result.toLocaleString().replace(/,/g,"").length)},
      {label:"log10(n!)",value:(Math.log10(result)).toFixed(4)},
    ]
  }
""",
  """{id:"n",label:"Number (n)",type:"number",placeholder:"10",min:0,max:20,defaultValue:10}""",
  [("Small (0-5)","#22c55e",0,25),("Medium (6-12)","#3b82f6",25,60),("Large (13-20)","#f59e0b",60,100)],
  "% of max (20)","100",
  [("What is a factorial?","n! (n factorial) is the product of all positive integers from 1 to n. Example: 5! = 5 x 4 x 3 x 2 x 1 = 120. Special case: 0! = 1 by definition. Factorials grow extremely fast: 20! = 2,432,902,008,176,640,000."),
   ("Why is 0! = 1?","0! = 1 is defined (not derived) to make combinatorics work correctly. C(n,0) = n!/(0! x n!) = 1/1 = 1, meaning there is exactly 1 way to choose 0 items from n. Without 0!=1, the combination formula would break down at boundaries."),
   ("How fast do factorials grow?","Extremely fast: 1!=1, 5!=120, 10!=3,628,800, 15!=1.3 trillion, 20!=2.4 quintillion. At n=70, n! exceeds the number of atoms in the observable universe (~10^80). Standard 64-bit integers overflow at 21!. Python handles arbitrarily large integers."),
   ("What are factorials used for?","Combinatorics: C(n,r) = n!/(r!(n-r)!), P(n,r) = n!/(n-r)!. Probability: arranging n items = n! ways. Power series in calculus: e^x = sum(x^n/n!). Statistics: binomial coefficients. Physics: Stirling approximation for large n."),
   ("What is Stirling approximation?","For large n: ln(n!) ≈ n*ln(n) - n + 0.5*ln(2*pi*n). Or n! ≈ sqrt(2*pi*n) * (n/e)^n. This approximation is accurate to < 1% for n > 10 and gets more accurate as n grows. Useful when exact computation is infeasible.")],
  [("Combination Calculator","/calculators/combination-calculator"),("Average Calculator","/calculators/average-calculator"),("Percentage Calculator","/calculators/percentage-calculator"),("Z-Score Calculator","/calculators/z-score-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Factorial Table</h3>
          <div class="grid grid-cols-2 gap-1 text-xs">
            {[[0,"1"],[1,"1"],[2,"2"],[3,"6"],[4,"24"],[5,"120"],[6,"720"],[7,"5,040"],[8,"40,320"],[9,"362,880"],[10,"3,628,800"]].map(r => (
              <div class="flex justify-between border-b border-blue-100 pb-0.5 text-blue-900 font-mono"><span>{r[0]}!</span><span>{r[1]}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Key Factorial Facts</h2>
        <div class="space-y-2">
          {["0! = 1 by convention","1! = 1, 2! = 2, 3! = 6, 4! = 24, 5! = 120","n! = n × (n−1)! (recursive definition)","21! exceeds 64-bit integer limit","C(n,r) = n! / (r! × (n−r)!) — combinations","P(n,r) = n! / (n−r)! — permutations"].map(f => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{f}</span></div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Applications of Factorials</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Formula</th><th class="p-2 text-xs font-semibold text-right">Use</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["C(n,r) = n!/(r!(n-r)!)","Combinations"],["P(n,r) = n!/(n-r)!","Permutations"],["e^x = Σ x^n/n!","Euler number"],["sin(x) = x - x^3/3! + ...","Taylor series"],["n! ≈ (n/e)^n √(2πn)","Stirling approx."]].map(r => (
              <tr><td class="p-2 text-xs font-mono">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "Factorial","Calculate n! step by step")

# ── LOGARITHM ─────────────────────────────────────────────────────────────────
w("logarithm","Logarithm Calculator","Math","math",
  "Logarithm Calculator: log, ln, log2, log base n",
  "Calculate logarithms in any base: log10, natural log (ln), log2, or any base. Step-by-step antilog calculation. Free log calculator.",
  """
  const value = parseFloat(inputs.value)||0
  const base = inputs.base||"10"
  if(value<=0) throw new Error("Value must be positive.")
  let result, logName
  if(base==="e"){
    result=Math.log(value); logName="ln("+value+")"
  } else if(base==="2"){
    result=Math.log2(value); logName="log2("+value+")"
  } else {
    const b=parseFloat(base)||10
    if(b<=0||b===1) throw new Error("Base must be positive and not equal to 1.")
    result=Math.log(value)/Math.log(b); logName="log_"+b+"("+value+")"
  }
  const antilog=Math.pow(parseFloat(base==="e"?Math.E:parseFloat(base)||10),result)
  return {
    value:logName+" = "+result.toFixed(6),
    gaugeValue:Math.min(Math.max(result*10+50,0),100),
    breakdown:[logName+" = "+result.toFixed(8),"Antilog verification: "+antilog.toFixed(4)+" ≈ "+value,"ln("+value+") = "+Math.log(value).toFixed(6),"log10("+value+") = "+Math.log10(value).toFixed(6),"log2("+value+") = "+Math.log2(value).toFixed(6)],
    stats:[
      {label:"Result",value:result.toFixed(6)},
      {label:"ln (natural log)",value:Math.log(value).toFixed(6)},
      {label:"log10",value:Math.log10(value).toFixed(6)},
      {label:"log2",value:Math.log2(value).toFixed(6)},
    ]
  }
""",
  """{id:"value",label:"Value (x)",type:"number",placeholder:"100",min:0.000001,step:0.001,defaultValue:100},
            {id:"base",label:"Logarithm base",type:"select",options:[
              {value:"10",label:"log₁₀ (common log)"},
              {value:"e",label:"ln (natural log, base e)"},
              {value:"2",label:"log₂ (binary log)"},
              {value:"3",label:"log₃"},
              {value:"5",label:"log₅"},
            ],defaultValue:"10"}""",
  [("Negative result","#ef4444",0,40),("Near zero","#f59e0b",40,55),("Positive","#22c55e",55,100)],
  "gauge","100",
  [("What is a logarithm?","log_b(x) = y means b^y = x. The logarithm answers: what power must I raise b to, to get x? log10(1000) = 3 because 10^3 = 1000. ln(e) = 1 because e^1 = e. log2(8) = 3 because 2^3 = 8."),
   ("What is the natural logarithm (ln)?","The natural logarithm uses base e ≈ 2.71828. ln(x) = log_e(x). It is the inverse of e^x: ln(e^x) = x, e^(ln(x)) = x. Natural logs appear naturally in calculus, growth models, and compound interest: A = Pe^(rt)."),
   ("What are the logarithm rules?","Product: log(ab) = log(a) + log(b). Quotient: log(a/b) = log(a) - log(b). Power: log(a^n) = n*log(a). Change of base: log_b(x) = log(x)/log(b) = ln(x)/ln(b). These rules simplify multiplication into addition."),
   ("When is log base 2 used?","log2 is used in computer science and information theory. Bits needed to represent n values = ceil(log2(n)). Binary search takes log2(n) steps. Sorting n items takes O(n log2(n)) comparisons. log2(1,000,000) ≈ 20, so 20 bits encode 1 million values."),
   ("What is the difference between log and ln?","log (or log10) is the common logarithm, base 10. Used in pH, decibels, Richter scale. ln is the natural logarithm, base e. Used in calculus, probability, growth models. They are related: ln(x) = log(x) / log(e) ≈ log(x) / 0.4343, or ln(x) = 2.3026 x log10(x).")],
  [("Exponent Calculator","/calculators/exponent-calculator"),("Scientific Notation","/calculators/scientific-notation-calculator"),("Z-Score Calculator","/calculators/z-score-calculator"),("Average Calculator","/calculators/average-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Log Rules</h3>
          <div class="text-xs text-blue-800 font-mono space-y-1">
            <div>log(ab) = log a + log b</div>
            <div>log(a/b) = log a − log b</div>
            <div>log(a^n) = n × log a</div>
            <div>log_b(x) = log(x)/log(b)</div>
            <div>ln(e) = 1, log10(10) = 1</div>
            <div>log(1) = 0 for any base</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Common Logarithm Values</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">x</th><th class="p-2 text-xs font-semibold text-right">log10(x)</th><th class="p-2 text-xs font-semibold text-right">ln(x)</th><th class="p-2 text-xs font-semibold text-right">log2(x)</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[[1,0,0,0],[2,"0.3010","0.6931",1],[10,1,"2.3026","3.3219"],[100,2,"4.6052","6.6439"],[1000,3,"6.9078","9.9658"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td><td class="p-2 text-xs text-right">{r[3]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Real-World Uses</h2>
        <div class="space-y-2">
          {["pH = -log10([H+]) — acidity scale","Decibels dB = 10 x log10(P2/P1) — sound","Richter scale = log10 of earthquake amplitude","Compound interest: t = ln(A/P)/(r) — time to grow","Bits in binary: log2(n) bits encode n values","Shannon entropy uses log2 in information theory"].map(a => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{a}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Logarithm","Calculate log in any base with step-by-step solution")

# ── PERCENTAGE ERROR ──────────────────────────────────────────────────────────
w("percentage-error","Percentage Error Calculator","Math","math",
  "Percentage Error Calculator: Experimental vs Actual Value",
  "Calculate percentage error between experimental and actual values. Used in science, math, and quality control. Free percent error calculator.",
  """
  const experimental = parseFloat(inputs.experimental)
  const actual = parseFloat(inputs.actual)
  if(isNaN(experimental)||isNaN(actual)) throw new Error("Enter both values.")
  if(actual===0) throw new Error("Actual value cannot be zero.")
  const error=experimental-actual
  const percentError=Math.abs(error)/Math.abs(actual)*100
  const relativeError=error/actual
  const absError=Math.abs(error)
  return {
    value:percentError.toFixed(4)+"%",
    gaugeValue:Math.min(percentError,100),
    breakdown:["Experimental: "+experimental,"Actual: "+actual,"Absolute error: "+error.toFixed(6),"Absolute error: |"+error.toFixed(4)+"|","Percent error: "+percentError.toFixed(4)+"%","Relative error: "+relativeError.toFixed(6)],
    stats:[
      {label:"% Error",value:percentError.toFixed(4)+"%"},
      {label:"Absolute Error",value:absError.toFixed(4)},
      {label:"Signed Error",value:(error>0?"+":"")+error.toFixed(4)},
      {label:"Relative Error",value:relativeError.toFixed(6)},
    ]
  }
""",
  """{id:"experimental",label:"Experimental (measured) value",type:"number",placeholder:"9.8",step:0.000001,defaultValue:9.8},
            {id:"actual",label:"Actual (accepted/true) value",type:"number",placeholder:"9.81",step:0.000001,defaultValue:9.81}""",
  [("Excellent (<1%)","#22c55e",0,1),("Good (1-5%)","#3b82f6",1,5),("Acceptable (5-10%)","#f59e0b",5,10),("Poor (10%+)","#ef4444",10,100)],
  "% error","100",
  [("What is percentage error?","Percentage error = |experimental - actual| / |actual| x 100%. It measures how far off a measured value is from the true value. A 2% error means your measurement was 2% away from the true value. Lower percentage error = more accurate measurement."),
   ("Why use absolute value in percentage error?","The absolute value |experimental - actual| gives us the magnitude of the error regardless of direction. Without it, being 5% too high and 5% too low would cancel out. Percentage error is always reported as a positive number representing the size of the discrepancy."),
   ("What percentage error is acceptable in science?","Depends on the field: Physics lab (student level): <5% is good, <10% acceptable. Analytical chemistry: <2%. Manufacturing quality control: often <1%. Medical devices: <0.5% or even less. Research science: depends on the measurement, but typically strive for <5%."),
   ("What is the difference between percent error and percent difference?","Percent error compares a measurement to a known true value: |measured - true| / |true| x 100%. Percent difference compares two measurements neither of which is designated the true value: |A - B| / ((A+B)/2) x 100%. Use percent error when a true value is known; percent difference when comparing two measurements."),
   ("How do I reduce experimental error?","Systematic errors (shift in one direction): calibrate equipment, use better measuring tools, control experimental conditions. Random errors (scatter in both directions): repeat measurements and average, use larger sample sizes. Human errors: double-check readings, use digital instruments, blind measurements.")],
  [("Average Calculator","/calculators/average-calculator"),("Percentage Calculator","/calculators/percentage-calculator"),("Z-Score Calculator","/calculators/z-score-calculator"),("Sig Figs Calculator","/calculators/sig-figs-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Percentage Error Formula</h3>
          <div class="text-center text-blue-800 font-mono text-sm bg-blue-100 rounded p-3 mb-2">% Error = |E - A| / |A| × 100%</div>
          <div class="text-xs text-blue-700">E = Experimental value<br/>A = Actual (accepted) value</div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Acceptable Error by Field</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Field</th><th class="p-2 text-xs font-semibold text-right">Typical Acceptable Error</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Student physics lab","< 10%"],["Engineering","< 5%"],["Analytical chemistry","< 2%"],["Medical devices","< 1%"],["Precision manufacturing","< 0.5%"],["Research science","< 5% typical"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-medium">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Error Types</h2>
        <div class="space-y-3">
          {[
            {t:"Systematic Error",d:"Consistent bias in one direction. Caused by faulty calibration, instrument zero offset. Cannot be reduced by averaging."},
            {t:"Random Error",d:"Unpredictable scatter in both directions. Reduced by taking more measurements and averaging results."},
            {t:"Human Error",d:"Reading scales wrong, parallax, transcription errors. Reduced by careful technique and digital instruments."},
          ].map(e => (
            <div class="bg-gray-50 rounded-lg p-3"><div class="font-semibold text-xs text-blue-700">{e.t}</div><div class="text-xs text-gray-600">{e.d}</div></div>
          ))}
        </div>
      </div>
    </div>""",
  "% Error","Calculate percentage error between measured and true values")

# ── SCIENTIFIC NOTATION ───────────────────────────────────────────────────────
w("scientific-notation","Scientific Notation Calculator","Math","math",
  "Scientific Notation Calculator: Convert & Calculate",
  "Convert numbers to/from scientific notation. Multiply, divide, add scientific notation numbers. Free scientific notation calculator.",
  """
  const value = inputs.value||""
  const operation = inputs.operation||"convert"
  const value2 = inputs.value2||""
  let num1=parseFloat(value)
  if(isNaN(num1)) throw new Error("Enter a valid number.")
  const toSci = n => {
    if(n===0) return "0"
    const exp=Math.floor(Math.log10(Math.abs(n)))
    const coeff=n/Math.pow(10,exp)
    return coeff.toFixed(4)+" × 10^"+exp
  }
  if(operation==="convert"){
    return {
      value:toSci(num1),
      gaugeValue:Math.min(Math.abs(Math.log10(Math.abs(num1)||1))/20*100,100),
      breakdown:["Input: "+num1,"Scientific notation: "+toSci(num1),"Standard form: "+num1.toLocaleString(),"Exponent: "+Math.floor(Math.log10(Math.abs(num1)||1))],
      stats:[
        {label:"Scientific Notation",value:toSci(num1)},
        {label:"Standard",value:num1.toLocaleString()},
        {label:"Exponent",value:String(Math.floor(Math.log10(Math.abs(num1)||1)))},
        {label:"Coefficient",value:(num1/Math.pow(10,Math.floor(Math.log10(Math.abs(num1)||1)))).toFixed(4)},
      ]
    }
  }
  let num2=parseFloat(value2)
  if(isNaN(num2)) throw new Error("Enter second value for operations.")
  let result
  if(operation==="multiply") result=num1*num2
  else if(operation==="divide"){if(num2===0) throw new Error("Cannot divide by zero."); result=num1/num2}
  else if(operation==="add") result=num1+num2
  else if(operation==="subtract") result=num1-num2
  else throw new Error("Unknown operation.")
  return {
    value:toSci(result),
    gaugeValue:50,
    breakdown:[toSci(num1)+" "+operation+" "+toSci(num2),"= "+result,"= "+toSci(result),"Standard: "+result.toLocaleString()],
    stats:[
      {label:"Result",value:toSci(result)},
      {label:"Standard Form",value:result.toLocaleString()},
      {label:"Input 1",value:toSci(num1)},
      {label:"Input 2",value:toSci(num2)},
    ]
  }
""",
  """{id:"value",label:"Number 1",type:"number",placeholder:"0.00045",step:"any",defaultValue:0.00045},
            {id:"operation",label:"Operation",type:"select",options:[
              {value:"convert",label:"Convert to scientific notation"},
              {value:"multiply",label:"Multiply (× number 2)"},
              {value:"divide",label:"Divide (÷ number 2)"},
              {value:"add",label:"Add (+ number 2)"},
              {value:"subtract",label:"Subtract (− number 2)"},
            ],defaultValue:"convert"},
            {id:"value2",label:"Number 2 (for operations)",type:"number",placeholder:"1000",step:"any",defaultValue:1000}""",
  [("Small (<10^-5)","#3b82f6",0,25),("Medium (10^-5 to 10^5)","#22c55e",25,75),("Large (>10^5)","#f59e0b",75,100)],
  "magnitude","100",
  [("What is scientific notation?","Scientific notation expresses numbers as coefficient × 10^exponent, where 1 ≤ |coefficient| < 10. Example: 45,000 = 4.5 × 10^4. 0.00045 = 4.5 × 10^-4. Used in science to represent very large (distance to stars) or very small (size of atoms) numbers compactly."),
   ("How do I multiply numbers in scientific notation?","Multiply the coefficients, add the exponents: (3.2 × 10^4) × (2.5 × 10^3) = (3.2 × 2.5) × 10^(4+3) = 8.0 × 10^7. If the new coefficient is not between 1 and 10, adjust: 15 × 10^5 = 1.5 × 10^6."),
   ("How do I add numbers in scientific notation?","First make exponents equal: 3.2 × 10^4 + 5.0 × 10^3 = 3.2 × 10^4 + 0.5 × 10^4 = 3.7 × 10^4. Convert to same exponent, add coefficients, adjust if needed."),
   ("What are common scientific notation examples?","Speed of light: 3.0 × 10^8 m/s. Electron mass: 9.11 × 10^-31 kg. Distance to sun: 1.496 × 10^11 m. Avogadro number: 6.022 × 10^23 mol^-1. Size of hydrogen atom: 5.3 × 10^-11 m. Age of universe: 1.38 × 10^10 years."),
   ("What is E notation on a calculator?","E notation is scientific notation shorthand: 4.5E4 means 4.5 × 10^4 = 45,000. 3.2E-7 means 3.2 × 10^-7 = 0.00000032. Most calculators and programming languages use E notation when numbers are too large or small for standard display.")],
  [("Exponent Calculator","/calculators/exponent-calculator"),("Significant Figures Calculator","/calculators/sig-figs-calculator"),("Logarithm Calculator","/calculators/logarithm-calculator"),("Unit Converter","/calculators/unit-converter-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Quick Reference</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700"><th class="text-left">Prefix</th><th class="text-right">Power</th></tr></thead>
            <tbody class="text-blue-900">
              {[["Nano","10⁻⁹"],["Micro","10⁻⁶"],["Milli","10⁻³"],["Kilo","10³"],["Mega","10⁶"],["Giga","10⁹"],["Tera","10¹²"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right">{r[1]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Operations Rules</h2>
        <div class="space-y-2">
          {[
            {op:"Multiply",r:"(a × 10^m) × (b × 10^n) = ab × 10^(m+n)"},
            {op:"Divide",r:"(a × 10^m) ÷ (b × 10^n) = (a/b) × 10^(m−n)"},
            {op:"Add/Subtract",r:"Convert to same exponent first, then add coefficients"},
            {op:"Power",r:"(a × 10^m)^n = a^n × 10^(mn)"},
          ].map(o => (
            <div class="bg-gray-50 rounded-lg p-3"><div class="font-semibold text-xs text-blue-700">{o.op}</div><div class="text-xs font-mono text-gray-600">{o.r}</div></div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Real-World Numbers</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Value</th><th class="p-2 text-xs font-semibold text-right">Scientific Notation</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Speed of light","3.0 × 10⁸ m/s"],["Electron mass","9.1 × 10⁻³¹ kg"],["Avogadro number","6.022 × 10²³"],["Earth mass","5.97 × 10²⁴ kg"],["Atom diameter","1.0 × 10⁻¹⁰ m"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-mono">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "Result","Convert numbers to/from scientific notation and perform operations")

# ── SIG FIGS ─────────────────────────────────────────────────────────────────
w("sig-figs","Significant Figures Calculator","Math","math",
  "Significant Figures Calculator: Count & Round Sig Figs",
  "Count significant figures in a number and round to any number of sig figs. Learn the rules for significant figures. Free sig figs calculator.",
  """
  const value = inputs.value||""
  const roundTo = parseInt(inputs.roundTo)||3
  const numStr = value.toString().trim()
  const num = parseFloat(numStr)
  if(isNaN(num)) throw new Error("Enter a valid number.")
  // Count sig figs
  const countSigFigs = s => {
    s=s.replace(/^-/,"").replace(/^0+(?=[1-9])/,"")
    if(s.includes(".")){
      s=s.replace(/^0+/,"")
      if(s.startsWith(".")) s=s.replace(/^\.0*/,"").replace(/^$/,"0")
      return s.replace(".","").replace(/^0+/,"").length||1
    } else {
      return s.replace(/0+$/,"").length
    }
  }
  const sigFigCount=countSigFigs(numStr)
  const roundedToN = parseFloat(num.toPrecision(roundTo))
  return {
    value:sigFigCount+" significant figures",
    gaugeValue:Math.min(sigFigCount/10*100,100),
    breakdown:["Number: "+numStr,"Significant figures: "+sigFigCount,"Rounded to "+roundTo+" sig figs: "+roundedToN,"Scientific notation: "+num.toExponential(roundTo-1)],
    stats:[
      {label:"Sig Figs Count",value:String(sigFigCount)},
      {label:"Rounded ("+roundTo+" SF)",value:String(roundedToN)},
      {label:"In Sci Notation",value:num.toExponential(roundTo-1)},
      {label:"Original",value:numStr},
    ]
  }
""",
  """{id:"value",label:"Number",type:"text",placeholder:"0.00470",defaultValue:"0.00470"},
            {id:"roundTo",label:"Round to (significant figures)",type:"number",placeholder:"3",min:1,max:10,defaultValue:3}""",
  [("1-2 sig figs","#ef4444",0,20),("3-4 sig figs","#f59e0b",20,40),("5-7 sig figs","#22c55e",40,70),("8+ sig figs","#3b82f6",70,100)],
  "sig figs (of 10)","100",
  [("What are significant figures?","Significant figures (sig figs) are the meaningful digits in a number that reflect measurement precision. Non-zero digits are always significant. Zeros between non-zero digits are significant. Trailing zeros after a decimal point are significant. Leading zeros are never significant."),
   ("How many sig figs does 0.00470 have?","0.00470 has 3 significant figures: 4, 7, and the trailing 0 after the 7. The leading zeros (0.00) are not significant — they are just placeholders showing the decimal place. The trailing zero IS significant because it shows precision to the ten-thousandths place."),
   ("What are the rules for significant figures in calculations?","Multiplication/Division: round to the fewest sig figs in the inputs. 2.5 × 3.42 = 8.6 (2 sig figs). Addition/Subtraction: round to the fewest decimal places in the inputs. 12.52 + 1.1 = 13.6 (1 decimal place). Scientific notation makes sig figs unambiguous: 3.50 × 10^4 has exactly 3 sig figs."),
   ("How do I round to 3 significant figures?","Find the 3rd significant digit, then look at the next digit. If it is 5 or more, round up; if less than 5, round down. Examples: 0.004726 → 0.00473. 12,456 → 12,500. 1.2349 → 1.23. Zeros used as placeholders do not count, only measurement-meaningful digits do."),
   ("Why are significant figures important?","They communicate the precision of a measurement. Writing 12.5 g implies precision to ±0.05 g; writing 12.500 g implies ±0.0005 g. In engineering and science, false precision can lead to errors. A calculated result cannot be more precise than the least precise measurement it came from.")],
  [("Scientific Notation","/calculators/scientific-notation-calculator"),("Percentage Error Calculator","/calculators/percentage-error-calculator"),("Rounding Calculator","/calculators/rounding-calculator"),("Average Calculator","/calculators/average-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Sig Fig Rules</h3>
          <div class="space-y-1 text-xs text-blue-800">
            <div>✓ Non-zero digits: always significant</div>
            <div>✓ Zeros between non-zero: significant</div>
            <div>✓ Trailing zeros after decimal: significant</div>
            <div>✗ Leading zeros: NOT significant</div>
            <div>✗ Trailing zeros without decimal: ambiguous</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Examples</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Number</th><th class="p-2 text-xs font-semibold text-right">Sig Figs</th><th class="p-2 text-xs font-semibold text-right">Reason</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["7230","3","trailing zero ambiguous"],["7230.","4","decimal point makes trailing 0 sig"],["0.00830","3","4 and 7 and trailing 0"],["3.00 × 10^4","3","coefficient determines sig figs"],["100.0","4","trailing zeros after decimal sig"]].map(r => (
              <tr><td class="p-2 text-xs font-mono">{r[0]}</td><td class="p-2 text-xs text-right font-medium">{r[1]}</td><td class="p-2 text-xs text-right text-gray-500">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Calculation Rules</h2>
        <div class="space-y-2">
          {[
            {op:"Multiply / Divide",r:"Round to the fewest sig figs among all inputs"},
            {op:"Add / Subtract",r:"Round to the fewest decimal places among inputs"},
            {op:"Exact numbers",r:"Counting numbers (3 apples) and defined constants have infinite sig figs"},
          ].map(o => (
            <div class="bg-gray-50 rounded-lg p-3"><div class="font-semibold text-xs text-blue-700">{o.op}</div><div class="text-xs text-gray-600">{o.r}</div></div>
          ))}
        </div>
      </div>
    </div>""",
  "Sig Figs","Count significant figures and round to a target number of sig figs")

# ── MODULO ───────────────────────────────────────────────────────────────────
w("modulo","Modulo Calculator","Math","math",
  "Modulo Calculator: Remainder & Modulus Operation",
  "Calculate the remainder (modulus) when dividing two numbers. Find if a number is even, odd, or divisible. Free modulo calculator.",
  """
  const a = parseFloat(inputs.a)
  const b = parseFloat(inputs.b)
  if(isNaN(a)||isNaN(b)) throw new Error("Enter both values.")
  if(b===0) throw new Error("Cannot compute modulo with divisor 0.")
  const remainder = ((a%b)+b)%b
  const quotient = Math.floor(a/b)
  const isEven = Number.isInteger(a)&&(a%2===0)
  const isDivisible = remainder===0
  return {
    value:a+" mod "+b+" = "+remainder,
    gaugeValue:Math.min((remainder/Math.abs(b))*100,100),
    breakdown:[a+" = "+b+" × "+quotient+" + "+remainder,a+" mod "+b+" = "+remainder,"Is divisible by "+b+": "+(isDivisible?"Yes":"No"),"Is even: "+(isEven?"Yes":"No"),"Quotient (floor): "+quotient,"Remainder: "+remainder],
    stats:[
      {label:"Remainder",value:String(remainder)},
      {label:"Quotient",value:String(quotient)},
      {label:"Divisible",value:isDivisible?"Yes":"No"},
      {label:"Even / Odd",value:Number.isInteger(a)?(a%2===0?"Even":"Odd"):"N/A"},
    ]
  }
""",
  """{id:"a",label:"Dividend (a)",type:"number",placeholder:"17",step:1,defaultValue:17},
            {id:"b",label:"Divisor (b)",type:"number",placeholder:"5",step:1,defaultValue:5}""",
  [("No remainder (divisible)","#22c55e",0,5),("Small remainder","#3b82f6",5,50),("Large remainder","#f59e0b",50,100)],
  "% remainder","100",
  [("What is modulo (mod)?","Modulo gives the remainder after division. 17 mod 5 = 2 because 17 = 5 × 3 + 2. The remainder is always in the range [0, divisor-1]. In programming: Python uses %, JavaScript uses %. Note: programming languages may handle negative numbers differently."),
   ("How is modulo used in programming?","Even/odd check: n%2==0 means even. Wrapping around: array index i%length keeps within bounds. Cyclic operations: day-of-week = (day+7)%7. Hashing: hash%tableSize. Last n digits: number%10^n. Scheduling: task runs every k units when t%k==0."),
   ("What is the difference between modulo and remainder?","For positive numbers, they are the same. For negative numbers: In math, modulo is always in [0, b-1]: -7 mod 3 = 2 (because -7 = 3 × -3 + 2). In many programming languages, the % operator gives the C-style remainder with the same sign as the dividend: -7 % 3 = -1 in C/Java/JavaScript."),
   ("What is modular arithmetic?","Modular arithmetic (clock arithmetic) wraps numbers around a fixed modulus. On a 12-hour clock: 11 + 3 = 14 ≡ 2 (mod 12). Key operations: (a+b) mod n, (a×b) mod n. Used in cryptography (RSA encryption), computer science, and number theory."),
   ("How do I check divisibility with modulo?","a is divisible by b if a mod b == 0. Examples: 20 mod 4 = 0 (divisible). 21 mod 4 = 1 (not divisible). Divisibility rules: mod 2 for even/odd, mod 9 for sum-of-digits rule, mod 10 for last digit. Used in leap year: year%4==0 (with exceptions for century years).")],
  [("GCD LCM Calculator","/calculators/lcm-gcd-calculator"),("Prime Number Calculator","/calculators/prime-calculator"),("Number Base Calculator","/calculators/number-base-calculator"),("Average Calculator","/calculators/average-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Modulo Examples</h3>
          <div class="text-xs text-blue-800 font-mono space-y-1">
            <div>10 mod 3 = 1</div>
            <div>17 mod 5 = 2</div>
            <div>20 mod 4 = 0 (divisible)</div>
            <div>8 mod 2 = 0 (even)</div>
            <div>9 mod 2 = 1 (odd)</div>
            <div>2025 mod 7 = ? (day of week)</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Divisibility Rules via Modulo</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Divisor</th><th class="p-2 text-xs font-semibold text-right">Rule</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["2","Last digit even (0,2,4,6,8)"],["3","Sum of digits divisible by 3"],["4","Last 2 digits divisible by 4"],["5","Last digit 0 or 5"],["9","Sum of digits divisible by 9"],["10","Last digit is 0"]].map(r => (
              <tr><td class="p-2 text-xs font-medium">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Modulo in Programming</h2>
        <div class="space-y-2">
          {["n%2==0 → even number","i%arr.length → circular array indexing","(hour+offset)%24 → time zone wrapping","id%shards → database sharding","turn%players → whose turn next","n%10 → last digit of any integer"].map(a => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 font-mono mt-0.5">•</span><span class="font-mono">{a}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Remainder","Calculate modulo (remainder) and check divisibility")

# ── ROUNDING ─────────────────────────────────────────────────────────────────
w("rounding","Rounding Calculator","Math","math",
  "Rounding Calculator: Round to Decimal Places, Nearest Whole",
  "Round any number to decimal places, nearest whole number, nearest 5, 10, 100, etc. Multiple rounding modes. Free rounding calculator.",
  """
  const value = parseFloat(inputs.value)
  const mode = inputs.mode||"decimal"
  const places = parseInt(inputs.places)||0
  if(isNaN(value)) throw new Error("Enter a valid number.")
  let rounded, label
  if(mode==="decimal"){
    const factor=Math.pow(10,places)
    rounded=Math.round(value*factor)/factor; label="to "+places+" decimal places"
  } else if(mode==="up"){
    const factor=Math.pow(10,places)
    rounded=Math.ceil(value*factor)/factor; label="up to "+places+" decimal places"
  } else if(mode==="down"){
    const factor=Math.pow(10,places)
    rounded=Math.floor(value*factor)/factor; label="down to "+places+" decimal places"
  } else if(mode==="nearest5"){
    rounded=Math.round(value/5)*5; label="to nearest 5"
  } else if(mode==="nearest10"){
    rounded=Math.round(value/10)*10; label="to nearest 10"
  } else if(mode==="nearest100"){
    rounded=Math.round(value/100)*100; label="to nearest 100"
  } else if(mode==="nearest1000"){
    rounded=Math.round(value/1000)*1000; label="to nearest 1,000"
  } else throw new Error("Unknown mode.")
  const diff=rounded-value
  return {
    value:rounded.toString(),
    gaugeValue:Math.abs(diff)/(Math.abs(value)||1)*100*10,
    breakdown:["Original: "+value,"Rounded "+label+": "+rounded,"Difference: "+diff.toFixed(8),"Error %: "+(Math.abs(diff)/(Math.abs(value)||1)*100).toFixed(4)+"%"],
    stats:[
      {label:"Rounded",value:String(rounded)},
      {label:"Original",value:String(value)},
      {label:"Difference",value:diff.toFixed(6)},
      {label:"Rounding Mode",value:mode},
    ]
  }
""",
  """{id:"value",label:"Number to round",type:"number",placeholder:"3.14159",step:"any",defaultValue:3.14159},
            {id:"mode",label:"Rounding mode",type:"select",options:[
              {value:"decimal",label:"Round to decimal places (standard)"},
              {value:"up",label:"Round up (ceiling)"},
              {value:"down",label:"Round down (floor)"},
              {value:"nearest5",label:"Round to nearest 5"},
              {value:"nearest10",label:"Round to nearest 10"},
              {value:"nearest100",label:"Round to nearest 100"},
              {value:"nearest1000",label:"Round to nearest 1,000"},
            ],defaultValue:"decimal"},
            {id:"places",label:"Decimal places (for decimal modes)",type:"number",placeholder:"2",min:0,max:10,defaultValue:2}""",
  [("Exact (no rounding)","#22c55e",0,1),("Small rounding","#3b82f6",1,10),("Large rounding","#f59e0b",10,100)],
  "% change","100",
  [("What are the rounding rules?","Standard rounding (half-up): if the digit after your rounding place is 5 or more, round up; if 4 or less, round down. Example: 3.145 rounded to 2 decimal places = 3.15 (since 5 ≥ 5, round up). 3.144 = 3.14 (since 4 < 5, round down)."),
   ("What is the difference between floor and ceiling?","Floor (round down): always rounds toward negative infinity. floor(3.9) = 3, floor(-3.1) = -4. Ceiling (round up): always rounds toward positive infinity. ceil(3.1) = 4, ceil(-3.9) = -3. Standard rounding (half-up) rounds 0.5 cases up: round(2.5) = 3, round(3.5) = 4."),
   ("What is banker rounding (round half to even)?","Banker rounding rounds 0.5 cases to the nearest even digit: 2.5 → 2, 3.5 → 4, 4.5 → 4, 5.5 → 6. This reduces cumulative rounding bias when processing many numbers. Used in Python built-in round(), financial calculations, and IEEE 754 floating-point standard."),
   ("How do I round to the nearest 5?","Divide by 5, round to nearest integer, multiply by 5. Example: round 17 to nearest 5: 17/5 = 3.4, round to 3, 3 x 5 = 15. Round 18: 18/5 = 3.6, round to 4, 4 x 5 = 20. Used in pricing (prices ending in 0 or 5) and practical measurements."),
   ("Why does floating-point rounding sometimes give unexpected results?","Floating-point numbers (how computers store decimals) cannot exactly represent most decimal fractions. 0.1 + 0.2 = 0.30000000000000004 in JavaScript. This is not a bug — it is how binary floating-point works. For financial calculations, use integer arithmetic (store cents, not dollars) or decimal libraries to avoid these issues.")],
  [("Significant Figures Calculator","/calculators/sig-figs-calculator"),("Percentage Error Calculator","/calculators/percentage-error-calculator"),("Fraction Calculator","/calculators/fraction-calculator"),("Average Calculator","/calculators/average-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Rounding Modes</h3>
          <div class="space-y-1 text-xs text-blue-800">
            <div><span class="font-semibold">Standard:</span> ≥5 rounds up, &lt;5 rounds down</div>
            <div><span class="font-semibold">Floor:</span> always rounds toward -∞</div>
            <div><span class="font-semibold">Ceiling:</span> always rounds toward +∞</div>
            <div><span class="font-semibold">Truncate:</span> always toward zero</div>
            <div><span class="font-semibold">Banker:</span> 0.5 rounds to nearest even</div>
          </div>
        </div>""",
  """    <div class="mt-10">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Rounding Comparison</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Value</th><th class="p-2 text-xs text-right">Round (2dp)</th><th class="p-2 text-xs text-right">Floor (2dp)</th><th class="p-2 text-xs text-right">Ceil (2dp)</th><th class="p-2 text-xs text-right">To 10</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[[3.145,3.15,3.14,3.15,10],[3.144,3.14,3.14,3.15,10],[7.895,7.9,7.89,7.9,10],[-3.145,-3.15,-3.15,-3.14,-10],[17.5,17.5,17.5,17.5,20]].map(r => (
              <tr><td class="p-2 text-xs font-medium">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td><td class="p-2 text-xs text-right">{r[3]}</td><td class="p-2 text-xs text-right">{r[4]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "Rounded","Round numbers with multiple modes and precision")

print(f"\nWritten: {written} pages (factorial, logarithm, percentage-error, scientific-notation, sig-figs, modulo, rounding)")
