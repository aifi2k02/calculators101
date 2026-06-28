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

# ── PREGNANCY WEIGHT ──────────────────────────────────────────────────────────
w("pregnancy-weight","Pregnancy Weight Gain Calculator","Fitness","fitness",
  "Pregnancy Weight Gain Calculator: Healthy Gestational Weight",
  "Calculate recommended pregnancy weight gain based on pre-pregnancy BMI. Track your gestational weight. Free pregnancy weight calculator.",
  """
  const preWeight = parseFloat(inputs.preWeight)||0
  const height = parseFloat(inputs.height)||0
  const week = parseInt(inputs.week)||20
  const unit = inputs.unit||"imperial"
  if(preWeight<=0||height<=0) throw new Error("Enter weight and height.")
  const wkg = unit==="imperial"?preWeight*0.453592:preWeight
  const hm = unit==="imperial"?height*0.0254:height/100
  const bmi = wkg/(hm*hm)
  let minTotal, maxTotal, category
  if(bmi<18.5){category="Underweight";minTotal=28;maxTotal=40}
  else if(bmi<25){category="Normal weight";minTotal=25;maxTotal=35}
  else if(bmi<30){category="Overweight";minTotal=15;maxTotal=25}
  else{category="Obese";minTotal=11;maxTotal=20}
  const trimesterRate = week<=12?0.5:week<=27?1.0:1.0
  const expectedGain = week<=12?0.5*week/4:(0.5*3)+(week-12)*trimesterRate/4
  const minGain = (expectedGain/40)*minTotal
  const maxGain = (expectedGain/40)*maxTotal
  return {
    value:"Goal: "+minTotal+"-"+maxTotal+" lbs total",
    gaugeValue:(week/40)*100,
    breakdown:["Pre-pregnancy BMI: "+bmi.toFixed(1)+" ("+category+")","BMI category: "+category,"Total recommended gain: "+minTotal+"-"+maxTotal+" lbs","At week "+week+": expect "+minGain.toFixed(0)+"-"+maxGain.toFixed(0)+" lbs gained","On track: "+minGain.toFixed(0)+" to "+maxGain.toFixed(0)+" lbs gained so far is normal"],
    stats:[
      {label:"Pre-Pregnancy BMI",value:bmi.toFixed(1)},
      {label:"BMI Category",value:category},
      {label:"Total Gain Goal",value:minTotal+"-"+maxTotal+" lbs"},
      {label:"At Week "+week,value:minGain.toFixed(0)+"-"+maxGain.toFixed(0)+" lbs"},
    ]
  }
""",
  """{id:"preWeight",label:"Pre-Pregnancy Weight",type:"number",placeholder:"140",min:80,max:400,defaultValue:140},
            {id:"height",label:"Height",type:"number",placeholder:"65",min:50,max:90,defaultValue:65},
            {id:"unit",label:"Units",type:"select",options:[{value:"imperial",label:"Imperial (lbs, inches)"},{value:"metric",label:"Metric (kg, cm)"}],defaultValue:"imperial"},
            {id:"week",label:"Current Week of Pregnancy",type:"number",placeholder:"20",min:1,max:42,unit:"weeks",defaultValue:20}""",
  [("1st Trimester","#3b82f6",0,30),("2nd Trimester","#22c55e",30,68),("3rd Trimester","#f59e0b",68,100)],
  "% of pregnancy","100",
  [("How much weight should I gain during pregnancy?","IOM guidelines by pre-pregnancy BMI: Underweight (<18.5): 28-40 lbs. Normal (18.5-24.9): 25-35 lbs. Overweight (25-29.9): 15-25 lbs. Obese (30+): 11-20 lbs. Gaining in the recommended range is associated with better outcomes for both mother and baby."),
   ("Where does pregnancy weight gain go?","At delivery: Baby 7-8 lbs, Placenta 1-2 lbs, Amniotic fluid 2 lbs, Breast tissue 2 lbs, Uterus growth 2 lbs, Blood volume increase 3-4 lbs, Fluid retention 4 lbs, Fat stores 5-9 lbs. Total: 25-40 lbs for a normal-weight woman."),
   ("Is it dangerous to gain too much during pregnancy?","Excessive weight gain increases risks of: gestational diabetes, preeclampsia, large baby (macrosomia) making delivery harder, cesarean section, difficulty losing weight after delivery. It also increases the baby risk of childhood obesity. Gaining within guidelines benefits both mother and child."),
   ("What if I lose weight in the first trimester?","Mild weight loss in the first trimester is common due to morning sickness and nausea — generally not concerning. However, significant weight loss (5+ lbs) in the first trimester should be discussed with your healthcare provider. The baby draws nutrients from your body regardless, but severe morning sickness (hyperemesis gravidarum) may require medical treatment."),
   ("How fast should I gain weight during pregnancy?","First trimester: 1-4 lbs total is typical. Second trimester: about 1 lb per week. Third trimester: about 1 lb per week. This is a general guide — every pregnancy is different. Individual variation is normal. What matters most is the total gain, not week-to-week fluctuations.")],
  [("Due Date Calculator","/calculators/due-date-calculator"),("BMI Calculator","/calculators/bmi-calculator"),("Ovulation Calculator","/calculators/ovulation-calculator")],
  """        <div class="bg-pink-50 border border-pink-200 rounded-xl p-5">
          <h3 class="font-bold text-pink-900 mb-3">Weight Gain by Pre-pregnancy BMI</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-pink-700 border-b border-pink-200"><th class="text-left pb-1">BMI</th><th class="text-right pb-1">Gain Range</th></tr></thead>
            <tbody class="text-pink-900">
              {[["Underweight (<18.5)","28–40 lbs"],["Normal (18.5–24.9)","25–35 lbs"],["Overweight (25–29.9)","15–25 lbs"],["Obese (30+)","11–20 lbs"]].map(r => (
                <tr class="border-t border-pink-100"><td class="py-0.5">{r[0]}</td><td class="text-right font-medium">{r[1]}</td></tr>
              ))}
            </tbody>
          </table>
          <p class="text-xs text-pink-600 mt-1">Source: Institute of Medicine (IOM) 2009</p>
        </div>""",
  """    <div class="mt-10">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Where Does Pregnancy Weight Go?</h2>
      <div class="grid md:grid-cols-2 gap-4">
        <div class="space-y-2">
          {[["Baby","7–8 lbs"],["Placenta","1–2 lbs"],["Amniotic fluid","2 lbs"],["Breast tissue growth","2 lbs"],["Uterus enlargement","2 lbs"]].map(([comp,wt]) => (
            <div class="flex justify-between bg-pink-50 rounded-lg px-3 py-2 text-xs">
              <span class="text-pink-800">{comp}</span>
              <span class="font-medium text-pink-900">{wt}</span>
            </div>
          ))}
        </div>
        <div class="space-y-2">
          {[["Blood volume increase","3–4 lbs"],["Body fluid retention","4 lbs"],["Fat stores (energy reserves)","5–9 lbs"],["Total","25–40 lbs"]].map(([comp,wt]) => (
            <div class="flex justify-between bg-pink-50 rounded-lg px-3 py-2 text-xs">
              <span class="text-pink-800">{comp}</span>
              <span class="font-medium text-pink-900">{wt}</span>
            </div>
          ))}
        </div>
      </div>
    </div>""",
  "Pregnancy Weight Goal","Calculate recommended pregnancy weight gain based on pre-pregnancy BMI")

# ── NOW DO MATH PAGES ─────────────────────────────────────────────────────────

# ── AREA ──────────────────────────────────────────────────────────────────────
w("area","Area Calculator","Math","math",
  "Area Calculator: Rectangle, Circle, Triangle & More",
  "Calculate area of any shape: rectangle, circle, triangle, square, trapezoid, and more. Free area calculator.",
  """
  const shape = inputs.shape||"rectangle"
  const a = parseFloat(inputs.a)||0
  const b = parseFloat(inputs.b)||0
  const c = parseFloat(inputs.c)||0
  let area, perimeter, formula
  if(shape==="rectangle"){
    if(a<=0||b<=0) throw new Error("Enter length and width.")
    area=a*b; perimeter=2*(a+b); formula="A = l x w"
  } else if(shape==="circle"){
    if(a<=0) throw new Error("Enter radius.")
    area=Math.PI*a*a; perimeter=2*Math.PI*a; formula="A = pi r^2"
  } else if(shape==="triangle"){
    if(a<=0||b<=0) throw new Error("Enter base and height.")
    area=0.5*a*b; perimeter=a+b+(c||Math.sqrt(a*a+b*b)); formula="A = 1/2 x b x h"
  } else if(shape==="square"){
    if(a<=0) throw new Error("Enter side length.")
    area=a*a; perimeter=4*a; formula="A = s^2"
  } else if(shape==="trapezoid"){
    if(a<=0||b<=0||c<=0) throw new Error("Enter both bases and height.")
    area=0.5*(a+b)*c; perimeter=0; formula="A = 1/2 x (a+b) x h"
  } else if(shape==="ellipse"){
    area=Math.PI*a*b; perimeter=Math.PI*(3*(a+b)-Math.sqrt((3*a+b)*(a+3*b))); formula="A = pi a b"
  } else {
    throw new Error("Unknown shape")
  }
  return {
    value:area.toFixed(4)+" sq units",
    gaugeValue:Math.min(area/1000*100,100),
    breakdown:["Shape: "+shape,"Formula: "+formula,"Area: "+area.toFixed(4)+" sq units","Perimeter: "+perimeter.toFixed(4)+" units"],
    stats:[
      {label:"Area",value:area.toFixed(4)},
      {label:"Shape",value:shape.charAt(0).toUpperCase()+shape.slice(1)},
      {label:"Perimeter",value:perimeter.toFixed(4)},
      {label:"Formula",value:formula},
    ]
  }
""",
  """{id:"shape",label:"Shape",type:"select",options:[
              {value:"rectangle",label:"Rectangle"},
              {value:"square",label:"Square"},
              {value:"circle",label:"Circle"},
              {value:"triangle",label:"Triangle (base & height)"},
              {value:"trapezoid",label:"Trapezoid"},
              {value:"ellipse",label:"Ellipse"},
            ],defaultValue:"rectangle"},
            {id:"a",label:"Side A / Length / Radius / Base 1",type:"number",placeholder:"10",min:0,step:0.01,defaultValue:10},
            {id:"b",label:"Side B / Width / Height / Base 2",type:"number",placeholder:"5",min:0,step:0.01,defaultValue:5},
            {id:"c",label:"Side C / Height (trapezoid/triangle 3rd side)",type:"number",placeholder:"0",min:0,step:0.01,defaultValue:0}""",
  [("Small (<50)","#3b82f6",0,5),("Medium (50-500)","#22c55e",5,50),("Large (500+)","#f59e0b",50,100)],
  "sq units (of 1000)","100",
  [("How do I calculate the area of a rectangle?","Area = Length x Width. A room that is 12 feet by 15 feet has an area of 180 square feet. For square units, make sure both measurements use the same unit before multiplying."),
   ("How do I calculate the area of a circle?","Area = pi x r2, where r is the radius. Circumference = 2 x pi x r. A circle with radius 5 has area = pi x 25 = 78.54 sq units. If you know the diameter, radius = diameter / 2."),
   ("How do I calculate triangle area without height?","If you know all three sides (a, b, c), use Heron formula: s = (a+b+c)/2, Area = sqrt(s(s-a)(s-b)(s-c)). If you know two sides and the included angle: Area = 0.5 x a x b x sin(C)."),
   ("How do I convert square feet to square meters?","1 square foot = 0.0929 square meters. 1 square meter = 10.764 square feet. To convert: sq ft x 0.0929 = sq meters. A 2,000 sq ft house = 185.8 sq meters."),
   ("What is the area of a regular hexagon?","Regular hexagon area = (3 x sqrt(3) / 2) x s2, where s is the side length. A hexagon with side length 5 has area = (3 x 1.732 / 2) x 25 = 64.95 sq units.")],
  [("Volume Calculator","/calculators/volume-calculator"),("Triangle Calculator","/calculators/triangle-calculator"),("Circle Calculator","/calculators/circle-calculator"),("Pythagorean Theorem Calculator","/calculators/triangle-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Area Formulas</h3>
          <div class="space-y-1 text-xs text-blue-800 font-mono">
            <div>Rectangle: A = l x w</div>
            <div>Square: A = s^2</div>
            <div>Circle: A = pi x r^2</div>
            <div>Triangle: A = 1/2 x b x h</div>
            <div>Trapezoid: A = 1/2 x (a+b) x h</div>
            <div>Ellipse: A = pi x a x b</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Real-World Area Examples</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Space</th><th class="text-right p-2 text-xs font-semibold">Typical Area</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Bedroom","120–200 sq ft"],["Living room","250–400 sq ft"],["House (US avg)","2,300 sq ft"],["Tennis court","2,808 sq ft"],["Football field","57,600 sq ft"],["Acre","43,560 sq ft"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Unit Conversions</h2>
        <div class="space-y-1 text-xs text-gray-600 bg-gray-50 rounded-xl p-4 font-mono">
          <div>1 sq ft = 144 sq inches</div>
          <div>1 sq yard = 9 sq ft</div>
          <div>1 sq meter = 10.764 sq ft</div>
          <div>1 acre = 43,560 sq ft</div>
          <div>1 hectare = 2.471 acres</div>
          <div>1 sq mile = 640 acres</div>
        </div>
      </div>
    </div>""",
  "Area","Calculate area of any geometric shape")

# ── DISTANCE ──────────────────────────────────────────────────────────────────
w("distance","Distance Calculator","Math","math",
  "Distance Calculator: Distance Between Two Points",
  "Calculate the distance between two points using the distance formula. Convert between miles, km, and more. Free distance calculator.",
  """
  const x1 = parseFloat(inputs.x1)||0
  const y1 = parseFloat(inputs.y1)||0
  const x2 = parseFloat(inputs.x2)||0
  const y2 = parseFloat(inputs.y2)||0
  const dx = x2-x1, dy = y2-y1
  const distance = Math.sqrt(dx*dx+dy*dy)
  const midX = (x1+x2)/2, midY = (y1+y2)/2
  const angle = Math.atan2(dy,dx)*180/Math.PI
  return {
    value:distance.toFixed(6),
    gaugeValue:Math.min(distance/100*100,100),
    breakdown:["Point 1: ("+x1+", "+y1+")","Point 2: ("+x2+", "+y2+")","Distance: "+distance.toFixed(6),"Midpoint: ("+midX.toFixed(3)+", "+midY.toFixed(3)+")","Slope: "+(dx!==0?(dy/dx).toFixed(4):"undefined"),"Angle: "+angle.toFixed(2)+"deg"],
    stats:[
      {label:"Distance",value:distance.toFixed(4)},
      {label:"Midpoint X",value:midX.toFixed(3)},
      {label:"Midpoint Y",value:midY.toFixed(3)},
      {label:"Angle",value:angle.toFixed(2)+"°"},
    ]
  }
""",
  """{id:"x1",label:"Point 1 — X coordinate",type:"number",placeholder:"0",step:0.001,defaultValue:0},
            {id:"y1",label:"Point 1 — Y coordinate",type:"number",placeholder:"0",step:0.001,defaultValue:0},
            {id:"x2",label:"Point 2 — X coordinate",type:"number",placeholder:"3",step:0.001,defaultValue:3},
            {id:"y2",label:"Point 2 — Y coordinate",type:"number",placeholder:"4",step:0.001,defaultValue:4}""",
  [("Short","#3b82f6",0,25),("Medium","#22c55e",25,75),("Long","#f59e0b",75,100)],
  "distance","100",
  [("What is the distance formula?","Distance = sqrt((x2-x1)^2 + (y2-y1)^2). This is derived from the Pythagorean theorem: the distance is the hypotenuse of a right triangle with legs (x2-x1) and (y2-y1). For a 3D distance: sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2)."),
   ("How do I find the midpoint of two points?","Midpoint = ((x1+x2)/2, (y1+y2)/2). The midpoint is exactly halfway between the two points. For a line segment from (2,4) to (8,10): midpoint = ((2+8)/2, (4+10)/2) = (5, 7)."),
   ("What is the slope between two points?","Slope = (y2-y1)/(x2-x1) = rise/run. A positive slope goes up-right. Negative slope goes down-right. Zero slope is horizontal. Undefined slope is vertical (x1=x2). Slope is the m in y = mx + b (slope-intercept form)."),
   ("How do I calculate geographic distance between cities?","For real-world coordinates (latitude/longitude), use the Haversine formula or spherical law of cosines. The straight-line distance between two lat/lon points is the great-circle distance. Google Maps uses road network distance, which is always longer."),
   ("What is the unit circle?","A unit circle has center at origin (0,0) and radius 1. Any point on it satisfies x^2 + y^2 = 1. Distance from origin to any point on the unit circle = 1. It is fundamental to trigonometry: cos(theta) = x-coordinate, sin(theta) = y-coordinate for any angle theta.")],
  [("Triangle Calculator","/calculators/triangle-calculator"),("Slope Calculator","/calculators/slope-calculator"),("Area Calculator","/calculators/area-calculator"),("Pythagorean Theorem Calculator","/calculators/triangle-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Distance Formula</h3>
          <div class="text-xs text-blue-800 font-mono bg-blue-100 rounded p-2 mb-3">d = sqrt((x2-x1)^2 + (y2-y1)^2)</div>
          <div class="text-xs text-blue-800"><strong>Example:</strong> (0,0) to (3,4)<br/>d = sqrt(9+16) = sqrt(25) = 5</div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Common Pythagorean Triples</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Point 1</th><th class="text-right p-2 text-xs font-semibold">Point 2</th><th class="text-right p-2 text-xs font-semibold">Distance</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["(0,0)","(3,4)","5"],["(0,0)","(5,12)","13"],["(0,0)","(8,15)","17"],["(0,0)","(7,24)","25"],["(0,0)","(20,21)","29"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right font-medium text-blue-700">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Related Distance Concepts</h2>
        <div class="space-y-3">
          {[
            {concept:"Manhattan Distance",formula:"d = |x2-x1| + |y2-y1|",use:"Used in grid-based navigation (city blocks)"},
            {concept:"Euclidean Distance",formula:"d = sqrt(dx^2 + dy^2)",use:"Straight-line distance (this calculator)"},
            {concept:"Chebyshev Distance",formula:"d = max(|dx|, |dy|)",use:"King moves on chessboard — used in AI"},
            {concept:"Haversine Distance",formula:"For lat/lon spherical coords",use:"Great-circle distance between GPS points"},
          ].map(c => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-xs text-gray-800">{c.concept}</div>
              <div class="text-xs font-mono text-blue-600">{c.formula}</div>
              <div class="text-xs text-gray-500">{c.use}</div>
            </div>
          ))}
        </div>
      </div>
    </div>""",
  "Distance","Calculate distance between two points using the distance formula")

# ── SLOPE ────────────────────────────────────────────────────────────────────
w("slope","Slope Calculator","Math","math",
  "Slope Calculator: Slope of a Line Between Two Points",
  "Calculate the slope, angle, line equation, and x/y intercepts from two points. Free slope calculator.",
  """
  const x1 = parseFloat(inputs.x1)||0
  const y1 = parseFloat(inputs.y1)||0
  const x2 = parseFloat(inputs.x2)||0
  const y2 = parseFloat(inputs.y2)||0
  const dx = x2-x1, dy = y2-y1
  if(dx===0) {
    return {
      value:"Undefined (vertical line)",
      gaugeValue:100,
      breakdown:["Vertical line: x = "+x1,"Slope is undefined (division by zero)"],
      stats:[{label:"Line Type",value:"Vertical"},{label:"x = ",value:String(x1)},{label:"Slope",value:"Undefined"},{label:"Angle",value:"90°"}]
    }
  }
  const slope = dy/dx
  const yIntercept = y1-slope*x1
  const xIntercept = slope!==0?(-yIntercept/slope):undefined
  const angle = Math.atan(slope)*180/Math.PI
  const direction = slope>0?"Positive (rising)":slope<0?"Negative (falling)":"Zero (horizontal)"
  return {
    value:"Slope: "+slope.toFixed(4),
    gaugeValue:Math.min(Math.abs(slope)/10*100,100),
    breakdown:["Slope: "+slope.toFixed(4)+" ("+direction+")","y-intercept: "+yIntercept.toFixed(4),"x-intercept: "+(xIntercept!==undefined?xIntercept.toFixed(4):"None (horizontal)"),"Equation: y = "+slope.toFixed(4)+"x + "+yIntercept.toFixed(4),"Angle: "+angle.toFixed(2)+"deg"],
    stats:[
      {label:"Slope",value:slope.toFixed(4)},
      {label:"Y-Intercept",value:yIntercept.toFixed(4)},
      {label:"Angle",value:angle.toFixed(2)+"°"},
      {label:"Direction",value:direction.split(" ")[0]},
    ]
  }
""",
  """{id:"x1",label:"Point 1 — X",type:"number",placeholder:"0",step:0.001,defaultValue:0},
            {id:"y1",label:"Point 1 — Y",type:"number",placeholder:"0",step:0.001,defaultValue:0},
            {id:"x2",label:"Point 2 — X",type:"number",placeholder:"4",step:0.001,defaultValue:4},
            {id:"y2",label:"Point 2 — Y",type:"number",placeholder:"8",step:0.001,defaultValue:8}""",
  [("Negative slope","#ef4444",0,50),("Zero slope","#3b82f6",50,50),("Positive slope","#22c55e",50,100)],
  "slope direction","100",
  [("What is slope?","Slope = rise/run = (y2-y1)/(x2-x1). It measures how steep a line is and in which direction it goes. Positive slope: line goes up-right. Negative slope: line goes down-right. Zero slope: horizontal line. Undefined slope: vertical line."),
   ("What is the slope-intercept form?","y = mx + b, where m is slope and b is y-intercept. This is the most common form of a linear equation. Once you have slope and any point, you can find b: b = y - mx. For point (2,5) with slope 3: b = 5 - 3x2 = -1. Equation: y = 3x - 1."),
   ("What is the point-slope form?","y - y1 = m(x - x1), where m is slope and (x1,y1) is a known point. Useful when you know slope and one point but not the y-intercept. Example: slope 2, point (3,7): y - 7 = 2(x - 3) → y = 2x + 1."),
   ("How are slopes of parallel and perpendicular lines related?","Parallel lines have EQUAL slopes. Perpendicular lines have slopes that are negative reciprocals: if slope1 = m, then slope2 = -1/m. Example: slope 2/3 is perpendicular to slope -3/2. This is true for all perpendicular lines except horizontal/vertical."),
   ("What does slope mean in real life?","Slope is rate of change. A road grade of 6% means rise 6 units per 100 units horizontal (slope = 0.06). A salary that increases $2,000 per year has slope of 2,000. Stock price change over time has slope = price change rate. In physics, slope of a distance-time graph = speed.")],
  [("Distance Calculator","/calculators/distance-calculator"),("Area Calculator","/calculators/area-calculator"),("Triangle Calculator","/calculators/triangle-calculator"),("Z-Score Calculator","/calculators/z-score-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Slope Formula</h3>
          <div class="text-xs text-blue-800 font-mono bg-blue-100 rounded p-2 mb-2">m = (y2-y1)/(x2-x1)</div>
          <div class="text-xs text-blue-800 space-y-1">
            <div>m &gt; 0: Rising (positive slope)</div>
            <div>m &lt; 0: Falling (negative slope)</div>
            <div>m = 0: Horizontal line</div>
            <div>m = undefined: Vertical line</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Forms of Linear Equations</h2>
        <div class="space-y-3">
          {[
            {name:"Slope-Intercept",form:"y = mx + b",desc:"m = slope, b = y-intercept. Most common form."},
            {name:"Point-Slope",form:"y - y1 = m(x - x1)",desc:"Use when you know slope and one point."},
            {name:"Standard Form",form:"Ax + By = C",desc:"Useful for some algebraic operations."},
            {name:"Two-Point Form",form:"(y-y1)/(y2-y1) = (x-x1)/(x2-x1)",desc:"Use when you know exactly two points."},
          ].map(f => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-xs text-gray-800">{f.name}</div>
              <div class="text-xs font-mono text-blue-600">{f.form}</div>
              <div class="text-xs text-gray-500">{f.desc}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Slope Angle Reference</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold">Slope</th><th class="text-right p-2 text-xs font-semibold">Angle</th><th class="text-right p-2 text-xs font-semibold">Description</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["0","0°","Horizontal"],["0.268","15°","Gentle slope"],["0.577","30°","Moderate"],["1.0","45°","45-degree"],["1.732","60°","Steep"],["∞","90°","Vertical"]].map(r => (
              <tr><td class="p-2 text-xs font-mono">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "Slope","Calculate slope, line equation, and intercepts from two points")

print(f"\nWritten: {written} pages (pregnancy-weight, area, distance, slope)")
