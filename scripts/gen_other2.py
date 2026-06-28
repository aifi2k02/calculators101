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

# ── DOG AGE ────────────────────────────────────────────────────────────────────
w("dog-age","Dog Age Calculator","Other","other",
  "Dog Age Calculator: Dog Years to Human Years",
  "Convert your dog age to human years. Uses size-adjusted formula for small, medium, and large dog breeds. Free dog age calculator.",
  """
  const dogYears = parseFloat(inputs.dogYears)||0
  const size = inputs.size||"medium"
  if(dogYears<=0||dogYears>30) throw new Error("Enter a valid dog age (1-30).")
  const humanAgeMap = {
    small: [15,24,28,32,36,40,44,48,52,56,60,64,68,72,76,80,84,88,92,96,100,104,108,112,116,120,124,128,132,136],
    medium:[15,24,28,32,36,42,47,51,56,60,64,68,72,77,81,85,89,93,97,101,105,109,113,117,121,125,129,133,137,141],
    large: [15,24,28,32,36,45,50,55,61,66,72,77,82,88,93,99,104,109,115,120,126,131,136,142,147,153,158,163,169,174]
  }
  const map = humanAgeMap[size]||humanAgeMap.medium
  const idx = Math.min(Math.floor(dogYears)-1, map.length-1)
  const humanAge = map[Math.max(0,idx)]
  const lifeExpectancy = {small:14,medium:12,large:10}[size]||12
  const pctLife = dogYears/lifeExpectancy*100
  return {
    value:humanAge+" human years",
    gaugeValue:Math.min(pctLife,100),
    breakdown:["Dog age: "+dogYears+" years","Size: "+size,"Human equivalent: "+humanAge+" years","Life expectancy ("+size+"): ~"+lifeExpectancy+" years","% of life lived: "+pctLife.toFixed(1)+"%"],
    stats:[
      {label:"Human Age Equivalent",value:humanAge+" years"},
      {label:"Dog Age",value:dogYears+" years"},
      {label:"Size Category",value:size.charAt(0).toUpperCase()+size.slice(1)},
      {label:"Life Stage",value:pctLife<25?"Puppy":pctLife<50?"Young Adult":pctLife<75?"Adult":"Senior"},
    ]
  }
""",
  """{id:"dogYears",label:"Dog age (years)",type:"number",placeholder:"5",min:0,max:30,step:0.5,defaultValue:5},
            {id:"size",label:"Dog size",type:"select",options:[
              {value:"small",label:"Small (under 20 lbs)"},
              {value:"medium",label:"Medium (20-50 lbs)"},
              {value:"large",label:"Large (over 50 lbs)"},
            ],defaultValue:"medium"}""",
  [("Puppy","#22c55e",0,25),("Young adult","#3b82f6",25,50),("Adult","#f59e0b",50,75),("Senior","#ef4444",75,100)],
  "% of lifespan","100",
  [("Is the 7 dog years to 1 human year rule accurate?","No — the 7-to-1 rule is a myth. A 1-year-old dog is already sexually mature and roughly equivalent to a 15-year-old human. By age 2, they match ~24 human years. After that, aging slows to about 4-5 human years per dog year, depending on breed size. Larger dogs age faster than smaller ones."),
   ("Why do large dogs age faster than small dogs?","Larger dogs have higher metabolic rates, grow faster, and their organs work harder. A Great Dane may only live 8-10 years, while a Chihuahua can reach 14-16 years. Scientifically, larger animals tend to have shorter lifespans in general (elephant vs mouse), though the pattern reverses between species."),
   ("What are the life stages of a dog?","Puppy (0-1 year): rapid growth, socialization window 3-12 weeks. Adolescent (1-2 years): hormone surge, testing boundaries. Young adult (2-3 years): peak energy, fully trained behavior. Prime adult (3-7 years): stable, healthy years. Mature adult (7-10 years): starting to slow. Senior (10+ years): special health needs."),
   ("When is a dog considered a senior?","Small dogs: 10-12 years. Medium dogs: 8-10 years. Large dogs: 7-9 years. Giant breeds: 5-7 years. At this stage, twice-yearly vet visits are recommended. Watch for arthritis, vision/hearing loss, cognitive dysfunction, and organ changes that often appear in senior dogs."),
   ("How can I help my dog live longer?","Maintain healthy weight (obesity reduces lifespan by 2+ years). Regular exercise matching breed needs. Dental care (dental disease affects heart, kidneys). Yearly vet checkups (twice-yearly for seniors). Quality nutrition — avoid fillers and excess calories. Mental stimulation to maintain cognitive health. Avoid harmful substances.")],
  [("Age Calculator","/calculators/age-calculator"),("BMI Calculator","/calculators/bmi-calculator"),("Ideal Weight Calculator","/calculators/ideal-weight-calculator"),("Heart Rate Calculator","/calculators/heart-rate-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Life Expectancy by Size</h3>
          <div class="text-xs text-blue-800 space-y-2">
            {[["Small breeds (<20 lbs)","12-16 years","Chihuahua, Poodle"],["Medium breeds (20-50 lbs)","10-14 years","Beagle, Border Collie"],["Large breeds (50-90 lbs)","8-12 years","Lab, Golden Retriever"],["Giant breeds (90+ lbs)","6-10 years","Great Dane, Mastiff"]].map(([s,l,e]) => (
              <div class="border-b border-blue-100 pb-1"><div class="font-semibold">{s}</div><div>{l} — {e}</div></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Dog to Human Age Chart</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Dog Age</th><th class="p-2 text-xs text-right">Small</th><th class="p-2 text-xs text-right">Medium</th><th class="p-2 text-xs text-right">Large</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[[1,15,15,15],[2,24,24,24],[5,36,36,36],[7,44,47,50],[10,56,60,66],[12,64,69,77],[15,76,83,93]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]} yrs</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td><td class="p-2 text-xs text-right">{r[3]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Senior Dog Care Tips</h2>
        <div class="space-y-2">
          {["Vet visits every 6 months (not annually) after age 7","Senior dog food: lower calorie, joint support formulas","Ramps and orthopedic beds ease joint pain","Shorter but more frequent walks for arthritic dogs","Mental stimulation: puzzle feeders, nose work, training","Watch for: excessive thirst, weight changes, lethargy"].map(t => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{t}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Human Years","Convert dog years to human years by breed size")

# ── HEIGHT CONVERTER ──────────────────────────────────────────────────────────
w("height-converter","Height Converter","Other","other",
  "Height Converter: Feet Inches to cm and Meters",
  "Convert height between feet and inches, centimeters, and meters instantly. Free height converter for people and objects.",
  """
  const from = inputs.from||"feet"
  const feetVal = parseFloat(inputs.feet)||0
  const inchesVal = parseFloat(inputs.inches)||0
  const cmVal = parseFloat(inputs.cm)||0
  let totalInches
  if(from==="feet") totalInches=feetVal*12+inchesVal
  else if(from==="cm") totalInches=cmVal/2.54
  else if(from==="meters") totalInches=cmVal*100/2.54
  else throw new Error("Unknown unit.")
  const cm=totalInches*2.54
  const meters=cm/100
  const totalFeet=Math.floor(totalInches/12)
  const remInches=totalInches%12
  return {
    value:totalFeet+"ft "+remInches.toFixed(2)+"in = "+cm.toFixed(1)+"cm",
    gaugeValue:Math.min(cm/200*100,100),
    breakdown:[from==="feet"?feetVal+"ft "+inchesVal+"in → "+cm.toFixed(2)+"cm":cmVal+"cm → "+totalFeet+"ft "+remInches.toFixed(2)+"in","Centimeters: "+cm.toFixed(2)+" cm","Meters: "+meters.toFixed(4)+" m","Total inches: "+totalInches.toFixed(4)+" in","Total feet: "+(totalInches/12).toFixed(4)+" ft"],
    stats:[
      {label:"Feet & Inches",value:totalFeet+"ft "+remInches.toFixed(1)+"in"},
      {label:"Centimeters",value:cm.toFixed(1)+" cm"},
      {label:"Meters",value:meters.toFixed(3)+" m"},
      {label:"Total Inches",value:totalInches.toFixed(2)+" in"},
    ]
  }
""",
  """{id:"from",label:"Convert from",type:"select",options:[
              {value:"feet",label:"Feet and inches"},
              {value:"cm",label:"Centimeters"},
              {value:"meters",label:"Meters (enter value in cm field)"},
            ],defaultValue:"feet"},
            {id:"feet",label:"Feet",type:"number",placeholder:"5",min:0,step:1,defaultValue:5},
            {id:"inches",label:"Inches (for feet+inches input)",type:"number",placeholder:"11",min:0,max:11,step:0.5,defaultValue:11},
            {id:"cm",label:"Centimeters or meters value (for cm/m input)",type:"number",placeholder:"180",min:0,step:0.1,defaultValue:180}""",
  [("Short (<155cm)","#3b82f6",0,40),("Average (155-180cm)","#22c55e",40,75),("Tall (180-200cm)","#f59e0b",75,90),("Very tall (200+cm)","#ef4444",90,100)],
  "% of 200cm","200",
  [("How do I convert feet and inches to centimeters?","Total inches = feet x 12 + inches. Then cm = total inches x 2.54. Example: 5ft 11in = (5 x 12) + 11 = 71 inches. 71 x 2.54 = 180.34 cm. Shortcut: roughly 1 foot ≈ 30.48 cm, 1 inch ≈ 2.54 cm."),
   ("What is the average height for men and women?","US average: Men 5ft 9in (175.3 cm), Women 5ft 4in (162.6 cm). Global averages vary: Netherlands men average 6ft (182.9 cm), Bolivian women average 4ft 11in (149.8 cm). Heights have been increasing over the 20th century due to improved nutrition and healthcare."),
   ("How do I convert cm to feet and inches?","Divide cm by 2.54 to get total inches. Then floor(total inches / 12) = feet, and total inches mod 12 = remaining inches. Example: 180 cm / 2.54 = 70.866 inches. 70.866 / 12 = 5 feet remainder 10.866 inches ≈ 5ft 10.9in."),
   ("What height is considered tall?","Culturally varies by country. In the US: men above 6ft (183 cm) are often considered tall, while 6ft 2in+ (188 cm) is very tall. Women: above 5ft 8in (173 cm) is often considered tall. Medically, tall stature means height above the 95th percentile. Extremely tall heights may be investigated for growth hormone disorders."),
   ("Why do some countries use centimeters for height?","The metric system (centimeters, kilograms) is used in most countries worldwide. The US, Liberia, and Myanmar primarily use the imperial system (feet, inches, pounds). Medically and scientifically, metric is standard globally. Many US-born individuals know their height in feet/inches but have to look up the centimeter equivalent.")],
  [("BMI Calculator","/calculators/bmi-calculator"),("Ideal Weight Calculator","/calculators/ideal-weight-calculator"),("Shoe Size Calculator","/calculators/shoe-size-calculator"),("Unit Converter","/calculators/unit-converter-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Quick Reference</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700"><th class="text-left">Feet & In</th><th class="text-right">cm</th></tr></thead>
            <tbody class="text-blue-900">
              {[["5ft 0in","152.4"],["5ft 4in","162.6"],["5ft 9in","175.3"],["6ft 0in","182.9"],["6ft 4in","193.0"],["6ft 8in","203.2"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right">{r[1]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Height Conversion Formula</h2>
        <div class="bg-gray-50 rounded-xl p-4">
          <div class="text-xs text-gray-600 space-y-2 font-mono">
            <div>1 inch = 2.54 cm exactly</div>
            <div>1 foot = 12 inches = 30.48 cm</div>
            <div>1 meter = 100 cm = ~3 ft 3.4 in</div>
            <div class="mt-2">Feet+Inches → cm:</div>
            <div>cm = (feet × 12 + inches) × 2.54</div>
            <div class="mt-1">cm → Feet+Inches:</div>
            <div>inches = cm / 2.54</div>
            <div>feet = floor(inches / 12)</div>
            <div>remaining = inches mod 12</div>
          </div>
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Average Heights by Country</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Country</th><th class="p-2 text-xs text-right">Men</th><th class="p-2 text-xs text-right">Women</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Netherlands","182.9cm","170.7cm"],["USA","175.4cm","162.1cm"],["Germany","179.9cm","165.9cm"],["Japan","171.2cm","158.8cm"],["India","165.3cm","152.6cm"],["Brazil","170.7cm","159.3cm"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "Result","Convert height between feet/inches and centimeters")

# ── GST / VAT ─────────────────────────────────────────────────────────────────
w("gst-vat","GST VAT Calculator","Other","other",
  "GST VAT Calculator: Add or Remove Tax from Prices",
  "Calculate GST (Goods and Services Tax) or VAT (Value Added Tax). Add tax to a price or remove tax from a GST-inclusive amount. Free tax calculator.",
  """
  const price = parseFloat(inputs.price)||0
  const rate = parseFloat(inputs.rate)||10
  const mode = inputs.mode||"add"
  if(price<=0) throw new Error("Enter a price.")
  if(rate<=0||rate>100) throw new Error("Enter a valid tax rate (0-100%).")
  let excl, incl, taxAmount
  if(mode==="add"){
    excl=price; taxAmount=price*rate/100; incl=price+taxAmount
  } else {
    incl=price; excl=price/(1+rate/100); taxAmount=price-excl
  }
  return {
    value:mode==="add"?"$"+incl.toFixed(2)+" (inc. GST/VAT)":"$"+excl.toFixed(2)+" (exc. GST/VAT)",
    gaugeValue:rate,
    breakdown:["Price (excl. tax): $"+excl.toFixed(2),"Tax amount ("+rate+"%): $"+taxAmount.toFixed(2),"Price (incl. tax): $"+incl.toFixed(2),"Tax rate: "+rate+"%","Tax as % of incl. price: "+(taxAmount/incl*100).toFixed(2)+"%"],
    stats:[
      {label:"Excl. Tax",value:"$"+excl.toFixed(2)},
      {label:"Tax ("+rate+"%)",value:"$"+taxAmount.toFixed(2)},
      {label:"Incl. Tax",value:"$"+incl.toFixed(2)},
      {label:"Tax Rate",value:rate+"%"},
    ]
  }
""",
  """{id:"price",label:"Amount ($)",type:"number",placeholder:"100",min:0,step:0.01,defaultValue:100},
            {id:"rate",label:"Tax rate (%)",type:"number",placeholder:"10",min:0,max:100,step:0.1,defaultValue:10},
            {id:"mode",label:"Mode",type:"select",options:[
              {value:"add",label:"Add tax to price (price + GST)"},
              {value:"remove",label:"Remove tax from inclusive price (GST inclusive → exclusive)"},
            ],defaultValue:"add"}""",
  [("Low rate (<10%)","#22c55e",0,10),("Standard (10-20%)","#3b82f6",10,20),("High rate (20%+)","#ef4444",20,100)],
  "% tax rate","100",
  [("How do I calculate GST from an inclusive price?","To extract GST from a GST-inclusive price: Tax = Price × rate / (100 + rate). Excl. price = Price / (1 + rate/100). Example: price $110 including 10% GST: Tax = 110 × 10 / 110 = $10. Excl. = 110 / 1.1 = $100. This is the reverse calculation (remove GST)."),
   ("What are GST rates by country?","Australia: 10%. Canada: 5% GST + provincial tax (0-10%). New Zealand: 15%. Singapore: 9% (2024). India: multiple rates (0%, 5%, 12%, 18%, 28%). UK VAT: standard 20%, reduced 5%, zero-rated 0%. EU VAT: varies by country (Germany 19%, France 20%, Luxembourg 17%)."),
   ("What is the difference between GST and VAT?","GST (Goods and Services Tax) and VAT (Value Added Tax) are essentially the same concept: a consumption tax levied at each stage of production/sale, but the consumer ultimately pays. The naming varies by country. Australia, Canada, New Zealand use GST. UK, EU countries use VAT. India uses GST on a unified basis."),
   ("What goods and services are tax-exempt?","Common exemptions (vary by country): Basic food items (groceries, but not restaurant meals). Healthcare and medical services. Education. Financial services. Real property (residential). Religious services. In Australia, these are called GST-free supplies. In the UK, some items are zero-rated (taxable at 0%) vs exempt (outside the VAT system)."),
   ("How does a business collect and remit GST/VAT?","Businesses registered for GST/VAT charge tax on sales (output tax), can claim credit for tax paid on business purchases (input tax), and pay the net difference to the government. This is called input tax credits in Australia and input VAT in EU. Small businesses under the registration threshold (e.g., AUD $75,000 in Australia) may not need to register.")],
  [("Sales Tax Calculator","/calculators/sales-tax-calculator"),("Discount Calculator","/calculators/discount-calculator"),("Percentage Calculator","/calculators/percentage-calculator"),("Budget Calculator","/calculators/budget-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">GST/VAT Rates</h3>
          <div class="text-xs text-blue-800 space-y-1">
            {[["Australia","10%"],["New Zealand","15%"],["Canada (GST)","5%"],["UK (VAT)","20%"],["Germany (VAT)","19%"],["Singapore","9%"],["India (standard)","18%"],["USA","N/A (state sales tax)"]].map(([c,r]) => (
              <div class="flex justify-between border-b border-blue-100 pb-0.5"><span>{c}</span><span class="font-mono font-medium">{r}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">GST / VAT Formulas</h2>
        <div class="bg-gray-50 rounded-xl p-4">
          <div class="text-xs text-gray-600 space-y-2 font-mono">
            <div class="font-semibold text-gray-800">Add tax:</div>
            <div>Tax = Price × rate / 100</div>
            <div>Total = Price + Tax</div>
            <div class="mt-2 font-semibold text-gray-800">Remove tax from incl. price:</div>
            <div>Excl. = Incl. / (1 + rate/100)</div>
            <div>Tax = Incl. - Excl.</div>
            <div class="mt-2 font-semibold text-gray-800">Example at 10%:</div>
            <div>$100 + 10% = $110 incl.</div>
            <div>$110 incl. → $100 excl. + $10 tax</div>
          </div>
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Tax at Common Rates</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Excl. Price</th><th class="p-2 text-xs text-right">+10% tax</th><th class="p-2 text-xs text-right">+15%</th><th class="p-2 text-xs text-right">+20%</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["$10","$11.00","$11.50","$12.00"],["$50","$55.00","$57.50","$60.00"],["$100","$110.00","$115.00","$120.00"],["$500","$550.00","$575.00","$600.00"],["$1,000","$1,100","$1,150","$1,200"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td><td class="p-2 text-xs text-right">{r[3]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "Result","Calculate GST/VAT inclusive and exclusive prices")

# ── LOVE ─────────────────────────────────────────────────────────────────────
w("love","Love Compatibility Calculator","Other","other",
  "Love Compatibility Calculator: Relationship Compatibility Score",
  "Find your love compatibility score based on names and birthdays. Fun relationship compatibility calculator using numerology and astrology.",
  """
  const name1 = (inputs.name1||"").toLowerCase().trim()
  const name2 = (inputs.name2||"").toLowerCase().trim()
  if(!name1||!name2) throw new Error("Enter both names.")
  const numValue = s => s.split("").reduce((acc,c)=>{const code=c.charCodeAt(0)-96;return code>0&&code<=26?acc+code:acc},0)
  const n1 = numValue(name1)
  const n2 = numValue(name2)
  const combined = (n1+n2)
  const score = Math.abs((combined*37+name1.length*n2+name2.length*n1)%101)
  const adjScore = Math.max(score, 100-score)
  const level = adjScore>=90?"Perfect Match":adjScore>=75?"Strong Connection":adjScore>=60?"Good Compatibility":adjScore>=45?"Some Compatibility":"Challenging"
  return {
    value:adjScore+"% — "+level,
    gaugeValue:adjScore,
    breakdown:["Name 1: "+inputs.name1+" (value: "+n1+")","Name 2: "+inputs.name2+" (value: "+n2+")","Combined: "+combined,"Compatibility score: "+adjScore+"%","Status: "+level,"Note: This is just for fun — real compatibility is built over time!"],
    stats:[
      {label:"Compatibility",value:adjScore+"%"},
      {label:"Level",value:level},
      {label:inputs.name1+" value",value:String(n1)},
      {label:inputs.name2+" value",value:String(n2)},
    ]
  }
""",
  """{id:"name1",label:"Your name",type:"text",placeholder:"Alice",defaultValue:"Alice"},
            {id:"name2",label:"Partner name",type:"text",placeholder:"Bob",defaultValue:"Bob"}""",
  [("Challenging (<50%)","#ef4444",0,50),("Good (50-75%)","#f59e0b",50,75),("Strong (75-90%)","#3b82f6",75,90),("Perfect (90%+)","#22c55e",90,100)],
  "% compatibility","100",
  [("How does love compatibility work?","Our calculator assigns numerical values to letters in each name and computes a fun compatibility score. This is purely for entertainment — real relationship compatibility depends on shared values, communication, respect, trust, and time spent together, not on names or numbers."),
   ("What makes a relationship truly compatible?","Research shows the key factors are: shared values (most important), emotional intelligence (ability to manage conflict), similar relationship goals, respect and trust, good communication, and physical attraction. Couples who openly discuss differences and resolve conflicts constructively tend to have the most lasting relationships."),
   ("What is the FLAME compatibility method?","FLAME is a classic schoolyard compatibility game using both names. Write out FRIENDS LOVE AFFECTION MARRIAGE ENEMIES, then cross off shared letters between names, count what remains, and cycle through FLAME letters until one remains. It is purely a fun game with no scientific basis."),
   ("Do zodiac signs predict relationship compatibility?","Astrology compatibility is a popular cultural tradition. Sun signs are often matched (e.g., Taurus and Virgo as earth signs), but there is no scientific evidence that zodiac signs predict relationship outcomes. Real compatibility researchers (like John Gottman) focus on communication patterns, conflict resolution, and shared goals."),
   ("What is the most important factor in relationship success?","Research by John Gottman (University of Washington) identifies the ratio of positive to negative interactions. Successful couples average 5:1 positive-to-negative interactions. Other key factors: avoiding the four horsemen (criticism, contempt, defensiveness, stonewalling), turning toward each other during stress, and maintaining friendship and admiration.")],
  [("Age Calculator","/calculators/age-calculator"),("Zodiac Calculator","/calculators/zodiac-calculator"),("Numerology Calculator","/calculators/numerology-calculator"),("Birthday Calculator","/calculators/date-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Love Language Breakdown</h3>
          <div class="text-xs text-blue-800 space-y-1">
            {[["Words of Affirmation","Verbal compliments, appreciation"],["Quality Time","Undivided attention, shared experiences"],["Acts of Service","Helpful actions, taking care of tasks"],["Gifts","Thoughtful presents, symbolic tokens"],["Physical Touch","Hugs, holding hands, closeness"]].map(([l,d]) => (
              <div class="border-b border-blue-100 pb-0.5"><div class="font-semibold">{l}</div><div>{d}</div></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Zodiac Compatibility</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Sign</th><th class="p-2 text-xs font-semibold text-right">Best Matches</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Aries","Leo, Sagittarius"],["Taurus","Virgo, Capricorn"],["Gemini","Libra, Aquarius"],["Cancer","Scorpio, Pisces"],["Leo","Aries, Sagittarius"],["Virgo","Taurus, Capricorn"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Relationship Tips</h2>
        <div class="space-y-2">
          {["Learn your partner love language (Gary Chapman framework)","Gottman ratio: aim for 5 positive interactions per negative","Show appreciation daily — even small acknowledgements matter","Conflict is normal — it is how you resolve it that counts","Shared experiences build stronger bonds than material gifts","Maintain individual friendships and hobbies outside the relationship"].map(t => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-red-400 mt-0.5">♥</span><span>{t}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Compatibility %","Calculate fun love compatibility score")

# ── MILITARY TIME ─────────────────────────────────────────────────────────────
w("military-time","Military Time Converter","Other","other",
  "Military Time Converter: 24-Hour to 12-Hour Clock",
  "Convert between military time (24-hour clock) and standard 12-hour time (AM/PM). Free military time converter with chart.",
  """
  const input = (inputs.time||"").trim()
  const direction = inputs.direction||"to_standard"
  if(direction==="to_standard"){
    const h=parseInt(input.slice(0,2))||0
    const m=parseInt(input.slice(2,4))||0
    if(h<0||h>23||m<0||m>59) throw new Error("Enter valid military time (0000-2359).")
    const period=h<12?"AM":"PM"
    const h12=h===0?12:h>12?h-12:h
    const result=h12+":"+String(m).padStart(2,"0")+" "+period
    return {
      value:input+" → "+result,
      gaugeValue:((h*60+m)/1440)*100,
      breakdown:["Military: "+String(h).padStart(2,"0")+String(m).padStart(2,"0"),"Standard: "+result,"Hours (24h): "+h,"Minutes: "+m,"Time of day: "+h+" hours into the day"],
      stats:[
        {label:"Standard (12h)",value:result},
        {label:"Military (24h)",value:String(h).padStart(2,"0")+":"+String(m).padStart(2,"0")},
        {label:"AM or PM",value:period},
        {label:"% of day elapsed",value:((h*60+m)/1440*100).toFixed(1)+"%"},
      ]
    }
  } else {
    const match=input.match(/(\\d{1,2}):(\\d{2})\\s*(AM|PM|am|pm)/i)
    if(!match) throw new Error("Enter time as H:MM AM or H:MM PM")
    let h=parseInt(match[1]),m=parseInt(match[2])
    const period=match[3].toUpperCase()
    if(period==="AM"&&h===12) h=0
    else if(period==="PM"&&h!==12) h+=12
    const military=String(h).padStart(2,"0")+String(m).padStart(2,"0")
    return {
      value:input+" → "+military,
      gaugeValue:((h*60+m)/1440)*100,
      breakdown:["Standard: "+input,"Military: "+military,"24h time: "+h+":"+String(m).padStart(2,"0"),"Hours into day: "+h],
      stats:[
        {label:"Military Time",value:military},
        {label:"Standard",value:input},
        {label:"24h Format",value:String(h).padStart(2,"0")+":"+String(m).padStart(2,"0")},
        {label:"Day elapsed",value:((h*60+m)/1440*100).toFixed(1)+"%"},
      ]
    }
  }
""",
  """{id:"time",label:"Time to convert",type:"text",placeholder:"1430 or 2:30 PM",defaultValue:"1430"},
            {id:"direction",label:"Direction",type:"select",options:[
              {value:"to_standard",label:"Military → Standard (e.g. 1430 → 2:30 PM)"},
              {value:"to_military",label:"Standard → Military (e.g. 2:30 PM → 1430)"},
            ],defaultValue:"to_standard"}""",
  [("Midnight-6am","#3b82f6",0,25),("Morning 6am-12pm","#22c55e",25,50),("Afternoon 12-6pm","#f59e0b",50,75),("Evening 6pm-midnight","#ef4444",75,100)],
  "% of day","100",
  [("How does military time work?","Military time uses a 24-hour clock: 0000 to 2359. Hours go from 00 (midnight) to 23 (11 PM). There is no AM/PM. Read as 4 digits: 0830 is eight thirty, 1400 is fourteen hundred, 2230 is twenty-two thirty. To convert to 12-hour: for hours > 12, subtract 12 and add PM."),
   ("How do I convert 1730 to standard time?","1730 military: 17 - 12 = 5, so 5:30 PM. Any hour 1300-2359: subtract 12 for PM hours. Hours 1200-1259 remain as 12:xx PM. Hours 0000-0059 are 12:xx AM. Hours 0100-1159 are the same number in AM."),
   ("Why does the military use 24-hour time?","To avoid ambiguity. In military, emergency services, aviation, and healthcare, mistaking 6:00 AM for 6:00 PM could be catastrophic. 24-hour time is unambiguous. Also used internationally: most of the world uses 24-hour time in formal and professional contexts."),
   ("What time zones do the military use?","Military uses one-letter time zone abbreviations. Z = Zulu = UTC (Greenwich). Alpha through Mike (A-M, skipping J) are east of UTC. November through Yankee (N-Y) are west of UTC. Z (Zulu) is always UTC and is the military standard time for coordination across time zones."),
   ("What does 0000 vs 2400 mean?","0000 (zero-zero-zero-zero) = midnight (start of day). It is the first moment of a new day. 2400 is technically the last moment of the day (end of day) — equivalent to 0000 of the next day. In practice, most systems use 0000 for midnight and avoid 2400. 1200 = noon exactly.")],
  [("Time Calculator","/calculators/time-calculator"),("Age Calculator","/calculators/age-calculator"),("Date Calculator","/calculators/date-calculator"),("Days Until Calculator","/calculators/days-until-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Quick Conversion</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700"><th class="text-left">Military</th><th class="text-right">Standard</th></tr></thead>
            <tbody class="font-mono text-blue-900">
              {[["0000","12:00 AM"],["0600","6:00 AM"],["1200","12:00 PM"],["1300","1:00 PM"],["1800","6:00 PM"],["2000","8:00 PM"],["2359","11:59 PM"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right">{r[1]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-10">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Full Military Time Chart</h2>
      <div class="overflow-x-auto">
        <div class="grid grid-cols-4 md:grid-cols-6 gap-2">
          {Array.from({length:24},(_,h) => (
            <div class="bg-gray-50 rounded p-2 text-center">
              <div class="font-mono font-bold text-blue-700 text-xs">{String(h).padStart(2,"0")}00</div>
              <div class="text-xs text-gray-600">{h===0?"12:00 AM":h<12?h+":00 AM":h===12?"12:00 PM":(h-12)+":00 PM"}</div>
            </div>
          ))}
        </div>
      </div>
    </div>""",
  "Result","Convert between military time and 12-hour clock")

# ── WORD COUNT ────────────────────────────────────────────────────────────────
w("word-count","Word Count Calculator","Other","other",
  "Word Count Calculator: Count Words, Characters, Sentences",
  "Count words, characters, sentences, paragraphs, and estimate reading time for any text. Free word count tool.",
  """
  const text = inputs.text||""
  if(!text.trim()) throw new Error("Enter some text to analyze.")
  const words = text.trim().split(/\\s+/).filter(w=>w.length>0)
  const wordCount = words.length
  const charCount = text.length
  const charNoSpaces = text.replace(/\\s/g,"").length
  const sentences = (text.match(/[^.!?]+[.!?]+/g)||[]).length || (text.trim()? 1 : 0)
  const paragraphs = text.split(/\\n\\s*\\n/).filter(p=>p.trim()).length||1
  const readingTimeMin = wordCount/238
  const avgWordLen = charNoSpaces/Math.max(wordCount,1)
  return {
    value:wordCount+" words | "+charCount+" characters",
    gaugeValue:Math.min(wordCount/1000*100,100),
    breakdown:["Words: "+wordCount,"Characters (with spaces): "+charCount,"Characters (no spaces): "+charNoSpaces,"Sentences: "+sentences,"Paragraphs: "+paragraphs,"Reading time: "+readingTimeMin.toFixed(2)+" min (avg 238 wpm)","Average word length: "+avgWordLen.toFixed(1)+" chars"],
    stats:[
      {label:"Word Count",value:wordCount.toLocaleString()},
      {label:"Characters",value:charCount.toLocaleString()},
      {label:"Sentences",value:String(sentences)},
      {label:"Reading Time",value:readingTimeMin<1?Math.round(readingTimeMin*60)+" sec":readingTimeMin.toFixed(1)+" min"},
    ]
  }
""",
  """{id:"text",label:"Paste or type your text here",type:"textarea",placeholder:"Enter your text here...",rows:8,defaultValue:"The quick brown fox jumps over the lazy dog. This sentence is a classic pangram used to test typefaces and keyboards."}""",
  [("Short (<100 words)","#22c55e",0,10),("Medium (100-500)","#3b82f6",10,50),("Long (500-1000)","#f59e0b",50,100)],
  "words","1000",
  [("How many words is a typical essay, article, or book?","Tweet: 280 characters (~50 words). Blog post: 300-2,500 words. Short story: 1,000-7,500 words. Novella: 20,000-50,000 words. Novel: 50,000-100,000+ words. Academic essay: 500-5,000 words. Research paper: 3,000-8,000 words. PhD dissertation: 80,000-100,000 words."),
   ("How fast does the average person read?","Average adult: 238-250 words per minute (wpm) for comprehension. Faster readers with training: 300-400 wpm. Speed readers: 500-1,500 wpm (with reduced comprehension). Children: 100-200 wpm. Audio books typical speed: 150-160 wpm. This calculator uses 238 wpm for reading time estimates."),
   ("What is the ideal word count for SEO blog posts?","Studies suggest: long-form content (1,500-2,500 words) often ranks better for competitive keywords. Short posts (300-500 words) can rank for specific low-competition queries. Quality and relevance matter more than word count. Google prefers content that fully answers user intent, regardless of length."),
   ("How do I count words in Microsoft Word or Google Docs?","Microsoft Word: Review tab → Word Count (or Ctrl+Shift+G). Google Docs: Tools → Word Count (or Ctrl+Shift+C). Both show words, characters with/without spaces, and pages. Select text first to count only a portion. Many writing apps display word count in the bottom status bar."),
   ("What is a character limit and why does it matter?","Twitter: 280 characters. Instagram captions: 2,200. Meta descriptions (SEO): 150-160 characters. SMS: 160 characters (GSM) or 70 (Unicode). Database fields often have varchar limits. Email subject lines: ~50-60 characters to avoid truncation in email clients. Knowing character limits helps craft concise, effective content.")],
  [("Average Calculator","/calculators/average-calculator"),("Percentage Calculator","/calculators/percentage-calculator"),("Grade Calculator","/calculators/grade-calculator"),("GPA Calculator","/calculators/gpa-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Common Word Counts</h3>
          <div class="text-xs text-blue-800 space-y-1">
            {[["Tweet","~50 words"],["Blog post","300-2,500"],["Short story","1,000-7,500"],["Novella","20,000-50,000"],["Novel","50,000-100,000"],["PhD thesis","80,000-100,000"]].map(([t,c]) => (
              <div class="flex justify-between border-b border-blue-100 pb-0.5"><span>{t}</span><span class="font-mono">{c}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Reading Time Estimates</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Words</th><th class="p-2 text-xs font-semibold text-right">Reading Time (238 wpm)</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[[100,"~25 sec"],[300,"~1.3 min"],[500,"~2.1 min"],[1000,"~4.2 min"],[2500,"~10.5 min"],[5000,"~21 min"],[10000,"~42 min"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Character Limits</h2>
        <div class="space-y-2">
          {["Twitter/X: 280 characters per tweet","Instagram caption: 2,200 characters","Meta description (SEO): 150-160 chars","SMS: 160 chars (English), 70 (emoji/Unicode)","Email subject: ~60 chars before truncation","YouTube title: 100 chars (70 recommended)"].map(l => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{l}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Words","Count words, characters, sentences, and reading time")

print(f"\nWritten: {written} pages")
