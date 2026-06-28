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

# ── NUMEROLOGY ────────────────────────────────────────────────────────────────
w("numerology","Numerology Calculator","Other","other",
  "Numerology Calculator: Life Path, Expression & Soul Number",
  "Calculate your numerology numbers: life path, expression (destiny), soul urge, and personality numbers. Free numerology calculator.",
  """
  const name = (inputs.name||"").toUpperCase().replace(/[^A-Z]/g,"")
  const dob = inputs.dob||""
  const reduceNum = n => {
    while(n>9&&n!==11&&n!==22&&n!==33){
      n=n.toString().split("").reduce((a,d)=>a+parseInt(d),0)
    }
    return n
  }
  const vowels="AEIOU"
  const letterVals={A:1,B:2,C:3,D:4,E:5,F:6,G:7,H:8,I:9,J:1,K:2,L:3,M:4,N:5,O:6,P:7,Q:8,R:9,S:1,T:2,U:3,V:4,W:5,X:6,Y:7,Z:8}
  // Life Path from DOB
  let lifePathNum=0
  if(dob){
    const parts=dob.replace(/[^0-9]/g," ").trim().split(/\\s+/)
    const digits=dob.replace(/[^0-9]/g,"").split("").map(Number)
    lifePathNum=reduceNum(digits.reduce((a,b)=>a+b,0))
  }
  // Expression (full name)
  const expressionSum=name.split("").reduce((a,c)=>a+(letterVals[c]||0),0)
  const expressionNum=reduceNum(expressionSum)
  // Soul urge (vowels only)
  const soulSum=name.split("").filter(c=>vowels.includes(c)).reduce((a,c)=>a+(letterVals[c]||0),0)
  const soulNum=soulSum>0?reduceNum(soulSum):0
  // Personality (consonants only)
  const persSum=name.split("").filter(c=>!vowels.includes(c)).reduce((a,c)=>a+(letterVals[c]||0),0)
  const persNum=persSum>0?reduceNum(persSum):0
  const meanings={1:"Leadership",2:"Cooperation",3:"Creativity",4:"Stability",5:"Freedom",6:"Nurturing",7:"Wisdom",8:"Power",9:"Humanitarianism",11:"Intuition",22:"Master Builder",33:"Master Teacher"}
  return {
    value:"Life Path "+lifePathNum+(lifePathNum?"":" (enter DOB)"),
    gaugeValue:Math.min((lifePathNum||expressionNum)/33*100,100),
    breakdown:["Life Path: "+lifePathNum+" ("+( meanings[lifePathNum]||"enter DOB")+")","Expression: "+expressionNum+" ("+(meanings[expressionNum]||"unknown")+")","Soul Urge: "+soulNum+" ("+(meanings[soulNum]||"unknown")+")","Personality: "+persNum+" ("+(meanings[persNum]||"unknown")+")" ],
    stats:[
      {label:"Life Path",value:String(lifePathNum||"enter DOB")},
      {label:"Expression",value:String(expressionNum)},
      {label:"Soul Urge",value:String(soulNum)},
      {label:"Personality",value:String(persNum)},
    ]
  }
""",
  """{id:"name",label:"Full birth name",type:"text",placeholder:"John Michael Smith",defaultValue:"John Michael Smith"},
            {id:"dob",label:"Date of birth (YYYY-MM-DD)",type:"date",defaultValue:"1990-05-15"}""",
  [("1-3 (Pioneer/Creative)","#22c55e",0,33),("4-6 (Builder/Nurturer)","#3b82f6",33,66),("7-9 (Seeker/Humanitarian)","#f59e0b",66,90),("Master (11/22/33)","#ef4444",90,100)],
  "life path","33",
  [("What is a Life Path number in numerology?","The Life Path number is calculated by adding all digits of your birth date and reducing to a single digit (or master number 11, 22, 33). It is considered the most important number in numerology, representing your life purpose and the traits you carry throughout life."),
   ("How do I calculate my Life Path number?","Add all digits of your birthdate: born June 15, 1990: 6+1+5+1+9+9+0 = 31 → 3+1 = 4. Life Path = 4. Exception: if the sum equals 11, 22, or 33 (master numbers), do not reduce further. These master numbers carry additional significance in numerology."),
   ("What are the master numbers in numerology?","11, 22, and 33 are called master numbers. They are not reduced further. 11 = The Intuitive, 22 = The Master Builder, 33 = The Master Teacher. Master numbers are considered more spiritually evolved and carry both the positive potential and the challenges of both their digits. Not everyone with these numbers will express them at the master level."),
   ("What do the Life Path numbers mean?","1: Leadership, independence. 2: Cooperation, sensitivity. 3: Creativity, expression. 4: Stability, hard work. 5: Freedom, adventure. 6: Nurturing, responsibility. 7: Spirituality, introspection. 8: Power, ambition. 9: Humanitarianism, idealism. 11: Intuition, inspiration. 22: Master building, practicality. 33: Service, compassion."),
   ("Is numerology scientifically valid?","Numerology is a metaphysical tradition, not a science. There is no peer-reviewed evidence that birth dates or name values predict personality traits or life outcomes. It is used as a tool for self-reflection and inspiration by many people. Approach it as entertainment and personal exploration rather than definitive prediction.")],
  [("Zodiac Calculator","/calculators/zodiac-calculator"),("Love Calculator","/calculators/love-calculator"),("Age Calculator","/calculators/age-calculator"),("Date Calculator","/calculators/date-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Life Path Meanings</h3>
          <div class="text-xs text-blue-800 space-y-0.5">
            {[[1,"Leadership"],[2,"Cooperation"],[3,"Creativity"],[4,"Stability"],[5,"Freedom"],[6,"Nurturing"],[7,"Wisdom"],[8,"Ambition"],[9,"Humanitarian"],[11,"Intuition"],[22,"Master Builder"],[33,"Master Teacher"]].map(([n,m]) => (
              <div class="flex gap-2 border-b border-blue-100 pb-0.5"><span class="font-bold w-6">{n}:</span><span>{m}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Letter Number Values</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Value</th><th class="p-2 text-xs font-semibold text-right">Letters</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[[1,"A, J, S"],[2,"B, K, T"],[3,"C, L, U"],[4,"D, M, V"],[5,"E, N, W"],[6,"F, O, X"],[7,"G, P, Y"],[8,"H, Q, Z"],[9,"I, R"]].map(r => (
              <tr><td class="p-2 text-xs font-bold">{r[0]}</td><td class="p-2 text-xs text-right font-mono">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Four Core Numbers</h2>
        <div class="space-y-2">
          {[
            {n:"Life Path",s:"From date of birth",d:"Your life purpose and natural tendencies — the most important number."},
            {n:"Expression (Destiny)",s:"All letters of full name",d:"Your natural abilities and potential — what you are meant to do."},
            {n:"Soul Urge",s:"Vowels of full name",d:"Your inner desires and what motivates you at the deepest level."},
            {n:"Personality",s:"Consonants of full name",d:"How others perceive you — the mask you present to the world."},
          ].map(n => (
            <div class="bg-gray-50 rounded-lg p-2"><div class="font-semibold text-xs text-blue-700">{n.n} <span class="text-gray-500">({n.s})</span></div><div class="text-xs text-gray-600">{n.d}</div></div>
          ))}
        </div>
      </div>
    </div>""",
  "Life Path","Calculate life path, expression, soul urge, and personality numbers")

# ── PAINT ─────────────────────────────────────────────────────────────────────
w("paint","Paint Calculator","Other","other",
  "Paint Calculator: How Many Gallons Do I Need?",
  "Calculate how much paint you need to cover a room or surface. Accounts for doors, windows, and multiple coats. Free paint calculator.",
  """
  const length = parseFloat(inputs.length)||0
  const width = parseFloat(inputs.width)||0
  const height = parseFloat(inputs.height)||0
  const doors = parseFloat(inputs.doors)||0
  const windows = parseFloat(inputs.windows)||0
  const coats = parseFloat(inputs.coats)||2
  const coverage = parseFloat(inputs.coverage)||350
  if(length<=0||width<=0||height<=0) throw new Error("Enter room dimensions.")
  const wallArea = 2*(length+width)*height
  const doorArea = doors*21
  const windowArea = windows*15
  const paintableArea = wallArea-doorArea-windowArea
  const gallonsNeeded = (paintableArea/coverage)*coats
  const gallonsWithWaste = gallonsNeeded*1.1
  const ceilingArea = length*width
  const ceilingGallons = (ceilingArea/coverage)*coats
  return {
    value:gallonsWithWaste.toFixed(2)+" gallons (+10% waste)",
    gaugeValue:Math.min(gallonsWithWaste/20*100,100),
    breakdown:["Room: "+length+"ft x "+width+"ft x "+height+"ft","Wall area: "+wallArea.toFixed(1)+" sq ft","Doors ("+doors+"): -"+doorArea.toFixed(0)+" sq ft","Windows ("+windows+"): -"+windowArea.toFixed(0)+" sq ft","Paintable area: "+paintableArea.toFixed(1)+" sq ft","Coverage: "+coverage+" sq ft/gallon","Coats: "+coats,"Gallons needed: "+gallonsNeeded.toFixed(2),"With 10% waste: "+gallonsWithWaste.toFixed(2)],
    stats:[
      {label:"Paint (walls)",value:gallonsWithWaste.toFixed(2)+" gal"},
      {label:"Wall Area",value:paintableArea.toFixed(0)+" sq ft"},
      {label:"Ceiling Area",value:ceilingArea.toFixed(0)+" sq ft"},
      {label:"Ceiling Paint",value:(ceilingGallons*1.1).toFixed(2)+" gal"},
    ]
  }
""",
  """{id:"length",label:"Room length (ft)",type:"number",placeholder:"12",min:0,step:0.5,defaultValue:12},
            {id:"width",label:"Room width (ft)",type:"number",placeholder:"10",min:0,step:0.5,defaultValue:10},
            {id:"height",label:"Ceiling height (ft)",type:"number",placeholder:"8",min:0,step:0.5,defaultValue:8},
            {id:"doors",label:"Number of doors",type:"number",placeholder:"1",min:0,step:1,defaultValue:1},
            {id:"windows",label:"Number of windows",type:"number",placeholder:"2",min:0,step:1,defaultValue:2},
            {id:"coats",label:"Number of coats",type:"number",placeholder:"2",min:1,max:5,step:1,defaultValue:2},
            {id:"coverage",label:"Paint coverage (sq ft per gallon)",type:"number",placeholder:"350",min:100,step:10,defaultValue:350}""",
  [("Small room (<3 gal)","#22c55e",0,15),("Medium room (3-8 gal)","#3b82f6",15,40),("Large room (8+ gal)","#f59e0b",40,100)],
  "gallons","20",
  [("How much paint do I need for a room?","Measure total wall area (2 x (length + width) x height), subtract doors (~21 sq ft each) and windows (~15 sq ft each). Divide by coverage (typically 350-400 sq ft/gallon). Multiply by number of coats. Add 10% waste. Example: 12x10x8 room with 1 door, 2 windows, 2 coats = about 3 gallons."),
   ("How many square feet does 1 gallon of paint cover?","Most interior paints cover 350-400 sq ft per coat (one gallon). Higher-quality paints may cover 400-450 sq ft. Rough or porous surfaces (new drywall, stucco, brick) absorb more: 300 sq ft/gallon. Always check the manufacturer label for actual coverage."),
   ("Do I need a primer before painting?","Yes in these cases: New drywall or unpainted surfaces. Drastic color changes (dark to light). Stains, repairs, or water damage. Shiny surfaces being repainted. Primer improves adhesion, evens out surface porosity, and can reduce the number of paint coats needed. Self-priming paint claims to combine both."),
   ("What is the difference between eggshell, satin, and gloss paint?","Flat/matte: no sheen, hides imperfections well. Best for ceilings and low-traffic walls. Eggshell: slight sheen, slightly washable. Good for living rooms. Satin: medium sheen, more washable. Best for hallways, kids rooms. Semi-gloss: shinier, very washable. Best for trim, doors, bathrooms. High-gloss: highest sheen, most durable. Best for trim."),
   ("How long does a gallon of paint last if stored?","Latex/water-based paint: 10 years if stored properly (sealed, room temperature, never frozen). Oil-based paint: 15 years. Signs it has gone bad: lumpy, stringy, won separated with stirring, or smells very sour. Store paint cans upside-down initially to create a seal, then upright. Never store in freezing temperatures.")],
  [("Concrete Calculator","/calculators/concrete-calculator"),("Area Calculator","/calculators/area-calculator"),("Unit Converter","/calculators/unit-converter-calculator"),("Volume Calculator","/calculators/volume-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Paint Guide</h3>
          <div class="text-xs text-blue-800 space-y-1">
            <div>1 gallon ≈ 350-400 sq ft</div>
            <div>Standard door ≈ 21 sq ft</div>
            <div>Standard window ≈ 15 sq ft</div>
            <div>Always buy 10% extra</div>
            <div>2 coats typical for walls</div>
            <div>Ceiling usually 1 coat</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Paint Finish Guide</h2>
        <div class="space-y-2">
          {[
            {f:"Flat/Matte",r:"Ceilings, low-traffic walls",p:"Hides imperfections, not washable"},
            {f:"Eggshell",r:"Living rooms, dining rooms",p:"Slight sheen, slightly washable"},
            {f:"Satin",r:"Hallways, kids rooms",p:"Medium sheen, more durable"},
            {f:"Semi-gloss",r:"Trim, doors, bathrooms",p:"Shinier, very washable, water-resistant"},
            {f:"High-gloss",r:"Doors, cabinetry, trim",p:"Highest sheen, most durable"},
          ].map(p => (
            <div class="bg-gray-50 rounded-lg p-2"><div class="font-semibold text-xs text-blue-700">{p.f} — {p.r}</div><div class="text-xs text-gray-600">{p.p}</div></div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Typical Room Paint Needs</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Room</th><th class="p-2 text-xs font-semibold text-right">Gallons (2 coats)</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Bathroom (5×7ft)","1-2"],["Bedroom (10×12ft)","2-3"],["Living room (14×18ft)","4-5"],["Open plan (20×25ft)","6-8"],["Whole house avg","15-25+"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-medium">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
  "Gallons","Calculate how much paint you need for any room")

# ── PASSWORD ─────────────────────────────────────────────────────────────────
w("password","Password Strength Calculator","Other","other",
  "Password Strength Calculator: Check & Generate Strong Passwords",
  "Check the strength of any password and estimate how long it would take to crack. Free password strength calculator with security tips.",
  """
  const password = inputs.password||""
  if(!password) throw new Error("Enter a password to analyze.")
  const len = password.length
  const hasLower = /[a-z]/.test(password)
  const hasUpper = /[A-Z]/.test(password)
  const hasDigit = /[0-9]/.test(password)
  const hasSymbol = /[^a-zA-Z0-9]/.test(password)
  let charsetSize = 0
  if(hasLower) charsetSize+=26
  if(hasUpper) charsetSize+=26
  if(hasDigit) charsetSize+=10
  if(hasSymbol) charsetSize+=32
  const entropy = Math.log2(Math.pow(charsetSize||1, len))
  const cracksPerSec = 1e10
  const seconds = Math.pow(charsetSize||1, len) / cracksPerSec
  let crackTime
  if(seconds<1) crackTime="instantly"
  else if(seconds<60) crackTime=seconds.toFixed(0)+" seconds"
  else if(seconds<3600) crackTime=(seconds/60).toFixed(0)+" minutes"
  else if(seconds<86400) crackTime=(seconds/3600).toFixed(0)+" hours"
  else if(seconds<31536000) crackTime=(seconds/86400).toFixed(0)+" days"
  else if(seconds<31536000000) crackTime=(seconds/31536000).toFixed(0)+" years"
  else crackTime="centuries+"
  const score = Math.min(Math.round(entropy/128*100),100)
  const strength = score>=75?"Strong":score>=50?"Good":score>=25?"Fair":"Weak"
  const checks=[hasLower?"✓ Lowercase":"✗ Add lowercase",hasUpper?"✓ Uppercase":"✗ Add uppercase",hasDigit?"✓ Numbers":"✗ Add numbers",hasSymbol?"✓ Symbols":"✗ Add symbols",len>=12?"✓ 12+ characters":"✗ Use 12+ characters",len>=16?"✓ 16+ characters":"✗ Aim for 16+"]
  return {
    value:strength+" — "+entropy.toFixed(1)+" bits entropy",
    gaugeValue:score,
    breakdown:["Length: "+len+" characters","Charset size: "+charsetSize,"Entropy: "+entropy.toFixed(2)+" bits","Crack time (at 10B/sec): "+crackTime,"Strength: "+strength,...checks],
    stats:[
      {label:"Strength",value:strength},
      {label:"Entropy",value:entropy.toFixed(1)+" bits"},
      {label:"Length",value:len+" chars"},
      {label:"Time to crack",value:crackTime},
    ]
  }
""",
  """{id:"password",label:"Password to analyze",type:"text",placeholder:"Enter password...",defaultValue:"Password123"}""",
  [("Weak (<25%)","#ef4444",0,25),("Fair (25-50%)","#f59e0b",25,50),("Good (50-75%)","#3b82f6",50,75),("Strong (75%+)","#22c55e",75,100)],
  "strength score","100",
  [("What makes a password strong?","A strong password has: Length (12+ characters — each character multiplies possibilities). Character variety (uppercase, lowercase, digits, symbols). Randomness (no dictionary words, names, dates). Uniqueness (different for every site). A 16-character random password with full charset takes centuries to crack even with fast hardware."),
   ("How is password entropy calculated?","Entropy = log2(charsetSize ^ length) bits. Charset size: lowercase only=26, +uppercase=52, +digits=62, +symbols=94. A 12-character password using all character types: log2(94^12) ≈ 78.8 bits. Each additional character adds log2(94) ≈ 6.6 bits of entropy. 60+ bits is considered minimum strong."),
   ("What is the most common password mistake?","Using predictable patterns: dictionary words, names, dates, or simple substitutions (p@ssw0rd). Password re-use across sites is a major risk — if one site is breached, all your accounts are at risk. Most attacks use credential stuffing from known breach databases, not brute force."),
   ("Should I use a password manager?","Yes — strongly recommended. A password manager generates and stores unique strong passwords for every site. You only need to remember one strong master password. Top options: Bitwarden (free, open source), 1Password, LastPass. Browser built-in password managers (Chrome, Safari) are also good for most people."),
   ("What is multi-factor authentication (MFA)?","MFA requires a second proof beyond your password: a code from an authenticator app, SMS code, biometric (fingerprint/face), or hardware key. Even if your password is stolen, MFA blocks the attacker. Use authenticator apps (Google Authenticator, Authy) rather than SMS for best security. MFA is the single most effective account protection measure.")],
  [("Random Number Generator","/calculators/random-number-calculator"),("Combination Calculator","/calculators/combination-calculator"),("Percentage Calculator","/calculators/percentage-calculator"),("Average Calculator","/calculators/average-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Password Strength Guide</h3>
          <div class="text-xs text-blue-800 space-y-1">
            <div class="font-semibold">Do:</div>
            <div>✓ Use 12+ characters</div>
            <div>✓ Mix upper, lower, numbers, symbols</div>
            <div>✓ Use a password manager</div>
            <div>✓ Enable 2FA/MFA everywhere</div>
            <div>✓ Unique password per site</div>
            <div class="font-semibold mt-2">Don not:</div>
            <div>✗ Use your name or birthday</div>
            <div>✗ Use dictionary words</div>
            <div>✗ Reuse passwords</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Time to Crack (10 billion guesses/sec)</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Password Example</th><th class="p-2 text-xs font-semibold text-right">Time to Crack</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["abc","Instantly"],["abc123","~2 seconds"],["Abc123!","~2 hours"],["P@ssw0rd!","~5 hours"],["TrBcQ#9mXz","~4 years"],["Correct-Horse-Batt","~centuries"]].map(r => (
              <tr><td class="p-2 text-xs font-mono">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Charset Size Reference</h2>
        <div class="space-y-2">
          {["Lowercase only (a-z): 26 characters","+ Uppercase (A-Z): 52 total","+ Digits (0-9): 62 total","+ Common symbols: 94 total","Each extra character multiplies: 94^13 vs 94^12 = 94x more combinations","Longer password > more character types for same length"].map(c => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{c}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Strength","Analyze password strength and estimate crack time")

# ── ROMAN NUMERAL ─────────────────────────────────────────────────────────────
w("roman-numeral","Roman Numeral Converter","Other","other",
  "Roman Numeral Converter: Numbers to Roman Numerals",
  "Convert numbers to Roman numerals and Roman numerals to numbers. Supports 1-3,999. Free Roman numeral calculator.",
  """
  const mode = inputs.mode||"to_roman"
  const value = inputs.value||""
  if(mode==="to_roman"){
    const num=parseInt(value)||0
    if(num<1||num>3999) throw new Error("Enter a number from 1 to 3999.")
    const vals=[1000,900,500,400,100,90,50,40,10,9,5,4,1]
    const syms=["M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"]
    let n=num, result=""
    for(let i=0;i<vals.length;i++){while(n>=vals[i]){result+=syms[i];n-=vals[i]}}
    const breakdown=[num+" = "+result]
    let temp=num
    for(let i=0;i<vals.length;i++){
      while(temp>=vals[i]){breakdown.push(syms[i]+" ("+vals[i]+")");temp-=vals[i]}
    }
    return {
      value:result,
      gaugeValue:Math.min(num/3999*100,100),
      breakdown,
      stats:[
        {label:"Roman Numeral",value:result},
        {label:"Arabic Number",value:String(num)},
        {label:"Length",value:result.length+" symbols"},
        {label:"Largest symbol",value:result[0]||"-"},
      ]
    }
  } else {
    const str=(value||"").toUpperCase().trim()
    if(!/^[IVXLCDM]+$/.test(str)) throw new Error("Enter valid Roman numerals (I, V, X, L, C, D, M).")
    const vals={I:1,V:5,X:10,L:50,C:100,D:500,M:1000}
    let total=0
    for(let i=0;i<str.length;i++){
      const curr=vals[str[i]],next=vals[str[i+1]]
      if(next&&curr<next) total-=curr
      else total+=curr
    }
    return {
      value:String(total),
      gaugeValue:Math.min(total/3999*100,100),
      breakdown:[str+" = "+total,"Parsed symbol by symbol: "+str.split("").map((c,i)=>{const curr=vals[c],next=vals[str[i+1]];return c+"("+(next&&curr<next?"-":"+")+(vals[c])+")"}).join(" ")],
      stats:[
        {label:"Arabic Number",value:String(total)},
        {label:"Roman Numeral",value:str},
        {label:"Valid",value:"Yes"},
        {label:"Length",value:str.length+" symbols"},
      ]
    }
  }
""",
  """{id:"mode",label:"Direction",type:"select",options:[
              {value:"to_roman",label:"Number → Roman Numerals"},
              {value:"to_arabic",label:"Roman Numerals → Number"},
            ],defaultValue:"to_roman"},
            {id:"value",label:"Value to convert",type:"text",placeholder:"2024 or MMXXIV",defaultValue:"2024"}""",
  [("Small (I-XIX)","#22c55e",0,5),("Medium (XX-C)","#3b82f6",5,30),("Large (C-M)","#f59e0b",30,80),("Very large (M+)","#ef4444",80,100)],
  "% of 3999","3999",
  [("How do Roman numerals work?","Roman numerals use letters: I=1, V=5, X=10, L=50, C=100, D=500, M=1000. Read left to right adding values. When a smaller numeral precedes a larger one, subtract it: IV=4 (5-1), IX=9 (10-1), XL=40, XC=90, CD=400, CM=900. Example: 2024 = MMXXIV = 1000+1000+10+10+4."),
   ("What is the largest number in Roman numerals?","Standard Roman numerals go to 3,999 (MMMCMXCIX). For larger numbers, a bar over a letter multiplied by 1,000: V-bar = 5,000, X-bar = 10,000, M-bar = 1,000,000. This is called vinculum notation and allows representation of millions."),
   ("What are the Roman numeral rules?","Maximum 3 of same symbol in a row (III is valid, IIII is not — use IV). Subtraction: only I before V or X, X before L or C, C before D or M. Never subtract more than one symbol at once (not IIX for 8 — use VIII). Symbols decrease in value from left to right (except subtractive pairs)."),
   ("When are Roman numerals used today?","Clock faces (some use IIII instead of IV). Movie copyright dates and sequel numbering (Rocky IV). Super Bowl and Olympic Games numbering. Chapter numbers in books and outlines. Building inscriptions. Monarchs and popes (Henry VIII, Pope Francis I). Astronomy (planetary moons: Io, Europa, etc. are Jupiter I, II)."),
   ("Why did the Romans not have a zero?","Roman numeral systems developed as a counting notation — tallying quantities that exist. Zero represents the absence of quantity, which was not needed for Roman commerce or administration. Zero was developed independently in ancient India and the Maya civilization. Arab traders brought Indian zero to Europe in the Middle Ages.")],
  [("Number to Words Calculator","/calculators/number-to-words-calculator"),("Number Base Calculator","/calculators/number-base-calculator"),("Average Calculator","/calculators/average-calculator"),("Percentage Calculator","/calculators/percentage-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Roman Numeral Symbols</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700"><th class="text-left">Symbol</th><th class="text-right">Value</th></tr></thead>
            <tbody class="text-blue-900 font-mono">
              {[["I",1],["V",5],["X",10],["L",50],["C",100],["D",500],["M",1000]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5 font-bold">{r[0]}</td><td class="text-right">{r[1]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Common Roman Numeral Examples</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Roman</th><th class="p-2 text-xs font-semibold text-right">Number</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["I",1],["IV",4],["IX",9],["XIV",14],["XL",40],["XC",90],["CD",400],["CM",900],["MMXXIV",2024],["MMMDCCCLXXXVIII",3888]].map(r => (
              <tr><td class="p-2 text-xs font-mono font-bold">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Subtractive Pairs</h2>
        <div class="space-y-2">
          {[["IV","4 (5-1)"],["IX","9 (10-1)"],["XL","40 (50-10)"],["XC","90 (100-10)"],["CD","400 (500-100)"],["CM","900 (1000-100)"]].map(([r,v]) => (
            <div class="flex justify-between bg-gray-50 rounded-lg px-3 py-1.5 text-xs"><span class="font-mono font-bold text-blue-700">{r}</span><span class="text-gray-600">= {v}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Roman Numeral","Convert between numbers and Roman numerals")

# ── SPEED ─────────────────────────────────────────────────────────────────────
w("speed","Speed Converter","Other","other",
  "Speed Converter: mph, km/h, m/s, knots, Mach",
  "Convert speed between mph, km/h, m/s, knots, and Mach number. Free speed converter with distance and time calculator.",
  """
  const value = parseFloat(inputs.value)||0
  const from = inputs.from||"mph"
  if(value<0) throw new Error("Enter a non-negative speed.")
  const toMs = {
    mph:0.44704, kmh:1/3.6, ms:1, knots:0.514444, mach:340.29,
    fps:0.3048, light:299792458
  }
  const ms = value*(toMs[from]||1)
  const mph = ms/toMs.mph
  const kmh = ms*3.6
  const knots = ms/toMs.knots
  const mach = ms/toMs.mach
  const fps = ms/toMs.fps
  const kph = kmh
  return {
    value:mph.toFixed(4)+" mph | "+kmh.toFixed(4)+" km/h",
    gaugeValue:Math.min(mph/200*100,100),
    breakdown:["Input: "+value+" "+from,"mph: "+mph.toFixed(4),"km/h: "+kmh.toFixed(4),"m/s: "+ms.toFixed(4),"knots: "+knots.toFixed(4),"Mach: "+mach.toFixed(6),"ft/s: "+fps.toFixed(4)],
    stats:[
      {label:"mph",value:mph.toFixed(3)},
      {label:"km/h",value:kmh.toFixed(3)},
      {label:"m/s",value:ms.toFixed(3)},
      {label:"Knots",value:knots.toFixed(3)},
    ]
  }
""",
  """{id:"value",label:"Speed value",type:"number",placeholder:"60",min:0,step:0.001,defaultValue:60},
            {id:"from",label:"Convert from",type:"select",options:[
              {value:"mph",label:"Miles per hour (mph)"},
              {value:"kmh",label:"Kilometers per hour (km/h)"},
              {value:"ms",label:"Meters per second (m/s)"},
              {value:"knots",label:"Knots (nautical mph)"},
              {value:"mach",label:"Mach number"},
              {value:"fps",label:"Feet per second (fps)"},
            ],defaultValue:"mph"}""",
  [("Slow (<30mph)","#22c55e",0,15),("Highway (30-80mph)","#3b82f6",15,40),("Fast (80-200mph)","#f59e0b",40,100)],
  "mph","200",
  [("How do I convert mph to km/h?","Multiply mph by 1.60934. Example: 60 mph = 60 × 1.60934 = 96.56 km/h. To convert km/h to mph: divide by 1.60934 (or multiply by 0.6214). Quick mental estimate: km/h ≈ mph × 1.6 (or mph × 8/5)."),
   ("What is a knot in speed?","1 knot = 1 nautical mile per hour = 1.852 km/h = 1.151 mph. Knots are used in aviation and maritime navigation because nautical miles correspond to degrees of latitude (1 nautical mile = 1 arcminute of latitude), making navigation easier. A hurricane is Category 1 at 64-82 knots (74-95 mph)."),
   ("What is Mach 1?","Mach 1 = the speed of sound in air, approximately 343 m/s = 1,235 km/h = 767 mph at sea level (15 degrees C). Mach number = object speed / speed of sound. Subsonic: Mach < 1. Transonic: Mach 0.8-1.2. Supersonic: Mach 1-5. Hypersonic: Mach 5+. The exact value varies with temperature and altitude."),
   ("How fast is the fastest car, plane, and runner?","Fastest production car (2024): Bugatti Bolide ~500 km/h (311 mph). Fastest jet aircraft: SR-71 Blackbird at Mach 3.3 (3,540 km/h, 2,200 mph). Fastest human runner: Usain Bolt at 44.72 km/h (27.79 mph) in 2009. International Space Station: 28,000 km/h (17,500 mph)."),
   ("What is escape velocity?","Escape velocity is the speed needed to break free from a celestial body gravity without further propulsion. Earth: 11.2 km/s = 40,320 km/h = 25,054 mph. Moon: 2.38 km/s. Mars: 5.03 km/s. Jupiter: 59.5 km/s. The Sun: 617.5 km/s. Rockets do not need to reach this instantly — they can use thrust continuously.")],
  [("Distance Calculator","/calculators/distance-calculator"),("Fuel Cost Calculator","/calculators/fuel-cost-calculator"),("Unit Converter","/calculators/unit-converter-calculator"),("Pace Calculator","/calculators/pace-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Speed Reference Points</h3>
          <div class="text-xs text-blue-800 space-y-1">
            {[["Walking","3-4 mph / 5-6 km/h"],["Cycling","12-15 mph / 20-24 km/h"],["Car (highway)","65-75 mph / 105-120 km/h"],["Commercial jet","550-600 mph / 885-965 km/h"],["Sound (Mach 1)","767 mph / 1,235 km/h"],["ISS orbit","17,500 mph / 28,000 km/h"]].map(([t,s]) => (
              <div class="flex justify-between border-b border-blue-100 pb-0.5"><span>{t}</span><span class="font-mono">{s}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Speed Conversion Table</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">mph</th><th class="p-2 text-xs text-right">km/h</th><th class="p-2 text-xs text-right">m/s</th><th class="p-2 text-xs text-right">knots</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[[10,16.1,4.5,8.7],[30,48.3,13.4,26.1],[55,88.5,24.6,47.8],[65,104.6,29.1,56.5],[75,120.7,33.5,65.2],[100,160.9,44.7,86.9],[200,321.9,89.4,173.8]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td><td class="p-2 text-xs text-right">{r[3]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Time / Distance / Speed</h2>
        <div class="bg-gray-50 rounded-xl p-4 text-xs text-gray-600 space-y-2">
          <div class="font-mono text-blue-700">Speed = Distance / Time</div>
          <div class="font-mono text-blue-700">Distance = Speed × Time</div>
          <div class="font-mono text-blue-700">Time = Distance / Speed</div>
          <div class="mt-2">At 60 mph: 1 mile per minute</div>
          <div>At 100 km/h: 1 km per 36 seconds</div>
          <div>Light travels 300,000 km in 1 second</div>
        </div>
      </div>
    </div>""",
  "Speed","Convert speeds between mph, km/h, m/s, knots, and Mach")

# ── SHOE SIZE ─────────────────────────────────────────────────────────────────
w("shoe-size","Shoe Size Converter","Other","other",
  "Shoe Size Converter: US, UK, EU, CM Sizes",
  "Convert shoe sizes between US, UK, European (EU), and centimeter sizing for men and women. Free shoe size converter chart.",
  """
  const size = parseFloat(inputs.size)||0
  const from = inputs.from||"us_men"
  const gender = inputs.gender||"men"
  if(size<=0) throw new Error("Enter a valid shoe size.")
  let usMen, usWomen, uk, eu, cm
  const toUSMen = {
    us_men: s=>s,
    us_women: s=>s-1.5,
    uk: s=>s+0.5,
    eu: s=>(s-31.5)/0.667,
    cm: s=>(s-9.3)/0.85
  }
  usMen = (toUSMen[from]||toUSMen.us_men)(size)
  usWomen = usMen+1.5
  uk = usMen-0.5
  eu = Math.round(usMen*0.667+31.5)
  cm = (usMen*0.85+9.3).toFixed(1)
  return {
    value:"US Men: "+usMen.toFixed(1)+" | EU: "+eu+" | UK: "+uk.toFixed(1),
    gaugeValue:Math.min(usMen/18*100,100),
    breakdown:["Input: "+size+" ("+from.replace("_"," ")+")","US Men: "+usMen.toFixed(1),"US Women: "+usWomen.toFixed(1),"UK: "+uk.toFixed(1),"EU: "+eu,"CM (foot length): "+cm+" cm"],
    stats:[
      {label:"US Men",value:usMen.toFixed(1)},
      {label:"US Women",value:usWomen.toFixed(1)},
      {label:"EU",value:String(eu)},
      {label:"UK",value:uk.toFixed(1)},
    ]
  }
""",
  """{id:"size",label:"Shoe size",type:"number",placeholder:"10",min:0,step:0.5,defaultValue:10},
            {id:"from",label:"Size system",type:"select",options:[
              {value:"us_men",label:"US Men"},
              {value:"us_women",label:"US Women"},
              {value:"uk",label:"UK"},
              {value:"eu",label:"EU (European)"},
              {value:"cm",label:"CM (foot length in cm)"},
            ],defaultValue:"us_men"}""",
  [("Small (US < 7)","#22c55e",0,38),("Average (US 7-11)","#3b82f6",38,61),("Large (US 11+)","#f59e0b",61,100)],
  "% of size 18","18",
  [("How do I convert US to EU shoe sizes?","EU = (US men size × 0.667) + 31.5, rounded to nearest whole. US Men 10 ≈ EU 43. US Men 11 ≈ EU 44. US Women are typically 1.5 sizes larger than US Men (US Women 10 = US Men 8.5 = EU 42). Always try shoes on as brands and styles vary."),
   ("What is the difference between US men and women sizes?","US Women sizes are 1.5 larger than US Men sizes. A US Women 8 = US Men 6.5. When shopping men shoes as a woman or vice versa: subtract 1.5 for women buying men shoes, add 1.5 for men buying women shoes. UK and EU sizes are unisex (usually men sizing)."),
   ("How do I measure my foot for shoe size?","Trace your foot on paper, measure the longest distance (heel to longest toe) in centimeters. Use this chart: 22cm = EU35, 23cm = EU36, 24cm = EU37, 25cm = EU38/39, 26cm = EU40, 27cm = EU41/42, 28cm = EU43, 29cm = EU44/45. Measure both feet — buy for the larger one."),
   ("How do UK and EU shoe sizes compare?","UK size = EU size - 33 (approximately). UK 7 ≈ EU 40. UK 8 ≈ EU 42. UK 9 ≈ EU 43. UK 10 ≈ EU 44. UK 11 ≈ EU 46. UK sizes are similar to US Men but typically 0.5 size smaller: US Men 10 = UK 9.5. UK and US women sizes differ by about 2 sizes."),
   ("Why do shoe sizes vary between brands?","Shoe sizes are not standardized internationally and vary by: country system (US, UK, EU, JP). Brand and model (some brands run narrow or wide). Style (sneakers vs dress shoes vs boots). Manufacturers develop lasts (foot-shaped forms) to their own specifications. Always check individual brand sizing charts and read reviews about fit.")],
  [("Height Converter","/calculators/height-converter-calculator"),("BMI Calculator","/calculators/bmi-calculator"),("Unit Converter","/calculators/unit-converter-calculator"),("Age Calculator","/calculators/age-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Men Size Chart</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700"><th class="text-left">US</th><th>UK</th><th>EU</th><th class="text-right">CM</th></tr></thead>
            <tbody class="text-blue-900">
              {[[7,6.5,40,25],[8,7.5,41,26],[9,8.5,42,27],[10,9.5,43,28],[11,10.5,44,29],[12,11.5,45,30],[13,12.5,47,31]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-center">{r[1]}</td><td class="text-center">{r[2]}</td><td class="text-right">{r[3]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Women Shoe Size Chart</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">US Women</th><th class="p-2 text-xs text-right">US Men</th><th class="p-2 text-xs text-right">EU</th><th class="p-2 text-xs text-right">UK</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[[5,3.5,36,3],[6,4.5,37,4],[7,5.5,38,5],[8,6.5,39,6],[9,7.5,40,7],[10,8.5,41,8],[11,9.5,42,9]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td><td class="p-2 text-xs text-right">{r[3]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Finding Your Size</h2>
        <div class="space-y-2">
          {["Measure foot at end of day (feet swell throughout the day)","Measure both feet — use the larger foot for sizing","Stand while measuring — feet spread under weight","Trace foot on paper, measure longest dimension","Add 0.5-1cm (0.2-0.4in) for toe space in closed shoes","Check brand specific sizing guides — they vary significantly"].map(t => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{t}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Size","Convert shoe sizes between US, UK, EU, and cm")

# ── ZODIAC ───────────────────────────────────────────────────────────────────
w("zodiac","Zodiac Sign Calculator","Other","other",
  "Zodiac Sign Calculator: Find Your Astrology Sign & Traits",
  "Find your zodiac sign from any birthday. Learn about your sun sign traits, compatibility, and element. Free zodiac calculator.",
  """
  const dob = inputs.dob||""
  if(!dob) throw new Error("Enter your date of birth.")
  const d = new Date(dob+"T00:00:00")
  if(isNaN(d.getTime())) throw new Error("Invalid date.")
  const month=d.getMonth()+1,day=d.getDate()
  const signs=[
    {name:"Capricorn",start:[12,22],end:[1,19],element:"Earth",ruling:"Saturn",traits:"Ambitious, disciplined, practical, patient"},
    {name:"Aquarius",start:[1,20],end:[2,18],element:"Air",ruling:"Uranus",traits:"Independent, progressive, humanitarian, analytical"},
    {name:"Pisces",start:[2,19],end:[3,20],element:"Water",ruling:"Neptune",traits:"Compassionate, artistic, intuitive, gentle"},
    {name:"Aries",start:[3,21],end:[4,19],element:"Fire",ruling:"Mars",traits:"Bold, competitive, energetic, pioneering"},
    {name:"Taurus",start:[4,20],end:[5,20],element:"Earth",ruling:"Venus",traits:"Reliable, patient, practical, devoted, stubborn"},
    {name:"Gemini",start:[5,21],end:[6,20],element:"Air",ruling:"Mercury",traits:"Adaptable, communicative, witty, curious"},
    {name:"Cancer",start:[6,21],end:[7,22],element:"Water",ruling:"Moon",traits:"Nurturing, loyal, intuitive, protective, moody"},
    {name:"Leo",start:[7,23],end:[8,22],element:"Fire",ruling:"Sun",traits:"Generous, warm, theatrical, creative, proud"},
    {name:"Virgo",start:[8,23],end:[9,22],element:"Earth",ruling:"Mercury",traits:"Analytical, meticulous, reliable, practical"},
    {name:"Libra",start:[9,23],end:[10,22],element:"Air",ruling:"Venus",traits:"Diplomatic, fair, social, cooperative, indecisive"},
    {name:"Scorpio",start:[10,23],end:[11,21],element:"Water",ruling:"Pluto",traits:"Intense, resourceful, brave, passionate, secretive"},
    {name:"Sagittarius",start:[11,22],end:[12,21],element:"Fire",ruling:"Jupiter",traits:"Optimistic, adventurous, honest, free-spirited"},
  ]
  let found=signs.find(s=>{
    const [sm,sd]=s.start,[em,ed]=s.end
    if(sm>em) return (month===sm&&day>=sd)||(month===em&&day<=ed)
    return (month===sm&&day>=sd)||(month===em&&day<=ed)||(month>sm&&month<em)
  })
  if(!found) found=signs[0]
  const elementColor={Fire:"#ef4444",Earth:"#a16207",Air:"#3b82f6",Water:"#06b6d4"}[found.element]
  return {
    value:found.name+" ("+found.element+")",
    gaugeValue:signs.indexOf(found)/11*100,
    breakdown:["Birthday: "+d.toDateString(),"Sun Sign: "+found.name,"Element: "+found.element,"Ruling Planet: "+found.ruling,"Traits: "+found.traits],
    stats:[
      {label:"Zodiac Sign",value:found.name},
      {label:"Element",value:found.element},
      {label:"Ruling Planet",value:found.ruling},
      {label:"Key Traits",value:found.traits.split(",")[0]+","+found.traits.split(",")[1]},
    ]
  }
""",
  """{id:"dob",label:"Date of birth",type:"date",defaultValue:"1990-03-21"}""",
  [("Fire signs","#ef4444",0,25),("Earth signs","#a16207",25,50),("Air signs","#3b82f6",50,75),("Water signs","#06b6d4",75,100)],
  "sign position","100",
  [("What are the 12 zodiac signs and their dates?","Aries (Mar 21-Apr 19), Taurus (Apr 20-May 20), Gemini (May 21-Jun 20), Cancer (Jun 21-Jul 22), Leo (Jul 23-Aug 22), Virgo (Aug 23-Sep 22), Libra (Sep 23-Oct 22), Scorpio (Oct 23-Nov 21), Sagittarius (Nov 22-Dec 21), Capricorn (Dec 22-Jan 19), Aquarius (Jan 20-Feb 18), Pisces (Feb 19-Mar 20)."),
   ("What are the four zodiac elements?","Fire (Aries, Leo, Sagittarius): passionate, energetic, impulsive. Earth (Taurus, Virgo, Capricorn): practical, reliable, grounded. Air (Gemini, Libra, Aquarius): intellectual, communicative, social. Water (Cancer, Scorpio, Pisces): emotional, intuitive, deep. Same element signs are often compatible."),
   ("What is the difference between Sun sign, Moon sign, and Rising sign?","Sun sign (your usual horoscope sign) represents your core identity. Moon sign (sign at the time the moon was in) represents emotions and inner self. Rising sign (Ascendant — sign on the eastern horizon at birth) represents how others see you. A full natal chart uses all planetary positions at your exact birth time and location."),
   ("What are the most compatible zodiac signs?","Generally: Fire signs (Aries, Leo, Sag) pair well with Air signs (Gemini, Libra, Aquarius). Earth signs (Taurus, Virgo, Cap) pair well with Water signs (Cancer, Scorpio, Pisces). Same-element pairings can be compatible but sometimes too similar. Opposites (Aries-Libra, Taurus-Scorpio) often attract each other."),
   ("Is astrology scientifically valid?","No scientific study has found reliable evidence that birth dates or astrological signs predict personality, relationships, or life events. The Barnum effect (people accept vague personality descriptions as accurate when told they are personalized) explains why horoscopes often feel accurate. Astrology is a cultural tradition and can be used as a tool for self-reflection and entertainment.")],
  [("Love Calculator","/calculators/love-calculator"),("Numerology Calculator","/calculators/numerology-calculator"),("Age Calculator","/calculators/age-calculator"),("Date Calculator","/calculators/date-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Zodiac Wheel</h3>
          <div class="text-xs text-blue-800 space-y-0.5">
            {[["Aries","Mar 21 - Apr 19","Fire"],["Taurus","Apr 20 - May 20","Earth"],["Gemini","May 21 - Jun 20","Air"],["Cancer","Jun 21 - Jul 22","Water"],["Leo","Jul 23 - Aug 22","Fire"],["Virgo","Aug 23 - Sep 22","Earth"]].map(([s,d,e]) => (
              <div class="border-b border-blue-100 pb-0.5 flex justify-between"><span class="font-semibold">{s}</span><span class="text-blue-600">{d}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">All 12 Signs</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Sign</th><th class="p-2 text-xs text-right">Dates</th><th class="p-2 text-xs text-right">Element</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Aries","Mar 21-Apr 19","Fire"],["Taurus","Apr 20-May 20","Earth"],["Gemini","May 21-Jun 20","Air"],["Cancer","Jun 21-Jul 22","Water"],["Leo","Jul 23-Aug 22","Fire"],["Virgo","Aug 23-Sep 22","Earth"],["Libra","Sep 23-Oct 22","Air"],["Scorpio","Oct 23-Nov 21","Water"],["Sagittarius","Nov 22-Dec 21","Fire"],["Capricorn","Dec 22-Jan 19","Earth"],["Aquarius","Jan 20-Feb 18","Air"],["Pisces","Feb 19-Mar 20","Water"]].map(r => (
              <tr><td class="p-2 text-xs font-medium">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Element Compatibility</h2>
        <div class="space-y-3">
          {[
            {e:"Fire + Air",r:"High compatibility",d:"Fire inspires, Air fuels — both love adventure and ideas."},
            {e:"Earth + Water",r:"High compatibility",d:"Earth provides stability, Water brings emotional depth."},
            {e:"Same Element",r:"Good compatibility",d:"Understand each other naturally but may be too similar."},
            {e:"Fire + Water",r:"Challenging",d:"Passion and emotion can clash or extinguish each other."},
            {e:"Earth + Air",r:"Challenging",d:"Practical vs intellectual — can complement if balanced."},
          ].map(c => (
            <div class="bg-gray-50 rounded-lg p-2"><div class="font-semibold text-xs text-blue-700">{c.e} <span class="text-gray-500">— {c.r}</span></div><div class="text-xs text-gray-600">{c.d}</div></div>
          ))}
        </div>
      </div>
    </div>""",
  "Zodiac Sign","Find your zodiac sun sign and learn about traits and compatibility")

# ── CRYPTO ───────────────────────────────────────────────────────────────────
w("crypto","Crypto Calculator","Other","other",
  "Crypto Calculator: Convert Crypto to USD & Calculate Gains",
  "Calculate cryptocurrency value in USD, profit/loss, and percent return. Supports Bitcoin, Ethereum, and major cryptos. Free crypto calculator.",
  """
  const amount = parseFloat(inputs.amount)||0
  const price = parseFloat(inputs.price)||0
  const buyCost = parseFloat(inputs.buyCost)||0
  if(amount<=0) throw new Error("Enter an amount of cryptocurrency.")
  if(price<=0) throw new Error("Enter the current price.")
  const currentValue = amount*price
  let profitLoss=0, pctReturn=0, breakEvenPrice=0
  if(buyCost>0){
    profitLoss=currentValue-buyCost
    pctReturn=(profitLoss/buyCost)*100
    breakEvenPrice=buyCost/amount
  }
  return {
    value:"$"+currentValue.toFixed(2)+" USD",
    gaugeValue:buyCost>0?Math.min(Math.max(pctReturn+50,0),100):50,
    breakdown:["Amount: "+amount+" coins/tokens","Current price: $"+price,"Current value: $"+currentValue.toFixed(2),...(buyCost>0?["Cost basis: $"+buyCost,"Profit/Loss: $"+profitLoss.toFixed(2)+(profitLoss>=0?" (profit)":" (loss)"),"Return: "+pctReturn.toFixed(2)+"%","Break-even price: $"+breakEvenPrice.toFixed(4)]:["Enter buy cost for P&L"])],
    stats:[
      {label:"Current Value",value:"$"+currentValue.toFixed(2)},
      {label:"Profit/Loss",value:buyCost>0?"$"+profitLoss.toFixed(2):"Enter buy cost"},
      {label:"Return",value:buyCost>0?pctReturn.toFixed(2)+"%":"Enter buy cost"},
      {label:"Break-Even",value:buyCost>0?"$"+breakEvenPrice.toFixed(4):"Enter buy cost"},
    ]
  }
""",
  """{id:"amount",label:"Amount (coins/tokens)",type:"number",placeholder:"0.5",min:0,step:0.000001,defaultValue:0.5},
            {id:"price",label:"Current price ($ USD)",type:"number",placeholder:"45000",min:0,step:0.01,defaultValue:45000},
            {id:"buyCost",label:"Total buy cost ($ — optional for P&L)",type:"number",placeholder:"20000",min:0,step:0.01,defaultValue:20000}""",
  [("Loss (< -20%)","#ef4444",0,30),("Small gain","#f59e0b",30,55),("Good gain (20%+)","#3b82f6",55,75),("Large gain (50%+)","#22c55e",75,100)],
  "return gauge","100",
  [("How do I calculate my crypto profit or loss?","Profit = Current Value - Cost Basis. Current Value = Amount × Current Price. Cost Basis = total amount paid (including fees). % Return = (Profit / Cost Basis) × 100. Example: bought 0.5 BTC for $20,000, now worth $25,000: Profit = $5,000, Return = 25%."),
   ("What is the break-even price for crypto?","Break-even price = Total cost paid / Number of coins. If you paid $20,000 for 0.5 BTC: break-even = $20,000 / 0.5 = $40,000 per BTC. The price must exceed $40,000 for you to be in profit. This is also called your average cost basis per coin."),
   ("How are crypto gains taxed in the US?","IRS treats crypto as property. Short-term gains (held <1 year): taxed as ordinary income (10-37%). Long-term gains (held >1 year): taxed at 0%, 15%, or 20% depending on income. Each sale, trade, or crypto-to-crypto exchange is a taxable event. You must report gains/losses on Form 8949. Keep detailed records of all transactions."),
   ("What is dollar-cost averaging (DCA) in crypto?","DCA means investing a fixed amount at regular intervals (e.g., $100 every week in Bitcoin) regardless of price. This reduces the impact of volatility — you buy more when prices are low and less when high. DCA lowers your average cost basis over time and removes the need to time the market perfectly."),
   ("What is market cap in cryptocurrency?","Market cap = Total coins in circulation × Current price. It represents the total value of a cryptocurrency. Bitcoin market cap: ~$800B-$1T at peak. Used to rank cryptocurrencies by size. Large cap (>$10B) are generally less volatile. Small cap (<$1B) are riskier but potentially higher reward.")],
  [("Investment Calculator","/calculators/investment-calculator"),("ROI Calculator","/calculators/roi-calculator"),("Compound Interest Calculator","/calculators/compound-interest-calculator"),("Savings Calculator","/calculators/savings-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Crypto Tax Overview (US)</h3>
          <div class="text-xs text-blue-800 space-y-1">
            <div><span class="font-semibold">Short-term gain</span> (held &lt;1yr)</div>
            <div>Taxed as ordinary income (10-37%)</div>
            <div class="mt-1"><span class="font-semibold">Long-term gain</span> (held &gt;1yr)</div>
            <div>0%, 15%, or 20% capital gains rate</div>
            <div class="mt-1">⚠ Crypto-to-crypto trades are taxable</div>
            <div>⚠ Keep records of ALL transactions</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Crypto Risk Levels</h2>
        <div class="space-y-2">
          {[
            {t:"Large Cap (BTC, ETH)",r:"High",d:"Most liquid, least volatile among crypto. Still very volatile vs stocks."},
            {t:"Mid Cap (top 20-50)",r:"Very High",d:"Established projects but smaller. 2-3× more volatile than BTC."},
            {t:"Small Cap (top 50-200)",r:"Extreme",d:"Can gain or lose 90%+ in weeks. High research required."},
            {t:"Meme coins / New tokens",r:"Speculative",d:"Extremely high risk of total loss. Often pump-and-dump schemes."},
          ].map(c => (
            <div class="bg-gray-50 rounded-lg p-2"><div class="font-semibold text-xs text-blue-700">{c.t} — {c.r} risk</div><div class="text-xs text-gray-600">{c.d}</div></div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Key Crypto Metrics</h2>
        <div class="space-y-2">
          {["Market Cap = Price × Circulating Supply","Volume: higher = more liquidity and price discovery","Circulating vs max supply affects inflation potential","24h change: crypto markets run 24/7/365 unlike stocks","All-time high (ATH) and all-time low (ATL) — key reference points","Hash rate (PoW) and staking (PoS) affect network security"].map(m => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{m}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "USD Value","Calculate crypto value, profit, and return on investment")

# ── ROOF PITCH ────────────────────────────────────────────────────────────────
w("roof-pitch","Roof Pitch Calculator","Other","other",
  "Roof Pitch Calculator: Angle, Rise, Run & Rafter Length",
  "Calculate roof pitch (slope), angle in degrees, rafter length, and roof area multiplier from rise and run. Free roof pitch calculator.",
  """
  const rise = parseFloat(inputs.rise)||0
  const run = parseFloat(inputs.run)||12
  if(rise<0) throw new Error("Rise must be non-negative.")
  if(run<=0) throw new Error("Run must be positive.")
  const pitch = rise/run
  const angleDeg = Math.atan(pitch)*180/Math.PI
  const rafterFactor = Math.sqrt(rise*rise+run*run)/run
  const exampleRoofRun = parseFloat(inputs.roofRun)||20
  const rafterLength = exampleRoofRun*rafterFactor
  const areaMultiplier = rafterFactor
  const commonPitches=[[3,12],[4,12],[6,12],[8,12],[12,12]]
  return {
    value:rise+"/12 pitch | "+angleDeg.toFixed(2)+"° angle",
    gaugeValue:Math.min(angleDeg/45*100,100),
    breakdown:["Pitch: "+rise+"/"+run+" ("+rise+"-in-12 notation: "+rise*(12/run).toFixed(2)+"/12)","Angle: "+angleDeg.toFixed(4)+" degrees","Slope %: "+(pitch*100).toFixed(2)+"%","Rafter factor: "+rafterFactor.toFixed(4)+" (multiply horizontal run by this)","Rafter for "+exampleRoofRun+"ft run: "+rafterLength.toFixed(2)+" ft","Area multiplier: "+areaMultiplier.toFixed(4)+"× flat area"],
    stats:[
      {label:"Pitch",value:rise*(12/run).toFixed(1)+"/12"},
      {label:"Angle",value:angleDeg.toFixed(2)+"°"},
      {label:"Rafter Factor",value:rafterFactor.toFixed(4)},
      {label:"Rafter Length",value:rafterLength.toFixed(2)+" ft"},
    ]
  }
""",
  """{id:"rise",label:"Rise (inches, for 12 inches of run)",type:"number",placeholder:"6",min:0,step:0.5,defaultValue:6},
            {id:"run",label:"Run (usually 12 for standard notation)",type:"number",placeholder:"12",min:1,step:1,defaultValue:12},
            {id:"roofRun",label:"Horizontal roof run (ft, for rafter length calculation)",type:"number",placeholder:"20",min:0,step:0.5,defaultValue:20}""",
  [("Low pitch (0-3/12)","#22c55e",0,25),("Common (4-6/12)","#3b82f6",25,50),("Steep (7-12/12)","#f59e0b",50,100)],
  "% of 45 degrees","45",
  [("What is roof pitch and how is it expressed?","Roof pitch is the slope of a roof expressed as rise over run. Standard notation: X/12 where X is how many inches the roof rises for every 12 inches of horizontal run. A 6/12 pitch rises 6 inches for every foot of run. It is equivalent to 26.6 degrees and is one of the most common residential pitches."),
   ("What is the minimum and maximum roof pitch?","Minimum for asphalt shingles: 2/12 (with underlayment). Flat roofs: 1/4:12 to 1/2:12 (uses membrane, not shingles). Common residential: 4/12 to 9/12. Steep: 9/12 to 12/12. Extra steep or mansard: above 12/12. Low-pitch roofs need more waterproofing attention; steep roofs shed water better but cost more to build."),
   ("How do I calculate rafter length?","Rafter length = horizontal run × rafter factor. Rafter factor = sqrt(rise² + run²) / run. For 6/12 pitch: factor = sqrt(36+144)/12 = sqrt(180)/12 = 1.118. If roof run is 20 feet: rafter length = 20 × 1.118 = 22.36 feet. Add overhang/eave length and ridge board deduction for actual cut length."),
   ("How does roof pitch affect material quantities?","Higher pitch = more surface area = more materials. Multiply the flat footprint area by the rafter factor to get actual roof area. For a 6/12 pitch, factor = 1.118: a 2,000 sq ft footprint needs 2,000 × 1.118 = 2,236 sq ft of roofing. Steeper roofs also require more care and labor, increasing cost."),
   ("What roof pitch is best for my climate?","Steep pitch (8/12+): heavy snow loads (steep sheds snow faster). High rainfall areas: 4/12+ for good runoff. Hot dry climates: lower pitch acceptable since rainfall is rare. Hurricane/wind: lower pitch with proper fasteners — steep roofs catch more wind. Architectural preference and HOA rules also affect pitch choice.")],
  [("Concrete Calculator","/calculators/concrete-calculator"),("Area Calculator","/calculators/area-calculator"),("Paint Calculator","/calculators/paint-calculator"),("Angle Converter","/calculators/angle-converter-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Common Pitches</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700"><th class="text-left">Pitch</th><th class="text-right">Angle</th><th class="text-right">Factor</th></tr></thead>
            <tbody class="text-blue-900 font-mono">
              {[["2/12","9.5°","1.014"],["4/12","18.4°","1.054"],["6/12","26.6°","1.118"],["8/12","33.7°","1.202"],["12/12","45.0°","1.414"]].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right">{r[1]}</td><td class="text-right">{r[2]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Minimum Slope by Material</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Roofing Material</th><th class="p-2 text-xs font-semibold text-right">Min Pitch</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["Built-up (flat roof)","1/4:12"],["Modified bitumen","1/2:12 to 1:12"],["Metal standing seam","1/4:12"],["Clay/concrete tile","2.5:12"],["Asphalt shingles","2:12 (w/ice barrier)"],["Wood shingles","3:12"],["Slate","4:12"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-medium">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Roof Pitch Tips</h2>
        <div class="space-y-2">
          {["Standard notation: rise/12 (e.g., 6/12 means 6 inches per foot)","Use a level and tape measure: hold 12in level horizontally at roof, measure rise","Rafter factor × horizontal run = rafter length (before overhang)","Area multiplier × flat footprint = actual shingle area needed","Add 10-15% waste to material estimates for cutting","Steep pitches need extra safety equipment for installation"].map(t => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{t}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Pitch","Calculate roof pitch angle, rafter length, and area multiplier")

# ── TIME (duration) ───────────────────────────────────────────────────────────
w("time","Time Calculator","Other","other",
  "Time Calculator: Add, Subtract & Convert Hours Minutes Seconds",
  "Add or subtract time durations. Convert between hours, minutes, seconds, and days. Calculate elapsed time. Free time calculator.",
  """
  const h1 = parseFloat(inputs.h1)||0
  const m1 = parseFloat(inputs.m1)||0
  const s1 = parseFloat(inputs.s1)||0
  const h2 = parseFloat(inputs.h2)||0
  const m2 = parseFloat(inputs.m2)||0
  const s2 = parseFloat(inputs.s2)||0
  const operation = inputs.operation||"add"
  const toSec = (h,m,s) => h*3600+m*60+s
  const sec1 = toSec(h1,m1,s1)
  const sec2 = toSec(h2,m2,s2)
  let total = operation==="add"?sec1+sec2:sec1-sec2
  const isNeg = total<0
  total = Math.abs(total)
  const rH = Math.floor(total/3600)
  const rM = Math.floor((total%3600)/60)
  const rS = Math.round(total%60)
  const result = (isNeg?"-":"")+(rH>0?rH+"h ":"")+rM+"m "+rS+"s"
  return {
    value:result,
    gaugeValue:Math.min(total/86400*100,100),
    breakdown:["Time 1: "+h1+"h "+m1+"m "+s1+"s = "+sec1+" seconds","Time 2: "+h2+"h "+m2+"m "+s2+"s = "+sec2+" seconds","Operation: "+operation,"Result: "+(isNeg?"-":"")+rH+"h "+rM+"m "+rS+"s","Total seconds: "+total,"Total minutes: "+(total/60).toFixed(2),"Total hours: "+(total/3600).toFixed(4)],
    stats:[
      {label:"Result",value:result},
      {label:"Total Hours",value:(total/3600).toFixed(3)},
      {label:"Total Minutes",value:(total/60).toFixed(2)},
      {label:"Total Seconds",value:String(total)},
    ]
  }
""",
  """{id:"h1",label:"Hours (time 1)",type:"number",placeholder:"2",min:0,step:1,defaultValue:2},
            {id:"m1",label:"Minutes (time 1)",type:"number",placeholder:"30",min:0,max:59,step:1,defaultValue:30},
            {id:"s1",label:"Seconds (time 1)",type:"number",placeholder:"0",min:0,max:59,step:1,defaultValue:0},
            {id:"operation",label:"Operation",type:"select",options:[
              {value:"add",label:"Add (+)"},
              {value:"subtract",label:"Subtract (−)"},
            ],defaultValue:"add"},
            {id:"h2",label:"Hours (time 2)",type:"number",placeholder:"1",min:0,step:1,defaultValue:1},
            {id:"m2",label:"Minutes (time 2)",type:"number",placeholder:"45",min:0,max:59,step:1,defaultValue:45},
            {id:"s2",label:"Seconds (time 2)",type:"number",placeholder:"30",min:0,max:59,step:1,defaultValue:30}""",
  [("< 1 hour","#22c55e",0,4),("1-8 hours","#3b82f6",4,33),("8-24 hours","#f59e0b",33,100)],
  "% of day","100",
  [("How do I add hours and minutes?","Add hours together, then minutes. If minutes exceed 60, carry over to hours. Example: 2h 45m + 1h 30m = 3h 75m = 4h 15m (carry 60 minutes = 1 hour). For larger durations, convert to total seconds first, then convert back to hours/minutes/seconds."),
   ("How do I calculate elapsed time?","Subtract start time from end time. If end < start, add 24 hours (for same-day crossing midnight). Example: 9:45 AM to 2:30 PM = 4 hours 45 minutes. In seconds: end - start = 14h30m - 9h45m = 4h45m = 17,100 seconds. Convert between units freely."),
   ("How many seconds are in a day, week, year?","60 seconds = 1 minute. 3,600 seconds = 1 hour. 86,400 seconds = 1 day. 604,800 seconds = 1 week. 31,536,000 seconds = 1 year (365 days). 31,557,600 seconds = 1 Julian year (365.25 days). Programmers often remember 86400 s/day and 3.15 × 10^7 s/year."),
   ("How do I convert decimal hours to hours and minutes?","0.5 hours = 30 minutes. 0.75 hours = 45 minutes. 2.25 hours = 2 hours 15 minutes. Formula: hours = floor(decimal). minutes = round((decimal - floor(decimal)) × 60). Example: 3.833 hours = 3 hours + (0.833 × 60) = 3 hours 50 minutes."),
   ("How do time zones work?","The Earth is divided into 24 standard time zones, each generally 15 degrees of longitude wide. UTC (Coordinated Universal Time) is the reference. US time zones: Eastern = UTC-5 (winter), UTC-4 (summer); Central = UTC-6/-5; Mountain = UTC-7/-6; Pacific = UTC-8/-7. Daylight Saving Time (DST) shifts clocks forward 1 hour in spring and back in fall (not all regions observe DST).")],
  [("Military Time Calculator","/calculators/military-time-calculator"),("Days Until Calculator","/calculators/days-until-calculator"),("Age Calculator","/calculators/age-calculator"),("Date Calculator","/calculators/date-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Time Conversions</h3>
          <div class="text-xs text-blue-800 font-mono space-y-1">
            <div>1 min = 60 sec</div>
            <div>1 hour = 60 min = 3,600 sec</div>
            <div>1 day = 24h = 86,400 sec</div>
            <div>1 week = 7 days = 604,800 sec</div>
            <div>1 year = 365 days = 8,760 hours</div>
            <div>1 year ≈ 31,536,000 seconds</div>
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Time Addition Example</h2>
        <div class="bg-gray-50 rounded-xl p-4">
          <div class="text-xs text-gray-600 space-y-2 font-mono">
            <div>Add 2h 45m + 1h 30m:</div>
            <div>Hours: 2 + 1 = 3h</div>
            <div>Minutes: 45 + 30 = 75m</div>
            <div>75m ÷ 60 = 1h 15m</div>
            <div class="font-semibold text-blue-700">= 4h 15m</div>
            <div class="mt-2">Or in seconds:</div>
            <div>9,900 + 5,400 = 15,300 sec</div>
            <div class="font-semibold text-blue-700">= 4h 15m 0s</div>
          </div>
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Common Time Calculations</h2>
        <div class="space-y-2">
          {["Workout tracking — total exercise time per week","Work hours — total billable hours in a day or project","Travel — flight duration across time zones","Recipe timing — total preparation + cooking time","Project management — task duration estimation","Payroll — overtime hours above 8h/day or 40h/week"].map(u => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{u}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Duration","Add, subtract, and convert time durations")

# ── CURRENCY ──────────────────────────────────────────────────────────────────
w("currency","Currency Converter","Other","other",
  "Currency Converter: USD, EUR, GBP, JPY & 150+ Currencies",
  "Convert between major world currencies with approximate exchange rates. USD to EUR, GBP, JPY, CAD, AUD, and more. Free currency calculator.",
  """
  const amount = parseFloat(inputs.amount)||1
  const from = inputs.from||"USD"
  const to = inputs.to||"EUR"
  // Approximate rates vs USD (update periodically)
  const rates={USD:1,EUR:0.921,GBP:0.787,JPY:149.5,CAD:1.360,AUD:1.530,CHF:0.896,CNY:7.24,INR:83.1,MXN:17.2,BRL:4.97,KRW:1325,SGD:1.34,HKD:7.82,NOK:10.7,SEK:10.4,DKK:6.89,NZD:1.63,ZAR:18.7,AED:3.67,SAR:3.75,THB:35.1,MYR:4.68,PHP:56.8}
  if(!rates[from]||!rates[to]) throw new Error("Unknown currency. Use USD, EUR, GBP, JPY, etc.")
  const usd=amount/rates[from]
  const result=usd*rates[to]
  const rate=rates[to]/rates[from]
  return {
    value:result.toFixed(4)+" "+to,
    gaugeValue:Math.min(result/1000*100,100),
    breakdown:[amount+" "+from+" = "+result.toFixed(4)+" "+to,"Exchange rate: 1 "+from+" = "+rate.toFixed(4)+" "+to,"Inverse: 1 "+to+" = "+(1/rate).toFixed(4)+" "+from,"In USD: $"+usd.toFixed(4),"Note: Rates are approximate — use a bank or broker for live rates."],
    stats:[
      {label:"Result",value:result.toFixed(2)+" "+to},
      {label:"Exchange Rate",value:"1 "+from+" = "+rate.toFixed(4)+" "+to},
      {label:"Amount",value:amount+" "+from},
      {label:"In USD",value:"$"+usd.toFixed(2)},
    ]
  }
""",
  """{id:"amount",label:"Amount",type:"number",placeholder:"100",min:0,step:0.01,defaultValue:100},
            {id:"from",label:"From currency",type:"select",options:[
              {value:"USD",label:"USD — US Dollar"},
              {value:"EUR",label:"EUR — Euro"},
              {value:"GBP",label:"GBP — British Pound"},
              {value:"JPY",label:"JPY — Japanese Yen"},
              {value:"CAD",label:"CAD — Canadian Dollar"},
              {value:"AUD",label:"AUD — Australian Dollar"},
              {value:"CHF",label:"CHF — Swiss Franc"},
              {value:"CNY",label:"CNY — Chinese Yuan"},
              {value:"INR",label:"INR — Indian Rupee"},
              {value:"MXN",label:"MXN — Mexican Peso"},
              {value:"BRL",label:"BRL — Brazilian Real"},
            ],defaultValue:"USD"},
            {id:"to",label:"To currency",type:"select",options:[
              {value:"EUR",label:"EUR — Euro"},
              {value:"USD",label:"USD — US Dollar"},
              {value:"GBP",label:"GBP — British Pound"},
              {value:"JPY",label:"JPY — Japanese Yen"},
              {value:"CAD",label:"CAD — Canadian Dollar"},
              {value:"AUD",label:"AUD — Australian Dollar"},
              {value:"CHF",label:"CHF — Swiss Franc"},
              {value:"CNY",label:"CNY — Chinese Yuan"},
              {value:"INR",label:"INR — Indian Rupee"},
              {value:"MXN",label:"MXN — Mexican Peso"},
              {value:"AED",label:"AED — UAE Dirham"},
            ],defaultValue:"EUR"}""",
  [("Small amount (<$100)","#22c55e",0,10),("Medium ($100-$1000)","#3b82f6",10,100)],
  "$ value","1000",
  [("What determines exchange rates?","Exchange rates are driven by: Interest rate differentials (higher rates attract foreign capital). Inflation (lower inflation → stronger currency). Trade balance (surplus → stronger). Political stability and economic performance. Market speculation. Central bank interventions. The USD is the world reserve currency, so many commodity prices (oil, gold) are denominated in USD."),
   ("What is the difference between bid and ask exchange rate?","When exchanging currency, banks quote two rates: bid (what they buy at) and ask (what they sell at). The difference is the spread — their profit. Airport exchange booths have the widest spreads (worst rates). Banks and online platforms offer better rates. For large amounts, negotiating the rate is possible."),
   ("How do I get the best exchange rate when traveling?","Best options (best to worst): Notify your bank and use your debit card at local ATMs abroad. Use a no-foreign-transaction-fee credit card. Exchange at a local bank in the destination country. Worst: airport currency exchange booths (high spreads), hotel desks, pre-purchased travelers checks. Never use dynamic currency conversion (DCC) which forces you to pay in your home currency."),
   ("What is purchasing power parity (PPP)?","PPP adjusts exchange rates to account for price differences between countries. The Big Mac Index (by The Economist) is a famous example: if a Big Mac costs $5 in the US and €4 in Europe, the PPP exchange rate is $1.25/€. GDP comparisons often use PPP to give a more accurate picture of economic output and living standards."),
   ("What is the strongest and weakest currency in the world?","Strongest (highest value per unit vs USD, 2024): Kuwaiti Dinar (~$3.27/KWD). Bahraini Dinar (~$2.65). Omani Rial (~$2.60). British Pound (~$1.27). Weakest (largest units per USD): Iranian Rial (~42,000 IRR/USD). Vietnamese Dong (~25,000 VND/USD). Indonesian Rupiah (~15,700 IDR/USD). Note: high units do not mean weak economy.")],
  [("Investment Calculator","/calculators/investment-calculator"),("Inflation Calculator","/calculators/inflation-calculator"),("Savings Calculator","/calculators/savings-calculator"),("Salary Calculator","/calculators/salary-calculator")],
  """        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Major Rates vs USD</h3>
          <div class="text-xs text-blue-800 space-y-1">
            <div class="text-blue-600 text-xs mb-1">Approximate rates (verify for current)</div>
            {[["EUR","~0.92"],["GBP","~0.79"],["JPY","~149"],["CAD","~1.36"],["AUD","~1.53"],["CHF","~0.90"],["CNY","~7.24"],["INR","~83"]].map(([c,r]) => (
              <div class="flex justify-between border-b border-blue-100 pb-0.5"><span class="font-semibold">{c}</span><span class="font-mono">{r}</span></div>
            ))}
          </div>
        </div>""",
  """    <div class="mt-10 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Currency Code Reference</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="p-2 text-xs font-semibold text-left">Code</th><th class="p-2 text-xs font-semibold text-right">Currency</th><th class="p-2 text-xs font-semibold text-right">Country</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["USD","US Dollar","United States"],["EUR","Euro","Eurozone (20 nations)"],["GBP","Pound Sterling","United Kingdom"],["JPY","Yen","Japan"],["CAD","Canadian Dollar","Canada"],["AUD","Australian Dollar","Australia"],["CHF","Swiss Franc","Switzerland"],["CNY/RMB","Chinese Yuan","China"]].map(r => (
              <tr><td class="p-2 text-xs font-mono font-bold">{r[0]}</td><td class="p-2 text-xs">{r[1]}</td><td class="p-2 text-xs text-right text-gray-500">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Exchange Rate Tips</h2>
        <div class="space-y-2">
          {["Use local ATMs abroad for best rates (check your bank fees)","No-foreign-transaction-fee cards save 1-3% on every purchase","Avoid airport exchange — worst rates, up to 10% markup","Set up rate alerts for large transactions","Check the mid-market rate on XE.com for reference","Book flights/hotels in local currency, not USD (avoid DCC)"].map(t => (
            <div class="flex gap-2 text-xs text-gray-600"><span class="text-blue-500 mt-0.5">•</span><span>{t}</span></div>
          ))}
        </div>
      </div>
    </div>""",
  "Converted","Convert between major world currencies")

print(f"\nWritten: {written} pages")
