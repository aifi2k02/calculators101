#!/usr/bin/env python3
import os
CALC_DIR = "/Users/apple/Documents/Projects/calculators-for-free/src/pages/calculators"

formula = """
  const value = parseFloat(inputs.value)||0
  const category = inputs.category||"length"
  const from = inputs.from||"meters"
  const to = inputs.to||"feet"
  if(isNaN(value)) throw new Error("Enter a valid number.")
  const conversions = {
    length: {
      meters:1, feet:0.3048, inches:0.0254, centimeters:0.01, kilometers:1000,
      miles:1609.344, yards:0.9144, millimeters:0.001, nautical_miles:1852
    },
    weight: {
      kilograms:1, pounds:0.453592, grams:0.001, ounces:0.0283495,
      tons_metric:1000, tons_us:907.185, milligrams:0.000001, stone:6.35029
    },
    temperature: {celsius:null,fahrenheit:null,kelvin:null},
    volume: {
      liters:1, gallons_us:3.78541, milliliters:0.001, cubic_meters:1000,
      cups:0.236588, pints:0.473176, quarts:0.946353, fluid_oz:0.0295735, tablespoons:0.0147868
    },
    area: {
      square_meters:1, square_feet:0.0929, square_inches:0.000645, square_kilometers:1000000,
      square_miles:2589988, acres:4046.86, hectares:10000
    },
    speed: {
      mps:1, mph:0.44704, kmh:1/3.6, knots:0.514444
    },
    time: {
      seconds:1, minutes:60, hours:3600, days:86400, weeks:604800
    }
  }
  let result, fromLabel=from.replace(/_/g," "), toLabel=to.replace(/_/g," ")
  if(category==="temperature"){
    let celsius
    if(from==="celsius") celsius=value
    else if(from==="fahrenheit") celsius=(value-32)*5/9
    else if(from==="kelvin") celsius=value-273.15
    else throw new Error("Unknown temperature unit.")
    if(to==="celsius") result=celsius
    else if(to==="fahrenheit") result=celsius*9/5+32
    else if(to==="kelvin") result=celsius+273.15
    else throw new Error("Unknown temperature unit.")
  } else {
    const cat=conversions[category]
    if(!cat||!cat[from]||!cat[to]) throw new Error("Unknown unit for category "+category+".")
    const base=value*cat[from]
    result=base/cat[to]
  }
  return {
    value:result.toFixed(6)+" "+toLabel,
    gaugeValue:50,
    breakdown:[value+" "+fromLabel+" = "+result.toFixed(6)+" "+toLabel,"Category: "+category,"Exact: "+result+" "+toLabel],
    stats:[
      {label:"Result",value:result.toFixed(4)+" "+toLabel},
      {label:"Input",value:value+" "+fromLabel},
      {label:"Category",value:category.charAt(0).toUpperCase()+category.slice(1)},
      {label:"Conversion",value:fromLabel+" → "+toLabel},
    ]
  }
"""

faqs = [
    ("How do I convert meters to feet?","Multiply meters by 3.28084 to get feet. Or: divide by 0.3048. Example: 10 meters = 10 × 3.28084 = 32.8084 feet. For a quick mental estimate: 1 meter ≈ 3.28 feet, or 3 feet 3.37 inches.",""),
    ("How do I convert kg to pounds?","Multiply kilograms by 2.20462 to get pounds. Example: 70 kg = 70 × 2.20462 = 154.32 pounds. Reverse: divide pounds by 2.20462 to get kg. Or: divide pounds by 2.2 for a quick estimate.",""),
    ("How do I convert Celsius to Fahrenheit?","F = C × 9/5 + 32. Example: 20°C = 20 × 1.8 + 32 = 36 + 32 = 68°F. Key benchmarks: 0°C = 32°F (freezing), 100°C = 212°F (boiling), 37°C = 98.6°F (body temperature). Reverse: C = (F - 32) × 5/9.",""),
    ("How do I convert liters to gallons?","1 liter = 0.264172 US gallons. Multiply liters by 0.264172 for gallons. Or: 1 US gallon = 3.78541 liters. Example: 10 liters = 10 × 0.264172 = 2.64 gallons. Note: UK gallons are larger — 1 UK gallon = 4.546 liters.",""),
    ("How do I convert miles to kilometers?","Multiply miles by 1.60934 to get kilometers. Example: 60 miles = 96.56 km. Reverse: divide km by 1.60934 (or multiply by 0.6214). Quick mental estimate: km = miles × 1.6, or add 60% to miles.",""),
]

sidebar = """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Quick Conversions</h3>
          <div class="text-xs text-blue-800 space-y-1">
            <div>1 meter = 3.28084 feet</div>
            <div>1 kg = 2.20462 lbs</div>
            <div>1 liter = 0.2642 US gallons</div>
            <div>1 mile = 1.60934 km</div>
            <div>1 inch = 2.54 cm</div>
            <div>°F = °C × 1.8 + 32</div>
            <div>1 acre = 4,046.86 m²</div>
          </div>
        </div>"""

content_html = """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Common Conversions</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">From</th><th class="p-2 text-xs font-semibold text-right">To</th><th class="p-2 text-xs font-semibold text-right">Multiply by</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Meters","Feet","3.28084"],["Kg","Pounds","2.20462"],["Liters","US Gallons","0.26417"],["Miles","Kilometers","1.60934"],["Inches","Centimeters","2.54"],["Acres","Square meters","4046.86"],["MPH","km/h","1.60934"],["Fluid oz","mL","29.574"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right font-mono">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Categories</h2>
        <div class="space-y-2">
          {[
            {c:"Length",u:"meters, feet, inches, cm, km, miles, yards"},
            {c:"Weight",u:"kg, pounds, grams, ounces, tons, stone"},
            {c:"Temperature",u:"Celsius, Fahrenheit, Kelvin"},
            {c:"Volume",u:"liters, gallons, cups, pints, quarts, mL"},
            {c:"Area",u:"sq meters, sq feet, acres, hectares"},
            {c:"Speed",u:"mph, km/h, m/s, knots"},
            {c:"Time",u:"seconds, minutes, hours, days, weeks"},
          ].map(cat => (
            <div class="bg-gray-50 rounded-lg p-2"><div class="font-semibold text-xs text-blue-700">{cat.c}</div><div class="text-xs text-gray-600">{cat.u}</div></div>
          ))}
        </div>
      </div>
    </div>"""

zones_js = '\n'.join(f'              {{ label: "{z[0]}", color: "{z[1]}", from: {z[2]}, to: {z[3]} }},' for z in [
    ("Small","#22c55e",0,33), ("Medium","#3b82f6",33,66), ("Large","#f59e0b",66,100)
])
related_js = '\n            '.join(f'{{ name: "{n}", href: "{h}" }},' for n,h in [
    ("Height Converter","/calculators/height-converter-calculator"),
    ("Speed Converter","/calculators/speed-calculator"),
    ("Area Calculator","/calculators/area-calculator"),
    ("Distance Calculator","/calculators/distance-calculator"),
])
faqs_js = "[\n" + ",\n".join(f'  {{ question: "{q.replace(chr(34), chr(92)+chr(34))}", answer: "{a.replace(chr(34), chr(92)+chr(34))}" }}' for q,a,_ in faqs) + "\n]"

content = f'''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
{formula}
`

const faqs = {faqs_js}
---
<Layout
  title="Unit Converter: Length, Weight, Temperature, Volume & More"
  description="Convert between hundreds of units: length, weight, temperature, volume, area, speed, and time. Free unit converter calculator."
  breadcrumbs={{[
    {{ name: "Home", href: "/" }},
    {{ name: "Other", href: "/calculators/other" }},
    {{ name: "Unit Converter", href: "/calculators/unit-converter-calculator" }},
  ]}}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/other" class="hover:text-blue-600">Other</a><span>›</span>
      <span class="text-gray-900">Unit Converter</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Unit Converter"
          description="Convert between length, weight, temperature, volume, area, speed, and time units instantly."
          formulaId="unit-converter"
          formulaFn={{formulaFn}}
          resultLabel="Converted Value"
          inputs={{[
            {{id:"category",label:"Category",type:"select",options:[
              {{value:"length",label:"Length"}},
              {{value:"weight",label:"Weight / Mass"}},
              {{value:"temperature",label:"Temperature"}},
              {{value:"volume",label:"Volume"}},
              {{value:"area",label:"Area"}},
              {{value:"speed",label:"Speed"}},
              {{value:"time",label:"Time"}},
            ],defaultValue:"length"}},
            {{id:"value",label:"Value",type:"number",placeholder:"1",step:0.000001,defaultValue:1}},
            {{id:"from",label:"From unit",type:"select",options:[
              {{value:"meters",label:"Meters"}},
              {{value:"feet",label:"Feet"}},
              {{value:"inches",label:"Inches"}},
              {{value:"centimeters",label:"Centimeters"}},
              {{value:"kilometers",label:"Kilometers"}},
              {{value:"miles",label:"Miles"}},
              {{value:"yards",label:"Yards"}},
              {{value:"kilograms",label:"Kilograms"}},
              {{value:"pounds",label:"Pounds"}},
              {{value:"grams",label:"Grams"}},
              {{value:"ounces",label:"Ounces"}},
              {{value:"celsius",label:"Celsius (°C)"}},
              {{value:"fahrenheit",label:"Fahrenheit (°F)"}},
              {{value:"kelvin",label:"Kelvin (K)"}},
              {{value:"liters",label:"Liters"}},
              {{value:"gallons_us",label:"Gallons (US)"}},
              {{value:"milliliters",label:"Milliliters"}},
              {{value:"cups",label:"Cups"}},
              {{value:"square_meters",label:"Square Meters"}},
              {{value:"square_feet",label:"Square Feet"}},
              {{value:"acres",label:"Acres"}},
              {{value:"mph",label:"MPH"}},
              {{value:"kmh",label:"km/h"}},
              {{value:"mps",label:"m/s"}},
              {{value:"seconds",label:"Seconds"}},
              {{value:"minutes",label:"Minutes"}},
              {{value:"hours",label:"Hours"}},
              {{value:"days",label:"Days"}},
            ],defaultValue:"meters"}},
            {{id:"to",label:"To unit",type:"select",options:[
              {{value:"feet",label:"Feet"}},
              {{value:"meters",label:"Meters"}},
              {{value:"inches",label:"Inches"}},
              {{value:"centimeters",label:"Centimeters"}},
              {{value:"kilometers",label:"Kilometers"}},
              {{value:"miles",label:"Miles"}},
              {{value:"pounds",label:"Pounds"}},
              {{value:"kilograms",label:"Kilograms"}},
              {{value:"grams",label:"Grams"}},
              {{value:"ounces",label:"Ounces"}},
              {{value:"fahrenheit",label:"Fahrenheit (°F)"}},
              {{value:"celsius",label:"Celsius (°C)"}},
              {{value:"kelvin",label:"Kelvin (K)"}},
              {{value:"gallons_us",label:"Gallons (US)"}},
              {{value:"liters",label:"Liters"}},
              {{value:"milliliters",label:"Milliliters"}},
              {{value:"cups",label:"Cups"}},
              {{value:"square_feet",label:"Square Feet"}},
              {{value:"square_meters",label:"Square Meters"}},
              {{value:"acres",label:"Acres"}},
              {{value:"kmh",label:"km/h"}},
              {{value:"mph",label:"MPH"}},
              {{value:"mps",label:"m/s"}},
              {{value:"minutes",label:"Minutes"}},
              {{value:"seconds",label:"Seconds"}},
              {{value:"hours",label:"Hours"}},
            ],defaultValue:"feet"}},
          ]}}
          gauge={{{{
            min: 0, max: 100, unit: "gauge",
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
{sidebar}
      </aside>
    </div>
{content_html}
  </div>
</Layout>
'''

path = os.path.join(CALC_DIR, "unit-converter-calculator.astro")
open(path,'w').write(content)
print("✓ unit-converter")
