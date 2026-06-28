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

# ── BINARY ────────────────────────────────────────────────────────────────────
w("binary","Binary Calculator","Math","math",
  "Binary Calculator: Convert & Calculate Binary, Decimal, Hex",
  "Convert between binary, decimal, hexadecimal, and octal. Perform binary addition, subtraction, AND, OR, XOR operations. Free binary calculator.",
  """
  const value = inputs.value||"0"
  const fromBase = inputs.fromBase||"decimal"
  const toBase = inputs.toBase||"binary"
  let decimal
  if(fromBase==="decimal") decimal=parseInt(value)||0
  else if(fromBase==="binary") decimal=parseInt(value,2)
  else if(fromBase==="hex") decimal=parseInt(value,16)
  else if(fromBase==="octal") decimal=parseInt(value,8)
  else throw new Error("Unknown base.")
  if(isNaN(decimal)||decimal<0) throw new Error("Enter a valid non-negative integer.")
  let result
  if(toBase==="binary") result=decimal.toString(2)
  else if(toBase==="decimal") result=decimal.toString(10)
  else if(toBase==="hex") result=decimal.toString(16).toUpperCase()
  else if(toBase==="octal") result=decimal.toString(8)
  else throw new Error("Unknown target base.")
  return {
    value:result+" ("+toBase+")",
    gaugeValue:Math.min(decimal/255*100,100),
    breakdown:["Input: "+value+" ("+fromBase+")","Decimal value: "+decimal,"Binary: "+decimal.toString(2),"Octal: "+decimal.toString(8),"Decimal: "+decimal.toString(10),"Hexadecimal: "+decimal.toString(16).toUpperCase(),"Result in "+toBase+": "+result],
    stats:[
      {label:"Result ("+toBase+")",value:result},
      {label:"Binary",value:decimal.toString(2)},
      {label:"Decimal",value:String(decimal)},
      {label:"Hexadecimal",value:decimal.toString(16).toUpperCase()},
    ]
  }
""",
  """{id:"value",label:"Number to convert",type:"text",placeholder:"255",defaultValue:"255"},
            {id:"fromBase",label:"Input base (from)",type:"select",options:[
              {value:"decimal",label:"Decimal (base 10)"},
              {value:"binary",label:"Binary (base 2)"},
              {value:"hex",label:"Hexadecimal (base 16)"},
              {value:"octal",label:"Octal (base 8)"},
            ],defaultValue:"decimal"},
            {id:"toBase",label:"Output base (to)",type:"select",options:[
              {value:"binary",label:"Binary (base 2)"},
              {value:"decimal",label:"Decimal (base 10)"},
              {value:"hex",label:"Hexadecimal (base 16)"},
              {value:"octal",label:"Octal (base 8)"},
            ],defaultValue:"binary"}""",
  [("Small (0-63)","#22c55e",0,25),("Medium (64-127)","#3b82f6",25,50),("Large (128-191)","#f59e0b",50,75),("Very large (192+)","#ef4444",75,100)],
  "% of 255","100",
  [("How do I convert decimal to binary?","Divide by 2 repeatedly, writing down the remainders from bottom to top. Example: 13 ÷ 2 = 6 R1, 6 ÷ 2 = 3 R0, 3 ÷ 2 = 1 R1, 1 ÷ 2 = 0 R1. Reading remainders bottom-up: 1101. Verify: 8+4+0+1 = 13. Each bit represents a power of 2: 2^3+2^2+2^0 = 8+4+1 = 13."),
   ("What is hexadecimal and why is it used?","Hexadecimal (base 16) uses digits 0-9 and A-F. One hex digit represents exactly 4 binary bits (a nibble), and two hex digits = 1 byte (8 bits). So FF hex = 11111111 binary = 255 decimal. Hex is compact: the 24-bit color #FF6B35 is much shorter than its 24-digit binary equivalent."),
   ("How do I count in binary?","Binary uses only 0 and 1. Counting: 0, 1, 10, 11, 100, 101, 110, 111, 1000... Each position is a power of 2. To read binary 1010: 1x8 + 0x4 + 1x2 + 0x1 = 10. With n bits you can represent 0 to 2^n - 1: 8 bits = 0-255, 16 bits = 0-65535, 32 bits = 0-4,294,967,295."),
   ("What are AND, OR, XOR operations?","These are bitwise operations on binary numbers. AND (both must be 1): 1010 AND 1100 = 1000. OR (either can be 1): 1010 OR 1100 = 1110. XOR (exactly one must be 1): 1010 XOR 1100 = 0110. NOT (flip all bits): NOT 1010 = 0101. Used in programming for bit manipulation, flags, and masks."),
   ("What is two complement representation?","Two complement is how computers store negative integers. To negate: flip all bits and add 1. Example: 5 = 00000101, -5 = 11111010 + 1 = 11111011. Benefits: addition works the same way for positive and negative. 8-bit two complement: range is -128 to +127.")],
  [("Number Base Calculator","/calculators/number-base-calculator"),("Modulo Calculator","/calculators/modulo-calculator"),("Scientific Notation","/calculators/scientific-notation-calculator"),("Average Calculator","/calculators/average-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Quick Conversions</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700"><th class="text-left">Dec</th><th>Bin</th><th>Hex</th><th class="text-right">Oct</th></tr></thead>
            <tbody class="font-mono text-blue-900">
              {[[0,"0000","0","0"],[1,"0001","1","1"],[10,"1010","A","12"],[15,"1111","F","17"],[16,"10000","10","20"],[255,"11111111","FF","377"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-center">{r[1]}</td><td class="text-center">{r[2]}</td><td class="text-right">{r[3]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Binary Place Values</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Bit position</th><th class="p-2 text-xs font-semibold text-right">Power of 2</th><th class="p-2 text-xs font-semibold text-right">Value</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[[0,1],[1,2],[2,4],[3,8],[4,16],[5,32],[6,64],[7,128]].map(r => (
              <tr><td class="p-2 text-xs">Bit {r[0]} (2^{r[0]})</td><td class="p-2 text-xs text-right font-mono">2^{r[0]}</td><td class="p-2 text-xs text-right font-medium">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Real-World Uses</h2>
        <div class="space-y-2">
          {["IP addresses — 32-bit binary (IPv4), 128-bit (IPv6)","Colors — #RRGGBB hex = 3 bytes = 24 bits","ASCII codes — each character is 7 bits (0-127)","File permissions — rwxrwxrwx = 9 bits","Bitmasks — toggle features with AND/OR/XOR","Unicode — up to 21 bits per character (UTF-8)"].map(u => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{u}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Result","Convert between binary, decimal, hex, and octal number systems")

# ── CIRCLE ────────────────────────────────────────────────────────────────────
w("circle","Circle Calculator","Math","math",
  "Circle Calculator: Area, Circumference, Diameter, Radius",
  "Calculate circle area, circumference, diameter, and radius from any single measurement. Free circle calculator with formulas.",
  """
  const inputType = inputs.inputType||"radius"
  const value = parseFloat(inputs.value)||0
  if(value<=0) throw new Error("Enter a positive measurement.")
  let r
  if(inputType==="radius") r=value
  else if(inputType==="diameter") r=value/2
  else if(inputType==="circumference") r=value/(2*Math.PI)
  else if(inputType==="area") r=Math.sqrt(value/Math.PI)
  else throw new Error("Unknown input type.")
  const diameter=2*r
  const circumference=2*Math.PI*r
  const area=Math.PI*r*r
  return {
    value:"Area: "+area.toFixed(4)+" | Circumference: "+circumference.toFixed(4),
    gaugeValue:Math.min(r/100*100,100),
    breakdown:["Radius: "+r.toFixed(6),"Diameter: "+diameter.toFixed(6),"Circumference: "+circumference.toFixed(6),"Area: "+area.toFixed(6),"Sector: 360 deg total"],
    stats:[
      {label:"Radius",value:r.toFixed(4)},
      {label:"Diameter",value:diameter.toFixed(4)},
      {label:"Circumference",value:circumference.toFixed(4)},
      {label:"Area",value:area.toFixed(4)},
    ]
  }
""",
  """{id:"inputType",label:"Known measurement",type:"select",options:[
              {value:"radius",label:"Radius (r)"},
              {value:"diameter",label:"Diameter (d)"},
              {value:"circumference",label:"Circumference (C)"},
              {value:"area",label:"Area (A)"},
            ],defaultValue:"radius"},
            {id:"value",label:"Value",type:"number",placeholder:"5",min:0,step:0.0001,defaultValue:5}""",
  [("Small (r<10)","#22c55e",0,10),("Medium (r 10-50)","#3b82f6",10,50),("Large (r 50+)","#f59e0b",50,100)],
  "radius","100",
  [("What are the circle formulas?","For a circle with radius r: Area = pi x r^2. Circumference = 2 x pi x r = pi x d. Diameter = 2r. If you know any one measurement, you can find all others. Pi (pi) ≈ 3.14159265358979."),
   ("How do I find the area of a circle from the circumference?","First find radius: r = C / (2 x pi). Then area = pi x r^2. Shortcut: Area = C^2 / (4 x pi). Example: circumference = 31.416, area = (31.416)^2 / (4 x pi) ≈ 78.54 square units."),
   ("What is the difference between circumference and perimeter?","Circumference is specifically the perimeter (boundary length) of a circle. Perimeter is the general term for the boundary length of any 2D shape. All circles have circumference; other shapes have perimeter. C = 2 x pi x r = pi x d."),
   ("What is pi (pi) and why is it important?","Pi (pi) ≈ 3.14159265... is the ratio of any circle circumference to its diameter: C/d = pi. It is irrational (never ending decimal) and transcendental (cannot be expressed as a root of a polynomial). Pi appears in countless formulas beyond circles: sphere volumes, wave equations, Fourier transforms, and probability."),
   ("What is the area of a semicircle?","Area of semicircle = (pi x r^2) / 2. The straight edge has length 2r. Perimeter = pi x r + 2r = r(pi + 2). For a quarter circle: Area = (pi x r^2) / 4. For a sector with angle theta (degrees): Area = (theta/360) x pi x r^2.")],
  [("Area Calculator","/calculators/area-calculator"),("Triangle Calculator","/calculators/triangle-calculator"),("Volume Calculator","/calculators/volume-calculator"),("Distance Calculator","/calculators/distance-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Circle Formulas</h3>
          <div class="text-xs text-blue-800 font-mono space-y-1">
            <div>Area = π × r²</div>
            <div>Circumference = 2πr = πd</div>
            <div>Diameter = 2r</div>
            <div>r = C / (2π)</div>
            <div>r = √(A / π)</div>
            <div>π ≈ 3.14159265...</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Circle Parts</h2>
        <div class="space-y-2">
          {[
            {t:"Radius",d:"Distance from center to edge (r). Half the diameter."},
            {t:"Diameter",d:"Longest chord through center (d = 2r). Width of the circle."},
            {t:"Circumference",d:"Perimeter of the circle (C = 2πr). Distance around the edge."},
            {t:"Area",d:"Space inside the circle (A = πr²). Measured in square units."},
            {t:"Chord",d:"Any line segment connecting two points on the circle. Diameter is the longest chord."},
            {t:"Sector",d:"Pie-slice shaped region. Area = (θ/360) × πr²."},
          ].map(p => (
            <div class="bg-gray-50 rounded-lg p-2"><div class="font-semibold text-xs text-blue-700">{p.t}</div><div class="text-xs text-gray-600">{p.d}</div></div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Common Circles</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Radius</th><th class="p-2 text-xs font-semibold text-right">Area</th><th class="p-2 text-xs font-semibold text-right">Circumference</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[[1,"3.14","6.28"],[5,"78.54","31.42"],[10,"314.16","62.83"],[12,"452.39","75.40"],[100,"31,415.93","628.32"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "Area","Calculate all circle measurements from any single input")

# ── EXPONENT ─────────────────────────────────────────────────────────────────
w("exponent","Exponent Calculator","Math","math",
  "Exponent Calculator: Powers, Roots, Nth Powers",
  "Calculate any exponent or power: a^b, square roots, cube roots, fractional exponents. Free exponent calculator with steps.",
  """
  const base = parseFloat(inputs.base)
  const exp = parseFloat(inputs.exp)
  if(isNaN(base)||isNaN(exp)) throw new Error("Enter base and exponent.")
  const result=Math.pow(base,exp)
  if(!isFinite(result)) throw new Error("Result is too large or undefined.")
  const sqRoot=base>0?Math.sqrt(base):NaN
  const cubeRoot=Math.cbrt(base)
  return {
    value:base+"^"+exp+" = "+result,
    gaugeValue:Math.min(Math.abs(result)/1000000*100,100),
    breakdown:[base+"^"+exp+" = "+result,"Square root of base: "+(base>0?sqRoot.toFixed(6):"undefined (negative)"),"Cube root of base: "+cubeRoot.toFixed(6),"log base: "+(base>0?Math.log(base).toFixed(4):"N/A"),"Result in sci notation: "+result.toExponential(4)],
    stats:[
      {label:"Result",value:result.toLocaleString(undefined,{maximumFractionDigits:6})},
      {label:"Scientific Notation",value:result.toExponential(4)},
      {label:"Square Root of Base",value:base>0?sqRoot.toFixed(6):"N/A"},
      {label:"Cube Root of Base",value:cubeRoot.toFixed(6)},
    ]
  }
""",
  """{id:"base",label:"Base (a)",type:"number",placeholder:"2",step:0.001,defaultValue:2},
            {id:"exp",label:"Exponent (n)",type:"number",placeholder:"10",step:0.001,defaultValue:10}""",
  [("Small result","#22c55e",0,10),("Medium result","#3b82f6",10,50),("Large result","#f59e0b",50,100)],
  "% of million","100",
  [("What is an exponent?","An exponent (power) says how many times to multiply the base by itself. 2^3 = 2 x 2 x 2 = 8. The base is the number being multiplied, the exponent is how many times. Notation: a^n, a^n, or pow(a,n). Special cases: a^0 = 1, a^1 = a, a^-1 = 1/a."),
   ("What are negative exponents?","a^(-n) = 1/a^n. Example: 2^(-3) = 1/2^3 = 1/8 = 0.125. Negative exponents represent fractions/reciprocals. 10^(-3) = 0.001 (milli-). In scientific notation: 1.5 x 10^(-6) = 0.0000015 (1.5 microseconds)."),
   ("What are fractional exponents?","a^(1/2) = sqrt(a). a^(1/3) = cube root of a. a^(m/n) = nth root of a^m = (nth root of a)^m. Examples: 9^(1/2) = 3, 8^(1/3) = 2, 16^(3/4) = (16^(1/4))^3 = 2^3 = 8. Fractional exponents connect powers and roots."),
   ("What are the exponent rules?","Product: a^m x a^n = a^(m+n). Quotient: a^m / a^n = a^(m-n). Power of power: (a^m)^n = a^(mn). Power of product: (ab)^n = a^n x b^n. Zero exponent: a^0 = 1 (for a ≠ 0). Negative: a^(-n) = 1/a^n."),
   ("What does it mean to square or cube a number?","Squaring a number means raising it to the power 2: n^2 = n x n. The result is the area of a square with side n. Cubing means n^3 = n x n x n — the volume of a cube with side n. Perfect squares: 1,4,9,16,25,36... Perfect cubes: 1,8,27,64,125...")],
  [("Logarithm Calculator","/calculators/logarithm-calculator"),("Scientific Notation","/calculators/scientific-notation-calculator"),("Square Root Calculator","/calculators/square-root-calculator"),("Average Calculator","/calculators/average-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Exponent Rules</h3>
          <div class="text-xs text-blue-800 font-mono space-y-1">
            <div>a^m × a^n = a^(m+n)</div>
            <div>a^m ÷ a^n = a^(m−n)</div>
            <div>(a^m)^n = a^(mn)</div>
            <div>a^0 = 1</div>
            <div>a^(-n) = 1/a^n</div>
            <div>a^(1/n) = nth root of a</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Powers of 2</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">n</th><th class="p-2 text-xs font-semibold text-right">2^n</th><th class="p-2 text-xs font-semibold text-right">Meaning</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[[0,1,"1"],[1,2,"2"],[8,256,"1 byte"],[10,1024,"1 KB"],[20,"1,048,576","1 MB"],[30,"1,073,741,824","1 GB"],[32,"4,294,967,296","32-bit max"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-mono">{r[1]}</td><td class="p-2 text-xs text-right text-gray-500">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Common Powers</h2>
        <div class="space-y-2">
          {["Perfect squares: 1,4,9,16,25,36,49,64,81,100","Perfect cubes: 1,8,27,64,125,216,343","e^1 = 2.71828... (Euler number)","10^6 = 1 million, 10^9 = 1 billion","2^10 ≈ 10^3 (handy approximation for memory)","phi^2 = phi + 1 where phi = golden ratio"].map(p => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{p}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Result","Calculate any exponent or power with step-by-step breakdown")

# ── LAW OF COSINES ───────────────────────────────────────────────────────────
w("law-of-cosines","Law of Cosines Calculator","Math","math",
  "Law of Cosines Calculator: Solve Any Triangle",
  "Use the law of cosines to solve any triangle. Find side lengths and angles from SSS or SAS configurations. Free law of cosines calculator.",
  """
  const a = parseFloat(inputs.a)||0
  const b = parseFloat(inputs.b)||0
  const c = parseFloat(inputs.c)||0
  const angleC = parseFloat(inputs.angleC)||0
  if(a>0&&b>0&&angleC>0){
    const C=angleC*Math.PI/180
    const cSide=Math.sqrt(a*a+b*b-2*a*b*Math.cos(C))
    const cosA=(b*b+cSide*cSide-a*a)/(2*b*cSide)
    const A=Math.acos(cosA)*180/Math.PI
    const B=180-angleC-A
    const area=0.5*a*b*Math.sin(C)
    return {
      value:"c = "+cSide.toFixed(4),
      gaugeValue:Math.min(cSide/100*100,100),
      breakdown:["Given: a="+a+", b="+b+", C="+angleC+"deg","c = sqrt(a^2+b^2-2ab*cos(C)) = "+cSide.toFixed(4),"Angle A = "+A.toFixed(4)+"deg","Angle B = "+B.toFixed(4)+"deg","Area = "+area.toFixed(4)],
      stats:[
        {label:"Side c",value:cSide.toFixed(4)},
        {label:"Angle A",value:A.toFixed(4)+"°"},
        {label:"Angle B",value:B.toFixed(4)+"°"},
        {label:"Area",value:area.toFixed(4)},
      ]
    }
  } else if(a>0&&b>0&&c>0){
    const cosC=(a*a+b*b-c*c)/(2*a*b)
    if(Math.abs(cosC)>1) throw new Error("Invalid triangle: these sides do not form a triangle.")
    const C=Math.acos(cosC)*180/Math.PI
    const cosA=(b*b+c*c-a*a)/(2*b*c)
    const A=Math.acos(cosA)*180/Math.PI
    const B=180-C-A
    const s=(a+b+c)/2
    const area=Math.sqrt(s*(s-a)*(s-b)*(s-c))
    return {
      value:"C = "+C.toFixed(4)+"deg",
      gaugeValue:Math.min(C,100),
      breakdown:["Given: a="+a+", b="+b+", c="+c,"cos(C) = (a^2+b^2-c^2)/(2ab) = "+cosC.toFixed(4),"Angle C = "+C.toFixed(4)+"deg","Angle A = "+A.toFixed(4)+"deg","Angle B = "+B.toFixed(4)+"deg","Area (Heron) = "+area.toFixed(4)],
      stats:[
        {label:"Angle C",value:C.toFixed(4)+"°"},
        {label:"Angle A",value:A.toFixed(4)+"°"},
        {label:"Angle B",value:B.toFixed(4)+"°"},
        {label:"Area",value:area.toFixed(4)},
      ]
    }
  }
  throw new Error("Enter all 3 sides (SSS), or sides a, b and angle C (SAS).")
""",
  """{id:"a",label:"Side a",type:"number",placeholder:"5",min:0,step:0.001,defaultValue:5},
            {id:"b",label:"Side b",type:"number",placeholder:"7",min:0,step:0.001,defaultValue:7},
            {id:"c",label:"Side c (for SSS — leave 0 for SAS)",type:"number",placeholder:"0",min:0,step:0.001,defaultValue:0},
            {id:"angleC",label:"Angle C in degrees (for SAS — leave 0 for SSS)",type:"number",placeholder:"60",min:0,max:180,step:0.001,defaultValue:60}""",
  [("Acute angle","#22c55e",0,90),("Right angle","#3b82f6",85,95),("Obtuse angle","#f59e0b",90,180)],
  "degrees","180",
  [("What is the law of cosines?","For a triangle with sides a, b, c and angle C opposite side c: c^2 = a^2 + b^2 - 2ab*cos(C). This generalizes the Pythagorean theorem: when C = 90deg, cos(90) = 0 and c^2 = a^2 + b^2. Use it when you know SSS (three sides) or SAS (two sides + included angle)."),
   ("When should I use the law of cosines vs law of sines?","Law of cosines: use for SSS (three sides) or SAS (two sides + included angle). Law of sines: use for AAS (two angles + one side) or ASA (two angles + included side). For SSA (two sides + non-included angle), law of sines has the ambiguous case — law of cosines may be clearer."),
   ("How does the law of cosines reduce to Pythagoras?","In a right triangle, the angle C at the right angle is 90 degrees. cos(90) = 0, so 2ab*cos(C) = 0. The law of cosines becomes: c^2 = a^2 + b^2 + 0 = a^2 + b^2. This is exactly the Pythagorean theorem! The law of cosines is the general case."),
   ("How do I find all angles of a triangle from three sides (SSS)?","Use the law of cosines to find each angle: cos(A) = (b^2+c^2-a^2)/(2bc), cos(B) = (a^2+c^2-b^2)/(2ac), cos(C) = (a^2+b^2-c^2)/(2ab). Take arccos() to get the angles in degrees. Verify: A + B + C = 180 degrees."),
   ("What is the triangle inequality?","For sides a, b, c to form a valid triangle: a + b > c, a + c > b, and b + c > a. All three conditions must hold. The law of cosines will give cos(C) outside [-1, 1] for invalid triangles, which this calculator detects. Examples: sides 3,4,5 valid; sides 1,2,10 invalid (1+2 < 10).")],
  [("Triangle Calculator","/calculators/triangle-calculator"),("Area Calculator","/calculators/area-calculator"),("Distance Calculator","/calculators/distance-calculator"),("Angle Converter","/calculators/angle-converter-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Law of Cosines</h3>
          <div class="text-xs text-blue-800 font-mono space-y-2 mb-2">
            <div>c² = a² + b² − 2ab·cos(C)</div>
            <div>cos(C) = (a²+b²−c²) / 2ab</div>
          </div>
          <div class="text-xs text-blue-700">Use for SSS or SAS triangles.<br/>When C=90°, reduces to Pythagoras.</div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Triangle-Solving Decision Guide</h2>
        <div class="space-y-2">
          {[
            {case:"SSS (3 sides known)",law:"Law of Cosines → find all angles"},
            {case:"SAS (2 sides + included angle)",law:"Law of Cosines → find missing side"},
            {case:"ASA (2 angles + included side)",law:"Law of Sines → find missing sides"},
            {case:"AAS (2 angles + non-included side)",law:"Law of Sines → find missing sides"},
            {case:"SSA (2 sides + non-included angle)",law:"Law of Sines (ambiguous case) or Law of Cosines"},
            {case:"AAA (3 angles only)",law:"Cannot determine side lengths — infinitely many triangles"},
          ].map(c => (
            <div class="bg-gray-50 rounded-lg p-2"><div class="font-semibold text-xs text-blue-700">{c.case}</div><div class="text-xs text-gray-600">{c.law}</div></div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Cosine Values to Remember</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Angle</th><th class="p-2 text-xs font-semibold text-right">cos(θ)</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["0°","1"],["30°","√3/2 ≈ 0.866"],["45°","√2/2 ≈ 0.707"],["60°","1/2 = 0.5"],["90°","0"],["120°","−0.5"],["180°","−1"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-mono">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "Result","Solve triangles using the law of cosines (SSS or SAS)")

# ── LCM & GCD ────────────────────────────────────────────────────────────────
w("lcm-gcd","LCM & GCD Calculator","Math","math",
  "LCM and GCD Calculator: Least Common Multiple & Greatest Common Divisor",
  "Find the LCM (least common multiple) and GCD (greatest common divisor/HCF) of two or more numbers. Shows prime factorization. Free LCM GCD calculator.",
  """
  const a = parseInt(inputs.a)||0
  const b = parseInt(inputs.b)||0
  const c = parseInt(inputs.c)||0
  if(a<=0||b<=0) throw new Error("Enter at least two positive integers.")
  const gcd = (x,y) => y===0?x:gcd(y,x%y)
  const lcm = (x,y) => x/gcd(x,y)*y
  const primeFactors = n => {
    const factors=[]
    let d=2
    while(d*d<=n){while(n%d===0){factors.push(d);n=Math.floor(n/d)}d++}
    if(n>1) factors.push(n)
    return factors
  }
  const numbers = c>0?[a,b,c]:[a,b]
  const overallGcd = numbers.reduce(gcd)
  const overallLcm = numbers.reduce(lcm)
  const factA = primeFactors(a).join(" × ")||String(a)
  const factB = primeFactors(b).join(" × ")||String(b)
  return {
    value:"GCD="+overallGcd+" | LCM="+overallLcm,
    gaugeValue:Math.min(overallGcd/Math.min(a,b)*100,100),
    breakdown:["Numbers: "+numbers.join(", "),"GCD (HCF): "+overallGcd,"LCM: "+overallLcm,"GCD × LCM = "+overallGcd*overallLcm+" = a×b = "+a*b,a+": "+factA,b+": "+factB],
    stats:[
      {label:"GCD / HCF",value:String(overallGcd)},
      {label:"LCM",value:String(overallLcm)},
      {label:"GCD × LCM",value:String(overallGcd*overallLcm)},
      {label:"a × b",value:String(a*b)},
    ]
  }
""",
  """{id:"a",label:"First number",type:"number",placeholder:"12",min:1,step:1,defaultValue:12},
            {id:"b",label:"Second number",type:"number",placeholder:"18",min:1,step:1,defaultValue:18},
            {id:"c",label:"Third number (optional)",type:"number",placeholder:"0",min:0,step:1,defaultValue:0}""",
  [("Coprime (GCD=1)","#ef4444",0,5),("Partial factor","#f59e0b",5,50),("Strong factor","#22c55e",50,100)],
  "% GCD of smaller","100",
  [("What is GCD (Greatest Common Divisor)?","The GCD (also called HCF — Highest Common Factor) is the largest number that divides all given numbers evenly. GCD(12, 18) = 6 because 6 is the largest number that divides both 12 and 18. Use the Euclidean algorithm: GCD(18,12) = GCD(12,6) = GCD(6,0) = 6."),
   ("What is LCM (Least Common Multiple)?","The LCM is the smallest positive integer that is divisible by all given numbers. LCM(4, 6) = 12 because 12 is the smallest number that both 4 and 6 divide into evenly. Key relationship: LCM(a,b) = a × b / GCD(a,b)."),
   ("How do I find LCM using prime factorization?","Example: LCM(12, 18). 12 = 2^2 × 3. 18 = 2 × 3^2. LCM = take highest power of each prime: 2^2 × 3^2 = 4 × 9 = 36. GCD = take lowest power of each prime: 2^1 × 3^1 = 6. This method works for any number of inputs."),
   ("What are GCD and LCM used for?","GCD: simplifying fractions (divide numerator and denominator by GCD), finding common units, RSA cryptography. LCM: finding common denominators when adding fractions (1/4 + 1/6: LCD = LCM(4,6) = 12), scheduling repeating events, gear ratios."),
   ("What does it mean for two numbers to be coprime?","Two numbers are coprime (relatively prime) if their GCD = 1. Examples: 8 and 9 (GCD=1), 14 and 15 (GCD=1). Coprime numbers have no common prime factors. Consecutive integers are always coprime. Coprimality is important in fractions, modular arithmetic, and cryptography.")],
  [("Modulo Calculator","/calculators/modulo-calculator"),("Prime Number Calculator","/calculators/prime-calculator"),("Fraction Calculator","/calculators/fraction-calculator"),("Combination Calculator","/calculators/combination-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Key Formulas</h3>
          <div class="text-xs text-blue-800 font-mono space-y-2">
            <div>LCM(a,b) = a × b / GCD(a,b)</div>
            <div>GCD via Euclidean Algorithm:</div>
            <div>GCD(a,b) = GCD(b, a mod b)</div>
            <div>Until b=0, then GCD = a</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Euclidean Algorithm Example</h2>
        <div class="bg-gray-50 rounded-xl p-4">
          <div class="text-xs font-semibold text-gray-700 mb-2">GCD(48, 18) step by step:</div>
          <div class="text-xs text-gray-600 font-mono space-y-1">
            <div>GCD(48, 18): 48 = 2×18 + 12 → GCD(18, 12)</div>
            <div>GCD(18, 12): 18 = 1×12 + 6 → GCD(12, 6)</div>
            <div>GCD(12, 6): 12 = 2×6 + 0 → GCD = 6</div>
            <div class="mt-2 font-semibold text-blue-700">GCD(48,18) = 6</div>
            <div class="font-semibold text-blue-700">LCM(48,18) = 48×18/6 = 144</div>
          </div>
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Common Examples</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">a, b</th><th class="p-2 text-xs font-semibold text-right">GCD</th><th class="p-2 text-xs font-semibold text-right">LCM</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["6, 9",3,18],["8, 12",4,24],["14, 21",7,42],["15, 25",5,75],["17, 13",1,221]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-medium">{r[1]}</td><td class="p-2 text-xs text-right font-medium">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "GCD & LCM","Find GCD and LCM with prime factorization")

# ── PRIME ────────────────────────────────────────────────────────────────────
w("prime","Prime Number Calculator","Math","math",
  "Prime Number Calculator: Check Primality & Factorize",
  "Check if any number is prime and find its prime factorization. List primes up to a limit. Free prime number calculator.",
  """
  const value = parseInt(inputs.value)||0
  const mode = inputs.mode||"check"
  if(value<2) throw new Error("Enter an integer of 2 or greater.")
  if(value>10000000) throw new Error("Number too large (max 10,000,000).")
  const isPrime = n => {
    if(n<2) return false
    if(n===2) return true
    if(n%2===0) return false
    for(let i=3;i*i<=n;i+=2) if(n%i===0) return false
    return true
  }
  const primeFactors = n => {
    const factors=[]
    let d=2
    while(d*d<=n){while(n%d===0){factors.push(d);n=Math.floor(n/d)}d++}
    if(n>1) factors.push(n)
    return factors
  }
  if(mode==="check"){
    const prime=isPrime(value)
    const factors=prime?[value]:primeFactors(value)
    const factStr=factors.join(" × ")
    return {
      value:value+" is "+(prime?"PRIME":"NOT prime"),
      gaugeValue:prime?100:Math.min(factors.length/10*100,80),
      breakdown:[value+(prime?" IS prime":" is NOT prime"),"Prime factorization: "+factStr,"Number of prime factors: "+factors.length,"Divisors count: "+(prime?2:"2+"),"Nearest prime below: "+(()=>{let n=value-1;while(n>=2&&!isPrime(n))n--;return n>=2?n:"N/A"})()],
      stats:[
        {label:"Prime?",value:prime?"YES":"NO"},
        {label:"Factorization",value:factStr},
        {label:"Factors Count",value:String(factors.length)},
        {label:"Nearest prime",value:(()=>{let n=value+1;while(!isPrime(n))n++;return String(n)})()},
      ]
    }
  } else {
    const primes=[]
    for(let n=2;n<=value&&primes.length<50;n++) if(isPrime(n)) primes.push(n)
    return {
      value:"Found "+primes.length+" primes up to "+(primes[primes.length-1]||0),
      gaugeValue:Math.min(primes.length/50*100,100),
      breakdown:["Primes up to "+value+":","Count: "+primes.length,"First 10: "+primes.slice(0,10).join(", "),"Last 5: "+primes.slice(-5).join(", ")],
      stats:[
        {label:"Count (≤"+value+")",value:String(primes.length)},
        {label:"Largest found",value:String(primes[primes.length-1]||0)},
        {label:"First prime",value:"2"},
        {label:"10th prime",value:String(primes[9]||"N/A")},
      ]
    }
  }
""",
  """{id:"value",label:"Number",type:"number",placeholder:"97",min:2,step:1,defaultValue:97},
            {id:"mode",label:"Mode",type:"select",options:[
              {value:"check",label:"Check if prime & factorize"},
              {value:"list",label:"List all primes up to this number"},
            ],defaultValue:"check"}""",
  [("Not prime","#ef4444",0,50),("Prime!","#22c55e",90,100)],
  "prime score","100",
  [("What is a prime number?","A prime number is a natural number greater than 1 that has exactly two divisors: 1 and itself. Examples: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29... The number 1 is NOT prime (only 1 divisor). 2 is the only even prime. There are infinitely many primes (Euclid proved this around 300 BC)."),
   ("How do I check if a number is prime?","Trial division: test if any integer from 2 to sqrt(n) divides n. If none do, n is prime. For n=97: sqrt(97) ≈ 9.8, check divisors 2,3,5,7. None divide 97, so 97 is prime. This is O(sqrt(n)). For very large numbers, use probabilistic tests like Miller-Rabin."),
   ("What is prime factorization?","Every composite (non-prime) number can be uniquely expressed as a product of primes. 360 = 2^3 × 3^2 × 5. This is the Fundamental Theorem of Arithmetic. Applications: GCD, LCM, RSA encryption (based on difficulty of factoring large semiprimes), divisibility rules."),
   ("What are twin primes?","Twin primes are prime pairs that differ by 2: (3,5), (5,7), (11,13), (17,19), (29,31), (41,43)... The Twin Prime Conjecture says there are infinitely many twin prime pairs, but this is unproven. The largest known twin prime pair has over 300,000 digits."),
   ("Why is 1 not a prime number?","If 1 were prime, the Fundamental Theorem of Arithmetic (unique prime factorization) would fail: 6 = 2×3 = 1×2×3 = 1^2×2×3, making factorization non-unique. By defining primes as having exactly 2 divisors (excluding 1 and itself), we preserve unique factorization. 1 is called a unit.")],
  [("LCM GCD Calculator","/calculators/lcm-gcd-calculator"),("Modulo Calculator","/calculators/modulo-calculator"),("Combination Calculator","/calculators/combination-calculator"),("Factorial Calculator","/calculators/factorial-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Primes to 100</h3>
          <div class="flex flex-wrap gap-1 text-xs font-mono text-blue-900">
            {[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97].map(p => (
              <span class="bg-blue-100 rounded px-1">{p}</span>
            ))}
          </div>
          <div class="text-xs text-blue-700 mt-2">25 primes below 100</div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Prime Factorization Examples</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Number</th><th class="p-2 text-xs font-semibold text-right">Prime Factorization</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["12","2² × 3"],["60","2² × 3 × 5"],["100","2² × 5²"],["360","2³ × 3² × 5"],["1000","2³ × 5³"],["1024","2¹⁰"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-mono">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Prime Number Facts</h2>
        <div class="space-y-2">
          {["2 is the ONLY even prime number","All primes > 3 are of the form 6k±1","There are infinitely many primes (Euclid, 300 BC)","Largest known prime (2024): 2^136,279,841 − 1 (41 million digits)","Prime Number Theorem: primes near n have density 1/ln(n)","Goldbach Conjecture (unproven): every even n>2 = sum of 2 primes"].map(f => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{f}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Primality","Check primality, factorize, and list prime numbers")

# ── NUMBER BASE ───────────────────────────────────────────────────────────────
w("number-base","Number Base Converter","Math","math",
  "Number Base Converter: Any Base to Any Base",
  "Convert numbers between any numeral system: base 2 to 36. Binary, octal, decimal, hexadecimal, and custom bases. Free base converter.",
  """
  const value = (inputs.value||"").toString().trim().toUpperCase()
  const fromBase = parseInt(inputs.fromBase)||10
  const toBase = parseInt(inputs.toBase)||2
  if(fromBase<2||fromBase>36) throw new Error("From base must be between 2 and 36.")
  if(toBase<2||toBase>36) throw new Error("To base must be between 2 and 36.")
  const DIGITS="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  const toDecimal = (v,base) => {
    let result=0,power=1
    for(let i=v.length-1;i>=0;i--){
      const d=DIGITS.indexOf(v[i])
      if(d<0||d>=base) throw new Error("Digit "+v[i]+" is invalid for base "+base+".")
      result+=d*power; power*=base
    }
    return result
  }
  const fromDecimal = (n,base) => {
    if(n===0) return "0"
    let result=""
    while(n>0){result=DIGITS[n%base]+result;n=Math.floor(n/base)}
    return result
  }
  const decimal=toDecimal(value,fromBase)
  const result=fromDecimal(decimal,toBase)
  return {
    value:value+" (base "+fromBase+") = "+result+" (base "+toBase+")",
    gaugeValue:Math.min(decimal/1000*100,100),
    breakdown:["Input: "+value+" in base "+fromBase,"Decimal value: "+decimal,"Binary (base 2): "+fromDecimal(decimal,2),"Octal (base 8): "+fromDecimal(decimal,8),"Hex (base 16): "+fromDecimal(decimal,16),"Result in base "+toBase+": "+result],
    stats:[
      {label:"Result (base "+toBase+")",value:result},
      {label:"Decimal",value:String(decimal)},
      {label:"Binary",value:fromDecimal(decimal,2)},
      {label:"Hexadecimal",value:fromDecimal(decimal,16)},
    ]
  }
""",
  """{id:"value",label:"Number to convert",type:"text",placeholder:"FF",defaultValue:"FF"},
            {id:"fromBase",label:"Input base (from)",type:"number",placeholder:"16",min:2,max:36,defaultValue:16},
            {id:"toBase",label:"Output base (to)",type:"number",placeholder:"10",min:2,max:36,defaultValue:10}""",
  [("Small (<256)","#22c55e",0,25),("Medium (256-1023)","#3b82f6",25,50),("Large (1024+)","#f59e0b",50,100)],
  "% of 1000","100",
  [("What is a number base (radix)?","A number base (radix) is the number of digits in the numeral system. Base 10 (decimal) uses digits 0-9. Base 2 (binary) uses 0,1. Base 16 (hexadecimal) uses 0-9 and A-F. Base n uses n digits from 0 to n-1, with letters extending beyond 9."),
   ("What is base 36?","Base 36 uses all 36 alphanumeric characters: 0-9 and A-Z. It is the most compact way to represent numbers using standard keyboard characters. Example: 1000 in decimal = RS in base 36. URL shorteners and ID systems often use base 36 or base 62 for compact, URL-safe IDs."),
   ("How do I convert between bases?","Two-step method: (1) convert the source number to decimal, (2) convert from decimal to the target base. To decimal: multiply each digit by base^position and sum. From decimal: repeatedly divide by target base, collect remainders bottom-up. This calculator does both steps."),
   ("What is base 60 (sexagesimal)?","Base 60 was used by ancient Babylonians and is still used for time (60 seconds/minute, 60 minutes/hour) and angles (60 arcminutes/degree). 60 has many divisors (1,2,3,4,5,6,10,12,15,20,30,60), making it convenient for division."),
   ("Why do computers use binary and hexadecimal?","Computers use binary because electronic circuits have two states: on/off (1/0). Binary is perfect for digital logic. Hexadecimal is used as a compact representation: each hex digit = exactly 4 binary bits, making conversion trivial. One byte (8 bits) = two hex digits. Octal was also used historically (each octal digit = 3 bits).")],
  [("Binary Calculator","/calculators/binary-calculator"),("Modulo Calculator","/calculators/modulo-calculator"),("Scientific Notation","/calculators/scientific-notation-calculator"),("Roman Numeral Calculator","/calculators/roman-numeral-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Common Bases</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[["Base 2","Binary — computers, logic"],["Base 8","Octal — Unix file permissions"],["Base 10","Decimal — everyday math"],["Base 16","Hex — colors, memory addresses"],["Base 36","Alphanumeric — URL shorteners"],["Base 60","Sexagesimal — time & angles"]].map(([b,d]) => (
              <div class="border-b border-blue-100 pb-0.5"><span class="font-semibold">{b}:</span> <span>{d}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Number 255 in Various Bases</h2>
      <div class="grid md:grid-cols-3 gap-4">
        {[[2,"11111111"],[3,"100110"],[4,"3333"],[5,"2010"],[8,"377"],[10,"255"],[12,"193"],[16,"FF"],[32,"7V"],[36,"73"]].map(r => (
          <div class="bg-gray-50 rounded-lg p-3 flex justify-between items-center">
            <span class="text-xs text-gray-500">Base {r[0]}</span>
            <span class="font-mono font-bold text-blue-700">{r[1]}</span>
          </div>
        ))}
      </div>
    </div>""",
  "Result","Convert numbers between any bases from 2 to 36")

# ── NUMBER TO WORDS ───────────────────────────────────────────────────────────
w("number-to-words","Number to Words Calculator","Math","math",
  "Number to Words Calculator: Convert Numbers to English Words",
  "Convert any number to English words. Spell out numbers for checks, legal documents, and writing. Free number to words converter.",
  """
  const value = parseFloat(inputs.value)
  if(isNaN(value)) throw new Error("Enter a valid number.")
  if(Math.abs(value)>999999999999) throw new Error("Number too large (max 999,999,999,999).")
  const ones=["","one","two","three","four","five","six","seven","eight","nine","ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"]
  const tens=["","","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety"]
  const toWords = n => {
    if(n===0) return "zero"
    let result=""
    if(n>=1000000000){result+=toWords(Math.floor(n/1000000000))+" billion ";n%=1000000000}
    if(n>=1000000){result+=toWords(Math.floor(n/1000000))+" million ";n%=1000000}
    if(n>=1000){result+=toWords(Math.floor(n/1000))+" thousand ";n%=1000}
    if(n>=100){result+=ones[Math.floor(n/100)]+" hundred ";n%=100}
    if(n>=20){result+=tens[Math.floor(n/10)]+(n%10?" "+ones[n%10]:"");n=0}
    else if(n>0){result+=ones[n];n=0}
    return result.trim()
  }
  const negative = value<0
  const absVal = Math.abs(Math.round(value))
  let words = (negative?"negative ":"")+toWords(absVal)
  const cents = Math.round((Math.abs(value)%1)*100)
  const dollarWords = words + (cents>0?" and "+toWords(cents)+"/100":"")
  return {
    value:words,
    gaugeValue:Math.min(absVal/1000000000*100,100),
    breakdown:["Number: "+value,"In words: "+words,"Check format: "+dollarWords+" dollars","Digits: "+Math.abs(Math.round(value)).toString().length],
    stats:[
      {label:"In Words",value:words.substring(0,20)+(words.length>20?"...":"")},
      {label:"Number",value:value.toLocaleString()},
      {label:"Check Format",value:dollarWords.substring(0,30)+(dollarWords.length>30?"...":"")},
      {label:"Digit Count",value:String(Math.abs(Math.round(value)).toString().length)},
    ]
  }
""",
  """{id:"value",label:"Number",type:"number",placeholder:"1234567",step:1,defaultValue:1234567}""",
  [("Ones/Tens","#22c55e",0,10),("Hundreds/Thousands","#3b82f6",10,50),("Millions+","#f59e0b",50,100)],
  "% of billion","100",
  [("How do I write a check amount in words?","Write the dollar amount in words, then the cents as a fraction. Example: $1,234.56 = One thousand two hundred thirty-four and 56/100 dollars. Start at the far left of the line, use a capital first letter, and draw a line through any unused space to prevent fraud."),
   ("How are large numbers named in English?","Thousand (10^3), million (10^6), billion (10^9), trillion (10^12), quadrillion (10^15), quintillion (10^18). In the British system, a billion used to mean 10^12 (a million millions), but the American system (10^9) is now standard globally in business and science."),
   ("How do I write ordinal numbers (first, second, third)?","Ordinals: 1st (first), 2nd (second), 3rd (third), 4th-19th (fourth...nineteenth), 20th (twentieth), 21st (twenty-first), 22nd (twenty-second), 23rd (twenty-third), 24th-29th (twenty-fourth...twenty-ninth). Pattern: most end in -th, except those ending in 1 (-st), 2 (-nd), 3 (-rd)."),
   ("When should numbers be spelled out in writing?","Style guides vary, but common rules: spell out numbers zero through nine, use numerals for 10 and above. Always spell out at sentence start. Use numerals for specific measurements (5 miles, 3 hours). In checks and legal documents, always spell out dollar amounts to prevent alteration."),
   ("What is the difference between cardinal and ordinal numbers?","Cardinal numbers count quantity: one, two, three, four... They answer how many? Ordinal numbers indicate position: first, second, third, fourth... They answer which order? In English, most ordinals add -th to the cardinal: seven → seventh, nineteen → nineteenth.")],
  [("Roman Numeral Calculator","/calculators/roman-numeral-calculator"),("Average Calculator","/calculators/average-calculator"),("Percentage Calculator","/calculators/percentage-calculator"),("Currency Calculator","/calculators/currency-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Number System</h3>
          <div class="text-xs text-blue-800 space-y-1">
            <div><span class="font-mono">1–19</span>: one, two... nineteen</div>
            <div><span class="font-mono">20–99</span>: twenty-one... ninety-nine</div>
            <div><span class="font-mono">100–999</span>: one hundred...</div>
            <div><span class="font-mono">1,000+</span>: one thousand...</div>
            <div><span class="font-mono">1,000,000+</span>: one million...</div>
            <div><span class="font-mono">1,000,000,000+</span>: one billion...</div>
          </div>
        </div>""",
  """    <div class="mt-10">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Check Writing Guide</h2>
      <div class="bg-gray-50 rounded-xl p-5">
        <div class="text-xs text-gray-700 space-y-2">
          <div class="grid grid-cols-2 gap-4">
            {[["$5.00","Five and 00/100 dollars"],["$99.99","Ninety-nine and 99/100 dollars"],["$100.00","One hundred and 00/100 dollars"],["$1,000.50","One thousand and 50/100 dollars"],["$10,000.00","Ten thousand and 00/100 dollars"],["$1,234,567.89","One million two hundred thirty-four thousand five hundred sixty-seven and 89/100 dollars"]].map(r => (
              <div class="bg-white rounded p-2 col-span-full md:col-span-1">
                <div class="font-semibold text-blue-700">{r[0]}</div>
                <div class="text-gray-600">{r[1]}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>""",
  "Words","Convert numbers to English words for checks and documents")

# ── RANDOM NUMBER ────────────────────────────────────────────────────────────
w("random-number","Random Number Generator","Math","math",
  "Random Number Generator: Generate Random Numbers & Lists",
  "Generate random numbers between any range, create random number lists, simulate dice, and randomize sequences. Free random number generator.",
  """
  const min = parseFloat(inputs.min)||0
  const max = parseFloat(inputs.max)||100
  const count = parseInt(inputs.count)||1
  const type = inputs.type||"integer"
  if(min>=max) throw new Error("Minimum must be less than maximum.")
  if(count<1||count>20) throw new Error("Count must be between 1 and 20.")
  const nums=[]
  for(let i=0;i<count;i++){
    const r=Math.random()*(max-min)+min
    nums.push(type==="integer"?Math.floor(r):parseFloat(r.toFixed(4)))
  }
  const avg=nums.reduce((a,b)=>a+b,0)/nums.length
  const sorted=[...nums].sort((a,b)=>a-b)
  return {
    value:nums.join(", "),
    gaugeValue:(avg-min)/(max-min)*100,
    breakdown:["Range: "+min+" to "+max,"Count: "+count,"Numbers: "+nums.join(", "),"Average: "+avg.toFixed(4),"Min generated: "+sorted[0],"Max generated: "+sorted[sorted.length-1]],
    stats:[
      {label:"Generated",value:nums.slice(0,3).join(",")+"..("+count+" total)"},
      {label:"Average",value:avg.toFixed(4)},
      {label:"Min",value:String(sorted[0])},
      {label:"Max",value:String(sorted[sorted.length-1])},
    ]
  }
""",
  """{id:"min",label:"Minimum value",type:"number",placeholder:"1",step:1,defaultValue:1},
            {id:"max",label:"Maximum value",type:"number",placeholder:"100",step:1,defaultValue:100},
            {id:"count",label:"Count (how many numbers, 1-20)",type:"number",placeholder:"1",min:1,max:20,defaultValue:1},
            {id:"type",label:"Number type",type:"select",options:[
              {value:"integer",label:"Integers (whole numbers)"},
              {value:"decimal",label:"Decimal numbers"},
            ],defaultValue:"integer"}""",
  [("Low range","#3b82f6",0,33),("Mid range","#22c55e",33,67),("High range","#f59e0b",67,100)],
  "% within range","100",
  [("Are these numbers truly random?","No — these are pseudorandom numbers generated by Math.random(), a deterministic algorithm seeded by the system clock. Pseudorandom numbers look random and pass statistical tests, but they are predictable if you know the seed. For cryptographic purposes, use a cryptographically secure random number generator (CSPRNG)."),
   ("How do I generate a random number in a specific range?","Formula: Math.floor(Math.random() * (max - min + 1)) + min for integers. For decimals: Math.random() * (max - min) + min. Example for 1-6 (dice): Math.floor(Math.random() * 6) + 1. In Python: random.randint(1, 6) or random.uniform(1.0, 6.0)."),
   ("What is the uniform distribution?","Math.random() produces uniformly distributed numbers — each value in [0,1) is equally likely. After scaling to [min, max], the probability of any subrange is proportional to its length. This means generating 1-10 gives equal probability to each digit."),
   ("How do I shuffle a list randomly?","Fisher-Yates algorithm: for i from n-1 to 1, swap element[i] with element[Math.floor(Math.random() * (i+1))]. This gives exactly n! equally likely permutations. In Python: random.shuffle(list). In JavaScript: list.sort(() => Math.random() - 0.5) is biased — use Fisher-Yates instead."),
   ("What are random numbers used for?","Statistics and simulations (Monte Carlo methods), games (dice rolls, card shuffles), cryptography (key generation — must use CSPRNG), A/B testing randomization, statistical sampling, random art and music generation, lottery draws, password generation.")],
  [("Combination Calculator","/calculators/combination-calculator"),("Probability (Percentage)","/calculators/percentage-calculator"),("Z-Score Calculator","/calculators/z-score-calculator"),("Password Calculator","/calculators/password-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Dice Simulator</h3>
          <div class="text-xs text-blue-800 space-y-1">
            <div><span class="font-semibold">d4:</span> 1 to 4</div>
            <div><span class="font-semibold">d6:</span> 1 to 6 (standard dice)</div>
            <div><span class="font-semibold">d8:</span> 1 to 8</div>
            <div><span class="font-semibold">d10:</span> 1 to 10</div>
            <div><span class="font-semibold">d12:</span> 1 to 12</div>
            <div><span class="font-semibold">d20:</span> 1 to 20</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">True vs Pseudorandom</h2>
        <div class="space-y-3">
          {[
            {t:"Pseudorandom (Math.random)",d:"Deterministic algorithm, fast, passes statistical tests. Sufficient for games, simulations, sampling."},
            {t:"Cryptographically Secure (CSPRNG)",d:"Uses hardware entropy (mouse movement, disk timing). Required for keys, passwords, tokens."},
            {t:"True Random (hardware)",d:"Physical processes like radioactive decay or atmospheric noise. Very slow, used for high-stakes randomness."},
          ].map(e => (
            <div class="bg-gray-50 rounded-lg p-3"><div class="font-semibold text-xs text-blue-700">{e.t}</div><div class="text-xs text-gray-600">{e.d}</div></div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Applications</h2>
        <div class="space-y-2">
          {["Monte Carlo simulations — estimate pi by random sampling","Card shuffling — generate random deck orders","A/B testing — randomly assign users to groups","Statistical sampling — pick random subset from population","Music and art generation — procedural randomness","Lottery and sweepstakes — fair random selection"].map(a => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{a}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Numbers","Generate random numbers in any range")

print(f"\nWritten: {written} pages")
