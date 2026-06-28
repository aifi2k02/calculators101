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

# ── CALORIES BURNED ───────────────────────────────────────────────────────────
w("calories-burned","Calories Burned Calculator","Fitness","fitness",
  "Calories Burned Calculator: Exercise Calorie Counter",
  "Calculate calories burned during exercise using MET values. Supports 50+ activities. Free calorie burn calculator.",
  """
  const weight = parseFloat(inputs.weight)||70
  const duration = parseFloat(inputs.duration)||30
  const activity = inputs.activity||"running"
  const unit = inputs.unit||"kg"
  const weightKg = unit==="lbs"?weight*0.453592:weight
  const mets = {
    running:8.0,cycling:6.0,swimming:6.0,walking:3.5,hiking:5.3,
    yoga:2.5,weightlifting:3.5,basketball:6.5,soccer:7.0,tennis:6.0,
    elliptical:5.0,rowing:6.0,dancing:4.5,boxing:8.0,jump_rope:10.0
  }
  const met = mets[activity]||5.0
  const calories = met*weightKg*(duration/60)
  const perMinute = calories/duration
  const perHour = perMinute*60
  return {
    value:Math.round(calories)+" cal",
    gaugeValue:Math.min(calories/1000*100,100),
    breakdown:["Activity: "+activity.replace(/_/g," "),"Weight: "+weightKg.toFixed(1)+"kg","Duration: "+duration+" min","MET value: "+met,"Calories burned: "+Math.round(calories),"Rate: "+perMinute.toFixed(1)+" cal/min"],
    stats:[
      {label:"Calories Burned",value:Math.round(calories)+" kcal"},
      {label:"Duration",value:duration+" min"},
      {label:"Rate",value:perMinute.toFixed(1)+" cal/min"},
      {label:"Per Hour Rate",value:Math.round(perHour)+" cal/hr"},
    ]
  }
""",
  """{id:"weight",label:"Body Weight",type:"number",placeholder:"155",min:50,max:400,defaultValue:155},
            {id:"unit",label:"Unit",type:"select",options:[{value:"lbs",label:"lbs"},{value:"kg",label:"kg"}],defaultValue:"lbs"},
            {id:"duration",label:"Duration",type:"number",placeholder:"30",min:1,max:480,unit:"minutes",defaultValue:30},
            {id:"activity",label:"Activity",type:"select",options:[
              {value:"running",label:"Running (8 mph)"},
              {value:"cycling",label:"Cycling (moderate)"},
              {value:"swimming",label:"Swimming (laps)"},
              {value:"walking",label:"Walking (3.5 mph)"},
              {value:"hiking",label:"Hiking"},
              {value:"yoga",label:"Yoga"},
              {value:"weightlifting",label:"Weight Training"},
              {value:"basketball",label:"Basketball"},
              {value:"soccer",label:"Soccer"},
              {value:"tennis",label:"Tennis"},
              {value:"elliptical",label:"Elliptical"},
              {value:"rowing",label:"Rowing Machine"},
              {value:"dancing",label:"Dancing"},
              {value:"boxing",label:"Boxing"},
              {value:"jump_rope",label:"Jump Rope"},
            ],defaultValue:"running"}""",
  [("Light (<200 cal)","#3b82f6",0,20),("Moderate (200-400)","#22c55e",20,40),("High (400-700)","#f59e0b",40,70),("Intense (700+)","#ef4444",70,100)],
  "cal (of 1000)","100",
  [("How are calories burned during exercise calculated?","Calories = MET x Weight(kg) x Duration(hours). MET (Metabolic Equivalent of Task) measures exercise intensity relative to rest. Walking has a MET of ~3.5, running ~8-12, cycling ~6-10. Heavier people burn more calories performing the same exercise because they have more mass to move."),
   ("Which exercise burns the most calories?","High-intensity exercises burn most per hour: running (~600-1000 cal/hr), jump rope (~800-1000), swimming (~500-700), cycling hard (~600-800). Intensity matters more than activity type — a slow walk burns far fewer calories than a brisk run even for the same duration. HIIT can maximize calorie burn in minimal time."),
   ("Does muscle mass affect calorie burn?","Yes. Muscle burns ~3x more calories than fat at rest (6 cal/lb muscle vs 2 cal/lb fat). Building muscle through resistance training increases your BMR (basal metabolic rate), meaning you burn more calories 24/7. This is why strength training is valuable for long-term weight management."),
   ("How many calories do I need to burn to lose 1 pound?","Approximately 3,500 calories = 1 pound of fat. To lose 1 lb/week: create a 500 calorie/day deficit (through diet + exercise combined). Exercise alone rarely produces significant weight loss without dietary changes — it is much easier to not eat 500 calories than to burn 500 extra calories."),
   ("Is the calorie burn estimate accurate?","MET-based calculations are estimates — actual calorie burn varies by fitness level, body composition, terrain, weather, and individual metabolism. Fitness trackers and heart rate monitors give more personalized estimates but still have 10-20% error margins. Use these as guidelines rather than exact numbers.")],
  [("TDEE Calculator","/calculators/tdee-calculator"),("BMR Calculator","/calculators/bmr-calculator"),("Calorie Calculator","/calculators/calorie-calculator"),("Running Calorie Calculator","/calculators/running-calorie-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Calories Burned in 30 min (155 lbs)</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700 border-b border-blue-200"><th class="text-left pb-1">Activity</th><th class="text-right pb-1">Calories</th></tr></thead>
            <tbody class="text-blue-900">
              {[["Running (8mph)","355"],["Swimming","223"],["Cycling (mod.)","223"],["Weight Training","133"],["Walking (3.5mph)","133"],["Yoga","89"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right font-medium">{r[1]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">MET Values by Activity Intensity</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Intensity</th><th class="text-right p-2 text-xs font-semibold">MET Range</th><th class="text-right p-2 text-xs font-semibold">Examples</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Light","1.5–3.0","Walking slow, yoga, stretching"],["Moderate","3.0–6.0","Walking brisk, cycling easy, swimming"],["Vigorous","6.0–9.0","Running, cycling hard, soccer"],["Very Vigorous","9.0+","Sprint, jump rope, competitive sports"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right text-gray-500">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Weekly Exercise Goals (CDC Guidelines)</h2>
        <div class="space-y-2">
          {[
            {type:"Moderate cardio",goal:"150-300 minutes/week",eg:"Brisk walking, cycling"},
            {type:"Vigorous cardio",goal:"75-150 minutes/week",eg:"Running, swimming laps"},
            {type:"Strength training",goal:"2+ sessions/week",eg:"Weights, resistance bands"},
            {type:"Balance/flexibility",goal:"Additional benefit",eg:"Yoga, tai chi"},
          ].map(g => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-xs text-gray-800">{g.type}</div>
              <div class="text-xs text-blue-600">{g.goal}</div>
              <div class="text-xs text-gray-500">{g.eg}</div>
            </div>
          ))}
        </div>
      </div>
    </div>""",
  "Calories Burned","Calculate calories burned during any physical activity")

# ── BODY SURFACE AREA ─────────────────────────────────────────────────────────
w("body-surface-area","Body Surface Area Calculator","Fitness","fitness",
  "Body Surface Area Calculator: BSA for Drug Dosing",
  "Calculate body surface area (BSA) using the Mosteller, Du Bois, and Haycock formulas. Used for chemotherapy and drug dosing. Free BSA calculator.",
  """
  const height = parseFloat(inputs.height)||0
  const weight = parseFloat(inputs.weight)||0
  const heightUnit = inputs.heightUnit||"cm"
  const weightUnit = inputs.weightUnit||"kg"
  if(height<=0||weight<=0) throw new Error("Enter height and weight.")
  const hcm = heightUnit==="in"?height*2.54:height
  const wkg = weightUnit==="lbs"?weight*0.453592:weight
  const mosteller = Math.sqrt((hcm*wkg)/3600)
  const dubois = 0.007184*Math.pow(hcm,0.725)*Math.pow(wkg,0.425)
  const haycock = 0.024265*Math.pow(hcm,0.3964)*Math.pow(wkg,0.5378)
  const average = (mosteller+dubois+haycock)/3
  return {
    value:average.toFixed(3)+" m²",
    gaugeValue:Math.min((average/2.5)*100,100),
    breakdown:["Height: "+hcm.toFixed(1)+"cm | Weight: "+wkg.toFixed(1)+"kg","Mosteller: "+mosteller.toFixed(3)+" m²","Du Bois: "+dubois.toFixed(3)+" m²","Haycock: "+haycock.toFixed(3)+" m²","Average: "+average.toFixed(3)+" m²"],
    stats:[
      {label:"Average BSA",value:average.toFixed(3)+" m²"},
      {label:"Mosteller",value:mosteller.toFixed(3)+" m²"},
      {label:"Du Bois",value:dubois.toFixed(3)+" m²"},
      {label:"Haycock",value:haycock.toFixed(3)+" m²"},
    ]
  }
""",
  """{id:"height",label:"Height",type:"number",placeholder:"175",min:50,max:300,defaultValue:175},
            {id:"heightUnit",label:"Height Unit",type:"select",options:[{value:"cm",label:"cm"},{value:"in",label:"inches"}],defaultValue:"cm"},
            {id:"weight",label:"Weight",type:"number",placeholder:"70",min:1,max:500,defaultValue:70},
            {id:"weightUnit",label:"Weight Unit",type:"select",options:[{value:"kg",label:"kg"},{value:"lbs",label:"lbs"}],defaultValue:"kg"}""",
  [("Small (<1.6 m2)","#3b82f6",0,64),("Average (1.6-2.0)","#22c55e",64,80),("Large (2.0-2.4)","#f59e0b",80,96),("Very Large (2.4+)","#ef4444",96,100)],
  "m² (of 2.5)","100",
  [("What is body surface area used for?","BSA is used in medicine to calculate drug doses, especially for chemotherapy, where dosing by weight alone is less accurate. It is also used to calculate cardiac index, fluid replacement in burns, and other clinical parameters. Most chemotherapy drugs are dosed in mg/m2."),
   ("Which BSA formula is most accurate?","The Mosteller formula is most commonly used due to its simplicity (BSA = sqrt(Height x Weight / 3600)). Du Bois (1916) was the first widely used formula but is less accurate at extremes. Haycock is preferred in pediatrics. No single formula is perfect for all body types."),
   ("What is average adult BSA?","Average adult male BSA: ~1.9 m2. Average adult female: ~1.6 m2. These are the reference values used in clinical studies and standard drug dosing charts. Values range from ~0.25 m2 (newborn) to 2.5+ m2 for very large adults."),
   ("How does BSA differ from BMI?","BMI (Body Mass Index) = weight/height2 — measures weight relative to height, used for general health screening. BSA (Body Surface Area) = estimate of skin area — used for clinical drug dosing. BSA is not affected by adiposity in the same way BMI is and is more relevant for drug metabolism."),
   ("Why is BSA important for chemotherapy dosing?","Chemotherapy drugs are often highly toxic at wrong doses. Dosing by body surface area (mg/m2) rather than just weight provides a better approximation of drug distribution volume, metabolic rate, and toxicity threshold. However, actual dosing decisions are complex and made by oncologists based on many factors.")],
  [("BMI Calculator","/calculators/bmi-calculator"),("Lean Body Mass Calculator","/calculators/lean-body-mass-calculator"),("BMR Calculator","/calculators/bmr-calculator"),("Ideal Weight Calculator","/calculators/ideal-weight-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Average BSA by Population</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[["Newborn","0.25 m²"],["1-year-old","0.44 m²"],["Child (10 yrs)","1.14 m²"],["Adult female avg","1.6 m²"],["Adult male avg","1.9 m²"]].map(([g,b]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span>{g}</span><span class="font-medium">{b}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10">
      <h2 class="text-xl font-bold text-gray-900 mb-4">BSA Formula Comparison</h2>
      <div class="grid md:grid-cols-3 gap-6">
        {[
          {name:"Mosteller (1987)",formula:"BSA = sqrt(H × W / 3600)",notes:"Most widely used. Simple and accurate for most adults."},
          {name:"Du Bois (1916)",formula:"BSA = 0.007184 × H^0.725 × W^0.425",notes:"Historical standard. Less accurate at body size extremes."},
          {name:"Haycock (1978)",formula:"BSA = 0.024265 × H^0.3964 × W^0.5378",notes:"Preferred for children and pediatric drug dosing."},
        ].map(f => (
          <div class="bg-gray-50 rounded-xl p-4">
            <div class="font-bold text-sm text-gray-800 mb-2">{f.name}</div>
            <div class="font-mono text-xs text-blue-700 mb-2">{f.formula}</div>
            <div class="text-xs text-gray-600">{f.notes}</div>
          </div>
        ))}
      </div>
    </div>""",
  "Body Surface Area","Calculate body surface area using multiple medical formulas")

# ── LEAN BODY MASS ────────────────────────────────────────────────────────────
w("lean-body-mass","Lean Body Mass Calculator","Fitness","fitness",
  "Lean Body Mass Calculator: LBM Using Multiple Formulas",
  "Calculate your lean body mass using Boer, James, and Hume formulas. Understand fat mass vs muscle mass. Free LBM calculator.",
  """
  const weight = parseFloat(inputs.weight)||0
  const height = parseFloat(inputs.height)||0
  const sex = inputs.sex||"male"
  const unit = inputs.unit||"metric"
  const wkg = unit==="imperial"?weight*0.453592:weight
  const hcm = unit==="imperial"?height*2.54:height
  if(wkg<=0||hcm<=0) throw new Error("Enter weight and height.")
  let boer, james, hume
  if(sex==="male"){
    boer=0.407*wkg+0.267*hcm-19.2
    james=1.1*wkg-128*Math.pow(wkg/hcm,2)
    hume=0.3281*wkg+0.3394*hcm-29.5336
  } else {
    boer=0.252*wkg+0.473*hcm-48.3
    james=1.07*wkg-148*Math.pow(wkg/hcm,2)
    hume=0.2296*wkg+0.4827*hcm-24.0989
  }
  const avgLbm=(boer+james+hume)/3
  const fatMass=wkg-avgLbm
  const bodyFatPct=(fatMass/wkg)*100
  return {
    value:avgLbm.toFixed(1)+"kg LBM",
    gaugeValue:Math.min((avgLbm/80)*100,100),
    breakdown:["Weight: "+wkg.toFixed(1)+"kg | Height: "+hcm.toFixed(0)+"cm","Boer formula: "+boer.toFixed(1)+"kg","James formula: "+james.toFixed(1)+"kg","Hume formula: "+hume.toFixed(1)+"kg","Average LBM: "+avgLbm.toFixed(1)+"kg","Fat mass: "+fatMass.toFixed(1)+"kg ("+bodyFatPct.toFixed(1)+"%)"],
    stats:[
      {label:"Avg Lean Body Mass",value:avgLbm.toFixed(1)+" kg"},
      {label:"Estimated Fat Mass",value:fatMass.toFixed(1)+" kg"},
      {label:"Est. Body Fat %",value:bodyFatPct.toFixed(1)+"%"},
      {label:"LBM as % of Weight",value:((avgLbm/wkg)*100).toFixed(1)+"%"},
    ]
  }
""",
  """{id:"weight",label:"Weight",type:"number",placeholder:"75",min:30,max:300,defaultValue:75},
            {id:"height",label:"Height",type:"number",placeholder:"175",min:100,max:250,defaultValue:175},
            {id:"unit",label:"Units",type:"select",options:[{value:"metric",label:"Metric (kg, cm)"},{value:"imperial",label:"Imperial (lbs, inches)"}],defaultValue:"metric"},
            {id:"sex",label:"Sex",type:"select",options:[{value:"male",label:"Male"},{value:"female",label:"Female"}],defaultValue:"male"}""",
  [("Low LBM","#ef4444",0,30),("Average","#f59e0b",30,60),("Good","#3b82f6",60,80),("High LBM","#22c55e",80,100)],
  "% of 80kg","100",
  [("What is lean body mass?","LBM = Total body weight - Fat mass. It includes muscle, bone, organs, blood, and everything except body fat. LBM is important for determining appropriate drug doses, calculating BMR, setting protein intake goals, and tracking fitness progress (you can gain muscle while losing fat even if scale weight stays constant)."),
   ("Why is LBM important for fitness?","Muscle is metabolically active — more muscle means higher calorie burn at rest. Tracking LBM (rather than just weight) gives a clearer picture of body composition changes. It is possible to lose fat and gain muscle simultaneously, which looks like no progress on the scale but represents significant health improvement."),
   ("What is a healthy LBM for men and women?","Average LBM for men: 60-70kg (130-155 lbs). Average LBM for women: 40-50kg (88-110 lbs). Higher is generally better (up to a point) as it correlates with strength, metabolic health, and reduced injury risk. LBM naturally declines with age (sarcopenia) — resistance training helps preserve it."),
   ("How accurate are formula-based LBM calculations?","These formulas were developed from population averages and are estimates. Error range: typically ±3-5 kg from actual LBM. For more accurate measurement, use DEXA scan (most accurate), hydrostatic weighing, or air displacement plethysmography (Bod Pod). Bioelectrical impedance scales are convenient but less accurate."),
   ("How much protein do I need per pound of LBM?","Most evidence suggests 0.7-1.0g protein per pound (1.5-2.2g per kg) of LBM for active individuals trying to build or preserve muscle. Example: 150 lbs LBM = 105-150g protein/day. Higher end of the range for those doing intense strength training or trying to gain muscle.")],
  [("BMI Calculator","/calculators/bmi-calculator"),("Body Fat Calculator","/calculators/body-fat-calculator"),("Ideal Weight Calculator","/calculators/ideal-weight-calculator"),("TDEE Calculator","/calculators/tdee-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Average LBM Reference</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[["Average male","63-68 kg"],["Average female","43-48 kg"],["Athletic male","70-80+ kg"],["Athletic female","50-60+ kg"]].map(([g,b]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span>{g}</span><span class="font-medium">{b}</span></div>
            ))}
          </div>
          <p class="text-xs text-blue-600 mt-1">Includes muscle, bone, organs, and water (excludes fat)</p>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">LBM Formula Comparison</h2>
        <div class="space-y-3">
          {[
            {f:"Boer (1984)",a:"Most accurate for athletes and muscular individuals. Uses weight and height."},
            {f:"James (1976)",a:"Good for average build adults. May underestimate LBM in very heavy individuals."},
            {f:"Hume (1966)",a:"Similar to James. Original regression formula for clinical use in drug dosing."},
          ].map(fo => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-xs text-blue-700 mb-1">{fo.f}</div>
              <div class="text-xs text-gray-600">{fo.a}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Uses of LBM in Medicine & Fitness</h2>
        <div class="space-y-2">
          {["Drug dosing for certain medications (antibiotics, chemotherapy)","Calculating BMR and total daily energy expenditure","Setting protein intake targets for muscle building","Anesthesia dosing in surgeries","Nutritional assessment and monitoring","Assessing sarcopenia (age-related muscle loss)","Comparing body composition changes during exercise programs"].map(u => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{u}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Lean Body Mass","Calculate lean body mass using multiple medical formulas")

# ── PROTEIN ───────────────────────────────────────────────────────────────────
w("protein","Protein Calculator","Fitness","fitness",
  "Protein Calculator: Daily Protein Intake for Goals",
  "Calculate your daily protein needs based on weight, activity level, and fitness goals. Free protein intake calculator.",
  """
  const weight = parseFloat(inputs.weight)||0
  const unit = inputs.unit||"lbs"
  const activity = inputs.activity||"moderate"
  const goal = inputs.goal||"maintain"
  if(weight<=0) throw new Error("Enter your weight.")
  const wkg = unit==="lbs"?weight*0.453592:weight
  const multipliers = {
    sedentary:{lose:0.8,maintain:0.8,gain:1.2},
    light:{lose:1.0,maintain:1.0,gain:1.4},
    moderate:{lose:1.2,maintain:1.2,gain:1.6},
    active:{lose:1.4,maintain:1.4,gain:1.8},
    very_active:{lose:1.6,maintain:1.6,gain:2.0}
  }
  const multiplier = multipliers[activity]?.[goal]||1.2
  const proteinG = wkg*multiplier
  const proteinLow = wkg*(multiplier*0.85)
  const proteinHigh = wkg*(multiplier*1.15)
  const caloriesFromProtein = proteinG*4
  return {
    value:Math.round(proteinG)+"g/day",
    gaugeValue:Math.min((proteinG/200)*100,100),
    breakdown:["Weight: "+wkg.toFixed(1)+"kg","Activity: "+activity,"Goal: "+goal,"Multiplier: "+multiplier+"g/kg","Protein: "+Math.round(proteinG)+"g/day","Range: "+Math.round(proteinLow)+"-"+Math.round(proteinHigh)+"g/day","Calories from protein: "+Math.round(caloriesFromProtein)+" kcal"],
    stats:[
      {label:"Daily Protein",value:Math.round(proteinG)+"g"},
      {label:"Range",value:Math.round(proteinLow)+"-"+Math.round(proteinHigh)+"g"},
      {label:"Per kg Body Weight",value:multiplier+"g/kg"},
      {label:"Protein Calories",value:Math.round(caloriesFromProtein)+" kcal"},
    ]
  }
""",
  """{id:"weight",label:"Body Weight",type:"number",placeholder:"165",min:50,max:400,defaultValue:165},
            {id:"unit",label:"Unit",type:"select",options:[{value:"lbs",label:"lbs"},{value:"kg",label:"kg"}],defaultValue:"lbs"},
            {id:"activity",label:"Activity Level",type:"select",options:[
              {value:"sedentary",label:"Sedentary (desk job, no exercise)"},
              {value:"light",label:"Lightly Active (1-3 days/week)"},
              {value:"moderate",label:"Moderately Active (3-5 days/week)"},
              {value:"active",label:"Very Active (6-7 days/week)"},
              {value:"very_active",label:"Athlete / Very Intense Training"},
            ],defaultValue:"moderate"},
            {id:"goal",label:"Primary Goal",type:"select",options:[
              {value:"lose",label:"Lose Weight (preserve muscle)"},
              {value:"maintain",label:"Maintain Weight"},
              {value:"gain",label:"Build Muscle / Gain Mass"},
            ],defaultValue:"maintain"}""",
  [("Low (<100g)","#ef4444",0,50),("Adequate (100-150g)","#f59e0b",50,75),("Good (150-180g)","#3b82f6",75,90),("High (180g+)","#22c55e",90,100)],
  "g/day (of 200)","100",
  [("How much protein do I need per day?","The RDA (minimum to prevent deficiency) is 0.8g/kg body weight. However, for active people and those with body composition goals, research supports 1.2-2.2g/kg. The sweet spot for most active adults: 1.4-1.8g/kg (0.65-0.8g/lb). Athletes and those in a caloric deficit benefit from the higher end."),
   ("Can I eat too much protein?","For healthy people with normal kidney function, high protein intakes (2.5-3g/kg) appear safe. Excess protein is converted to glucose or stored as fat — it does not build extra muscle. However, excessive protein intakes may strain kidneys in those with pre-existing kidney disease. Aim for adequate, not excessive."),
   ("When should I eat protein — does timing matter?","Protein distribution matters more than timing. Eating 25-40g of protein per meal (every 3-4 hours) maximizes muscle protein synthesis throughout the day. Having protein within 2 hours post-workout helps recovery, but the anabolic window is larger than once thought. Total daily intake is most important."),
   ("What are the best sources of protein?","Complete proteins (all essential amino acids): meat, fish, eggs, dairy, soy. Incomplete proteins: most plant sources (combine beans+rice, hummus+pita for complete profile). Best sources per gram: egg whites, chicken breast, canned tuna, Greek yogurt, cottage cheese, whey protein powder. Plant sources: lentils, edamame, tofu, quinoa."),
   ("Does protein help with weight loss?","Yes, significantly. Protein is the most satiating macronutrient — it reduces hunger hormones and increases satiety hormones. High protein preserves muscle during caloric deficit, which keeps metabolism higher. Thermic effect of protein (25-30%) means you burn more calories digesting protein than carbs (6-8%) or fat (2-3%). Very strong evidence for increasing protein during weight loss.")],
  [("TDEE Calculator","/calculators/tdee-calculator"),("Macro Calculator","/calculators/macro-calculator"),("Calorie Calculator","/calculators/calorie-calculator"),("Lean Body Mass Calculator","/calculators/lean-body-mass-calculator")],
  """        <div class="bg-green-50 border border-green-200 rounded-xl p-5">
          <h3 class="font-bold text-green-900 mb-3">Protein by Goal (per kg body weight)</h3>
          <div class="space-y-1 text-xs text-green-800">
            {[["Sedentary","0.8g/kg (RDA minimum)"],["General fitness","1.2–1.4g/kg"],["Endurance sports","1.2–1.6g/kg"],["Muscle building","1.6–2.0g/kg"],["Cutting (preserve muscle)","1.8–2.2g/kg"]].map(([g,r]) => (
              <div class="flex justify-between border-b border-green-100 pb-1"><span>{g}</span><span class="font-medium">{r}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Protein Content of Common Foods</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Food</th><th class="text-right p-2 text-xs font-semibold">Protein per 100g</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Chicken breast (cooked)","32g"],["Canned tuna","30g"],["Greek yogurt","10g"],["Eggs (whole)","13g"],["Cottage cheese","11g"],["Lentils (cooked)","9g"],["Tofu","8g"],["Whey protein powder","70-80g"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-medium">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Sample High-Protein Day</h2>
        <div class="space-y-2">
          {[
            {meal:"Breakfast",food:"4 eggs + Greek yogurt",protein:"38g"},
            {meal:"Lunch",food:"200g chicken breast + veggies",protein:"64g"},
            {meal:"Snack",food:"Cottage cheese + nuts",protein:"22g"},
            {meal:"Dinner",food:"Salmon fillet + quinoa",protein:"44g"},
          ].map(m => (
            <div class="flex justify-between bg-gray-50 rounded-lg p-3">
              <div>
                <div class="font-semibold text-xs text-gray-800">{m.meal}</div>
                <div class="text-xs text-gray-600">{m.food}</div>
              </div>
              <div class="font-bold text-sm text-blue-700">{m.protein}</div>
            </div>
          ))}
          <div class="flex justify-between bg-blue-50 rounded-lg p-3">
            <div class="font-bold text-xs text-blue-800">Total</div>
            <div class="font-bold text-sm text-blue-800">168g</div>
          </div>
        </div>
      </div>
    </div>""",
  "Daily Protein (g)","Calculate your optimal daily protein intake for your fitness goals")

# ── STEPS TO MILES ────────────────────────────────────────────────────────────
w("steps-to-miles","Steps to Miles Calculator","Fitness","fitness",
  "Steps to Miles Calculator: Convert Steps to Distance",
  "Convert steps to miles, kilometers, and calories burned based on your height and stride length. Free steps to distance calculator.",
  """
  const steps = parseFloat(inputs.steps)||0
  const height = parseFloat(inputs.height)||0
  const unit = inputs.unit||"imperial"
  const weight = parseFloat(inputs.weight)||0
  if(steps<=0) throw new Error("Enter number of steps.")
  const heightInches = unit==="imperial"?height:height*0.393701
  const strideLength = heightInches>0?heightInches*0.413:30
  const miles = (steps*strideLength)/(5280*12)
  const km = miles*1.60934
  const wkg = unit==="imperial"?weight*0.453592:(weight||70)
  const hours = miles/3.0
  const met = 3.5
  const calories = met*wkg*hours
  return {
    value:miles.toFixed(2)+" miles",
    gaugeValue:Math.min((steps/10000)*100,100),
    breakdown:["Steps: "+steps.toLocaleString(),"Stride length: "+strideLength.toFixed(1)+"\\"","Distance: "+miles.toFixed(2)+" miles / "+km.toFixed(2)+"km","Estimated calories: "+Math.round(calories)+" kcal","Steps for 1 mile: ~"+Math.round(5280*12/strideLength)],
    stats:[
      {label:"Distance",value:miles.toFixed(2)+" miles"},
      {label:"Kilometers",value:km.toFixed(2)+" km"},
      {label:"Steps per Mile",value:Math.round(5280*12/strideLength).toLocaleString()},
      {label:"Est. Calories",value:Math.round(calories)+" kcal"},
    ]
  }
""",
  """{id:"steps",label:"Number of Steps",type:"number",placeholder:"10000",min:0,defaultValue:10000},
            {id:"height",label:"Your Height (for stride estimate)",type:"number",placeholder:"68",min:40,max:90,defaultValue:68},
            {id:"unit",label:"Units",type:"select",options:[{value:"imperial",label:"Imperial (inches, lbs, miles)"},{value:"metric",label:"Metric (cm, kg, km)"}],defaultValue:"imperial"},
            {id:"weight",label:"Weight (optional, for calorie estimate)",type:"number",placeholder:"155",min:0,defaultValue:155}""",
  [("Under 5,000","#ef4444",0,50),("5,000-7,500","#f59e0b",50,75),("7,500-10,000","#3b82f6",75,100)],
  "steps (of 10k)","100",
  [("How many steps are in a mile?","The average is 2,000-2,500 steps per mile, depending on height and stride length. Taller people have longer strides and take fewer steps per mile. A person who is 5ft 4in takes about 2,400 steps/mile. Someone 6ft tall takes about 1,900 steps/mile. Your stride length = height x 0.413 (approximately)."),
   ("Is 10,000 steps a day really the goal?","The 10,000 steps goal originated from a marketing campaign for a Japanese pedometer, not medical research. However, research confirms benefits: walking 7,000-10,000 steps/day significantly reduces mortality risk. Even 7,000 steps provides most of the health benefit, with diminishing returns beyond 10,000 steps."),
   ("How long does it take to walk 10,000 steps?","At an average pace of 3 mph (2,000 steps/mile), 10,000 steps takes about 80-100 minutes. At a brisk 3.5 mph pace: ~70-85 minutes. You can split this throughout the day — 15-20 minute walks 4-5 times daily is achievable for most people and eliminates prolonged sitting."),
   ("How many calories does 10,000 steps burn?","Approximately 300-500 calories for a 155 lb person walking 10,000 steps (about 5 miles). Calorie burn varies by speed, terrain, and body weight. Heavier people burn more; walking uphill burns significantly more than flat walking. Running the same distance burns about 2x more calories than walking."),
   ("What is a good daily step count for health?","Research shows clear health benefits at different thresholds: 4,000+ steps/day significantly reduces mortality risk vs. sedentary; 7,000-8,000 steps/day provides most cardiovascular benefits; 10,000 steps is a good general goal. For weight management, more is better — aim for 12,000-15,000 if weight loss is a priority.")],
  [("Calories Burned Calculator","/calculators/calories-burned-calculator"),("Running Calorie Calculator","/calculators/running-calorie-calculator"),("BMI Calculator","/calculators/bmi-calculator"),("TDEE Calculator","/calculators/tdee-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Steps by Height (per mile)</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700 border-b border-blue-200"><th class="text-left pb-1">Height</th><th class="text-right pb-1">Steps/Mile</th></tr></thead>
            <tbody class="text-blue-900">
              {[["5ft (152cm)","2,640"],["5ft 6in (168cm)","2,371"],["6ft (183cm)","2,112"],["6ft 6in (198cm)","1,907"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right font-medium">{r[1]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Daily Step Goals</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Steps/Day</th><th class="text-right p-2 text-xs font-semibold">Miles</th><th class="text-right p-2 text-xs font-semibold">Health Benefit</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["3,000","~1.5 mi","Basic movement"],["5,000","~2.5 mi","Sedentary limit"],["7,500","~3.75 mi","Good health"],["10,000","~5 mi","Optimal goal"],["15,000","~7.5 mi","Weight management"]].map(r => (
              <tr><td class="p-2 text-xs font-medium">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Tips to Increase Daily Steps</h2>
        <div class="space-y-2">
          {["Take stairs instead of elevator whenever possible","Park farther from the entrance and walk","Walk during phone calls and meetings","Take a 10-minute walk after each meal","Set hourly reminders to stand and move","Walk to nearby errands instead of driving","Use a lunch break walk — 20 minutes adds ~2,500 steps","Get a dog — dog owners walk 22 more minutes daily on average"].map(t => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{t}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Distance (miles)","Convert steps to miles, kilometers, and calories burned")

# ── RUNNING CALORIE ───────────────────────────────────────────────────────────
w("running-calorie","Running Calorie Calculator","Fitness","fitness",
  "Running Calorie Calculator: Calories Burned Running",
  "Calculate calories burned running based on distance, speed, weight, and terrain. Free running calorie calculator.",
  """
  const weight = parseFloat(inputs.weight)||155
  const distance = parseFloat(inputs.distance)||5
  const speed = parseFloat(inputs.speed)||6
  const unit = inputs.unit||"imperial"
  const terrain = inputs.terrain||"flat"
  const wkg = unit==="imperial"?weight*0.453592:weight
  const distKm = unit==="imperial"?distance*1.60934:distance
  const speedKmh = unit==="imperial"?speed*1.60934:speed
  const terrainBonus = {flat:0,slight_incline:0.15,moderate_incline:0.30,steep_incline:0.50,trail:0.10}
  const bonus = terrainBonus[terrain]||0
  const met = (speedKmh<8?6:speedKmh<10?8:speedKmh<12?10:speedKmh<14?11:12)*(1+bonus)
  const hours = distKm/speedKmh
  const calories = met*wkg*hours
  const perKm = calories/distKm
  const perMile = perKm*1.60934
  return {
    value:Math.round(calories)+" calories",
    gaugeValue:Math.min(calories/800*100,100),
    breakdown:["Weight: "+wkg.toFixed(1)+"kg | Distance: "+distKm.toFixed(1)+"km","Speed: "+speedKmh.toFixed(1)+"km/h","Terrain: "+terrain.replace(/_/g," "),"MET: "+met.toFixed(1),"Calories: "+Math.round(calories),"Per km: "+perKm.toFixed(0)+" | Per mile: "+perMile.toFixed(0)],
    stats:[
      {label:"Total Calories",value:Math.round(calories)+" kcal"},
      {label:"Per Mile",value:Math.round(perMile)+" kcal"},
      {label:"Per km",value:Math.round(perKm)+" kcal"},
      {label:"Duration",value:(hours*60).toFixed(0)+" min"},
    ]
  }
""",
  """{id:"weight",label:"Body Weight",type:"number",placeholder:"155",min:50,max:400,defaultValue:155},
            {id:"distance",label:"Distance",type:"number",placeholder:"3",min:0.1,max:100,step:0.1,defaultValue:3},
            {id:"speed",label:"Running Speed",type:"number",placeholder:"6",min:1,max:20,step:0.5,defaultValue:6},
            {id:"unit",label:"Units",type:"select",options:[{value:"imperial",label:"Imperial (lbs, miles, mph)"},{value:"metric",label:"Metric (kg, km, km/h)"}],defaultValue:"imperial"},
            {id:"terrain",label:"Terrain",type:"select",options:[
              {value:"flat",label:"Flat road/treadmill"},
              {value:"trail",label:"Trail running (+10%)"},
              {value:"slight_incline",label:"Slight incline (+15%)"},
              {value:"moderate_incline",label:"Moderate incline (+30%)"},
              {value:"steep_incline",label:"Steep hill (+50%)"},
            ],defaultValue:"flat"}""",
  [("Light (<300 cal)","#3b82f6",0,37),("Moderate (300-500)","#22c55e",37,62),("High (500-700)","#f59e0b",62,87),("Very High (700+)","#ef4444",87,100)],
  "cal (of 800)","100",
  [("How many calories does running burn?","Running burns approximately 80-140 calories per mile, depending on body weight and pace. A 155 lb person burns about 100 cal/mile at 6 mph. A 200 lb person burns about 130 cal/mile. Faster speeds and hills increase burn. Running consistently burns more than most other exercises per unit of time."),
   ("Does speed affect calorie burn in running?","Yes, but less than you might think. Faster running burns more calories per minute, but since you cover more distance faster, the per-mile calorie burn changes less. Running at 8 mph burns ~30% more per mile than 5 mph. Hill running adds 50-75% more calories due to greater effort against gravity."),
   ("Is running or walking better for calorie burn?","Running burns about 2x more calories per minute than walking at the same body weight. However, per mile, running only burns about 25-30% more than brisk walking. If you can only exercise for a set time, running wins. If you have unlimited time, the difference per mile narrows. Both are excellent for health."),
   ("Why does body weight affect calorie burn so much?","Heavier people burn more calories doing the same activity because they must move more mass. Moving 220 lbs requires significantly more energy than moving 150 lbs, even at the same speed and distance. This is why calorie burn calculators always require weight as an input — it is the single biggest variable."),
   ("Does running on a treadmill burn fewer calories than outdoors?","Slightly yes — no wind resistance, slight biomechanical differences. Setting treadmill incline to 1% compensates for the wind resistance difference. Trail running burns 10-15% more than treadmill due to uneven terrain engaging more stabilizer muscles. Treadmill calorie displays are notoriously inaccurate — use a formula-based calculator instead.")],
  [("Calories Burned Calculator","/calculators/calories-burned-calculator"),("Steps to Miles Calculator","/calculators/steps-to-miles-calculator"),("Pace Calculator","/calculators/pace-calculator"),("TDEE Calculator","/calculators/tdee-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Calories per Mile by Weight</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700 border-b border-blue-200"><th class="text-left pb-1">Weight</th><th class="text-right pb-1">Cal/mile</th></tr></thead>
            <tbody class="text-blue-900">
              {[["120 lbs","80 cal"],["150 lbs","100 cal"],["175 lbs","116 cal"],["200 lbs","132 cal"],["225 lbs","149 cal"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right font-medium">{r[1]}</td></tr>
              ))}
            </tbody>
          </table>
          <p class="text-xs text-blue-600 mt-1">At 6 mph pace on flat terrain</p>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Calorie Burn by Pace (155 lbs, 1 mile)</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Pace</th><th class="text-right p-2 text-xs font-semibold">Speed</th><th class="text-right p-2 text-xs font-semibold">Cal/mile</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["15 min/mile","4 mph","83"],["12 min/mile","5 mph","92"],["10 min/mile","6 mph","102"],["8 min/mile","7.5 mph","112"],["7 min/mile","8.5 mph","122"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right font-medium text-blue-700">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Running for Weight Loss</h2>
        <div class="space-y-3">
          {[
            {dist:"1 mile/day",cal:"~100 cal/day",annual:"~10 lb potential loss/year"},
            {dist:"3 miles/day",cal:"~300 cal/day",annual:"~30 lb potential loss/year"},
            {dist:"5 miles/day",cal:"~500 cal/day",annual:"~50 lb potential loss/year"},
          ].map(r => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-xs text-gray-800">{r.dist}</div>
              <div class="text-xs text-blue-600">{r.cal}</div>
              <div class="text-xs text-gray-500">{r.annual}</div>
            </div>
          ))}
          <p class="text-xs text-gray-500 mt-1">Estimates assume no dietary compensation. Diet adjustment is also needed for actual weight loss.</p>
        </div>
      </div>
    </div>""",
  "Calories Burned","Calculate calories burned running by distance, speed, and weight")

# ── VO2MAX ────────────────────────────────────────────────────────────────────
w("vo2max","VO2 Max Calculator","Fitness","fitness",
  "VO2 Max Calculator: Estimate Your Aerobic Fitness Level",
  "Estimate your VO2 max (maximal oxygen uptake) from resting heart rate or running tests. Free VO2 max calculator.",
  """
  const method = inputs.method||"resting_hr"
  const age = parseInt(inputs.age)||30
  const restingHR = parseInt(inputs.restingHR)||65
  const maxHR = inputs.maxHR?parseInt(inputs.maxHR):(220-age)
  const runTime = parseFloat(inputs.runTime)||12
  let vo2max, method_used
  if(method==="resting_hr"){
    vo2max = 15*(maxHR/restingHR)
    method_used="Heart Rate Ratio"
  } else {
    vo2max = (483/runTime)+3.5
    method_used="Cooper 12-min Test"
  }
  const zones = vo2max>=60?"Superior":vo2max>=52?"Excellent":vo2max>=44?"Good":vo2max>=36?"Fair":"Poor"
  return {
    value:vo2max.toFixed(1)+" mL/kg/min",
    gaugeValue:Math.min(vo2max/70*100,100),
    breakdown:["Method: "+method_used,"VO2 max: "+vo2max.toFixed(1)+" mL/kg/min","Rating: "+zones,"Max HR: "+maxHR+" bpm","Resting HR: "+restingHR+" bpm"],
    stats:[
      {label:"VO2 Max",value:vo2max.toFixed(1)+" mL/kg/min"},
      {label:"Fitness Rating",value:zones},
      {label:"Max Heart Rate",value:maxHR+" bpm"},
      {label:"HRR",value:maxHR+" / "+restingHR},
    ]
  }
""",
  """{id:"method",label:"Estimation Method",type:"select",options:[{value:"resting_hr",label:"Resting Heart Rate Method"},{value:"cooper",label:"Cooper 12-Minute Run Test"}],defaultValue:"resting_hr"},
            {id:"age",label:"Age",type:"number",placeholder:"30",min:10,max:90,unit:"years",defaultValue:30},
            {id:"restingHR",label:"Resting Heart Rate",type:"number",placeholder:"65",min:30,max:100,unit:"bpm",defaultValue:65},
            {id:"maxHR",label:"Max Heart Rate (leave 0 for age-based estimate)",type:"number",placeholder:"0",min:0,unit:"bpm",defaultValue:0},
            {id:"runTime",label:"Cooper Test: Distance in 12 min (km) — only if using Cooper method",type:"number",placeholder:"2.4",min:0.5,max:6,step:0.1,defaultValue:2.4}""",
  [("Poor (<36)","#ef4444",0,51),("Fair (36-44)","#f59e0b",51,63),("Good (44-52)","#3b82f6",63,74),("Excellent (52+)","#22c55e",74,100)],
  "mL/kg/min (of 70)","100",
  [("What is VO2 max?","VO2 max (maximal oxygen uptake) is the maximum rate at which your body can consume oxygen during intense exercise. It is the gold standard measure of cardiovascular fitness. Higher VO2 max means you can sustain higher exercise intensities and have better endurance capacity. It is measured in mL of O2 per kg of body weight per minute."),
   ("What is a good VO2 max for my age?","For men aged 30-39: Poor <39, Fair 39-43, Good 44-51, Excellent 52-58, Superior 59+. For women aged 30-39: Poor <31, Fair 31-34, Good 35-38, Excellent 39-45, Superior 46+. Elite endurance athletes often have VO2 max of 70-90+ mL/kg/min. Values decline ~1%/year after 25 without training."),
   ("How accurate are these estimation methods?","These are estimates, not lab measurements. The resting heart rate method has ±10-15% error. The Cooper 12-minute test is more accurate (±5%) if performed properly. Laboratory VO2 max testing (maximal treadmill test with respiratory analysis) is the gold standard. Smartwatches (Garmin, Apple Watch) use wrist HR and GPS data for reasonable estimates."),
   ("How can I improve my VO2 max?","VO2 max responds well to training. Best methods: high-intensity interval training (HIIT) — 4x4 minutes at 90-95% max HR; long slow distance runs; tempo runs at lactate threshold pace. Expect 5-15% improvement over 8-12 weeks of consistent training. Genetics set the ceiling but training can significantly improve your current level."),
   ("Is VO2 max related to longevity?","Strongly yes. Low cardiorespiratory fitness (low VO2 max) is one of the strongest predictors of all-cause mortality — stronger than hypertension, diabetes, or smoking in some studies. Going from low to moderate fitness reduces mortality risk by ~35%. Going from moderate to high fitness reduces it another ~15%.")],
  [("BMR Calculator","/calculators/bmr-calculator"),("Running Calorie Calculator","/calculators/running-calorie-calculator"),("Calories Burned Calculator","/calculators/calories-burned-calculator"),("Pace Calculator","/calculators/pace-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">VO2 Max Rating (Men 30-39)</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[["Superior","59+"],["Excellent","52–58"],["Good","44–51"],["Fair","39–43"],["Poor","Under 39"]].map(([r,v]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span>{r}</span><span class="font-medium">{v} mL/kg/min</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">VO2 Max of Elite Athletes</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Athlete</th><th class="text-right p-2 text-xs font-semibold">VO2 Max</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Oscar Svendsen (cyclist)","97.5"],["Espen Bjerke (cyclist)","96.0"],["Jon Brown (runner)","85.0"],["Mo Farah (runner)","81.5"],["Usain Bolt (sprinter)","54.9"],["Average fit adult","40–55"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-medium">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">How to Improve VO2 Max</h2>
        <div class="space-y-2">
          {[
            {method:"HIIT",desc:"4 x 4 minutes at 90-95% max HR with 3-min recovery. Most effective method. 2-3x/week."},
            {method:"Long runs",desc:"Weekly long run at easy pace (60-70% max HR). Builds aerobic base. 1x/week."},
            {method:"Tempo runs",desc:"20-40 min at lactate threshold pace (~80-85% max HR). Comfortable hard."},
            {method:"Consistency",desc:"The biggest driver is simply training regularly over months and years. No shortcuts."},
          ].map(m => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-xs text-blue-700">{m.method}</div>
              <div class="text-xs text-gray-600 mt-0.5">{m.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </div>""",
  "VO2 Max (mL/kg/min)","Estimate your aerobic fitness level with VO2 max")

# ── WAIST TO HIP ──────────────────────────────────────────────────────────────
w("waist-hip","Waist-to-Hip Ratio Calculator","Fitness","fitness",
  "Waist-to-Hip Ratio Calculator: WHR Health Risk Assessment",
  "Calculate your waist-to-hip ratio and health risk assessment. Determine cardiovascular disease risk from body fat distribution. Free WHR calculator.",
  """
  const waist = parseFloat(inputs.waist)||0
  const hip = parseFloat(inputs.hip)||0
  const sex = inputs.sex||"male"
  const unit = inputs.unit||"in"
  if(waist<=0||hip<=0) throw new Error("Enter waist and hip measurements.")
  const whr = waist/hip
  let risk, gauge
  if(sex==="male"){
    if(whr<0.90){risk="Low Risk";gauge=25}
    else if(whr<0.95){risk="Moderate Risk";gauge=55}
    else if(whr<1.00){risk="High Risk";gauge=75}
    else{risk="Very High Risk";gauge=95}
  } else {
    if(whr<0.80){risk="Low Risk";gauge=25}
    else if(whr<0.85){risk="Moderate Risk";gauge=55}
    else if(whr<0.90){risk="High Risk";gauge=75}
    else{risk="Very High Risk";gauge=95}
  }
  const waistIdeal = sex==="male"?(hip*0.90-0.01):(hip*0.80-0.01)
  return {
    value:"WHR: "+whr.toFixed(3)+" — "+risk,
    gaugeValue:gauge,
    breakdown:["Waist: "+waist+unit+" | Hip: "+hip+unit,"WHR: "+whr.toFixed(3),"Risk level: "+risk,"Ideal waist target: under "+waistIdeal.toFixed(1)+unit+" (for low risk)"],
    stats:[
      {label:"WHR",value:whr.toFixed(3)},
      {label:"Health Risk",value:risk},
      {label:"Waist",value:waist+unit},
      {label:"Hip",value:hip+unit},
    ]
  }
""",
  """{id:"waist",label:"Waist Circumference (at navel)",type:"number",placeholder:"34",min:20,max:80,step:0.5,defaultValue:34},
            {id:"hip",label:"Hip Circumference (widest point)",type:"number",placeholder:"38",min:20,max:80,step:0.5,defaultValue:38},
            {id:"unit",label:"Unit",type:"select",options:[{value:"in",label:"inches"},{value:"cm",label:"centimeters"}],defaultValue:"in"},
            {id:"sex",label:"Sex",type:"select",options:[{value:"male",label:"Male"},{value:"female",label:"Female"}],defaultValue:"male"}""",
  [("Low Risk","#22c55e",0,40),("Moderate Risk","#f59e0b",40,65),("High Risk","#ef4444",65,85),("Very High Risk","#dc2626",85,100)],
  "risk level","100",
  [("What is the waist-to-hip ratio?","WHR = Waist circumference / Hip circumference. It measures body fat distribution — specifically whether fat is concentrated in the abdomen (apple shape) vs. hips/thighs (pear shape). Abdominal fat is more metabolically active and associated with higher health risks than fat stored in the lower body."),
   ("What is a healthy WHR?","WHO guidelines. Men: Under 0.90 = low risk; 0.90-0.95 = moderate risk; Over 0.95 = high risk. Women: Under 0.80 = low risk; 0.80-0.85 = moderate risk; Over 0.85 = high risk. These thresholds vary slightly between populations and health organizations."),
   ("Is WHR or BMI better for assessing health?","WHR is better at predicting cardiovascular disease risk, diabetes, and metabolic syndrome than BMI. Two people can have the same BMI but very different WHRs — a muscular person and an abdominally obese person might have the same BMI but very different health risks. Waist circumference alone is also a strong predictor."),
   ("Why is abdominal fat more dangerous than hip fat?","Visceral fat (around abdominal organs) releases inflammatory chemicals, disrupts blood sugar regulation, and increases blood pressure. It is closely linked to insulin resistance, type 2 diabetes, heart disease, and certain cancers. Subcutaneous fat (under the skin in hips/thighs) is metabolically less harmful and may even have some protective effects."),
   ("How do I reduce my waist-to-hip ratio?","Diet: reduce processed foods, sugar, refined carbs. These preferentially increase visceral fat. Exercise: combination of aerobic exercise and strength training is most effective at reducing abdominal fat. Sleep: poor sleep strongly increases visceral fat. Stress reduction: cortisol promotes abdominal fat storage. Alcohol reduction: beer belly is real — alcohol promotes visceral fat.")],
  [("BMI Calculator","/calculators/bmi-calculator"),("Body Fat Calculator","/calculators/body-fat-calculator"),("Lean Body Mass Calculator","/calculators/lean-body-mass-calculator"),("Calorie Calculator","/calculators/calorie-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">WHR Thresholds (WHO)</h3>
          <div class="grid grid-cols-2 gap-3 text-xs">
            <div>
              <div class="font-bold text-blue-800 mb-1">Men</div>
              {[["Low Risk","< 0.90"],["Moderate","0.90–0.95"],["High Risk","0.95–1.0"],["Very High","> 1.0"]].map(([r,v]) => (
                <div class="flex justify-between border-b border-blue-100 pb-0.5 text-blue-800"><span>{r}</span><span class="font-medium">{v}</span></div>
              ))}
            </div>
            <div>
              <div class="font-bold text-blue-800 mb-1">Women</div>
              {[["Low Risk","< 0.80"],["Moderate","0.80–0.85"],["High Risk","0.85–0.90"],["Very High","> 0.90"]].map(([r,v]) => (
                <div class="flex justify-between border-b border-blue-100 pb-0.5 text-blue-800"><span>{r}</span><span class="font-medium">{v}</span></div>
              ))}
            </div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Apple vs Pear Body Shape</h2>
        <div class="grid grid-cols-2 gap-4">
          <div class="bg-red-50 rounded-xl p-4">
            <div class="font-bold text-red-800 text-sm mb-2">Apple Shape</div>
            <div class="text-xs text-red-700 space-y-1">
              <div>Higher WHR</div>
              <div>Fat stored abdominally</div>
              <div>More visceral fat</div>
              <div>Higher CVD risk</div>
              <div>Common in men</div>
            </div>
          </div>
          <div class="bg-green-50 rounded-xl p-4">
            <div class="font-bold text-green-800 text-sm mb-2">Pear Shape</div>
            <div class="text-xs text-green-700 space-y-1">
              <div>Lower WHR</div>
              <div>Fat stored in hips/thighs</div>
              <div>More subcutaneous fat</div>
              <div>Lower CVD risk</div>
              <div>More common in women</div>
            </div>
          </div>
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Reducing Abdominal Fat</h2>
        <div class="space-y-2">
          {["Create a caloric deficit — you cannot spot-reduce fat","Aerobic exercise: 150+ min/week of moderate or 75 min vigorous activity","HIIT specifically effective for visceral fat reduction","Reduce ultra-processed foods, sugar, and refined carbohydrates","Limit alcohol — strongly associated with abdominal fat","Prioritize sleep (7-9 hours) — sleep deprivation increases belly fat","Manage stress — cortisol promotes visceral fat storage","Strength training builds muscle which boosts resting metabolism"].map(t => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{t}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "WHR","Calculate waist-to-hip ratio and cardiovascular health risk")

print(f"\nWritten: {written} pages (calories-burned, body-surface-area, lean-body-mass, protein, steps-to-miles, running-calorie, vo2max, waist-hip)")
