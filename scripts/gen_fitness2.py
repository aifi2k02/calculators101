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

# ── INTERMITTENT FASTING ──────────────────────────────────────────────────────
w("intermittent-fasting","Intermittent Fasting Calculator","Fitness","fitness",
  "Intermittent Fasting Calculator: Fasting Window & Schedule",
  "Calculate your intermittent fasting window, eating schedule, and expected calorie deficit. Free IF calculator for 16:8, 18:6, and more.",
  """
  const protocol = inputs.protocol||"16:8"
  const wakeTime = parseInt(inputs.wakeTime)||7
  const parts = protocol.split(":")
  const fastHours = parseInt(parts[0])||16
  const eatHours = parseInt(parts[1])||8
  const fastEnd = (wakeTime+fastHours)%24
  const eatStart = fastEnd
  const eatEnd = (eatStart+eatHours)%24
  const formatTime = h => {
    const suffix = h>=12?"PM":"AM"
    const h12 = h===0?12:h>12?h-12:h
    return h12+":00 "+suffix
  }
  const calsIfNormal = 2000
  const deficit = Math.round(calsIfNormal*(fastHours/24)*0.3)
  return {
    value:protocol+" Fasting Schedule",
    gaugeValue:(fastHours/24)*100,
    breakdown:["Protocol: "+protocol,"Fast: "+fastHours+" hours | Eat: "+eatHours+" hours","Wake time: "+formatTime(wakeTime),"Fast ends / Eating starts: "+formatTime(eatStart),"Stop eating at: "+formatTime(eatEnd),"Estimated daily deficit: ~"+deficit+" cal"],
    stats:[
      {label:"Fasting Hours",value:fastHours+"hr"},
      {label:"Eating Window",value:eatHours+"hr"},
      {label:"Start Eating",value:formatTime(eatStart)},
      {label:"Stop Eating",value:formatTime(eatEnd)},
    ]
  }
""",
  """{id:"protocol",label:"Fasting Protocol",type:"select",options:[
              {value:"12:12",label:"12:12 — Beginner"},
              {value:"14:10",label:"14:10 — Easy"},
              {value:"16:8",label:"16:8 — Most Popular"},
              {value:"18:6",label:"18:6 — Moderate"},
              {value:"20:4",label:"20:4 — Advanced"},
              {value:"23:1",label:"23:1 — OMAD (One Meal a Day)"},
            ],defaultValue:"16:8"},
            {id:"wakeTime",label:"Wake-Up Time (24hr, e.g. 7 = 7AM)",type:"number",placeholder:"7",min:0,max:23,defaultValue:7}""",
  [("Light (12hr fast)","#3b82f6",0,50),("Moderate (16hr)","#22c55e",50,67),("Advanced (18-20hr)","#f59e0b",67,83),("OMAD (23hr)","#ef4444",83,100)],
  "% of day fasted","100",
  [("What is intermittent fasting?","Intermittent fasting (IF) cycles between periods of eating and fasting. The most popular approach is 16:8: fast for 16 hours, eat within an 8-hour window. This naturally reduces calorie intake for most people, improves insulin sensitivity, and may have cellular health benefits through a process called autophagy."),
   ("Which IF protocol is best for beginners?","Start with 12:12 (12 hours fasting, 12 hours eating) — this is barely different from not eating after dinner. Progress to 14:10, then 16:8 as your body adapts. Most people find 16:8 sustainable long-term. Skipping breakfast (eating from noon to 8pm) is the most common 16:8 implementation."),
   ("Can I drink anything during the fasting window?","Yes — water, black coffee, and plain tea have minimal/no calories and do not break the fast. Some people allow small amounts of cream in coffee (debated). Anything with calories, artificial sweeteners (in large amounts), or insulin-spiking ingredients technically breaks a metabolic fast. Hydration is important during fasting."),
   ("Does intermittent fasting work for weight loss?","IF works primarily by reducing total calorie intake — you have fewer hours to eat. Research shows IF produces weight loss similar to continuous calorie restriction when total calories are matched. The advantage: many people find it easier to skip a meal than to count calories throughout the day. It is a schedule, not a magic fix."),
   ("Who should NOT do intermittent fasting?","Pregnant or breastfeeding women, people with a history of eating disorders, those with type 1 diabetes or on insulin medication, children and adolescents, anyone who is underweight, and people with certain medical conditions. Always consult a doctor before starting, especially if you have any metabolic conditions or take medications.")],
  [("Calorie Calculator","/calculators/calorie-calculator"),("TDEE Calculator","/calculators/tdee-calculator"),("Caloric Deficit Calculator","/calculators/caloric-deficit-calculator"),("Macro Calculator","/calculators/macro-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Popular IF Protocols</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[["12:12","Beginner — no breakfast past 8pm"],["16:8","Most popular — skip breakfast"],["18:6","Advanced — 3hr longer fast"],["20:4","Extreme — 4hr eating window"],["5:2 Diet","5 normal days, 2 at 500-600 cal"],["OMAD","One meal a day — most extreme"]].map(([p,d]) => (
              <div class="border-b border-blue-100 pb-1"><span class="font-medium">{p}:</span> {d}</div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Potential Benefits of IF</h2>
        <div class="space-y-2">
          {[
            {b:"Weight Loss",d:"Reduces calorie intake naturally by limiting eating hours"},
            {b:"Insulin Sensitivity",d:"Fasting periods reduce blood insulin levels and improve sensitivity"},
            {b:"Autophagy",d:"Cellular cleanup process activated during extended fasting — may slow aging"},
            {b:"Simplified Eating",d:"Fewer meals to plan, prep, and think about — reduces decision fatigue"},
            {b:"Mental Clarity",d:"Many people report improved focus during fasting periods (ketone production)"},
          ].map(b => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-xs text-blue-700">{b.b}</div>
              <div class="text-xs text-gray-600">{b.d}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Common 16:8 Schedules</h2>
        <div class="space-y-2">
          {[
            {name:"Morning person",eat:"7am–3pm",fast:"3pm–7am"},
            {name:"Standard (skip breakfast)",eat:"12pm–8pm",fast:"8pm–12pm"},
            {name:"Late eater",eat:"2pm–10pm",fast:"10pm–2pm"},
          ].map(s => (
            <div class="bg-gray-50 rounded-xl p-3">
              <div class="font-semibold text-xs text-gray-800">{s.name}</div>
              <div class="text-xs text-green-700">Eat: {s.eat}</div>
              <div class="text-xs text-gray-500">Fast: {s.fast}</div>
            </div>
          ))}
        </div>
      </div>
    </div>""",
  "Fasting Schedule","Calculate your intermittent fasting window and eating schedule")

# ── KETO ─────────────────────────────────────────────────────────────────────
w("keto","Keto Calculator","Fitness","fitness",
  "Keto Calculator: Ketogenic Diet Macros",
  "Calculate your ketogenic diet macros (fat, protein, carbs) based on your goals. Get personalized keto macro targets. Free keto calculator.",
  """
  const weight = parseFloat(inputs.weight)||0
  const height = parseFloat(inputs.height)||0
  const age = parseInt(inputs.age)||30
  const sex = inputs.sex||"male"
  const activity = inputs.activity||"moderate"
  const goal = inputs.goal||"lose"
  const unit = inputs.unit||"imperial"
  if(weight<=0||height<=0) throw new Error("Enter weight and height.")
  const wkg = unit==="imperial"?weight*0.453592:weight
  const hcm = unit==="imperial"?height*2.54:height
  const bmr = sex==="male"?88.362+13.397*wkg+4.799*hcm-5.677*age:447.593+9.247*wkg+3.098*hcm-4.330*age
  const activityMultiplier = {sedentary:1.2,light:1.375,moderate:1.55,active:1.725,very_active:1.9}
  const tdee = bmr*(activityMultiplier[activity]||1.55)
  const calories = goal==="lose"?tdee-500:goal==="gain"?tdee+250:tdee
  const proteinG = wkg*1.76
  const carbG = 25
  const fatG = (calories-proteinG*4-carbG*4)/9
  const proteinCal = proteinG*4
  const carbCal = carbG*4
  const fatCal = fatG*9
  return {
    value:"Fat: "+fatG.toFixed(0)+"g | Protein: "+proteinG.toFixed(0)+"g | Carbs: "+carbG+"g",
    gaugeValue:Math.min(fatCal/calories*100,100),
    breakdown:["TDEE: "+tdee.toFixed(0)+" cal","Target calories: "+calories.toFixed(0)+" cal","Fat: "+fatG.toFixed(0)+"g ("+fatCal.toFixed(0)+" cal, "+(fatCal/calories*100).toFixed(0)+"%)","Protein: "+proteinG.toFixed(0)+"g ("+proteinCal.toFixed(0)+" cal)","Carbs: "+carbG+"g ("+carbCal+" cal, keep under 50g net)"],
    stats:[
      {label:"Daily Calories",value:calories.toFixed(0)+" kcal"},
      {label:"Fat Target",value:fatG.toFixed(0)+"g"},
      {label:"Protein Target",value:proteinG.toFixed(0)+"g"},
      {label:"Carb Limit",value:carbG+"g net"},
    ]
  }
""",
  """{id:"weight",label:"Weight",type:"number",placeholder:"170",min:50,max:500,defaultValue:170},
            {id:"height",label:"Height",type:"number",placeholder:"68",min:40,max:90,defaultValue:68},
            {id:"unit",label:"Units",type:"select",options:[{value:"imperial",label:"Imperial (lbs, inches)"},{value:"metric",label:"Metric (kg, cm)"}],defaultValue:"imperial"},
            {id:"age",label:"Age",type:"number",placeholder:"35",min:15,max:90,unit:"years",defaultValue:35},
            {id:"sex",label:"Sex",type:"select",options:[{value:"male",label:"Male"},{value:"female",label:"Female"}],defaultValue:"male"},
            {id:"activity",label:"Activity Level",type:"select",options:[
              {value:"sedentary",label:"Sedentary"},
              {value:"light",label:"Lightly Active"},
              {value:"moderate",label:"Moderately Active"},
              {value:"active",label:"Very Active"},
              {value:"very_active",label:"Extra Active"},
            ],defaultValue:"moderate"},
            {id:"goal",label:"Goal",type:"select",options:[
              {value:"lose",label:"Lose Weight (-500 cal/day)"},
              {value:"maintain",label:"Maintain Weight"},
              {value:"gain",label:"Gain Muscle (+250 cal/day)"},
            ],defaultValue:"lose"}""",
  [("Moderate fat %","#f59e0b",0,60),("Good keto (60-75%)","#3b82f6",60,75),("Standard keto (75%+)","#22c55e",75,100)],
  "% fat","100",
  [("What is the ketogenic diet?","Keto is a very-low-carbohydrate, high-fat diet that shifts your body from using glucose (from carbs) to using ketones (from fat) as primary fuel — a metabolic state called ketosis. Standard keto macro split: 70-75% fat, 20-25% protein, 5-10% carbs (typically under 25-50g net carbs per day)."),
   ("How many carbs can I eat on keto?","Most people achieve ketosis with under 25-50g net carbs per day. Net carbs = Total carbs - Fiber (fiber does not spike blood sugar). Active people may tolerate up to 50g. Very metabolically resistant individuals may need under 20g. Start at 25g net carbs and adjust based on whether ketone strips show you are in ketosis."),
   ("How long does it take to get into ketosis?","Typically 2-4 days of strict low-carb eating (under 25g net carbs/day). The process is faster if you exercise intensely (depletes glycogen stores). Signs of ketosis: reduced appetite, increased energy after initial adaptation, fruity breath smell (acetone), possibly increased urination in first days (water weight loss)."),
   ("What is the keto flu?","During the first 1-2 weeks, many people experience fatigue, headaches, brain fog, irritability, and muscle cramps as the body adapts. This is often caused by electrolyte loss (sodium, potassium, magnesium) from increased urination. Fix: add more salt, eat potassium-rich foods, supplement magnesium. Usually resolves within a week."),
   ("Is keto safe long-term?","Research on long-term keto (5+ years) is limited. Short-term (1-2 years): generally safe and effective for weight loss and blood sugar control. Potential concerns: kidney stone risk, nutrient deficiencies without careful food choices, high saturated fat intake (choose healthy fats). Those with kidney disease or diabetes should consult a doctor before starting.")],
  [("Calorie Calculator","/calculators/calorie-calculator"),("Macro Calculator","/calculators/macro-calculator"),("TDEE Calculator","/calculators/tdee-calculator"),("BMR Calculator","/calculators/bmr-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Standard Keto Macro Split</h3>
          <div class="space-y-2">
            <div class="flex items-center gap-2 text-xs text-blue-800">
              <div class="h-2 w-16 bg-yellow-500 rounded"></div>
              <span>Fat: <strong>70–75%</strong> of calories</span>
            </div>
            <div class="flex items-center gap-2 text-xs text-blue-800">
              <div class="h-2 w-8 bg-blue-500 rounded"></div>
              <span>Protein: <strong>20–25%</strong> of calories</span>
            </div>
            <div class="flex items-center gap-2 text-xs text-blue-800">
              <div class="h-2 w-2 bg-green-500 rounded"></div>
              <span>Carbs: <strong>5–10%</strong> (under 25-50g net)</span>
            </div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Keto-Friendly Foods</h2>
        <div class="grid grid-cols-2 gap-3">
          <div class="bg-green-50 rounded-xl p-3">
            <div class="font-bold text-green-800 text-xs mb-2">Good for Keto</div>
            <ul class="text-xs text-green-700 space-y-1">
              <li>Meat & poultry</li>
              <li>Fish & seafood</li>
              <li>Eggs</li>
              <li>Cheese & butter</li>
              <li>Avocado & oils</li>
              <li>Leafy greens</li>
              <li>Nuts & seeds</li>
            </ul>
          </div>
          <div class="bg-red-50 rounded-xl p-3">
            <div class="font-bold text-red-800 text-xs mb-2">Avoid on Keto</div>
            <ul class="text-xs text-red-700 space-y-1">
              <li>Bread & pasta</li>
              <li>Rice & grains</li>
              <li>Sugar & sweets</li>
              <li>Fruit (most)</li>
              <li>Potatoes</li>
              <li>Beans & legumes</li>
              <li>Soft drinks</li>
            </ul>
          </div>
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Net Carbs in Common Foods</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Food (100g)</th><th class="text-right p-2 text-xs font-semibold">Net Carbs</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Chicken breast","0g"],["Eggs (per egg)","0.5g"],["Spinach","1.4g"],["Broccoli","4g"],["Almonds","5g"],["Blueberries","12g"],["Apple","14g"],["Rice (cooked)","28g"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-medium">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "Keto Macros","Calculate your personalized ketogenic diet macro targets")

# ── OVULATION ─────────────────────────────────────────────────────────────────
w("ovulation","Ovulation Calculator","Fitness","fitness",
  "Ovulation Calculator: Fertile Window & Ovulation Date",
  "Calculate your ovulation date, fertile window, and next period date. Plan or prevent pregnancy naturally. Free ovulation calculator.",
  """
  const lastPeriod = inputs.lastPeriod||"2025-01-01"
  const cycleLength = parseInt(inputs.cycleLength)||28
  const lutealPhase = parseInt(inputs.lutealPhase)||14
  if(cycleLength<21||cycleLength>45) throw new Error("Cycle length should be between 21 and 45 days.")
  const lp = new Date(lastPeriod)
  const ovulationDay = cycleLength-lutealPhase
  const ovulationDate = new Date(lp)
  ovulationDate.setDate(ovulationDate.getDate()+ovulationDay-1)
  const fertileStart = new Date(ovulationDate)
  fertileStart.setDate(fertileStart.getDate()-5)
  const nextPeriod = new Date(lp)
  nextPeriod.setDate(nextPeriod.getDate()+cycleLength)
  const fmt = d => d.toLocaleDateString("en-US",{month:"short",day:"numeric",year:"numeric"})
  return {
    value:"Ovulation: "+fmt(ovulationDate),
    gaugeValue:50,
    breakdown:["Last period: "+fmt(lp),"Cycle length: "+cycleLength+" days","Ovulation day "+ovulationDay+" of cycle","Ovulation date: "+fmt(ovulationDate),"Fertile window: "+fmt(fertileStart)+" — "+fmt(ovulationDate),"Next period: "+fmt(nextPeriod)],
    stats:[
      {label:"Ovulation Date",value:fmt(ovulationDate)},
      {label:"Fertile Window Starts",value:fmt(fertileStart)},
      {label:"Next Period",value:fmt(nextPeriod)},
      {label:"Cycle Day",value:"Day "+ovulationDay+" of "+cycleLength},
    ]
  }
""",
  """{id:"lastPeriod",label:"First Day of Last Period",type:"date",defaultValue:"2025-01-01"},
            {id:"cycleLength",label:"Average Cycle Length",type:"number",placeholder:"28",min:21,max:45,unit:"days",defaultValue:28},
            {id:"lutealPhase",label:"Luteal Phase Length",type:"number",placeholder:"14",min:10,max:16,unit:"days",defaultValue:14}""",
  [("Fertile Window","#22c55e",45,55),("Non-fertile","#3b82f6",0,45),("Non-fertile","#3b82f6",55,100)],
  "cycle position","100",
  [("When do I ovulate?","In a standard 28-day cycle, ovulation typically occurs on day 14 (counting from the first day of your period). However, the exact day varies by cycle length: ovulation usually happens 14 days BEFORE your next period, not 14 days after your last period. If your cycle is 30 days, you likely ovulate around day 16."),
   ("What is the fertile window?","Sperm can survive in the reproductive tract for up to 5 days. An egg lives 12-24 hours after ovulation. Therefore, the fertile window is about 5-6 days: the 5 days before ovulation and the day of ovulation. Having sex during this window maximizes chances of conception."),
   ("How do I know if I am ovulating?","Signs of ovulation: cervical mucus becomes clear and stretchy (like egg whites); mild one-sided pelvic pain (mittelschmerz); slight increase in basal body temperature (BBT) of 0.2-0.5°F; ovulation predictor kits (OPKs) detect the LH surge 24-36 hours before ovulation; breast tenderness; increased libido."),
   ("How accurate is cycle tracking for preventing pregnancy?","With perfect use, calendar/cycle tracking methods (NFP/FAM) are about 99% effective. Typical use is closer to 76-88% effective. These methods work best for women with very regular cycles. They are not recommended as sole contraception for those with irregular cycles. Combine with BBT charting and cervical mucus monitoring for better accuracy."),
   ("What if my cycles are irregular?","Irregular cycles make prediction difficult. Track your BBT (basal body temperature) daily to detect the temperature rise that confirms ovulation occurred. Use OPKs starting from your earliest possible ovulation day. Apps like Natural Cycles use BBT data with algorithms for more accurate predictions. Consider consulting a gynecologist for persistent irregularity.")],
  [("Due Date Calculator","/calculators/due-date-calculator"),("Pregnancy Weight Calculator","/calculators/pregnancy-weight-calculator"),("Age Calculator","/calculators/age-calculator")],
  """        <div class="bg-pink-50 border border-pink-200 rounded-xl p-5">
          <h3 class="font-bold text-pink-900 mb-3">Ovulation Signs</h3>
          <div class="space-y-1 text-xs text-pink-800">
            <div>🌡 BBT rise 0.2-0.5°F after ovulation</div>
            <div>💧 Cervical mucus — clear, stretchy (egg white)</div>
            <div>📊 LH surge on OPK 24-36hr before ovulation</div>
            <div>⚡ Possible mild one-sided pain (mittelschmerz)</div>
            <div>📅 Typically day 14 of a 28-day cycle</div>
          </div>
        </div>""",
  """    <div class="mt-10">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Understanding Your Cycle</h2>
      <div class="grid md:grid-cols-4 gap-4">
        {[
          {phase:"Menstruation",days:"Days 1-5",desc:"Uterine lining sheds. FSH begins rising to stimulate follicle development."},
          {phase:"Follicular Phase",days:"Days 6-13",desc:"Follicle matures. Estrogen rises. Cervical mucus becomes more fertile."},
          {phase:"Ovulation",days:"Day 14 (avg)",desc:"LH surge triggers egg release. Fertile window: 5 days before + ovulation day."},
          {phase:"Luteal Phase",days:"Days 15-28",desc:"Progesterone rises. If no conception, it drops — triggering next period."},
        ].map(p => (
          <div class="bg-gray-50 rounded-xl p-4">
            <div class="font-bold text-sm text-blue-700 mb-1">{p.phase}</div>
            <div class="text-xs text-blue-500 mb-2">{p.days}</div>
            <div class="text-xs text-gray-600">{p.desc}</div>
          </div>
        ))}
      </div>
    </div>""",
  "Ovulation Date","Calculate ovulation date and fertile window based on cycle length")

# ── DUE DATE ──────────────────────────────────────────────────────────────────
w("due-date","Due Date Calculator","Fitness","fitness",
  "Due Date Calculator: Pregnancy Due Date by LMP or Conception",
  "Calculate your pregnancy due date by last menstrual period or conception date. Includes trimester dates and weekly milestones. Free due date calculator.",
  """
  const method = inputs.method||"lmp"
  const date = inputs.date||"2025-01-01"
  const cycleLength = parseInt(inputs.cycleLength)||28
  const d = new Date(date)
  let lmpDate
  if(method==="conception"){
    lmpDate = new Date(d)
    lmpDate.setDate(lmpDate.getDate()-14)
  } else {
    lmpDate = new Date(d)
  }
  const dueDate = new Date(lmpDate)
  dueDate.setDate(dueDate.getDate()+280+(cycleLength-28))
  const today = new Date()
  const daysPregnant = Math.max(0,Math.floor((today-lmpDate)/(1000*60*60*24)))
  const weeksPregnant = Math.floor(daysPregnant/7)
  const extraDays = daysPregnant%7
  const t1End = new Date(lmpDate); t1End.setDate(t1End.getDate()+91)
  const t2End = new Date(lmpDate); t2End.setDate(t2End.getDate()+182)
  const fmt = d => d.toLocaleDateString("en-US",{month:"short",day:"numeric",year:"numeric"})
  return {
    value:"Due: "+fmt(dueDate),
    gaugeValue:Math.min((daysPregnant/280)*100,100),
    breakdown:["LMP: "+fmt(lmpDate),"Due date: "+fmt(dueDate),"Current: "+weeksPregnant+"w "+extraDays+"d pregnant","1st trimester ends: "+fmt(t1End),"2nd trimester ends: "+fmt(t2End),"3rd trimester: "+fmt(t2End)+" to "+fmt(dueDate)],
    stats:[
      {label:"Due Date",value:fmt(dueDate)},
      {label:"Current Week",value:weeksPregnant+"w "+extraDays+"d"},
      {label:"Progress",value:(daysPregnant/280*100).toFixed(0)+"%"},
      {label:"Days Until Due",value:Math.max(0,Math.round((dueDate-today)/(1000*60*60*24)))+" days"},
    ]
  }
""",
  """{id:"method",label:"Calculation Method",type:"select",options:[{value:"lmp",label:"By Last Menstrual Period (LMP)"},{value:"conception",label:"By Conception Date"}],defaultValue:"lmp"},
            {id:"date",label:"Date",type:"date",defaultValue:"2025-01-01"},
            {id:"cycleLength",label:"Cycle Length (if using LMP)",type:"number",placeholder:"28",min:21,max:45,unit:"days",defaultValue:28}""",
  [("1st Trimester","#3b82f6",0,33),("2nd Trimester","#22c55e",33,66),("3rd Trimester","#f59e0b",66,95),("Full Term","#ef4444",95,100)],
  "% of pregnancy","100",
  [("How is a due date calculated?","The most common method: add 280 days (40 weeks) to the first day of your last menstrual period (LMP). This is Naegele rule. Another way: add 9 months and 7 days to the LMP. The standard assumes a 28-day cycle. If your cycle is longer or shorter, adjust by the difference."),
   ("How accurate is a due date?","Only about 5% of babies are born on their exact due date. About 80% of births occur within 2 weeks before or after the due date. Ultrasound dating (especially in the first trimester) is considered more accurate than LMP-based calculation because it directly measures fetal size."),
   ("What are the three trimesters?","First trimester: Weeks 1-12 (conception to 3 months). Second trimester: Weeks 13-26 (most comfortable period for many). Third trimester: Weeks 27-40+ (baby gains weight rapidly). Full term is considered 39-40 weeks. Early term: 37-38 weeks. Late/post-term: after 42 weeks."),
   ("What are important pregnancy milestones by week?","Week 8-10: heartbeat detectable by Doppler. Week 12: risk of miscarriage drops significantly, end of 1st trimester. Week 18-20: anatomy ultrasound, may learn sex. Week 24: viability milestone. Week 28: 3rd trimester begins. Week 36: weekly visits begin. Week 37-42: full term range."),
   ("What factors can affect the due date?","IVF conceptions have precise dating. Women with irregular cycles may have different ovulation timing than the LMP assumes. First-trimester ultrasound can adjust the due date. Multiple pregnancies (twins/triplets) typically deliver earlier. Prior pregnancy complications, maternal health, and fetal growth also affect actual delivery timing.")],
  [("Ovulation Calculator","/calculators/ovulation-calculator"),("Pregnancy Weight Calculator","/calculators/pregnancy-weight-calculator"),("Age Calculator","/calculators/age-calculator")],
  """        <div class="bg-pink-50 border border-pink-200 rounded-xl p-5">
          <h3 class="font-bold text-pink-900 mb-3">Pregnancy Quick Facts</h3>
          <div class="space-y-1 text-xs text-pink-800">
            {[["Full term","39-40 weeks"],["Normal range","37-42 weeks"],["Average length","280 days from LMP"],["Full-term birth weight","5.5-10 lbs"],["Typical weight gain","25-35 lbs"]].map(([k,v]) => (
              <div class="flex justify-between border-b border-pink-100 pb-1"><span>{k}</span><span class="font-medium">{v}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Pregnancy Trimesters</h2>
      <div class="grid md:grid-cols-3 gap-6">
        {[
          {t:"1st Trimester",w:"Weeks 1-12",highlights:["Organ formation begins","Morning sickness common","Heartbeat begins ~week 6","Miscarriage risk highest","Prenatal vitamins critical","Avoid: alcohol, raw fish, high-mercury fish"]},
          {t:"2nd Trimester",w:"Weeks 13-27",highlights:["Baby starts moving","Anatomy scan (~week 20)","May learn baby sex","Morning sickness improves","Energy often returns","Belly becomes visible"]},
          {t:"3rd Trimester",w:"Weeks 28-40",highlights:["Rapid weight gain","Baby positions head-down","Weekly OB visits begin","Hospital bag preparation","Braxton Hicks contractions","Baby fully developed by 37 weeks"]},
        ].map(t => (
          <div class="bg-gray-50 rounded-xl p-4">
            <div class="font-bold text-sm text-blue-700 mb-1">{t.t}</div>
            <div class="text-xs text-blue-500 mb-2">{t.w}</div>
            <ul class="text-xs text-gray-600 space-y-1">
              {t.highlights.map(h => <li>• {h}</li>)}
            </ul>
          </div>
        ))}
      </div>
    </div>""",
  "Due Date","Calculate your pregnancy due date and track trimester milestones")

print(f"\nWritten: {written} pages (intermittent-fasting, keto, ovulation, due-date)")
