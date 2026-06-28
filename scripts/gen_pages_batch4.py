#!/usr/bin/env python3
"""Batch 4: Math + Other calculators — average, fraction, ratio, area, volume, triangle, square-root, percentage-error, grade, final-grade, time, roman-numeral, speed, fuel-cost, electricity, word-count, password, paint, concrete, military-time, days-until, height-converter, dog-age, cooking, shoe-size, roof-pitch"""
import os, re

CALC_DIR = "/Users/apple/Documents/Projects/calculators-for-free/src/pages/calculators"

def write(slug, content):
    # Escape apostrophes in single-quoted JS strings
    path = os.path.join(CALC_DIR, f"{slug}-calculator.astro")
    with open(path, 'w') as f:
        f.write(content)
    print(f"  {slug}-calculator.astro")

def make_page(slug, title, category, cat_slug, seo_title, seo_desc, formula, inputs_str, gauge_str, faqs_list, related_list, sidebar_html, content_html, result_label="Result", calc_desc=""):
    """Generate a standard calculator page"""
    faqs_js = "[\n" + "\n".join(f"  {{ question: {repr(q)}, answer: {repr(a)} }}," for q, a in faqs_list) + "\n]"
    # Fix quotes for JS - repr uses double quotes which is fine
    # But we need to make sure apostrophes in answers are fine - they are in double-quoted strings
    related_js = "[\n" + "\n".join(f"    {{ name: {repr(n)}, href: {repr(h)} }}," for n, h in related_list) + "\n  "

    return f'''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
{formula}
`

const faqs = {faqs_js}
---
<Layout
  title={repr(seo_title)}
  description={repr(seo_desc)}
  breadcrumbs={{[
    {{ name: 'Home', href: '/' }},
    {{ name: {repr(category)}, href: {repr('/calculators/' + cat_slug)} }},
    {{ name: {repr(title)}, href: {repr('/calculators/' + slug + '-calculator')} }},
  ]}}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href={repr('/calculators/' + cat_slug)} class="hover:text-blue-600">{category}</a><span>›</span>
      <span class="text-gray-900">{title}</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title={repr(title)}
          description={repr(calc_desc or seo_desc[:80])}
          formulaId={repr(slug)}
          formulaFn={{formulaFn}}
          resultLabel={repr(result_label)}
          inputs={{{inputs_str}}}
          gauge={{{gauge_str}}}
          faqs={{faqs}}
          relatedCalcs={{[{related_js}]}}
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

# ─── AVERAGE ──────────────────────────────────────────────────────────────────
write("average", make_page(
    slug="average",
    title="Average Calculator",
    category="Math",
    cat_slug="math",
    seo_title="Average Calculator: Mean, Median & Mode",
    seo_desc="Calculate the mean, median, and mode of any set of numbers. Free average calculator with full statistical breakdown.",
    formula="""
  const raw = inputs.numbers || ''
  const nums = raw.split(/[,\\s]+/).map(Number).filter(n => !isNaN(n) && n !== undefined)
  if (nums.length === 0) throw new Error('Enter numbers separated by commas or spaces.')
  const mean = nums.reduce((a,b) => a+b, 0) / nums.length
  const sorted = [...nums].sort((a,b) => a-b)
  const mid = Math.floor(sorted.length / 2)
  const median = sorted.length % 2 === 0 ? (sorted[mid-1] + sorted[mid]) / 2 : sorted[mid]
  const freq = {}
  nums.forEach(n => freq[n] = (freq[n]||0) + 1)
  const maxFreq = Math.max(...Object.values(freq))
  const mode = maxFreq > 1 ? Object.keys(freq).filter(k => freq[k] === maxFreq).join(', ') : 'None'
  const variance = nums.reduce((a,b) => a + (b-mean)**2, 0) / nums.length
  const stdDev = Math.sqrt(variance)
  return {
    value: mean.toFixed(4),
    gaugeValue: 50,
    breakdown: ['Count: ' + nums.length, 'Sum: ' + nums.reduce((a,b)=>a+b,0), 'Mean: ' + mean.toFixed(4), 'Median: ' + median, 'Mode: ' + mode, 'Std Dev: ' + stdDev.toFixed(4)],
    stats: [
      { label: 'Mean (Average)', value: mean.toFixed(4) },
      { label: 'Median', value: String(median) },
      { label: 'Mode', value: mode },
      { label: 'Std Deviation', value: stdDev.toFixed(4) },
    ]
  }
""",
    inputs_str="""[
            { id: 'numbers', label: 'Numbers (comma or space separated)', type: 'text', placeholder: '4, 8, 15, 16, 23, 42', defaultValue: '4, 8, 15, 16, 23, 42' },
          ]""",
    gauge_str="""{
            min: 0, max: 100, unit: '%',
            zones: [
              { label: 'Low', color: '#3b82f6', from: 0, to: 33 },
              { label: 'Mid', color: '#22c55e', from: 33, to: 67 },
              { label: 'High', color: '#f59e0b', from: 67, to: 100 },
            ]
          }""",
    faqs_list=[
        ("What is the difference between mean, median, and mode?", "Mean is the arithmetic average (sum divided by count). Median is the middle value when sorted. Mode is the most frequent value. For symmetric distributions, all three are similar. For skewed data (like income), the median is often more representative than the mean."),
        ("When should I use median instead of mean?", "Use median when data is skewed or has outliers. For example, average household income is misleading because billionaires pull it up — median income better represents the typical household. Mean works best for symmetric data without extreme outliers."),
        ("What is standard deviation?", "Standard deviation measures how spread out data is from the mean. Low std dev means values cluster near the mean; high std dev means they spread widely. About 68% of data falls within 1 standard deviation, 95% within 2."),
        ("How do I calculate a weighted average?", "Multiply each value by its weight, sum the results, and divide by the total weight. Example: if a final exam is worth 40% and midterm 60%, and you scored 80 and 70: weighted avg = (80×0.4 + 70×0.6) = 32 + 42 = 74."),
        ("What is the difference between population and sample standard deviation?", "Population std dev divides by N (total count); sample std dev divides by N-1 (Bessel's correction). When your data is a sample from a larger population (most real-world cases), use sample std dev. Our calculator uses population std dev."),
    ],
    related_list=[("Percentage Calculator", "/calculators/percentage-calculator"), ("Grade Calculator", "/calculators/grade-calculator"), ("Z-Score Calculator", "/calculators/z-score-calculator")],
    sidebar_html="""        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Measures of Central Tendency</h3>
          <div class="space-y-2 text-xs text-blue-800">
            <div><strong>Mean:</strong> Sum ÷ Count. Sensitive to outliers.</div>
            <div><strong>Median:</strong> Middle value. Robust to outliers.</div>
            <div><strong>Mode:</strong> Most frequent value. Can be multiple.</div>
          </div>
        </div>
        <div class="bg-green-50 border border-green-200 rounded-xl p-5">
          <h3 class="font-bold text-green-900 mb-2">Quick Example</h3>
          <p class="text-xs text-green-800">Data: 2, 4, 4, 6, 8, 12</p>
          <ul class="text-xs text-green-800 mt-1 space-y-0.5">
            <li>Mean: 36 ÷ 6 = <strong>6</strong></li>
            <li>Median: (4+6) ÷ 2 = <strong>5</strong></li>
            <li>Mode: <strong>4</strong> (appears twice)</li>
          </ul>
        </div>""",
    content_html="""    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">When to Use Each Measure</h2>
        <div class="space-y-3">
          {[
            { measure: 'Mean', use: 'Test scores, temperatures, measurements — symmetric data with no extreme outliers' },
            { measure: 'Median', use: 'Income, home prices, response times — skewed data or when outliers exist' },
            { measure: 'Mode', use: 'Shoe sizes, survey responses, categorical data — most common value matters' },
          ].map(m => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-blue-700 text-sm mb-1">{m.measure}</div>
              <div class="text-xs text-gray-600">{m.use}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Average vs Median: Income Example</h2>
        <p class="text-gray-600 text-sm mb-3">Data: $30k, $35k, $40k, $45k, $200k (one high earner)</p>
        <div class="bg-gray-50 rounded-lg p-4 text-sm">
          <div class="flex justify-between mb-2"><span class="text-gray-600">Mean:</span><span class="font-bold text-red-600">$70,000 — misleading!</span></div>
          <div class="flex justify-between"><span class="text-gray-600">Median:</span><span class="font-bold text-green-600">$40,000 — representative</span></div>
        </div>
        <p class="text-xs text-gray-500 mt-2">The single $200k value pulls the mean far above what most people earn. Median tells the true story.</p>
      </div>
    </div>""",
    result_label="Mean",
    calc_desc="Calculate mean, median, mode, and standard deviation for any set of numbers"
))

# ─── FRACTION ─────────────────────────────────────────────────────────────────
write("fraction", make_page(
    slug="fraction",
    title="Fraction Calculator",
    category="Math",
    cat_slug="math",
    seo_title="Fraction Calculator: Add, Subtract, Multiply & Divide Fractions",
    seo_desc="Add, subtract, multiply, or divide any two fractions instantly. Shows simplified results and decimal equivalents. Free fraction calculator.",
    formula="""
  const n1 = parseInt(inputs.n1) || 0
  const d1 = parseInt(inputs.d1) || 1
  const n2 = parseInt(inputs.n2) || 0
  const d2 = parseInt(inputs.d2) || 1
  const op = inputs.op || 'add'
  if (d1 === 0 || d2 === 0) throw new Error('Denominator cannot be zero.')
  let rn, rd
  if (op === 'add') { rn = n1*d2 + n2*d1; rd = d1*d2 }
  else if (op === 'sub') { rn = n1*d2 - n2*d1; rd = d1*d2 }
  else if (op === 'mul') { rn = n1*n2; rd = d1*d2 }
  else { if (n2 === 0) throw new Error('Cannot divide by zero.'); rn = n1*d2; rd = d1*n2 }
  const gcd = (a,b) => b === 0 ? Math.abs(a) : gcd(b, a%b)
  const g = gcd(Math.abs(rn), Math.abs(rd))
  const sn = rn/g, sd = rd/g
  if (sd < 0) { sn *= -1; sd *= -1 }
  const decimal = sn/sd
  return {
    value: sn + '/' + sd + ' = ' + decimal.toFixed(6),
    gaugeValue: Math.min(Math.abs(decimal) * 50, 100),
    breakdown: ['Unsimplified: ' + rn + '/' + rd, 'Simplified: ' + sn + '/' + sd, 'Decimal: ' + decimal.toFixed(8), 'As mixed number: ' + (Math.abs(sn) >= Math.abs(sd) ? Math.floor(Math.abs(sn/sd)) + ' ' + (Math.abs(sn)%Math.abs(sd)) + '/' + Math.abs(sd) : sn + '/' + sd)],
    stats: [
      { label: 'Result', value: sn + '/' + sd },
      { label: 'Decimal', value: decimal.toFixed(6) },
      { label: 'Percentage', value: (decimal*100).toFixed(2) + '%' },
      { label: 'GCD used', value: String(g) },
    ]
  }
""",
    inputs_str="""[
            { id: 'n1', label: 'Numerator 1', type: 'number', placeholder: '1', defaultValue: 1 },
            { id: 'd1', label: 'Denominator 1', type: 'number', placeholder: '2', defaultValue: 2 },
            { id: 'op', label: 'Operation', type: 'select', options: [
              { value: 'add', label: 'Add (+)' },
              { value: 'sub', label: 'Subtract (−)' },
              { value: 'mul', label: 'Multiply (×)' },
              { value: 'div', label: 'Divide (÷)' },
            ], defaultValue: 'add' },
            { id: 'n2', label: 'Numerator 2', type: 'number', placeholder: '1', defaultValue: 1 },
            { id: 'd2', label: 'Denominator 2', type: 'number', placeholder: '3', defaultValue: 3 },
          ]""",
    gauge_str="""{
            min: 0, max: 100, unit: '% value',
            zones: [
              { label: '0–25%', color: '#3b82f6', from: 0, to: 25 },
              { label: '25–50%', color: '#22c55e', from: 25, to: 50 },
              { label: '50–75%', color: '#f59e0b', from: 50, to: 75 },
              { label: '75–100%', color: '#8b5cf6', from: 75, to: 100 },
            ]
          }""",
    faqs_list=[
        ("How do I add fractions?", "Find a common denominator (LCD), convert both fractions, then add the numerators. Example: 1/3 + 1/4 → LCD=12 → 4/12 + 3/12 = 7/12. Always simplify by dividing numerator and denominator by their GCD."),
        ("How do I multiply fractions?", "Simply multiply numerators together and denominators together. Example: 2/3 × 3/4 = 6/12 = 1/2. Cross-simplification first can make the arithmetic easier."),
        ("How do I divide fractions?", "Multiply the first fraction by the reciprocal (flip) of the second. Example: 2/3 ÷ 3/4 = 2/3 × 4/3 = 8/9. 'Keep, Change, Flip' is the common mnemonic."),
        ("How do I simplify a fraction?", "Find the Greatest Common Divisor (GCD) of numerator and denominator, then divide both by it. Example: 12/18 — GCD(12,18)=6 → 12/6 = 2, 18/6 = 3 → simplified to 2/3."),
        ("What is a mixed number?", "A mixed number combines a whole number and a proper fraction: 2½. To convert: divide numerator by denominator for the whole part; the remainder is the new numerator. Example: 7/3 = 2 remainder 1 = 2 1/3."),
    ],
    related_list=[("Percentage Calculator", "/calculators/percentage-calculator"), ("Ratio Calculator", "/calculators/ratio-calculator"), ("Average Calculator", "/calculators/average-calculator")],
    sidebar_html="""        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Fraction Operations</h3>
          <div class="space-y-2 text-xs text-blue-800 font-mono">
            <div>a/b + c/d = (ad+bc)/bd</div>
            <div>a/b − c/d = (ad−bc)/bd</div>
            <div>a/b × c/d = ac/bd</div>
            <div>a/b ÷ c/d = ad/bc</div>
          </div>
        </div>
        <div class="bg-green-50 border border-green-200 rounded-xl p-5">
          <h3 class="font-bold text-green-900 mb-2">Common Fractions</h3>
          <div class="grid grid-cols-2 gap-1 text-xs text-green-800">
            {[['1/2','0.5'],['1/3','0.333'],['1/4','0.25'],['3/4','0.75'],['1/8','0.125'],['2/3','0.667']].map(([f,d]) => (
              <div class="flex justify-between border-b border-green-100 pb-0.5"><span>{f}</span><span>{d}</span></div>
            ))}
          </div>
        </div>""",
    content_html="""    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Step-by-Step: Adding 1/3 + 1/4</h2>
        <div class="space-y-2">
          {[
            { step: '1', text: 'Find LCD of 3 and 4 → LCD = 12' },
            { step: '2', text: 'Convert: 1/3 = 4/12 and 1/4 = 3/12' },
            { step: '3', text: 'Add numerators: 4 + 3 = 7' },
            { step: '4', text: 'Result: 7/12 (already simplified)' },
          ].map(s => (
            <div class="flex gap-3 bg-gray-50 rounded-lg p-3">
              <div class="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">{s.step}</div>
              <div class="text-sm text-gray-700">{s.text}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Fraction to Decimal Reference</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold text-gray-700">Fraction</th><th class="text-right p-2 text-xs font-semibold text-gray-700">Decimal</th><th class="text-right p-2 text-xs font-semibold text-gray-700">Percent</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[['1/5','0.2','20%'],['1/6','0.1667','16.67%'],['1/7','0.1429','14.29%'],['1/8','0.125','12.5%'],['1/9','0.1111','11.11%'],['1/10','0.1','10%']].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>""",
    result_label="Result",
    calc_desc="Add, subtract, multiply, or divide fractions with automatic simplification"
))

# ─── SQUARE ROOT ──────────────────────────────────────────────────────────────
write("square-root", make_page(
    slug="square-root",
    title="Square Root Calculator",
    category="Math",
    cat_slug="math",
    seo_title="Square Root Calculator: √x, Cube Root, and Nth Root",
    seo_desc="Calculate the square root, cube root, or any nth root of a number. Shows step-by-step simplification. Free square root calculator.",
    formula="""
  const num = parseFloat(inputs.number) || 0
  const n = parseInt(inputs.root) || 2
  if (n < 1) throw new Error('Root must be 1 or greater.')
  if (num < 0 && n % 2 === 0) throw new Error('Cannot take even root of negative number.')
  const result = num < 0 ? -Math.pow(-num, 1/n) : Math.pow(num, 1/n)
  const isExact = Number.isInteger(result)
  return {
    value: isExact ? String(result) : result.toFixed(8),
    gaugeValue: Math.min(Math.abs(result), 100),
    breakdown: [
      'Input: ' + num, 'Root: ' + n, 'Result: ' + result.toFixed(8), 'Exact: ' + (isExact ? 'Yes — ' + result : 'No (irrational)'), 'Squared back: ' + Math.pow(result, n).toFixed(4),
    ],
    stats: [
      { label: 'Result', value: result.toFixed(8) },
      { label: 'Root Type', value: n === 2 ? 'Square Root' : n === 3 ? 'Cube Root' : n + 'th Root' },
      { label: 'Exact?', value: isExact ? 'Yes' : 'Irrational' },
      { label: 'Rounded (4dp)', value: result.toFixed(4) },
    ]
  }
""",
    inputs_str="""[
            { id: 'number', label: 'Number', type: 'number', placeholder: '144', defaultValue: 144 },
            { id: 'root', label: 'Root (n)', type: 'select', options: [
              { value: '2', label: 'Square Root (√)' },
              { value: '3', label: 'Cube Root (∛)' },
              { value: '4', label: '4th Root' },
              { value: '5', label: '5th Root' },
              { value: '10', label: '10th Root' },
            ], defaultValue: '2' },
          ]""",
    gauge_str="""{
            min: 0, max: 100, unit: 'result magnitude',
            zones: [
              { label: '0–25', color: '#3b82f6', from: 0, to: 25 },
              { label: '25–50', color: '#22c55e', from: 25, to: 50 },
              { label: '50–75', color: '#f59e0b', from: 50, to: 75 },
              { label: '75–100+', color: '#8b5cf6', from: 75, to: 100 },
            ]
          }""",
    faqs_list=[
        ("What is a square root?", "The square root of a number x is a value y such that y² = x. For example, √144 = 12 because 12² = 144. Every positive number has two square roots (positive and negative), but we conventionally report the positive (principal) root."),
        ("What is an irrational square root?", "Most square roots are irrational — they cannot be expressed as a simple fraction and their decimals go on forever without repeating. √2 = 1.41421356... Perfect squares (1, 4, 9, 16, 25...) have exact integer square roots."),
        ("What are perfect squares?", "Numbers whose square roots are whole integers: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400... The square root of a perfect square is always an integer."),
        ("How do I simplify a square root?", "Factor out perfect squares. Example: √72 = √(36×2) = 6√2. Find the largest perfect square factor, take its root, and leave the remainder under the radical."),
        ("What is the difference between square root and exponent 0.5?", "They are identical. √x = x^(1/2) = x^0.5. Similarly, cube root = x^(1/3). This is why calculators use the ^ operator for roots as well as powers."),
    ],
    related_list=[("Exponent Calculator", "/calculators/exponent-calculator"), ("Scientific Notation Calculator", "/calculators/scientific-notation-calculator"), ("Percentage Calculator", "/calculators/percentage-calculator")],
    sidebar_html="""        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Perfect Squares</h3>
          <div class="grid grid-cols-2 gap-1 text-xs text-blue-800">
            {[[1,1],[4,2],[9,3],[16,4],[25,5],[36,6],[49,7],[64,8],[81,9],[100,10],[121,11],[144,12]].map(([n,r]) => (
              <div class="flex justify-between border-b border-blue-100 pb-0.5"><span>{n}</span><span>√ = {r}</span></div>
            ))}
          </div>
        </div>""",
    content_html="""    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Common Square Roots</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr><th class="text-left p-2 text-xs font-semibold text-gray-700">Number</th><th class="text-right p-2 text-xs font-semibold text-gray-700">Square Root</th><th class="text-right p-2 text-xs font-semibold text-gray-700">Exact?</th></tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[[2,'1.41421','No'],[3,'1.73205','No'],[5,'2.23607','No'],[7,'2.64575','No'],[10,'3.16228','No'],[12,'3.46410','No'],[25,'5','Yes'],[50,'7.07107','No']].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-mono">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Simplifying Square Roots</h2>
        <p class="text-gray-600 text-sm mb-3">Factor out perfect squares to simplify:</p>
        <div class="space-y-2">
          {[
            { from: '√12', to: '√(4×3) = 2√3 ≈ 3.464' },
            { from: '√18', to: '√(9×2) = 3√2 ≈ 4.243' },
            { from: '√50', to: '√(25×2) = 5√2 ≈ 7.071' },
            { from: '√72', to: '√(36×2) = 6√2 ≈ 8.485' },
            { from: '√98', to: '√(49×2) = 7√2 ≈ 9.899' },
          ].map(e => (
            <div class="flex gap-3 bg-gray-50 rounded-lg p-2 text-xs">
              <span class="font-mono text-blue-600 w-12">{e.from}</span>
              <span class="text-gray-400">=</span>
              <span class="font-mono text-green-600">{e.to}</span>
            </div>
          ))}
        </div>
      </div>
    </div>""",
    result_label="Result",
    calc_desc="Calculate square root, cube root, or any nth root with decimal precision"
))

# ─── GRADE ────────────────────────────────────────────────────────────────────
write("grade", make_page(
    slug="grade",
    title="Grade Calculator",
    category="Other",
    cat_slug="other",
    seo_title="Grade Calculator: Weighted Course Grade",
    seo_desc="Calculate your weighted course grade from assignments, tests, and exams. See what you need on the final exam. Free grade calculator.",
    formula="""
  const scores = [
    { score: parseFloat(inputs.s1)||0, weight: parseFloat(inputs.w1)||0 },
    { score: parseFloat(inputs.s2)||0, weight: parseFloat(inputs.w2)||0 },
    { score: parseFloat(inputs.s3)||0, weight: parseFloat(inputs.w3)||0 },
    { score: parseFloat(inputs.s4)||0, weight: parseFloat(inputs.w4)||0 },
  ].filter(x => x.weight > 0)
  if (scores.length === 0) throw new Error('Enter at least one score and weight.')
  const totalWeight = scores.reduce((s,x) => s+x.weight, 0)
  const weighted = scores.reduce((s,x) => s + x.score * x.weight, 0)
  const grade = weighted / totalWeight
  const letterGrade = grade >= 93 ? 'A' : grade >= 90 ? 'A-' : grade >= 87 ? 'B+' : grade >= 83 ? 'B' : grade >= 80 ? 'B-' : grade >= 77 ? 'C+' : grade >= 73 ? 'C' : grade >= 70 ? 'C-' : grade >= 67 ? 'D+' : grade >= 60 ? 'D' : 'F'
  return {
    value: grade.toFixed(2) + '% — ' + letterGrade,
    gaugeValue: grade,
    breakdown: scores.map((x,i) => 'Item ' + (i+1) + ': ' + x.score + '% × ' + x.weight + '% weight = ' + (x.score*x.weight/totalWeight).toFixed(1) + 'pts').concat(['Weighted Grade: ' + grade.toFixed(2) + '%']),
    stats: [
      { label: 'Weighted Grade', value: grade.toFixed(2) + '%' },
      { label: 'Letter Grade', value: letterGrade },
      { label: 'Total Weight', value: totalWeight + '%' },
      { label: 'GPA Points', value: grade >= 93 ? '4.0' : grade >= 90 ? '3.7' : grade >= 87 ? '3.3' : grade >= 83 ? '3.0' : grade >= 80 ? '2.7' : grade >= 70 ? '2.0' : '0.0' },
    ]
  }
""",
    inputs_str="""[
            { id: 's1', label: 'Homework / Assignments Score', type: 'number', placeholder: '88', min: 0, max: 100, unit: '%', defaultValue: 88 },
            { id: 'w1', label: 'Homework Weight', type: 'number', placeholder: '20', min: 0, max: 100, unit: '%', defaultValue: 20 },
            { id: 's2', label: 'Midterm Score', type: 'number', placeholder: '75', min: 0, max: 100, unit: '%', defaultValue: 75 },
            { id: 'w2', label: 'Midterm Weight', type: 'number', placeholder: '30', min: 0, max: 100, unit: '%', defaultValue: 30 },
            { id: 's3', label: 'Quizzes Score', type: 'number', placeholder: '82', min: 0, max: 100, unit: '%', defaultValue: 82 },
            { id: 'w3', label: 'Quizzes Weight', type: 'number', placeholder: '20', min: 0, max: 100, unit: '%', defaultValue: 20 },
            { id: 's4', label: 'Final Exam Score', type: 'number', placeholder: '79', min: 0, max: 100, unit: '%', defaultValue: 79 },
            { id: 'w4', label: 'Final Exam Weight', type: 'number', placeholder: '30', min: 0, max: 100, unit: '%', defaultValue: 30 },
          ]""",
    gauge_str="""{
            min: 0, max: 100, unit: '%',
            zones: [
              { label: 'F (<60)', color: '#ef4444', from: 0, to: 60 },
              { label: 'D (60–70)', color: '#f97316', from: 60, to: 70 },
              { label: 'C (70–80)', color: '#f59e0b', from: 70, to: 80 },
              { label: 'B (80–90)', color: '#3b82f6', from: 80, to: 90 },
              { label: 'A (90–100)', color: '#22c55e', from: 90, to: 100 },
            ]
          }""",
    faqs_list=[
        ("How do I calculate a weighted grade?", "Multiply each score by its weight percentage, sum all the products, and divide by the total weight. Example: 80% score with 30% weight contributes 80 × 0.30 = 24 points. Sum all contributions and divide by total weight."),
        ("What score do I need on the final exam to pass?", "Use our Final Grade Calculator for that. Rearranging the weighted grade formula: Final Score = (Target Grade - Current Weighted Points) / Final Weight. If you need 70% overall, have 65% from 70% of the course, you need: (70 - 65×0.7) / 0.3 = 81.7% on the final."),
        ("What is a 4.0 GPA scale?", "A: 4.0 | A-: 3.7 | B+: 3.3 | B: 3.0 | B-: 2.7 | C+: 2.3 | C: 2.0 | C-: 1.7 | D+: 1.3 | D: 1.0 | F: 0.0. Most US colleges use this scale. Some use a 4.33 scale where A+ = 4.33."),
        ("Does rounding matter in grade calculations?", "Yes. Many professors round final grades (e.g., 89.5% rounds to 90% = A-). Others truncate. Always check your syllabus. A 0.1% difference can change your letter grade, so every assignment matters throughout the semester."),
        ("How do extra credit points affect my grade?", "Extra credit adds points to your numerator without changing the denominator (total possible points). Even small amounts of extra credit can significantly affect your grade when you are borderline. A 2-point extra credit on a 100-point scale raises a 79 to 81."),
    ],
    related_list=[("GPA Calculator", "/calculators/gpa-calculator"), ("Final Grade Calculator", "/calculators/final-grade-calculator"), ("Percentage Calculator", "/calculators/percentage-calculator")],
    sidebar_html="""        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Grade Scale</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700"><th class="text-left pb-1">Grade</th><th class="text-right pb-1">%</th><th class="text-right pb-1">GPA</th></tr></thead>
            <tbody class="text-blue-900">
              {[['A','93–100','4.0'],['A-','90–92','3.7'],['B+','87–89','3.3'],['B','83–86','3.0'],['B-','80–82','2.7'],['C+','77–79','2.3'],['C','73–76','2.0'],['D','60–69','1.0'],['F','<60','0.0']].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right">{r[1]}</td><td class="text-right">{r[2]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
    content_html="""    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">How Weighted Grades Work</h2>
        <p class="text-gray-600 text-sm mb-3">Different assignments count for different percentages of your final grade. A 90% on an assignment worth 10% contributes less than a 75% on a final exam worth 40%.</p>
        <div class="bg-gray-50 rounded-lg p-4 text-sm">
          <p class="font-medium text-gray-800 mb-2">Example: 80% homework (20%) + 70% midterm (30%) + 75% final (50%)</p>
          <p class="text-xs text-gray-600">= (80×0.20) + (70×0.30) + (75×0.50)</p>
          <p class="text-xs text-gray-600">= 16 + 21 + 37.5 = <strong>74.5% overall</strong></p>
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Strategies to Improve Your Grade</h2>
        <div class="space-y-2">
          {[
            'Focus effort on high-weight components (midterms, finals)',
            'Never skip homework — even low-weight items add up',
            'Ask for extra credit opportunities early, not at semester end',
            'Calculate your current grade mid-semester to know where you stand',
            'Study for high-weight items using past exams and office hours',
          ].map(tip => (
            <div class="flex gap-2 text-xs text-gray-600">
              <span class="text-blue-500 mt-0.5">•</span>
              <span>{tip}</span>
            </div>
          ))}
        </div>
      </div>
    </div>""",
    result_label="Final Grade",
    calc_desc="Calculate your weighted course grade and see your letter grade"
))

# ─── FINAL GRADE ──────────────────────────────────────────────────────────────
write("final-grade", make_page(
    slug="final-grade",
    title="Final Grade Calculator",
    category="Other",
    cat_slug="other",
    seo_title="Final Grade Calculator: What Do I Need on My Final Exam?",
    seo_desc="Find out what score you need on your final exam to achieve your target course grade. Free final grade calculator.",
    formula="""
  const current = parseFloat(inputs.current) || 0
  const currentWeight = parseFloat(inputs.currentWeight) || 0
  const target = parseFloat(inputs.target) || 0
  const finalWeight = parseFloat(inputs.finalWeight) || 0
  if (currentWeight + finalWeight > 100.1) throw new Error('Weights add up to more than 100%.')
  if (finalWeight <= 0) throw new Error('Enter final exam weight.')
  const needed = (target - current * (currentWeight / 100)) / (finalWeight / 100)
  const feasible = needed <= 100
  return {
    value: needed.toFixed(1) + '% on final exam',
    gaugeValue: Math.max(0, Math.min(100, needed)),
    breakdown: [
      'Current grade: ' + current + '% (' + currentWeight + '% of course)',
      'Target grade: ' + target + '%',
      'Final weight: ' + finalWeight + '%',
      'Score needed: ' + needed.toFixed(1) + '%',
      feasible ? 'Achievable: YES' : 'NOTE: Score over 100% needed — target may not be achievable.',
    ],
    stats: [
      { label: 'Score Needed', value: needed.toFixed(1) + '%' },
      { label: 'Feasible?', value: feasible ? 'Yes' : 'Very Difficult' },
      { label: 'Current Grade', value: current + '%' },
      { label: 'Target Grade', value: target + '%' },
    ]
  }
""",
    inputs_str="""[
            { id: 'current', label: 'Current Grade', type: 'number', placeholder: '78', min: 0, max: 100, unit: '%', defaultValue: 78 },
            { id: 'currentWeight', label: 'Current Grade Weight', type: 'number', placeholder: '60', min: 0, max: 100, unit: '%', defaultValue: 60 },
            { id: 'finalWeight', label: 'Final Exam Weight', type: 'number', placeholder: '40', min: 0, max: 100, unit: '%', defaultValue: 40 },
            { id: 'target', label: 'Target Course Grade', type: 'number', placeholder: '80', min: 0, max: 100, unit: '%', defaultValue: 80 },
          ]""",
    gauge_str="""{
            min: 0, max: 100, unit: '% needed on final',
            zones: [
              { label: 'Easy (<60%)', color: '#22c55e', from: 0, to: 60 },
              { label: 'Doable (60–80%)', color: '#3b82f6', from: 60, to: 80 },
              { label: 'Hard (80–90%)', color: '#f59e0b', from: 80, to: 90 },
              { label: 'Very Hard (90–100%)', color: '#ef4444', from: 90, to: 100 },
            ]
          }""",
    faqs_list=[
        ("How do I calculate what I need on my final?", "Formula: Final Score = (Target Grade - Current Grade × Current Weight%) / Final Weight%. Example: current grade 78% (60% weight), target 80%, final worth 40%: needed = (80 - 78×0.60) / 0.40 = (80-46.8)/0.40 = 83.0%."),
        ("What if I need over 100% on the final?", "If the score needed exceeds 100%, your current grade makes the target mathematically impossible with standard grading. Options: ask about extra credit, or adjust your target grade to something achievable."),
        ("How do I figure out my current grade weight?", "Add up the weights of all components completed so far. If homework (20%) and midterm (30%) are done, your current weight is 50% and the remaining components (50%) still need to be completed."),
        ("What is a passing grade?", "Most US colleges require at least a D (60%) to earn credit, but many majors require C (73%) or higher. Graduate programs often require B (83%). Check your specific program requirements — some courses require passing with a C or higher."),
        ("Should I focus more on studying if the final is worth a lot?", "Absolutely. A final worth 50% can swing your grade dramatically. Going from 70% to 90% on a 50%-weight final changes your overall grade by 10 points. Prioritize studying for high-weight assessments."),
    ],
    related_list=[("Grade Calculator", "/calculators/grade-calculator"), ("GPA Calculator", "/calculators/gpa-calculator"), ("Percentage Calculator", "/calculators/percentage-calculator")],
    sidebar_html="""        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Score Needed Reference</h3>
          <p class="text-xs text-blue-700 mb-2">Current 75%, Final worth 40%:</p>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700"><th class="text-left pb-1">Target</th><th class="text-right pb-1">Need on Final</th></tr></thead>
            <tbody class="text-blue-900">
              {[['70% (C-)', '62.5%'],['75% (C)', '75.0%'],['80% (B-)', '87.5%'],['83% (B)', '96.25%'],['90% (A-)', '>100% — tough']].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right">{r[1]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>""",
    content_html="""    <div class="mt-12">
      <h2 class="text-xl font-bold text-gray-900 mb-4">The Formula</h2>
      <div class="bg-gray-50 rounded-xl p-6 text-sm">
        <p class="font-medium text-gray-800 mb-2">Final Score Needed =</p>
        <p class="font-mono text-blue-600 text-base mb-4">(Target Grade − Current Grade × Current Weight%) ÷ Final Weight%</p>
        <div class="grid md:grid-cols-2 gap-4 text-xs text-gray-600">
          <div>
            <p class="font-medium mb-1">Example A: Easily achievable</p>
            <p>Current: 85% (70% weight), Target: 80%, Final: 30%</p>
            <p>= (80 − 85×0.70) / 0.30 = (80−59.5)/0.30 = 68.3%</p>
          </div>
          <div>
            <p class="font-medium mb-1">Example B: Very difficult</p>
            <p>Current: 68% (70% weight), Target: 80%, Final: 30%</p>
            <p>= (80 − 68×0.70) / 0.30 = (80−47.6)/0.30 = 108% (impossible)</p>
          </div>
        </div>
      </div>
    </div>""",
    result_label="Score Needed on Final",
    calc_desc="Calculate what score you need on your final exam to hit your target grade"
))

print("\\nBatch 4 done: average, fraction, square-root, grade, final-grade")
