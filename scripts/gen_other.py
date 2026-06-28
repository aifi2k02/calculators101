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

# ── ANGLE CONVERTER ───────────────────────────────────────────────────────────
w("angle-converter","Angle Converter","Other","other",
  "Angle Converter: Degrees, Radians, Gradians, Turns",
  "Convert angles between degrees, radians, gradians, turns, and arcminutes/arcseconds. Free angle converter calculator.",
  """
  const value = parseFloat(inputs.value)||0
  const from = inputs.from||"degrees"
  let radians
  if(from==="degrees") radians=value*Math.PI/180
  else if(from==="radians") radians=value
  else if(from==="gradians") radians=value*Math.PI/200
  else if(from==="turns") radians=value*2*Math.PI
  else if(from==="arcminutes") radians=value*Math.PI/10800
  else if(from==="arcseconds") radians=value*Math.PI/648000
  else throw new Error("Unknown unit.")
  const degrees=radians*180/Math.PI
  const gradians=radians*200/Math.PI
  const turns=radians/(2*Math.PI)
  const arcmins=degrees*60
  const arcsecs=degrees*3600
  return {
    value:degrees.toFixed(6)+" degrees",
    gaugeValue:((degrees%360)+360)%360/360*100,
    breakdown:["Input: "+value+" "+from,"Degrees: "+degrees.toFixed(6),"Radians: "+radians.toFixed(6),"Gradians: "+gradians.toFixed(6),"Turns: "+turns.toFixed(6),"Arcminutes: "+arcmins.toFixed(4),"Arcseconds: "+arcsecs.toFixed(2)],
    stats:[
      {label:"Degrees",value:degrees.toFixed(4)},
      {label:"Radians",value:radians.toFixed(6)},
      {label:"Gradians",value:gradians.toFixed(4)},
      {label:"Turns",value:turns.toFixed(6)},
    ]
  }
""",
  """{id:"value",label:"Angle value",type:"number",placeholder:"90",step:0.0001,defaultValue:90},
            {id:"from",label:"Convert from",type:"select",options:[
              {value:"degrees",label:"Degrees (°)"},
              {value:"radians",label:"Radians (rad)"},
              {value:"gradians",label:"Gradians (gon)"},
              {value:"turns",label:"Turns (full rotations)"},
              {value:"arcminutes",label:"Arcminutes (')"},
              {value:"arcseconds",label:"Arcseconds (\")"},
            ],defaultValue:"degrees"}""",
  [("Acute (0-90)","#22c55e",0,25),("Right/Obtuse (90-180)","#3b82f6",25,50),("Reflex (180-360)","#f59e0b",50,100)],
  "% of circle","100",
  [("How do I convert degrees to radians?","Multiply degrees by pi/180. Example: 90 degrees = 90 x pi/180 = pi/2 radians ≈ 1.5708. Or use the proportion: degrees/180 = radians/pi. Key angles: 30deg=pi/6, 45deg=pi/4, 60deg=pi/3, 90deg=pi/2, 180deg=pi, 360deg=2pi."),
   ("What are gradians (gons)?","A gradian divides a full circle into 400 gradians (100 per right angle). Used mainly in surveying: a right angle = 100 gradians. Conversion: gradians = degrees x 400/360 = degrees x 10/9. A 90-degree angle = 100 gradians. Gradians make compass bearings easier to calculate."),
   ("What is an arcminute and arcsecond?","1 degree = 60 arcminutes (symbol: prime). 1 arcminute = 60 arcseconds (symbol: double-prime). These tiny units measure precise angles in astronomy and navigation. The moon is about 0.5 degrees = 30 arcminutes in diameter. GPS accuracy is expressed in arcseconds."),
   ("Why do we use radians in calculus?","Radians make calculus simpler: d/dx[sin(x)] = cos(x) only holds when x is in radians. If you use degrees, you get d/dx[sin(x)] = (pi/180)cos(x). Radians also give natural values: arc length = r x theta (in radians). Period of sin: 2pi radians, not 360 degrees."),
   ("What are the major angle benchmarks?","0 deg = no rotation. 30 deg = pi/6 rad (1/12 circle). 45 deg = pi/4 rad (1/8 circle). 60 deg = pi/3 rad (1/6 circle). 90 deg = pi/2 rad (1/4 circle = right angle). 180 deg = pi rad (straight line). 270 deg = 3pi/2 rad. 360 deg = 2pi rad (full circle).")],
  [("Unit Converter","/calculators/unit-converter-calculator"),("Distance Calculator","/calculators/distance-calculator"),("Triangle Calculator","/calculators/triangle-calculator"),("Law of Cosines Calculator","/calculators/law-of-cosines-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Key Conversions</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700"><th class="text-left">Degrees</th><th class="text-right">Radians</th><th class="text-right">Gradians</th></tr></thead>
            <tbody class="font-mono text-blue-900">
              {[[30,"π/6","33.3"],[45,"π/4","50"],[60,"π/3","66.7"],[90,"π/2","100"],[180,"π","200"],[360,"2π","400"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}°</td><td class="text-right">{r[1]}</td><td class="text-right">{r[2]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Angle Types</h2>
        <div class="space-y-2">
          {[{t:"Acute",r:"0° to 90°",d:"Smaller than a right angle"},
            {t:"Right",r:"Exactly 90°",d:"Quarter turn, forms an L shape"},
            {t:"Obtuse",r:"90° to 180°",d:"Larger than right angle"},
            {t:"Straight",r:"Exactly 180°",d:"Half turn, forms a straight line"},
            {t:"Reflex",r:"180° to 360°",d:"More than half a turn"},
            {t:"Full",r:"360°",d:"Complete rotation"}].map(a => (
            <div class="bg-gray-50 rounded-lg p-2"><div class="font-semibold text-xs text-blue-700">{a.t} <span class="text-gray-500">({a.r})</span></div><div class="text-xs text-gray-600">{a.d}</div></div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Trig Values at Key Angles</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Angle</th><th class="p-2 text-xs text-right">sin</th><th class="p-2 text-xs text-right">cos</th><th class="p-2 text-xs text-right">tan</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["0°","0","1","0"],["30°","0.5","0.866","0.577"],["45°","0.707","0.707","1"],["60°","0.866","0.5","1.732"],["90°","1","0","∞"],["180°","0","−1","0"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td><td class="p-2 text-xs text-right">{r[3]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "Degrees","Convert angles between degrees, radians, gradians, and more")

# ── COLOR CONVERTER ───────────────────────────────────────────────────────────
w("color-converter","Color Converter","Other","other",
  "Color Converter: HEX, RGB, HSL, HSV & CSS Colors",
  "Convert colors between HEX, RGB, HSL, HSV, and CMYK formats. Preview colors instantly. Free color converter and picker.",
  """
  const input = (inputs.color||"").trim()
  let r,g,b
  if(input.startsWith("#")){
    const hex=input.slice(1)
    if(hex.length===3){r=parseInt(hex[0]+hex[0],16);g=parseInt(hex[1]+hex[1],16);b=parseInt(hex[2]+hex[2],16)}
    else{r=parseInt(hex.slice(0,2),16);g=parseInt(hex.slice(2,4),16);b=parseInt(hex.slice(4,6),16)}
  } else if(input.toLowerCase().startsWith("rgb")){
    const m=input.match(/\\d+/g)
    if(!m||m.length<3) throw new Error("Invalid RGB. Use: rgb(255,100,0) or 255,100,0")
    r=parseInt(m[0]);g=parseInt(m[1]);b=parseInt(m[2])
  } else if(input.includes(",")){
    const parts=input.split(",")
    r=parseInt(parts[0]);g=parseInt(parts[1]);b=parseInt(parts[2])
  } else throw new Error("Enter HEX (#FF6B35) or RGB (255,107,53)")
  r=Math.max(0,Math.min(255,r));g=Math.max(0,Math.min(255,g));b=Math.max(0,Math.min(255,b))
  const hex="#"+[r,g,b].map(x=>x.toString(16).padStart(2,"0")).join("").toUpperCase()
  const rp=r/255,gp=g/255,bp=b/255
  const max=Math.max(rp,gp,bp),min=Math.min(rp,gp,bp),delta=max-min
  const l=(max+min)/2
  const s=delta===0?0:(l<0.5?delta/(max+min):delta/(2-max-min))
  let h=0
  if(delta!==0){
    if(max===rp) h=((gp-bp)/delta%6)*60
    else if(max===gp) h=((bp-rp)/delta+2)*60
    else h=((rp-gp)/delta+4)*60
    if(h<0) h+=360
  }
  const brightness=Math.round((r*299+g*587+b*114)/1000)
  return {
    value:hex,
    gaugeValue:brightness/255*100,
    breakdown:["HEX: "+hex,"RGB: rgb("+r+", "+g+", "+b+")","HSL: hsl("+h.toFixed(0)+", "+Math.round(s*100)+"%, "+Math.round(l*100)+"%)","Brightness: "+brightness+"/255","Is dark: "+(brightness<128?"Yes":"No")],
    stats:[
      {label:"HEX",value:hex},
      {label:"RGB",value:r+", "+g+", "+b},
      {label:"HSL",value:h.toFixed(0)+"°, "+Math.round(s*100)+"%, "+Math.round(l*100)+"%"},
      {label:"Brightness",value:brightness+"/255"},
    ]
  }
""",
  """{id:"color",label:"Color (HEX like #FF6B35 or RGB like 255,107,53)",type:"text",placeholder:"#FF6B35",defaultValue:"#FF6B35"}""",
  [("Dark color","#1e293b",0,30),("Mid-tone","#6366f1",30,70),("Light color","#fbbf24",70,100)],
  "brightness","100",
  [("What is the difference between RGB and HEX color codes?","RGB and HEX are two formats for the same color. RGB uses three decimal values (0-255): rgb(255, 107, 53). HEX uses hexadecimal: #FF6B35. They are identical: 255 in decimal = FF in hex, 107 = 6B, 53 = 35. HEX is compact for HTML/CSS. RGB is easier to understand intuitively."),
   ("What is HSL color format?","HSL stands for Hue (0-360 degrees on the color wheel), Saturation (0-100%, gray to vivid), and Lightness (0-100%, black to white). HSL is more intuitive for design: to make a color lighter, increase L. To desaturate, decrease S. Pure red = hsl(0, 100%, 50%)."),
   ("How do I find the complementary color?","The complementary color is directly opposite on the color wheel: rotate hue by 180 degrees. If your color is hsl(30, 80%, 50%) (orange), the complement is hsl(210, 80%, 50%) (blue). In RGB, the complement is (255-r, 255-g, 255-b). Complementary colors create strong contrast."),
   ("What colors are best for accessibility (contrast)?","WCAG AA requires a contrast ratio of at least 4.5:1 for normal text. Contrast ratio = (L1 + 0.05) / (L2 + 0.05) where L1 is the lighter color relative luminance. Dark text on white (#FFFFFF) or light text on very dark backgrounds works well. Avoid light gray on white, or yellow on white."),
   ("What is CMYK color?","CMYK (Cyan, Magenta, Yellow, Black) is used in printing. Unlike RGB (additive — mixing light), CMYK is subtractive — mixing inks. White paper = no ink (0,0,0,0). Black = K=100 (key plate). Formula: C=(1-R/255), M=(1-G/255), Y=(1-B/255), K=min(C,M,Y), then subtract K from each. RGB is for screens, CMYK for print.")],
  [("Unit Converter","/calculators/unit-converter-calculator"),("Percentage Calculator","/calculators/percentage-calculator"),("Average Calculator","/calculators/average-calculator"),("Number Base Calculator","/calculators/number-base-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Common CSS Colors</h3>
          <div class="grid grid-cols-2 gap-1 text-xs">
            {[["#FF0000","Red"],["#00FF00","Lime"],["#0000FF","Blue"],["#FFFF00","Yellow"],["#FF6600","Orange"],["#800080","Purple"],["#000000","Black"],["#FFFFFF","White"]].map(([hex,name]) => (
              <div class="flex items-center gap-1.5">
                <div class="w-4 h-4 rounded border" style={"background:"+hex}></div>
                <span class="font-mono text-blue-800">{hex}</span>
              </div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Color Model Comparison</h2>
        <div class="space-y-2">
          {[
            {m:"RGB",u:"Screens, web, digital",r:"0-255 per channel (16M colors)"},
            {m:"HEX",u:"CSS, HTML, design tools",r:"#RRGGBB (same as RGB in hex)"},
            {m:"HSL",u:"Design, color relationships",r:"Hue 0-360°, Sat/Light 0-100%"},
            {m:"HSV/HSB",u:"Photo editing (Photoshop)",r:"Hue 0-360°, Sat/Value 0-100%"},
            {m:"CMYK",u:"Print, physical materials",r:"0-100% per channel"},
          ].map(c => (
            <div class="bg-gray-50 rounded-lg p-2"><div class="font-semibold text-xs text-blue-700">{c.m} — {c.u}</div><div class="text-xs text-gray-600">{c.r}</div></div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Color Psychology</h2>
        <div class="space-y-2">
          {["Red — urgency, passion, danger (#FF0000)","Orange — energy, warmth, creativity (#FF6600)","Yellow — optimism, attention, warning (#FFFF00)","Green — nature, growth, safety (#00AA44)","Blue — trust, calm, professional (#0066CC)","Purple — luxury, mystery, spiritual (#8800CC)"].map(a => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{a}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "HEX Color","Convert colors between HEX, RGB, and HSL formats")

# ── CONCRETE ─────────────────────────────────────────────────────────────────
w("concrete","Concrete Calculator","Other","other",
  "Concrete Calculator: Bags, Cubic Yards, Volume for Slabs",
  "Calculate how many bags of concrete you need for a slab, column, or footing. Find cubic yards and cubic feet. Free concrete calculator.",
  """
  const shape = inputs.shape||"slab"
  const len = parseFloat(inputs.len)||0
  const width = parseFloat(inputs.width)||0
  const depth = parseFloat(inputs.depth)||0
  const bagSize = parseFloat(inputs.bagSize)||60
  let cubicFeet, description
  if(shape==="slab"){
    if(len<=0||width<=0||depth<=0) throw new Error("Enter length, width, and depth.")
    cubicFeet=len*width*depth/12; description=len+"ft x "+width+"ft x "+depth+"in slab"
  } else if(shape==="column"){
    const radius=len/2
    if(len<=0||depth<=0) throw new Error("Enter diameter and height.")
    cubicFeet=Math.PI*radius*radius*depth/144; description=len+"in dia x "+depth+"in column"
  } else if(shape==="footing"){
    if(len<=0||width<=0||depth<=0) throw new Error("Enter length, width, and depth.")
    cubicFeet=len*width*depth/144; description=len+"in x "+width+"in x "+depth+"in footing"
  }
  const cubicYards=cubicFeet/27
  const withWaste=cubicYards*1.1
  const bags60=Math.ceil(cubicFeet/0.45)
  const bags80=Math.ceil(cubicFeet/0.60)
  const actualBags=bagSize===60?bags60:bags80
  return {
    value:withWaste.toFixed(2)+" cubic yards (+10% waste)",
    gaugeValue:Math.min(cubicYards/10*100,100),
    breakdown:["Shape: "+description,"Cubic feet: "+cubicFeet.toFixed(4),"Cubic yards: "+cubicYards.toFixed(4),"With 10% waste: "+withWaste.toFixed(4)+" yd3",bagSize+"lb bags needed: "+actualBags,"60lb bags alt: "+bags60,"80lb bags alt: "+bags80],
    stats:[
      {label:"Cubic Yards",value:withWaste.toFixed(2)+" yd³"},
      {label:"Cubic Feet",value:cubicFeet.toFixed(2)+" ft³"},
      {label:"60lb Bags",value:String(bags60)},
      {label:"80lb Bags",value:String(bags80)},
    ]
  }
""",
  """{id:"shape",label:"Shape",type:"select",options:[
              {value:"slab",label:"Slab / Pad (length × width in feet, depth in inches)"},
              {value:"column",label:"Circular Column (diameter in inches, height in inches)"},
              {value:"footing",label:"Wall Footing (length × width in inches, depth in inches)"},
            ],defaultValue:"slab"},
            {id:"len",label:"Length (ft for slab, inches for column diameter/footing)",type:"number",placeholder:"10",min:0,step:0.01,defaultValue:10},
            {id:"width",label:"Width (ft for slab, inches for footing — skip for column)",type:"number",placeholder:"10",min:0,step:0.01,defaultValue:10},
            {id:"depth",label:"Depth/Thickness (inches for slab/footing, inches for column height)",type:"number",placeholder:"4",min:0,step:0.01,defaultValue:4},
            {id:"bagSize",label:"Bag size",type:"select",options:[
              {value:"60",label:"60 lb bags"},
              {value:"80",label:"80 lb bags"},
            ],defaultValue:"60"}""",
  [("Small (< 1 yd3)","#22c55e",0,10),("Medium (1-5 yd3)","#3b82f6",10,50),("Large (5+ yd3)","#f59e0b",50,100)],
  "cubic yards","10",
  [("How many bags of concrete per cubic yard?","At 60 lb bags: approximately 60 bags per cubic yard (1 bag = 0.45 cu ft, 1 cu yd = 27 cu ft, 27/0.45 = 60). At 80 lb bags: approximately 45 bags per cubic yard. Always add 10% extra for waste and overfill. Mix coverage can vary slightly by brand."),
   ("How thick should a concrete slab be?","Sidewalk/patio: 4 inches. Residential driveway: 4-6 inches. Garage floor: 4-6 inches. Road pavement: 6-8 inches. Heavy industrial: 8+ inches. Footings extend below the frost line (varies by climate). Always check local building codes."),
   ("What is the correct concrete mix ratio?","Standard mix (3000 psi): 1 part cement: 2 parts sand: 3 parts gravel (1:2:3) by volume, plus water-cement ratio of 0.5-0.6. For bags: follow manufacturer instructions — typically 2.5 quarts of water per 60 lb bag for 80% strength. Too much water weakens concrete."),
   ("How long does concrete take to cure?","Concrete reaches initial set in 24-48 hours (do not walk on). 70% strength in 7 days. Full strength (28-day strength) in 28 days. Avoid freezing temperatures in first 24-48 hours. Keep moist for 7 days by covering with wet burlap or plastic sheeting for optimal curing."),
   ("When should I use ready-mix vs bagged concrete?","Bagged concrete (60/80 lb bags): small projects under 1 cubic yard — patching, fence posts, small slabs. Ready-mix truck: over 1 cubic yard, large slabs, driveways, foundations. Ready-mix is usually more cost-effective above 0.5 cubic yards and gives better quality control.")],
  [("Paint Calculator","/calculators/paint-calculator"),("Area Calculator","/calculators/area-calculator"),("Volume Calculator","/calculators/volume-calculator"),("Unit Converter","/calculators/unit-converter-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Quick Reference</h3>
          <div class="text-xs text-blue-800 space-y-1">
            <div>1 cubic yard = 27 cubic feet</div>
            <div>60 lb bag ≈ 0.45 cubic feet</div>
            <div>80 lb bag ≈ 0.60 cubic feet</div>
            <div>~60 bags (60lb) per cubic yard</div>
            <div>~45 bags (80lb) per cubic yard</div>
            <div>Always add 10% for waste</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Concrete Slab Examples</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Slab Size</th><th class="p-2 text-xs font-semibold text-right">4in thick</th><th class="p-2 text-xs font-semibold text-right">60lb bags</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["5 ft × 5 ft","0.31 yd³","~19"],["10 ft × 10 ft","1.23 yd³","~74"],["12 ft × 12 ft","1.78 yd³","~107"],["20 ft × 20 ft","4.94 yd³","~296"],["8 ft × 20 ft","1.98 yd³","~119"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Concrete Strength Guide</h2>
        <div class="space-y-2">
          {["2500 psi — light residential (sidewalks, patios)","3000 psi — standard residential (slabs, driveways)","3500 psi — moderate commercial (foundations)","4000 psi — heavy duty (bridges, industrial floors)","Higher PSI = stronger but higher cement ratio","Fiber reinforcement reduces cracking without rebar"].map(s => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{s}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Cubic Yards","Calculate concrete volume and bags needed for any project")

# ── COOKING ───────────────────────────────────────────────────────────────────
w("cooking","Cooking Measurement Converter","Other","other",
  "Cooking Measurement Converter: Cups, Tbsp, Tsp, ml, oz",
  "Convert cooking measurements: cups, tablespoons, teaspoons, milliliters, fluid ounces, pints, quarts. Free cooking converter.",
  """
  const value = parseFloat(inputs.value)||0
  const from = inputs.from||"cups"
  const to = inputs.to||"tablespoons"
  const toMl = {
    cups:236.588, tablespoons:14.787, teaspoons:4.929, milliliters:1,
    liters:1000, fluidoz:29.574, pints:473.176, quarts:946.353, gallons:3785.41,
    tablespoons_dry:14.787, cups_dry:236.588
  }
  if(!toMl[from]||!toMl[to]) throw new Error("Unknown unit.")
  const ml=value*toMl[from]
  const result=ml/toMl[to]
  const breakdown=[value+" "+from+" = "+result.toFixed(4)+" "+to,"In ml: "+ml.toFixed(4)+"ml"]
  const allUnits=["cups","tablespoons","teaspoons","fluidoz","pints","quarts","milliliters"]
  allUnits.forEach(u=>{if(u!==from)breakdown.push(value+" "+from+" = "+(ml/toMl[u]).toFixed(4)+" "+u)})
  return {
    value:result.toFixed(4)+" "+to,
    gaugeValue:Math.min(ml/1000*100,100),
    breakdown,
    stats:[
      {label:"Result in "+to,value:result.toFixed(4)},
      {label:"In mL",value:ml.toFixed(2)},
      {label:"In cups",value:(ml/toMl.cups).toFixed(4)},
      {label:"In tablespoons",value:(ml/toMl.tablespoons).toFixed(2)},
    ]
  }
""",
  """{id:"value",label:"Amount",type:"number",placeholder:"1",min:0,step:0.001,defaultValue:1},
            {id:"from",label:"From",type:"select",options:[
              {value:"cups",label:"Cups"},
              {value:"tablespoons",label:"Tablespoons"},
              {value:"teaspoons",label:"Teaspoons"},
              {value:"milliliters",label:"Milliliters (ml)"},
              {value:"liters",label:"Liters"},
              {value:"fluidoz",label:"Fluid ounces (fl oz)"},
              {value:"pints",label:"Pints"},
              {value:"quarts",label:"Quarts"},
              {value:"gallons",label:"Gallons"},
            ],defaultValue:"cups"},
            {id:"to",label:"To",type:"select",options:[
              {value:"tablespoons",label:"Tablespoons"},
              {value:"teaspoons",label:"Teaspoons"},
              {value:"cups",label:"Cups"},
              {value:"milliliters",label:"Milliliters (ml)"},
              {value:"liters",label:"Liters"},
              {value:"fluidoz",label:"Fluid ounces (fl oz)"},
              {value:"pints",label:"Pints"},
              {value:"quarts",label:"Quarts"},
            ],defaultValue:"tablespoons"}""",
  [("< 1 cup","#22c55e",0,25),("1-4 cups","#3b82f6",25,50),("4+ cups","#f59e0b",50,100)],
  "% of 1 liter","100",
  [("How many tablespoons are in a cup?","1 cup = 16 tablespoons = 48 teaspoons = 8 fluid ounces = 236.6 ml. A tablespoon is 3 teaspoons = 14.8 ml. Half a cup = 8 tablespoons. Quarter cup = 4 tablespoons. These are US measurements — UK tablespoon = 15ml (vs 14.8ml US)."),
   ("How do I convert cups to grams?","Cups to grams depends on the ingredient density. 1 cup of water = 236g. 1 cup of flour = ~120-130g (all-purpose, sifted). 1 cup of sugar = ~200g (granulated). 1 cup of butter = ~227g. For precise baking, use a kitchen scale — volume measurements for dry ingredients are not as accurate as weight."),
   ("What is the difference between US and metric measurements?","US: cups (8 fl oz), tablespoons (0.5 fl oz), teaspoons (1/6 fl oz). Metric: milliliters (ml), liters. UK uses imperial measurements but tablespoon = 15ml vs US 14.8ml. Australia uses 20ml tablespoon. When following international recipes, note which system is used."),
   ("How do I scale a recipe up or down?","Multiply all ingredient quantities by the scaling factor. To double: multiply by 2. To halve: multiply by 0.5. For leavening agents (baking powder, soda) and salt, start with 75% of the scaled amount as they do not always scale linearly. Cooking time may also change when scaling pans."),
   ("What are the dry vs liquid measuring cups?","Liquid measuring cups have a spout and are measured to the top markings (meniscus at the line). Dry measuring cups are filled to the brim and leveled off. Using liquid cups for dry ingredients (or vice versa) causes inaccuracies. For best baking results, use a scale for dry ingredients.")],
  [("Unit Converter","/calculators/unit-converter-calculator"),("BMI Calculator","/calculators/bmi-calculator"),("Calorie Calculator","/calculators/calorie-calculator"),("TDEE Calculator","/calculators/tdee-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Quick Reference</h3>
          <div class="text-xs text-blue-800 font-mono space-y-1">
            <div>1 cup = 16 tbsp = 48 tsp</div>
            <div>1 cup = 8 fl oz = 236.6 ml</div>
            <div>1 tablespoon = 3 teaspoons</div>
            <div>1 tablespoon = 14.8 ml</div>
            <div>1 pint = 2 cups = 473 ml</div>
            <div>1 quart = 4 cups = 946 ml</div>
            <div>1 gallon = 16 cups = 3.785 L</div>
          </div>
        </div>""",
  """    <div class="mt-10">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Cooking Conversion Table</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Measurement</th><th class="p-2 text-xs text-right">Cups</th><th class="p-2 text-xs text-right">Tbsp</th><th class="p-2 text-xs text-right">Tsp</th><th class="p-2 text-xs text-right">ml</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["1 gallon","16","256","768","3,785"],["1 quart","4","64","192","946"],["1 pint","2","32","96","473"],["1 cup","1","16","48","237"],["½ cup","0.5","8","24","118"],["¼ cup","0.25","4","12","59"],["1 tablespoon","1/16","1","3","15"],["1 teaspoon","1/48","⅓","1","5"]].map(r => (
              <tr><td class="p-2 text-xs font-medium">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td><td class="p-2 text-xs text-right">{r[3]}</td><td class="p-2 text-xs text-right">{r[4]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "Result","Convert cooking measurements between cups, tablespoons, ml, and more")

# ── DAYS UNTIL ───────────────────────────────────────────────────────────────
w("days-until","Days Until Calculator","Other","other",
  "Days Until Calculator: Countdown Days to Any Date",
  "Calculate days until any event or date. Count business days, weeks, and months to deadlines, holidays, or special events. Free days until calculator.",
  """
  const targetDate = inputs.targetDate||""
  const mode = inputs.mode||"calendar"
  if(!targetDate) throw new Error("Enter a target date.")
  const target = new Date(targetDate+"T00:00:00")
  const today = new Date(); today.setHours(0,0,0,0)
  if(isNaN(target.getTime())) throw new Error("Invalid date format.")
  const diffMs = target-today
  const diffDays = Math.ceil(diffMs/(1000*60*60*24))
  const absDays = Math.abs(diffDays)
  const weeks = Math.floor(absDays/7)
  const remDays = absDays%7
  const months = Math.floor(absDays/30.44)
  const isPast = diffDays<0
  const label = isPast?"days since (past)":"days until"
  let businessDays=0
  const step=isPast?-1:1
  let d=new Date(today)
  for(let i=0;i<absDays;i++){
    d.setDate(d.getDate()+step)
    const dow=d.getDay()
    if(dow!==0&&dow!==6) businessDays++
  }
  return {
    value:absDays+" "+label+" "+targetDate,
    gaugeValue:Math.min(absDays/365*100,100),
    breakdown:[(isPast?"Past: "+absDays+" days ago":"Future: "+absDays+" days away"),"Business days: "+businessDays,"Weeks: "+weeks+" weeks + "+remDays+" days","Months (approx): "+months,"Date: "+target.toDateString()],
    stats:[
      {label:"Calendar Days",value:absDays+(isPast?" (past)":" (future)")},
      {label:"Business Days",value:String(businessDays)},
      {label:"Weeks + Days",value:weeks+"w "+remDays+"d"},
      {label:"Months (approx)",value:String(months)},
    ]
  }
""",
  """{id:"targetDate",label:"Target date",type:"date",defaultValue:"2025-12-25"},
            {id:"mode",label:"Count type",type:"select",options:[
              {value:"calendar",label:"Calendar days"},
              {value:"business",label:"Business days only"},
            ],defaultValue:"calendar"}""",
  [("< 1 week","#22c55e",0,2),("1-4 weeks","#3b82f6",2,11),("1-3 months","#f59e0b",11,25),("3+ months","#ef4444",25,100)],
  "days","365",
  [("How do I count days between two dates?","Subtract the earlier date from the later date in milliseconds, then divide by 86,400,000 (ms per day). In most spreadsheets (Excel, Google Sheets), simply subtract two date cells: =B1-A1 and format as a number. This calculator does that automatically, including business day calculation."),
   ("How many business days are there per month?","On average, 21-22 business days per month (Monday-Friday, excluding weekends). A standard work year has 260-261 business days (before holidays). A month with exactly 4 weeks has 20 business days. Many months have 22, and some 23. This calculator counts exact business days to your target date."),
   ("What are the biggest upcoming holidays?","Major US holidays: New Year (Jan 1), Martin Luther King Jr Day (3rd Mon in Jan), Presidents Day (3rd Mon in Feb), Memorial Day (last Mon in May), Independence Day (Jul 4), Labor Day (1st Mon in Sep), Thanksgiving (4th Thu in Nov), Christmas (Dec 25). This calculator counts all calendar days — subtract your holidays for net business days."),
   ("How do I calculate a project deadline?","Add business days to the start date. For agile sprints: count 10 business days (2 weeks) forward. For legal deadlines: use calendar days unless the rule specifies business days. For contracts: watch for terms like working days, business days, or calendar days as they lead to very different dates."),
   ("What is a Julian Day Number?","The Julian Day Number (JDN) is a continuous count of days from January 1, 4713 BC (Julian calendar). Jan 1, 2000 = JDN 2,451,545. Astronomers use it for date arithmetic across calendar systems. Modern Modified Julian Date (MJD) = JDN - 2,400,000.5, starting Nov 17, 1858.")],
  [("Age Calculator","/calculators/age-calculator"),("Date Calculator","/calculators/date-calculator"),("Retirement Calculator","/calculators/retirement-calculator"),("Days Until Calculator","/calculators/days-until-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Common Countdowns</h3>
          <div class="text-xs text-blue-800 space-y-1">
            <div>New Year Jan 1</div>
            <div>Valentine Feb 14</div>
            <div>Easter (varies)</div>
            <div>Independence Day Jul 4</div>
            <div>Halloween Oct 31</div>
            <div>Thanksgiving 4th Thu Nov</div>
            <div>Christmas Dec 25</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Time Units Reference</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Unit</th><th class="p-2 text-xs font-semibold text-right">Days</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["1 week","7"],["2 weeks","14"],["1 month (avg)","30.44"],["1 quarter","91"],["1 year","365"],["1 leap year","366"],["Business days/year","~261"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-medium">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Project Planning Tips</h2>
        <div class="space-y-2">
          {["Always add buffer — projects take ~1.5x longer than estimated","Convert deadline to calendar days, then subtract weekends and holidays","Agile sprints: 2 weeks = 10 business days","Legal deadlines: check if days means calendar or business days","Month-end deadlines: watch Feb 28/29 — not all months have 30 or 31 days","Daylight Saving Time changes can affect 24-hour countdowns"].map(t => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{t}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Days","Calculate how many days until or since any date")

# ── ELECTRICITY ───────────────────────────────────────────────────────────────
w("electricity","Electricity Cost Calculator","Other","other",
  "Electricity Cost Calculator: kWh Usage & Electric Bill",
  "Calculate electricity cost for any appliance or monthly bill. Find kWh usage, annual cost, and savings. Free electricity calculator.",
  """
  const watts = parseFloat(inputs.watts)||0
  const hours = parseFloat(inputs.hours)||0
  const days = parseFloat(inputs.days)||30
  const rate = parseFloat(inputs.rate)||0.13
  if(watts<=0) throw new Error("Enter wattage (watts).")
  if(hours<=0) throw new Error("Enter hours per day.")
  const kwh = watts/1000*hours*days
  const cost = kwh*rate
  const dailyKwh = watts/1000*hours
  const dailyCost = dailyKwh*rate
  const annualKwh = dailyKwh*365
  const annualCost = annualKwh*rate
  return {
    value:"$"+cost.toFixed(2)+" for "+days+" days",
    gaugeValue:Math.min(cost/100*100,100),
    breakdown:["Wattage: "+watts+"W","Hours per day: "+hours,"Days: "+days,"kWh used: "+kwh.toFixed(3),"Rate: $"+rate+"/kWh","Total cost: $"+cost.toFixed(2),"Daily cost: $"+dailyCost.toFixed(3),"Annual kWh: "+annualKwh.toFixed(0),"Annual cost: $"+annualCost.toFixed(2)],
    stats:[
      {label:"Total Cost",value:"$"+cost.toFixed(2)},
      {label:"Daily Cost",value:"$"+dailyCost.toFixed(3)},
      {label:"kWh Used",value:kwh.toFixed(2)},
      {label:"Annual Cost",value:"$"+annualCost.toFixed(2)},
    ]
  }
""",
  """{id:"watts",label:"Appliance wattage (W)",type:"number",placeholder:"1500",min:0,step:1,defaultValue:1500},
            {id:"hours",label:"Hours used per day",type:"number",placeholder:"8",min:0,step:0.5,defaultValue:8},
            {id:"days",label:"Number of days",type:"number",placeholder:"30",min:1,step:1,defaultValue:30},
            {id:"rate",label:"Electricity rate ($/kWh)",type:"number",placeholder:"0.13",min:0,step:0.001,defaultValue:0.13}""",
  [("Low cost (<$10)","#22c55e",0,10),("Moderate ($10-50)","#f59e0b",10,50),("High ($50+)","#ef4444",50,100)],
  "$ cost","100",
  [("How do I calculate electricity cost?","Cost = Watts / 1000 x Hours x Days x Rate ($/kWh). Example: 1500W heater running 8 hours/day for 30 days at $0.13/kWh: 1.5 x 8 x 30 x 0.13 = $46.80. Most utility bills show rate per kWh (kilowatt-hour). The US average is about $0.12-0.16/kWh."),
   ("How many watts does a typical house use?","Average US home: 10,500 kWh/year = 875 kWh/month ≈ 1,200W average. High-draw appliances: electric water heater (4,000W), dryer (5,000W), HVAC (3,500-7,000W), electric oven (2,000-5,000W). Low-draw: LED bulbs (8-12W), laptop (45-100W), phone charger (5-20W)."),
   ("What is a kilowatt-hour (kWh)?","1 kWh = 1,000 watts used for 1 hour. A 100W bulb running 10 hours uses 1 kWh. A 1,000W microwave running 1 hour uses 1 kWh. Your utility charges by the kWh. US average electricity price: ~$0.13/kWh. California: ~$0.25/kWh. Hawaii: ~$0.40/kWh."),
   ("How can I reduce my electricity bill?","Replace incandescent bulbs with LEDs (75% less energy). Unplug vampire loads (devices on standby draw power). Use a programmable thermostat. Wash clothes in cold water. Air dry dishes. Use Energy Star appliances. Seal windows and doors to improve HVAC efficiency."),
   ("What is a smart meter?","A smart meter records electricity usage in 30-minute intervals and sends data wirelessly to the utility. Benefits: accurate bills (no estimation), time-of-use pricing awareness, and real-time monitoring via apps. Time-of-use rates charge more during peak hours (evenings) — shifting usage to off-peak can save significantly.")],
  [("Fuel Cost Calculator","/calculators/fuel-cost-calculator"),("Savings Calculator","/calculators/savings-calculator"),("Unit Converter","/calculators/unit-converter-calculator"),("Budget Calculator","/calculators/budget-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Common Wattages</h3>
          <div class="text-xs text-blue-800 space-y-1">
            {[["LED bulb","8-12W"],["Laptop","45-100W"],["TV (LED 55in)","80-150W"],["Refrigerator","150-400W"],["Dishwasher","1,200-2,400W"],["Dryer","4,000-5,800W"],["AC (window)","500-1,440W"],["Water heater","3,500-5,500W"]].map(([a,w]) => (
              <div class="flex justify-between border-b border-blue-100 pb-0.5"><span>{a}</span><span class="font-mono">{w}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Annual Cost Estimates (US avg rate)</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Appliance</th><th class="p-2 text-xs font-semibold text-right">Annual Cost</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Refrigerator (run 24/7)","~$65"],["Electric water heater","~$580"],["HVAC (avg use)","~$600-900"],["Washer + Dryer","~$150"],["TV (4h/day)","~$20-45"],["Lighting (whole home)","~$100-300"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-medium">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Energy Saving Tips</h2>
        <div class="space-y-2">
          {["LED bulbs: 75% less energy than incandescent","Smart thermostat: saves $50-100/year on HVAC","Cold wash: 90% of washer energy is heating water","Unplug chargers: idle draw adds up over a year","Seal air leaks: HVAC is the biggest energy user","Solar panels: can cut electric bills by 50-90%"].map(t => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-green-500 mt-0.5">•</span><span>{t}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Cost","Calculate electricity cost for any appliance or device")

# ── FUEL COST ─────────────────────────────────────────────────────────────────
w("fuel-cost","Fuel Cost Calculator","Other","other",
  "Fuel Cost Calculator: Gas Cost per Mile & Trip",
  "Calculate fuel cost for any trip or monthly driving. Find cost per mile, annual gas spending, and savings from more efficient vehicles. Free fuel cost calculator.",
  """
  const miles = parseFloat(inputs.miles)||0
  const mpg = parseFloat(inputs.mpg)||0
  const gasPrice = parseFloat(inputs.gasPrice)||0
  const daysPerYear = parseFloat(inputs.daysPerYear)||365
  if(miles<=0) throw new Error("Enter miles driven.")
  if(mpg<=0) throw new Error("Enter fuel efficiency (MPG).")
  if(gasPrice<=0) throw new Error("Enter gas price per gallon.")
  const gallons = miles/mpg
  const cost = gallons*gasPrice
  const costPerMile = cost/miles
  const annualMiles = miles*(365/daysPerYear)
  const annualCost = annualMiles/mpg*gasPrice
  return {
    value:"$"+cost.toFixed(2)+" for "+miles+" miles",
    gaugeValue:Math.min(cost/100*100,100),
    breakdown:["Miles: "+miles,"MPG: "+mpg,"Gas price: $"+gasPrice+"/gal","Gallons needed: "+gallons.toFixed(3),"Total cost: $"+cost.toFixed(2),"Cost per mile: $"+costPerMile.toFixed(4),"Annual miles (extrapolated): "+annualMiles.toFixed(0),"Annual fuel cost: $"+annualCost.toFixed(2)],
    stats:[
      {label:"Trip Fuel Cost",value:"$"+cost.toFixed(2)},
      {label:"Cost Per Mile",value:"$"+costPerMile.toFixed(4)},
      {label:"Gallons Used",value:gallons.toFixed(3)},
      {label:"Annual Fuel Cost",value:"$"+annualCost.toFixed(2)},
    ]
  }
""",
  """{id:"miles",label:"Miles to drive",type:"number",placeholder:"100",min:0,step:1,defaultValue:100},
            {id:"mpg",label:"Fuel efficiency (MPG)",type:"number",placeholder:"30",min:0,step:0.5,defaultValue:30},
            {id:"gasPrice",label:"Gas price ($/gallon)",type:"number",placeholder:"3.50",min:0,step:0.01,defaultValue:3.50},
            {id:"daysPerYear",label:"This trip happens every N days (for annual estimate)",type:"number",placeholder:"1",min:1,step:1,defaultValue:1}""",
  [("Low cost (<$20)","#22c55e",0,20),("Moderate ($20-60)","#3b82f6",20,60),("High ($60+)","#ef4444",60,100)],
  "$ cost","100",
  [("How do I calculate fuel cost for a road trip?","Fuel cost = (miles / MPG) × gas price per gallon. A 500-mile trip in a 30 MPG car at $3.50/gallon: (500/30) × 3.50 = 16.67 gallons × $3.50 = $58.33. Always add 10-15% for detours, idling, and AC use which can reduce real-world MPG by 5-25%."),
   ("What is the average MPG for cars in the USA?","The average new car in 2024 gets about 26-28 MPG combined. Compact sedans: 35-45 MPG. SUVs/trucks: 18-25 MPG. Hybrid cars: 40-60 MPG. Plug-in hybrids: 50-100 MPGe. Electric vehicles: 100-140 MPGe. Older vehicles from 2000-2010 average 20-25 MPG."),
   ("How much does driving cost per mile?","Total cost per mile includes: fuel (~$0.10-0.20/mile at avg MPG and gas prices), plus depreciation, insurance, maintenance, tires, and registration (typically $0.20-0.40/mile additional). The IRS standard mileage rate for 2024 is $0.67/mile for business use, reflecting total average driving costs."),
   ("How much can I save with a more fuel-efficient car?","Savings per year = annual miles × gas price × (1/old MPG - 1/new MPG). Trading from 20 MPG to 35 MPG, driving 15,000 miles/year at $3.50/gas: 15,000 × 3.50 × (1/20 - 1/35) = 15,000 × 3.50 × 0.0214 = $1,125/year savings."),
   ("Does driving speed affect fuel economy?","Yes significantly. Most cars peak efficiency at 45-55 mph. Above 55 mph, aerodynamic drag increases rapidly: fuel economy drops about 7-14% for every 5 mph over 50 mph. At 70 mph, most cars use 15-25% more fuel than at 55 mph. Highway speed limits of 65-70 mph significantly impact real-world fuel costs.")],
  [("Electricity Cost Calculator","/calculators/electricity-calculator"),("Auto Loan Calculator","/calculators/auto-loan-calculator"),("Budget Calculator","/calculators/budget-calculator"),("Savings Calculator","/calculators/savings-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">MPG Reference</h3>
          <div class="text-xs text-blue-800 space-y-1">
            {[["Compact sedan","35-45 MPG"],["Midsize sedan","28-35 MPG"],["SUV / Crossover","22-30 MPG"],["Pickup truck","15-22 MPG"],["Hybrid car","40-55 MPG"],["Electric (MPGe)","100-140 MPGe"]].map(([v,m]) => (
              <div class="flex justify-between border-b border-blue-100 pb-0.5"><span>{v}</span><span class="font-mono">{m}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Annual Fuel Cost by MPG</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">MPG</th><th class="p-2 text-xs font-semibold text-right">15,000 mi/yr @ $3.50</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[[15,"$3,500"],[20,"$2,625"],[25,"$2,100"],[30,"$1,750"],[35,"$1,500"],[45,"$1,167"],[55,"$954"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]} MPG</td><td class="p-2 text-xs text-right font-medium">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Factors Affecting Real MPG</h2>
        <div class="space-y-2">
          {["Highway vs city driving (highway is more efficient)","AC use: reduces MPG by 5-25% in hot climates","Speed: drops significantly above 55 mph","Cold weather: reduces MPG by 15-24% in winter","Tire pressure: under-inflated reduces MPG by 0.5%/psi","Cargo weight: 100 lbs extra = 1% MPG reduction"].map(f => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{f}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Fuel Cost","Calculate gas cost for any trip or annual driving")

print(f"\nWritten: {written} pages")
