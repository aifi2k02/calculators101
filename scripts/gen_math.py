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

# ── TRIANGLE ──────────────────────────────────────────────────────────────────
w("triangle","Triangle Calculator","Math","math",
  "Triangle Calculator: Area, Perimeter, Angles & Sides",
  "Calculate triangle area, perimeter, all angles and sides from any 3 inputs (SSS, SAS, ASA, AAS). Free triangle calculator.",
  """
  const a = parseFloat(inputs.a)||0
  const b = parseFloat(inputs.b)||0
  const c = parseFloat(inputs.c)||0
  const angleA = parseFloat(inputs.angleA)||0
  if(a>0&&b>0&&c>0){
    const s=(a+b+c)/2
    const area=Math.sqrt(s*(s-a)*(s-b)*(s-c))
    const cosA=(b*b+c*c-a*a)/(2*b*c)
    const A=Math.acos(cosA)*180/Math.PI
    const B=Math.acos((a*a+c*c-b*b)/(2*a*c))*180/Math.PI
    const C=180-A-B
    return {
      value:"Area: "+area.toFixed(4),
      gaugeValue:Math.min(area/1000*100,100),
      breakdown:["Sides: a="+a+", b="+b+", c="+c,"Perimeter: "+(a+b+c).toFixed(4),"Area: "+area.toFixed(4),"Angle A: "+A.toFixed(2)+"deg","Angle B: "+B.toFixed(2)+"deg","Angle C: "+C.toFixed(2)+"deg"],
      stats:[
        {label:"Area",value:area.toFixed(4)},
        {label:"Perimeter",value:(a+b+c).toFixed(4)},
        {label:"Angle A",value:A.toFixed(2)+"°"},
        {label:"Angle C",value:C.toFixed(2)+"°"},
      ]
    }
  } else if(a>0&&b>0&&angleA>0){
    const A=angleA*Math.PI/180
    const sinB=b*Math.sin(A)/a
    const B=Math.asin(sinB)*180/Math.PI
    const C=180-angleA-B
    const c=a*Math.sin(C*Math.PI/180)/Math.sin(A)
    const area=0.5*a*b*Math.sin(C*Math.PI/180)
    return {
      value:"Area: "+area.toFixed(4),
      gaugeValue:Math.min(area/1000*100,100),
      breakdown:["Using SSA: a="+a+", b="+b+", A="+angleA+"deg","c: "+c.toFixed(4),"Angle B: "+B.toFixed(2)+"deg","Angle C: "+C.toFixed(2)+"deg","Area: "+area.toFixed(4)],
      stats:[{label:"Side c",value:c.toFixed(4)},{label:"Angle B",value:B.toFixed(2)+"°"},{label:"Angle C",value:C.toFixed(2)+"°"},{label:"Area",value:area.toFixed(4)}]
    }
  }
  throw new Error("Enter all 3 sides (SSS) or 2 sides + 1 angle (SSA).")
""",
  """{id:"a",label:"Side a",type:"number",placeholder:"3",min:0,step:0.001,defaultValue:3},
            {id:"b",label:"Side b",type:"number",placeholder:"4",min:0,step:0.001,defaultValue:4},
            {id:"c",label:"Side c (or 0 to use angle below)",type:"number",placeholder:"5",min:0,step:0.001,defaultValue:5},
            {id:"angleA",label:"Angle A in degrees (optional if all 3 sides known)",type:"number",placeholder:"0",min:0,max:180,step:0.01,defaultValue:0}""",
  [("Small area","#3b82f6",0,10),("Medium","#22c55e",10,50),("Large","#f59e0b",50,100)],
  "area (of 1000)","100",
  [("What is the Pythagorean theorem?","For right triangles: a^2 + b^2 = c^2, where c is the hypotenuse (longest side, opposite the right angle). If a=3, b=4, then c = sqrt(9+16) = sqrt(25) = 5. This is the most famous equation in geometry and is used throughout engineering and architecture."),
   ("How do I find the area of a triangle?","Three methods: (1) Base x Height / 2 (if you know base and perpendicular height). (2) Heron formula: s=(a+b+c)/2, Area=sqrt(s(s-a)(s-b)(s-c)) (if you know all 3 sides). (3) (1/2) x a x b x sin(C) (if you know 2 sides and included angle)."),
   ("What are SSS, SAS, ASA, AAS, and SSA?","These are ways to specify a triangle: SSS=three sides, SAS=two sides and included angle, ASA=two angles and included side, AAS=two angles and non-included side, SSA=two sides and non-included angle (may have ambiguous case). All except SSA uniquely determine a triangle."),
   ("What are the types of triangles?","By sides: Equilateral (all 3 sides equal), Isosceles (2 sides equal), Scalene (no sides equal). By angles: Acute (all angles < 90deg), Right (one angle = 90deg), Obtuse (one angle > 90deg). An equilateral triangle is always acute. A right triangle can be scalene or isosceles."),
   ("What is the law of cosines?","c^2 = a^2 + b^2 - 2ab*cos(C). It generalizes the Pythagorean theorem to any triangle. When angle C = 90deg, cos(C) = 0 and it reduces to c^2 = a^2 + b^2. Use it when you know SSS or SAS and need to find unknown sides or angles.")],
  [("Area Calculator","/calculators/area-calculator"),("Angle Converter","/calculators/angle-converter-calculator"),("Law of Cosines Calculator","/calculators/law-of-cosines-calculator"),("Distance Calculator","/calculators/distance-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Triangle Formulas</h3>
          <div class="text-xs text-blue-800 font-mono space-y-1">
            <div>Area = b x h / 2</div>
            <div>Area = sqrt(s(s-a)(s-b)(s-c))</div>
            <div>Perimeter = a + b + c</div>
            <div>a^2 + b^2 = c^2 (right triangle)</div>
            <div>A + B + C = 180 degrees</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Common Triangle Types</h2>
        <div class="space-y-2">
          {[
            {t:"Equilateral",d:"All 3 sides equal, all angles = 60 degrees. Most symmetric triangle."},
            {t:"Isosceles",d:"Two sides equal, two base angles equal. Many architectural forms."},
            {t:"Right Triangle",d:"One 90-degree angle. Pythagorean theorem applies. Foundation of trigonometry."},
            {t:"Scalene",d:"No sides equal, no angles equal. Most triangles in nature are scalene."},
          ].map(t => (
            <div class="bg-gray-50 rounded-lg p-3"><div class="font-semibold text-xs text-blue-700">{t.t}</div><div class="text-xs text-gray-600">{t.d}</div></div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Pythagorean Triples</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">a</th><th class="p-2 text-xs font-semibold text-right">b</th><th class="p-2 text-xs font-semibold text-right">c (hypotenuse)</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[[3,4,5],[5,12,13],[8,15,17],[7,24,25],[20,21,29]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right font-medium">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "Area","Calculate triangle area, angles, and perimeter from any combination of inputs")

# ── VOLUME ────────────────────────────────────────────────────────────────────
w("volume","Volume Calculator","Math","math",
  "Volume Calculator: Cube, Sphere, Cylinder & More",
  "Calculate volume of any 3D shape: cube, sphere, cylinder, cone, pyramid, rectangular prism. Free volume calculator.",
  """
  const shape = inputs.shape||"cube"
  const a = parseFloat(inputs.a)||0
  const b = parseFloat(inputs.b)||0
  const c = parseFloat(inputs.c)||0
  let volume, surfaceArea, formula
  if(shape==="cube"){
    if(a<=0) throw new Error("Enter side length.")
    volume=a*a*a; surfaceArea=6*a*a; formula="V = s^3"
  } else if(shape==="box"){
    if(a<=0||b<=0||c<=0) throw new Error("Enter all dimensions.")
    volume=a*b*c; surfaceArea=2*(a*b+b*c+a*c); formula="V = l x w x h"
  } else if(shape==="sphere"){
    if(a<=0) throw new Error("Enter radius.")
    volume=(4/3)*Math.PI*a*a*a; surfaceArea=4*Math.PI*a*a; formula="V = 4/3 pi r^3"
  } else if(shape==="cylinder"){
    if(a<=0||b<=0) throw new Error("Enter radius and height.")
    volume=Math.PI*a*a*b; surfaceArea=2*Math.PI*a*(a+b); formula="V = pi r^2 h"
  } else if(shape==="cone"){
    if(a<=0||b<=0) throw new Error("Enter radius and height.")
    const slant=Math.sqrt(a*a+b*b)
    volume=(1/3)*Math.PI*a*a*b; surfaceArea=Math.PI*a*(a+slant); formula="V = 1/3 pi r^2 h"
  } else if(shape==="pyramid"){
    if(a<=0||b<=0||c<=0) throw new Error("Enter base length, base width, and height.")
    volume=(1/3)*a*b*c; surfaceArea=a*b+a*Math.sqrt((b/2)*(b/2)+c*c)+b*Math.sqrt((a/2)*(a/2)+c*c); formula="V = 1/3 l x w x h"
  } else throw new Error("Unknown shape")
  return {
    value:volume.toFixed(4)+" cubic units",
    gaugeValue:Math.min(volume/1000*100,100),
    breakdown:["Shape: "+shape,"Formula: "+formula,"Volume: "+volume.toFixed(4)+" cubic units","Surface area: "+surfaceArea.toFixed(4)+" sq units"],
    stats:[
      {label:"Volume",value:volume.toFixed(4)},
      {label:"Surface Area",value:surfaceArea.toFixed(4)},
      {label:"Shape",value:shape.charAt(0).toUpperCase()+shape.slice(1)},
      {label:"Formula",value:formula},
    ]
  }
""",
  """{id:"shape",label:"3D Shape",type:"select",options:[
              {value:"cube",label:"Cube"},
              {value:"box",label:"Rectangular Box"},
              {value:"sphere",label:"Sphere"},
              {value:"cylinder",label:"Cylinder"},
              {value:"cone",label:"Cone"},
              {value:"pyramid",label:"Square Pyramid"},
            ],defaultValue:"cylinder"},
            {id:"a",label:"Dimension A (side / radius / length)",type:"number",placeholder:"5",min:0,step:0.001,defaultValue:5},
            {id:"b",label:"Dimension B (width / height)",type:"number",placeholder:"10",min:0,step:0.001,defaultValue:10},
            {id:"c",label:"Dimension C (height for box/pyramid)",type:"number",placeholder:"3",min:0,step:0.001,defaultValue:3}""",
  [("Small","#3b82f6",0,10),("Medium","#22c55e",10,50),("Large","#f59e0b",50,100)],
  "vol (of 1000)","100",
  [("What is the volume formula for a cylinder?","V = pi x r^2 x h. A cylinder with radius 5 and height 10 has volume = pi x 25 x 10 = 785.4 cubic units. The base area is pi x r^2 (a circle), and you multiply by height."),
   ("What is the volume formula for a sphere?","V = (4/3) x pi x r^3. A sphere with radius 3: V = (4/3) x pi x 27 = 113.1 cubic units. Surface area = 4 x pi x r^2."),
   ("How does a cone volume compare to a cylinder?","A cone has exactly 1/3 the volume of a cylinder with the same base and height. V_cone = (1/3) x pi x r^2 x h. This is a useful fact: it takes 3 cone-fulls to fill a cylinder."),
   ("How do I convert cubic units?","1 cubic foot = 1,728 cubic inches. 1 cubic yard = 27 cubic feet. 1 cubic meter = 1,000 liters. 1 gallon = 231 cubic inches = 3.785 liters. 1 liter = 1,000 milliliters = 1,000 cubic centimeters."),
   ("What is the volume of a rectangular box?","V = length x width x height. A box 10 x 5 x 3 = 150 cubic units. Surface area = 2(lw + lh + wh). A cube is a special box where all sides are equal: V = s^3.")],
  [("Area Calculator","/calculators/area-calculator"),("Triangle Calculator","/calculators/triangle-calculator"),("Circle Calculator","/calculators/circle-calculator"),("Unit Converter","/calculators/unit-converter-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Volume Formulas</h3>
          <div class="text-xs text-blue-800 font-mono space-y-1">
            <div>Cube: V = s^3</div>
            <div>Box: V = l x w x h</div>
            <div>Sphere: V = 4/3 pi r^3</div>
            <div>Cylinder: V = pi r^2 h</div>
            <div>Cone: V = 1/3 pi r^2 h</div>
            <div>Pyramid: V = 1/3 l x w x h</div>
          </div>
        </div>""",
  """    <div class="mt-10">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Common Volume Conversions</h2>
      <div class="grid md:grid-cols-2 gap-4">
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Unit</th><th class="p-2 text-xs font-semibold text-right">Equivalent</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["1 cubic foot","1,728 cu in"],["1 cubic yard","27 cu ft"],["1 liter","1,000 mL"],["1 cubic meter","1,000 liters"],["1 gallon","3.785 liters"],["1 fl oz","29.57 mL"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
        <div class="bg-gray-50 rounded-xl p-4">
          <h3 class="font-bold text-sm text-gray-800 mb-3">Volume Key Facts</h3>
          <div class="text-xs text-gray-600 space-y-2">
            <div>A cone holds 1/3 the volume of the same-sized cylinder</div>
            <div>A sphere has 2/3 the volume of its circumscribed cylinder</div>
            <div>Doubling radius quadruples circle area but cubes sphere volume</div>
          </div>
        </div>
      </div>
    </div>""",
  "Volume","Calculate volume and surface area of any 3D shape")

# ── COMBINATION ───────────────────────────────────────────────────────────────
w("combination","Combination Calculator","Math","math",
  "Combination Calculator: nCr Combinations & Permutations",
  "Calculate combinations nCr and permutations nPr. Find all possible selections from a set. Free combination calculator.",
  """
  const n = parseInt(inputs.n)||0
  const r = parseInt(inputs.r)||0
  if(n<0||r<0) throw new Error("n and r must be non-negative.")
  if(r>n) throw new Error("r cannot be greater than n.")
  if(n>20) throw new Error("n must be 20 or less to prevent overflow.")
  const factorial = x => {
    if(x<=1) return 1
    let result=1
    for(let i=2;i<=x;i++) result*=i
    return result
  }
  const nCr = factorial(n)/(factorial(r)*factorial(n-r))
  const nPr = factorial(n)/factorial(n-r)
  return {
    value:"C("+n+","+r+") = "+nCr.toLocaleString(),
    gaugeValue:Math.min(nCr/1000*100,100),
    breakdown:["n = "+n+" items","r = "+r+" chosen","Combinations C("+n+","+r+") = "+nCr.toLocaleString(),"Permutations P("+n+","+r+") = "+nPr.toLocaleString(),"Ratio nPr/nCr = r! = "+factorial(r)],
    stats:[
      {label:"Combinations (nCr)",value:nCr.toLocaleString()},
      {label:"Permutations (nPr)",value:nPr.toLocaleString()},
      {label:"n",value:String(n)},
      {label:"r",value:String(r)},
    ]
  }
""",
  """{id:"n",label:"Total items (n)",type:"number",placeholder:"10",min:0,max:20,defaultValue:10},
            {id:"r",label:"Items chosen (r)",type:"number",placeholder:"3",min:0,max:20,defaultValue:3}""",
  [("Small (<100)","#22c55e",0,10),("Medium (100-1000)","#3b82f6",10,100),("Large (1000+)","#f59e0b",100,100)],
  "combinations","100",
  [("What is a combination?","A combination C(n,r) counts ways to choose r items from n items where ORDER DOES NOT MATTER. Choosing 3 people from 10 for a committee: C(10,3) = 10!/(3! x 7!) = 120 ways. If you chose Alice, Bob, Carol — that is the same as Carol, Bob, Alice in combinations."),
   ("What is a permutation?","A permutation P(n,r) counts ways to arrange r items from n where ORDER MATTERS. Choosing a president, VP, and treasurer from 10 people: P(10,3) = 720. Here, Alice-Bob-Carol and Carol-Bob-Alice are DIFFERENT arrangements. Permutations = Combinations x r!"),
   ("What is the difference between combinations and permutations?","Combinations: order does not matter (choosing committee members, lottery numbers). Permutations: order matters (ranking, passwords, assigned roles). P(n,r) = n!/(n-r)!. C(n,r) = n!/(r! x (n-r)!). Permutations are always >= combinations (for same n and r)."),
   ("How do I calculate combinations on a calculator?","On a scientific calculator: enter n, press nCr button, enter r, press =. On iPhone calculator (landscape): look for Cr. Most graphing calculators have MATH > PRB menu. In Excel: COMBIN(n,r). In Python: math.comb(n,r) or scipy.special.comb(n,r)."),
   ("What is the probability of winning a lottery?","Lottery (pick 6 from 49): C(49,6) = 13,983,816. Probability of winning = 1 in 13,983,816 (about 0.0000071%). Powerball (pick 5 from 69 + 1 from 26): C(69,5) x 26 = 292,201,338. Probability = 1 in 292 million. Combinations make these astronomical numbers precise.")],
  [("Factorial Calculator","/calculators/factorial-calculator"),("Probability Calculator","/calculators/percentage-calculator"),("Z-Score Calculator","/calculators/z-score-calculator"),("Average Calculator","/calculators/average-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Formulas</h3>
          <div class="text-xs text-blue-800 font-mono space-y-2">
            <div>C(n,r) = n! / (r! x (n-r)!)</div>
            <div>P(n,r) = n! / (n-r)!</div>
            <div class="mt-2 font-sans">nCr = nPr / r!</div>
          </div>
          <div class="text-xs text-blue-700 mt-3">C = Combinations (order does NOT matter)<br/>P = Permutations (order MATTERS)</div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Common Combination Values</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">C(n,r)</th><th class="p-2 text-xs font-semibold text-right">Result</th><th class="p-2 text-xs font-semibold text-right">Example</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["C(4,2)","6","Choose 2 from 4"],["C(6,2)","15","Pairs from 6"],["C(10,3)","120","3 from 10"],["C(13,5)","1,287","Poker hand"],["C(49,6)","13,983,816","Lottery 6/49"]].map(r => (
              <tr><td class="p-2 text-xs font-mono">{r[0]}</td><td class="p-2 text-xs text-right font-medium">{r[1]}</td><td class="p-2 text-xs text-right text-gray-500">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Real-World Applications</h2>
        <div class="space-y-2">
          {["Lottery — how many combinations of numbers exist","Poker — how many possible 5-card hands from 52 cards = C(52,5) = 2,598,960","Committee selection — pick 5 members from 20 candidates","Drug trials — choose which patients receive treatment","Sports brackets — matchup possibilities","Password security — combinations of characters in a password"].map(t => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{t}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Combinations","Calculate combinations nCr and permutations nPr")

# ── QUADRATIC ─────────────────────────────────────────────────────────────────
w("quadratic","Quadratic Formula Calculator","Math","math",
  "Quadratic Formula Calculator: Solve ax^2 + bx + c = 0",
  "Solve any quadratic equation using the quadratic formula. Find real and complex roots with full step-by-step solution. Free quadratic calculator.",
  """
  const a = parseFloat(inputs.a)||0
  const b = parseFloat(inputs.b)||0
  const c = parseFloat(inputs.c)||0
  if(a===0) throw new Error("a cannot be 0 (would not be quadratic).")
  const discriminant = b*b-4*a*c
  if(discriminant>0){
    const x1=(-b+Math.sqrt(discriminant))/(2*a)
    const x2=(-b-Math.sqrt(discriminant))/(2*a)
    return {
      value:"x = "+x1.toFixed(4)+" or "+x2.toFixed(4),
      gaugeValue:50,
      breakdown:["Equation: "+a+"x^2 + "+b+"x + "+c+" = 0","Discriminant: "+discriminant+" > 0 (2 real roots)","x1 = "+x1.toFixed(6),"x2 = "+x2.toFixed(6),"Vertex: ("+(-b/(2*a)).toFixed(4)+", "+(c-b*b/(4*a)).toFixed(4)+")"],
      stats:[
        {label:"Root x1",value:x1.toFixed(4)},
        {label:"Root x2",value:x2.toFixed(4)},
        {label:"Discriminant",value:discriminant.toFixed(4)},
        {label:"Vertex x",value:(-b/(2*a)).toFixed(4)},
      ]
    }
  } else if(discriminant===0){
    const x=-b/(2*a)
    return {
      value:"x = "+x.toFixed(4)+" (double root)",
      gaugeValue:50,
      breakdown:["Discriminant: 0 (one repeated root)","x = "+x.toFixed(6),"Vertex: ("+x.toFixed(4)+", 0)"],
      stats:[{label:"Root",value:x.toFixed(4)},{label:"Root type",value:"Double (repeated)"},{label:"Discriminant",value:"0"},{label:"Vertex x",value:x.toFixed(4)}]
    }
  } else {
    const realPart=-b/(2*a)
    const imagPart=Math.sqrt(-discriminant)/(2*a)
    return {
      value:"Complex roots: "+realPart.toFixed(3)+" ± "+imagPart.toFixed(3)+"i",
      gaugeValue:50,
      breakdown:["Discriminant: "+discriminant+" < 0 (complex roots)","x1 = "+realPart.toFixed(4)+" + "+imagPart.toFixed(4)+"i","x2 = "+realPart.toFixed(4)+" - "+imagPart.toFixed(4)+"i","No real solutions"],
      stats:[{label:"Real Part",value:realPart.toFixed(4)},{label:"Imaginary Part",value:"±"+imagPart.toFixed(4)+"i"},{label:"Discriminant",value:discriminant.toFixed(0)},{label:"Root Type",value:"Complex"}]
    }
  }
""",
  """{id:"a",label:"Coefficient a (ax²)",type:"number",placeholder:"1",step:0.001,defaultValue:1},
            {id:"b",label:"Coefficient b (bx)",type:"number",placeholder:"-5",step:0.001,defaultValue:-5},
            {id:"c",label:"Coefficient c (constant)",type:"number",placeholder:"6",step:0.001,defaultValue:6}""",
  [("Real roots","#22c55e",40,60),("Complex roots","#ef4444",0,40),("Complex roots","#ef4444",60,100)],
  "root type","100",
  [("What is the quadratic formula?","For ax^2 + bx + c = 0: x = (-b ± sqrt(b^2 - 4ac)) / (2a). The discriminant b^2 - 4ac determines the type of roots: positive = two distinct real roots; zero = one repeated real root; negative = two complex conjugate roots."),
   ("What is the discriminant?","The discriminant is b^2 - 4ac. If > 0: two distinct real roots (parabola crosses x-axis twice). If = 0: one repeated real root (parabola is tangent to x-axis). If < 0: no real roots, two complex conjugate roots (parabola does not cross x-axis)."),
   ("How do I factor a quadratic equation?","To factor x^2 - 5x + 6 = 0: find two numbers that multiply to c (6) and add to b (-5). Those are -2 and -3: (x-2)(x-3) = 0, so x = 2 or x = 3. When factoring is difficult, use the quadratic formula — it always works."),
   ("What is the vertex of a parabola?","The vertex is the minimum or maximum point of the parabola y = ax^2 + bx + c. Vertex x = -b/(2a). Vertex y = c - b^2/(4a). If a > 0, it is a minimum (parabola opens up). If a < 0, it is a maximum (parabola opens down)."),
   ("Can I solve a quadratic by completing the square?","Yes. For x^2 + bx + c = 0: (1) Move c: x^2 + bx = -c. (2) Add (b/2)^2 to both sides: x^2 + bx + (b/2)^2 = -c + (b/2)^2. (3) Factor left side: (x + b/2)^2 = discriminant/4. (4) Solve: x = -b/2 ± sqrt(discriminant/2). This is essentially how the quadratic formula is derived.")],
  [("Fraction Calculator","/calculators/fraction-calculator"),("Average Calculator","/calculators/average-calculator"),("Percentage Calculator","/calculators/percentage-calculator"),("Z-Score Calculator","/calculators/z-score-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Quadratic Formula</h3>
          <div class="text-center text-blue-800 font-mono text-sm bg-blue-100 rounded p-3 mb-2">x = (-b ± sqrt(b²-4ac)) / 2a</div>
          <div class="text-xs text-blue-700 space-y-1">
            <div>D &gt; 0: Two real roots</div>
            <div>D = 0: One repeated root</div>
            <div>D &lt; 0: Complex roots (no real solution)</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Solution Methods</h2>
        <div class="space-y-3">
          {[
            {m:"Factoring",w:"When?",d:"When you can find two integers that multiply to c and add to b. Fastest when it works."},
            {m:"Quadratic Formula",w:"Always works",d:"x = (-b ± sqrt(b^2-4ac)) / 2a. Use when factoring is difficult or discriminant is negative."},
            {m:"Completing the Square",w:"For understanding",d:"Algebraic technique that derives the quadratic formula. Useful for conic sections."},
            {m:"Graphing",w:"Approximate",d:"Find where parabola crosses x-axis. Accurate if using a graphing calculator."},
          ].map(s => (
            <div class="bg-gray-50 rounded-lg p-3"><div class="font-semibold text-xs text-blue-700">{s.m} <span class="text-gray-500">({s.w})</span></div><div class="text-xs text-gray-600">{s.d}</div></div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Real-World Applications</h2>
        <div class="space-y-2">
          {["Projectile motion: h = -16t^2 + v0t + h0 (find when ball hits ground)","Profit optimization: P = -x^2 + 50x - 200 (find max profit)","Area problems: find dimensions from area constraints","Physics: kinematics equations with constant acceleration","Engineering: beam deflection, stress calculations","Finance: break-even analysis with quadratic cost curves"].map(a => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{a}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Roots","Solve quadratic equations with the quadratic formula")

# ── RATIO ────────────────────────────────────────────────────────────────────
w("ratio","Ratio Calculator","Math","math",
  "Ratio Calculator: Simplify, Scale & Solve Ratios",
  "Simplify ratios, scale ratios, and solve ratio problems. Find missing values in proportions. Free ratio calculator.",
  """
  const a = parseFloat(inputs.a)||0
  const b = parseFloat(inputs.b)||0
  const scale = parseFloat(inputs.scale)||1
  if(a<=0||b<=0) throw new Error("Enter both ratio values.")
  const gcd = (x,y) => y===0?x:gcd(y,x%y)
  const g = gcd(Math.round(a),Math.round(b))
  const simplA = a/g, simplB = b/g
  const percentage = (a/(a+b))*100
  const scaledA = a*scale, scaledB = b*scale
  const asDecimal = a/b
  const asPct = percentage
  return {
    value:simplA.toFixed(0)+":"+simplB.toFixed(0)+" (simplified)",
    gaugeValue:percentage,
    breakdown:["Ratio: "+a+":"+b,"Simplified: "+simplA.toFixed(0)+":"+simplB.toFixed(0),"As decimal: "+asDecimal.toFixed(4),"As fraction: "+a+"/"+b+" = "+asDecimal.toFixed(4),"A as % of total: "+percentage.toFixed(2)+"%","Scaled x"+scale+": "+scaledA.toFixed(2)+":"+scaledB.toFixed(2)],
    stats:[
      {label:"Simplified Ratio",value:simplA.toFixed(0)+":"+simplB.toFixed(0)},
      {label:"A : Total",value:percentage.toFixed(2)+"%"},
      {label:"As Decimal",value:asDecimal.toFixed(4)},
      {label:"Scaled x"+scale,value:scaledA.toFixed(2)+":"+scaledB.toFixed(2)},
    ]
  }
""",
  """{id:"a",label:"First value (A)",type:"number",placeholder:"3",min:0,step:0.001,defaultValue:3},
            {id:"b",label:"Second value (B)",type:"number",placeholder:"4",min:0,step:0.001,defaultValue:4},
            {id:"scale",label:"Scale factor",type:"number",placeholder:"1",min:0,step:0.1,defaultValue:1}""",
  [("A much smaller","#3b82f6",0,25),("Balanced","#22c55e",40,60),("A much larger","#ef4444",75,100)],
  "% A of total","100",
  [("How do I simplify a ratio?","Divide both sides by the GCD (Greatest Common Divisor). For 12:8: GCD(12,8) = 4. Simplified: 3:2. You can also convert to fractions and simplify: 12/8 = 3/2, ratio 3:2."),
   ("How do I solve a proportion?","If a:b = c:d, then ad = bc (cross multiplication). Solve for the unknown: if 3:5 = x:20, then 5x = 60, x = 12. Or use equivalent fractions: 3/5 = x/20, x = 3 x 20/5 = 12."),
   ("What is a 1:2 ratio in practical terms?","A 1:2 ratio means for every 1 unit of A, there are 2 units of B. Total is 3 parts: A is 1/3 (33.3%), B is 2/3 (66.7%). In cooking: 1:2 water to flour means 1 cup water per 2 cups flour."),
   ("How do ratios relate to percentages?","In a ratio a:b, a is a/(a+b) x 100% of the total, and b is b/(a+b) x 100%. For ratio 3:1: a = 75%, b = 25%. Percentages and ratios are interchangeable — 75% = 3:1, 50% = 1:1."),
   ("What are common aspect ratios?","Screen/TV: 16:9 (widescreen HD), 4:3 (older TVs), 21:9 (ultrawide cinema). Photography: 3:2 (35mm film/DSLR), 4:3 (compact cameras), 1:1 (square). Architecture: golden ratio 1:1.618 (phi). Maps: scales like 1:100,000 (1cm = 1km).")],
  [("Fraction Calculator","/calculators/fraction-calculator"),("Percentage Calculator","/calculators/percentage-calculator"),("GCD LCM Calculator","/calculators/lcm-gcd-calculator"),("Unit Converter","/calculators/unit-converter-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Common Ratios</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[["1:1","50% : 50%"],["1:2","33% : 67%"],["3:1","75% : 25%"],["16:9","64% : 36% (HD)"],["1:1.618","61.8% : 38.2% (Golden)"]].map(([r,p]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span class="font-mono">{r}</span><span>{p}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Proportion Examples</h2>
      <div class="grid md:grid-cols-2 gap-6">
        <div class="bg-gray-50 rounded-xl p-4">
          <h3 class="font-bold text-sm text-gray-800 mb-3">Solving Proportions</h3>
          <div class="text-xs text-gray-600 space-y-2">
            <div>If 5 apples cost $3, how much do 12 apples cost?</div>
            <div class="font-mono text-blue-700">5/3 = 12/x → x = 12 x 3/5 = $7.20</div>
          </div>
        </div>
        <div class="bg-gray-50 rounded-xl p-4">
          <h3 class="font-bold text-sm text-gray-800 mb-3">Splitting by Ratio</h3>
          <div class="text-xs text-gray-600 space-y-2">
            <div>Split $240 in ratio 3:5 between A and B:</div>
            <div class="font-mono text-blue-700">Total parts = 8, each part = $30</div>
            <div class="font-mono text-blue-700">A = 3 x $30 = $90, B = 5 x $30 = $150</div>
          </div>
        </div>
      </div>
    </div>""",
  "Ratio","Simplify ratios, solve proportions, and scale ratio values")

# ── Z-SCORE ───────────────────────────────────────────────────────────────────
w("z-score","Z-Score Calculator","Math","math",
  "Z-Score Calculator: Standard Score & Percentile",
  "Calculate z-score (standard score) and find the corresponding percentile rank. Convert between z-scores and probabilities. Free z-score calculator.",
  """
  const value = parseFloat(inputs.value)||0
  const mean = parseFloat(inputs.mean)||0
  const stdDev = parseFloat(inputs.stdDev)||1
  if(stdDev<=0) throw new Error("Standard deviation must be positive.")
  const z = (value-mean)/stdDev
  const erf = x => {
    const a1=0.254829592,a2=-0.284496736,a3=1.421413741,a4=-1.453152027,a5=1.061405429,p=0.3275911
    const sign=x<0?-1:1
    const t=1/(1+p*Math.abs(x))
    return sign*(1-(a1*t+a2*t*t+a3*Math.pow(t,3)+a4*Math.pow(t,4)+a5*Math.pow(t,5))*Math.exp(-x*x))
  }
  const percentile = (1+erf(z/Math.sqrt(2)))/2*100
  const pctBelow = percentile
  const pctAbove = 100-percentile
  return {
    value:"z = "+z.toFixed(4),
    gaugeValue:Math.min(Math.max(percentile,0),100),
    breakdown:["Value: "+value,"Mean: "+mean,"Std Dev: "+stdDev,"z-score: "+z.toFixed(4),"Percentile: "+percentile.toFixed(2)+"%","Above: "+pctAbove.toFixed(2)+"% of data","Below: "+pctBelow.toFixed(2)+"% of data"],
    stats:[
      {label:"Z-Score",value:z.toFixed(4)},
      {label:"Percentile",value:percentile.toFixed(2)+"%"},
      {label:"% Below",value:pctBelow.toFixed(2)+"%"},
      {label:"% Above",value:pctAbove.toFixed(2)+"%"},
    ]
  }
""",
  """{id:"value",label:"Value (x)",type:"number",placeholder:"75",step:0.001,defaultValue:75},
            {id:"mean",label:"Mean (average)",type:"number",placeholder:"70",step:0.001,defaultValue:70},
            {id:"stdDev",label:"Standard Deviation",type:"number",placeholder:"10",min:0.001,step:0.001,defaultValue:10}""",
  [("Very low (<5%)","#ef4444",0,5),("Below avg (5-40%)","#f59e0b",5,40),("Average (40-60%)","#3b82f6",40,60),("Above avg (60%+)","#22c55e",60,100)],
  "% percentile","100",
  [("What is a z-score?","A z-score (standard score) measures how many standard deviations a value is from the mean. z = (x - mean) / standard_deviation. A z-score of 0 means exactly at the mean. z = +1 means 1 standard deviation above mean. z = -2 means 2 standard deviations below mean."),
   ("What percentile is a z-score of 1.65?","z = 1.65 corresponds to approximately the 95th percentile. Common z-score to percentile conversions: z=0 → 50th, z=1 → 84th, z=1.28 → 90th, z=1.65 → 95th, z=2 → 97.7th, z=2.33 → 99th, z=3 → 99.87th."),
   ("What is the empirical rule (68-95-99.7)?","For normal distributions: 68% of data falls within 1 standard deviation of mean; 95% within 2 standard deviations; 99.7% within 3 standard deviations. A z-score beyond ±3 is very unusual — less than 0.3% of data in a normal distribution."),
   ("How do I use z-scores to compare different distributions?","Z-scores standardize data across different scales. Example: a student scored 85 on math (mean=75, SD=8) and 76 on English (mean=70, SD=5). Math z = 1.25, English z = 1.2. Despite lower absolute English score, performance is very similar relative to peers."),
   ("What is the difference between z-score and t-score?","Both measure standard deviations from the mean. Z-score: used when population mean and standard deviation are known. T-score: used when estimating from a sample (more common in practice). T-distributions have heavier tails than normal and adjust for small samples. For large samples (n > 30), t and z are nearly identical.")],
  [("Average Calculator","/calculators/average-calculator"),("Percentage Calculator","/calculators/percentage-calculator"),("Combination Calculator","/calculators/combination-calculator"),("Grade Calculator","/calculators/grade-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Z-Score to Percentile</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700 border-b border-blue-200"><th class="text-left pb-1">z-score</th><th class="text-right pb-1">Percentile</th></tr></thead>
            <tbody class="text-blue-900">
              {[["-2.0","2.3%"],["-1.0","15.9%"],["0","50%"],["+1.0","84.1%"],["+1.65","95%"],["+2.0","97.7%"],["+3.0","99.87%"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5 font-mono">{r[0]}</td><td class="text-right">{r[1]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">The Empirical Rule (Normal Distribution)</h2>
        <div class="space-y-3">
          {[
            {range:"Within 1 SD (z = -1 to +1)",pct:"68.3% of data"},
            {range:"Within 2 SD (z = -2 to +2)",pct:"95.4% of data"},
            {range:"Within 3 SD (z = -3 to +3)",pct:"99.7% of data"},
            {range:"Beyond 3 SD",pct:"Only 0.3% of data — very unusual"},
          ].map(e => (
            <div class="flex justify-between bg-gray-50 rounded-lg px-3 py-2 text-xs">
              <span class="text-gray-700">{e.range}</span>
              <span class="font-medium text-blue-700">{e.pct}</span>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Z-Score Applications</h2>
        <div class="space-y-2">
          {["Standardized testing — compare scores across different tests","Identifying outliers in datasets (|z| > 2 or 3 is suspect)","Quality control — products outside 3 sigma are defective","Medical tests — compare patient values to reference ranges","Finance — z-scores used in Altman Z-Score for bankruptcy prediction","Sports analytics — compare player performance across leagues"].map(a => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{a}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Z-Score","Calculate z-score, percentile, and probability from any normal distribution")

print(f"\nWritten: {written} pages (triangle, volume, combination, quadratic, ratio, z-score)")
