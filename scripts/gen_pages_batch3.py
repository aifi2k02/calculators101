#!/usr/bin/env python3
"""Batch 3: Fitness calculators — ideal weight, macro, water, sleep, calories burned, protein, waist-hip, 1RM, lean body mass, pace, ovulation, due date, keto, intermittent fasting, steps-to-miles, vo2max, running calorie, pregnancy weight, body surface area"""
import os

CALC_DIR = "/Users/apple/Documents/Projects/calculators-for-free/src/pages/calculators"

def write(slug, content):
    path = os.path.join(CALC_DIR, f"{slug}-calculator.astro")
    with open(path, 'w') as f:
        f.write(content)
    print(f"✅ {slug}-calculator.astro")

write("ideal-weight", '''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const height = parseFloat(inputs.height) || 0
  const sex = inputs.sex || 'male'
  const unit = inputs.unit || 'imperial'
  let heightCm = height
  if (unit === 'imperial') heightCm = height * 2.54
  if (heightCm < 100) throw new Error('Enter a valid height.')
  const inchesOver5ft = Math.max(0, heightCm / 2.54 - 60)
  const robinson = sex === 'male' ? 52 + 1.9 * inchesOver5ft : 49 + 1.7 * inchesOver5ft
  const miller = sex === 'male' ? 56.2 + 1.41 * inchesOver5ft : 53.1 + 1.36 * inchesOver5ft
  const devine = sex === 'male' ? 50 + 2.3 * inchesOver5ft : 45.5 + 2.3 * inchesOver5ft
  const bmi_ideal = (22.5 * (heightCm / 100) ** 2)
  const avg = (robinson + miller + devine) / 3
  const low = avg * 0.9, high = avg * 1.1
  return {
    value: avg.toFixed(1) + ' kg (' + (avg * 2.205).toFixed(1) + ' lbs)',
    gaugeValue: 50,
    breakdown: [
      'Robinson formula: ' + robinson.toFixed(1) + ' kg',
      'Miller formula: ' + miller.toFixed(1) + ' kg',
      'Devine formula: ' + devine.toFixed(1) + ' kg',
      'Healthy BMI range: ' + (bmi_ideal * 0.89).toFixed(1) + '–' + (bmi_ideal * 1.11).toFixed(1) + ' kg',
    ],
    stats: [
      { label: 'Ideal Weight', value: avg.toFixed(1) + ' kg' },
      { label: 'In Pounds', value: (avg * 2.205).toFixed(1) + ' lbs' },
      { label: 'Healthy Range', value: low.toFixed(0) + '–' + high.toFixed(0) + ' kg' },
      { label: 'BMI Range', value: (bmi_ideal * 0.89).toFixed(0) + '–' + (bmi_ideal * 1.11).toFixed(0) + ' kg' },
    ]
  }
`

const faqs = [
  { question: 'What is ideal body weight?', answer: 'Ideal body weight (IBW) is an estimate of a healthy weight for a given height and sex, based on population studies. Multiple formulas exist (Robinson, Miller, Devine, Hamwi). They vary slightly — the average across formulas gives a reasonable target range.' },
  { question: 'Is there one perfect ideal weight?', answer: 'No. Ideal weight depends on muscle mass, bone density, age, body composition, and personal health goals. A heavily muscled athlete may weigh more than IBW formulas suggest while being extremely healthy. Use IBW as a rough guideline, not a strict target.' },
  { question: 'How is ideal weight different from BMI?', answer: 'BMI uses a range (18.5–24.9) rather than a single number. The "ideal" BMI center point (~22.5) gives a similar result to IBW formulas for average builds. IBW formulas were designed for clinical drug dosing, not general weight goals.' },
  { question: 'Can I be healthy above my ideal weight?', answer: 'Yes. Research shows that fitness level (cardiorespiratory fitness) is a better predictor of health outcomes than weight alone. A slightly overweight person who exercises regularly often has better health outcomes than a sedentary person at "ideal" weight.' },
  { question: 'How do I reach my ideal weight?', answer: 'Create a modest calorie deficit (300–500 calories/day) through diet and exercise. Aim to lose 0.5–1 kg (1–2 lbs) per week. Rapid weight loss loses muscle; slow, steady loss preserves muscle while losing fat. Use our TDEE calculator to find your calorie needs.' },
]
---
<Layout
  title="Ideal Weight Calculator: Find Your Healthy Target Weight"
  description="Calculate your ideal body weight using 4 proven formulas (Robinson, Miller, Devine, BMI). Free ideal weight calculator for men and women."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Fitness & Health', href: '/calculators/fitness' },
    { name: 'Ideal Weight Calculator', href: '/calculators/ideal-weight-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/fitness" class="hover:text-blue-600">Fitness</a><span>›</span>
      <span class="text-gray-900">Ideal Weight Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Ideal Weight Calculator"
          description="Find your ideal weight using 4 established clinical formulas"
          formulaId="ideal-weight"
          formulaFn={formulaFn}
          resultLabel="Ideal Weight"
          inputs={[
            { id: 'sex', label: 'Sex', type: 'select', options: [{ value: 'male', label: 'Male' }, { value: 'female', label: 'Female' }], defaultValue: 'male' },
            { id: 'height', label: 'Height (inches)', type: 'number', placeholder: '70', min: 48, max: 84, unit: 'in', defaultValue: 70 },
            { id: 'unit', label: 'Height Unit', type: 'select', options: [{ value: 'imperial', label: 'Inches' }, { value: 'metric', label: 'Centimeters' }], defaultValue: 'imperial' },
          ]}
          gauge={{
            min: 0, max: 100, unit: '% comparison',
            zones: [
              { label: 'Underweight', color: '#3b82f6', from: 0, to: 30 },
              { label: 'Near Ideal', color: '#22c55e', from: 30, to: 70 },
              { label: 'Above Ideal', color: '#f59e0b', from: 70, to: 100 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'BMI Calculator', href: '/calculators/bmi-calculator' },
            { name: 'Body Fat Calculator', href: '/calculators/body-fat-calculator' },
            { name: 'Caloric Deficit Calculator', href: '/calculators/caloric-deficit-calculator' },
            { name: 'TDEE Calculator', href: '/calculators/tdee-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Ideal Weight for 5\'10" Male</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[['Robinson (1983)','163 lbs / 74 kg'],['Miller (1983)','166 lbs / 75.5 kg'],['Devine (1974)','166 lbs / 75.5 kg'],['BMI 22.5','156 lbs / 71 kg'],['Average','163–166 lbs']].map(([f,w]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span>{f}</span><span class="font-medium">{w}</span></div>
            ))}
          </div>
        </div>
        <div class="bg-green-50 border border-green-200 rounded-xl p-5">
          <h3 class="font-bold text-green-900 mb-2">Healthy BMI Weight Range</h3>
          <p class="text-xs text-green-800">BMI 18.5–24.9 defines the healthy range. The midpoint (BMI ~22) aligns closely with IBW formula results for most heights.</p>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">The 4 IBW Formulas</h2>
        <div class="space-y-3">
          {[
            { name: 'Robinson (1983)', male: '52 kg + 1.9 kg/inch over 5ft', female: '49 kg + 1.7 kg/inch over 5ft' },
            { name: 'Miller (1983)', male: '56.2 kg + 1.41 kg/inch over 5ft', female: '53.1 kg + 1.36 kg/inch over 5ft' },
            { name: 'Devine (1974)', male: '50 kg + 2.3 kg/inch over 5ft', female: '45.5 kg + 2.3 kg/inch over 5ft' },
          ].map(f => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-gray-800 text-xs mb-1">{f.name}</div>
              <div class="text-xs text-blue-600">♂ {f.male}</div>
              <div class="text-xs text-pink-600">♀ {f.female}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Ideal Weight by Height (Male)</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr>
            <th class="text-left p-2 text-xs font-semibold text-gray-700">Height</th>
            <th class="text-right p-2 text-xs font-semibold text-gray-700">IBW Range</th>
            <th class="text-right p-2 text-xs font-semibold text-gray-700">BMI Range</th>
          </tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[["5'6\"","138–148 lbs","128–172 lbs"],["5'8\"","150–161 lbs","136–183 lbs"],["5'10\"","163–174 lbs","145–195 lbs"],["6'0\"","175–188 lbs","154–208 lbs"],["6'2\"","188–201 lbs","164–220 lbs"]].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right text-gray-500">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</Layout>
''')

write("macro", '''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const calories = parseFloat(inputs.calories) || 0
  const goal = inputs.goal || 'maintain'
  const style = inputs.style || 'balanced'
  if (calories < 800) throw new Error('Enter daily calories (minimum 800).')
  let proteinPct, carbPct, fatPct
  if (style === 'keto') { proteinPct = 25; carbPct = 5; fatPct = 70 }
  else if (style === 'low-carb') { proteinPct = 35; carbPct = 20; fatPct = 45 }
  else if (style === 'high-protein') { proteinPct = 40; carbPct = 35; fatPct = 25 }
  else { proteinPct = 30; carbPct = 40; fatPct = 30 }
  const protein = Math.round(calories * proteinPct / 100 / 4)
  const carbs = Math.round(calories * carbPct / 100 / 4)
  const fat = Math.round(calories * fatPct / 100 / 9)
  return {
    value: protein + 'g protein / ' + carbs + 'g carbs / ' + fat + 'g fat',
    gaugeValue: proteinPct,
    breakdown: [
      'Protein: ' + protein + 'g (' + proteinPct + '% = ' + Math.round(calories*proteinPct/100) + ' cal)',
      'Carbs: ' + carbs + 'g (' + carbPct + '% = ' + Math.round(calories*carbPct/100) + ' cal)',
      'Fat: ' + fat + 'g (' + fatPct + '% = ' + Math.round(calories*fatPct/100) + ' cal)',
    ],
    stats: [
      { label: 'Protein', value: protein + 'g/day' },
      { label: 'Carbohydrates', value: carbs + 'g/day' },
      { label: 'Fat', value: fat + 'g/day' },
      { label: 'Calorie Target', value: calories + ' kcal' },
    ]
  }
`

const faqs = [
  { question: 'What are macros and why do they matter?', answer: 'Macros (macronutrients) are protein, carbohydrates, and fat — the three nutrients that provide calories. Protein and carbs have 4 calories/gram; fat has 9 calories/gram. Tracking macros ensures you hit calorie goals while meeting nutritional needs for your specific goal (muscle gain, fat loss, performance).' },
  { question: 'How much protein do I need per day?', answer: 'For general health: 0.8g per kg body weight. For muscle building: 1.6–2.2g per kg. For fat loss while preserving muscle: 1.8–2.5g per kg. Higher protein keeps you full and preserves muscle during a calorie deficit.' },
  { question: 'What macro ratio is best for weight loss?', answer: 'Research shows any macro split can produce weight loss if calories are controlled. High protein helps preserve muscle (30–40%). Many find reducing carbs helps with satiety. A typical starting point: 30% protein, 35% carbs, 35% fat. Adjust based on preferences and results.' },
  { question: 'What is the difference between keto and low-carb macros?', answer: 'Keto is very low carb (under 5% or ~20–50g/day) to induce ketosis. Low-carb typically allows 20–30% carbs (~100–150g/day). Keto is more restrictive but some people find it helps control hunger. Both can be effective for weight loss.' },
  { question: 'Do I need to track macros, or just calories?', answer: 'Calories are the primary driver of weight change. Macros matter more for body composition (muscle vs. fat), athletic performance, and satiety. If you\'re new to tracking, start with just calories. Add macro tracking once you\'ve established the calorie habit.' },
]
---
<Layout
  title="Macro Calculator: Daily Protein, Carbs & Fat Targets"
  description="Calculate your daily macronutrient targets for any diet style — balanced, high-protein, low-carb, or keto. Free macro calculator."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Fitness & Health', href: '/calculators/fitness' },
    { name: 'Macro Calculator', href: '/calculators/macro-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/fitness" class="hover:text-blue-600">Fitness</a><span>›</span>
      <span class="text-gray-900">Macro Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Macro Calculator"
          description="Calculate daily protein, carbs, and fat targets for your diet style"
          formulaId="macro"
          formulaFn={formulaFn}
          resultLabel="Daily Macros"
          inputs={[
            { id: 'calories', label: 'Daily Calorie Target', type: 'number', placeholder: '2000', min: 800, max: 5000, unit: 'kcal', defaultValue: 2000 },
            { id: 'goal', label: 'Goal', type: 'select', options: [
              { value: 'maintain', label: 'Maintain weight' },
              { value: 'lose', label: 'Lose fat' },
              { value: 'gain', label: 'Build muscle' },
            ], defaultValue: 'maintain' },
            { id: 'style', label: 'Diet Style', type: 'select', options: [
              { value: 'balanced', label: 'Balanced (30/40/30)' },
              { value: 'high-protein', label: 'High Protein (40/35/25)' },
              { value: 'low-carb', label: 'Low Carb (35/20/45)' },
              { value: 'keto', label: 'Keto (25/5/70)' },
            ], defaultValue: 'balanced' },
          ]}
          gauge={{
            min: 0, max: 50, unit: '% protein',
            zones: [
              { label: 'Low Protein', color: '#94a3b8', from: 0, to: 20 },
              { label: 'Moderate', color: '#3b82f6', from: 20, to: 30 },
              { label: 'High Protein', color: '#22c55e', from: 30, to: 40 },
              { label: 'Very High', color: '#f59e0b', from: 40, to: 50 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'TDEE Calculator', href: '/calculators/tdee-calculator' },
            { name: 'Protein Calculator', href: '/calculators/protein-calculator' },
            { name: 'Calorie Calculator', href: '/calculators/calorie-calculator' },
            { name: 'Keto Calculator', href: '/calculators/keto-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Diet Style Comparison (2000 cal)</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700"><th class="text-left pb-1">Style</th><th class="text-right pb-1">Protein</th><th class="text-right pb-1">Carbs</th><th class="text-right pb-1">Fat</th></tr></thead>
            <tbody class="text-blue-900">
              {[['Balanced','150g','200g','67g'],['High Protein','200g','175g','56g'],['Low Carb','175g','100g','100g'],['Keto','125g','25g','156g']].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right">{r[1]}</td><td class="text-right">{r[2]}</td><td class="text-right">{r[3]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
        <div class="bg-green-50 border border-green-200 rounded-xl p-5">
          <h3 class="font-bold text-green-900 mb-2">Calories per Gram</h3>
          <ul class="text-xs text-green-800 space-y-1">
            <li>• Protein: <strong>4 cal/g</strong></li>
            <li>• Carbohydrates: <strong>4 cal/g</strong></li>
            <li>• Fat: <strong>9 cal/g</strong></li>
            <li>• Alcohol: <strong>7 cal/g</strong></li>
          </ul>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Protein Recommendations by Goal</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr>
            <th class="text-left p-2 text-xs font-semibold text-gray-700">Goal</th>
            <th class="text-right p-2 text-xs font-semibold text-gray-700">Protein Target</th>
          </tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[['Sedentary adult','0.8g/kg body weight'],['Active adult','1.0–1.3g/kg'],['Fat loss (muscle preservation)','1.8–2.5g/kg'],['Muscle building','1.6–2.2g/kg'],['Endurance athlete','1.2–1.6g/kg'],['Strength athlete','1.7–2.2g/kg']].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-medium">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">High-Protein Food Sources</h2>
        <div class="grid grid-cols-2 gap-2">
          {[
            { food: 'Chicken breast (100g)', protein: '31g' },
            { food: 'Greek yogurt (170g)', protein: '17g' },
            { food: 'Eggs (1 large)', protein: '6g' },
            { food: 'Tuna (85g)', protein: '25g' },
            { food: 'Whey protein (1 scoop)', protein: '25g' },
            { food: 'Cottage cheese (100g)', protein: '11g' },
            { food: 'Lentils (100g cooked)', protein: '9g' },
            { food: 'Salmon (100g)', protein: '25g' },
          ].map(f => (
            <div class="bg-gray-50 rounded-lg p-2 flex justify-between items-center">
              <span class="text-xs text-gray-600">{f.food}</span>
              <span class="text-xs font-bold text-blue-600">{f.protein}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
</Layout>
''')

write("water-intake", '''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const weight = parseFloat(inputs.weight) || 0
  const unit = inputs.unit || 'lbs'
  const activity = inputs.activity || 'moderate'
  const climate = inputs.climate || 'normal'
  if (weight <= 0) throw new Error('Enter your weight.')
  const weightLbs = unit === 'kg' ? weight * 2.205 : weight
  let baseOz = weightLbs * 0.5
  if (activity === 'active') baseOz += 16
  else if (activity === 'very-active') baseOz += 32
  if (climate === 'hot') baseOz += 16
  const liters = (baseOz * 29.5735) / 1000
  const cups = baseOz / 8
  const glasses = cups
  const pct = Math.min((liters / 3.0) * 100, 100)
  return {
    value: liters.toFixed(1) + 'L / day (' + baseOz.toFixed(0) + ' oz)',
    gaugeValue: pct,
    breakdown: [
      'Base intake: ' + (weightLbs * 0.5).toFixed(0) + ' oz',
      'Activity bonus: +' + (activity === 'active' ? 16 : activity === 'very-active' ? 32 : 0) + ' oz',
      'Climate bonus: +' + (climate === 'hot' ? 16 : 0) + ' oz',
      'Total: ' + baseOz.toFixed(0) + ' oz = ' + liters.toFixed(1) + 'L = ' + cups.toFixed(0) + ' cups',
    ],
    stats: [
      { label: 'Daily Water', value: liters.toFixed(1) + ' liters' },
      { label: 'In Ounces', value: baseOz.toFixed(0) + ' oz' },
      { label: 'In Cups', value: cups.toFixed(0) + ' cups (8oz)' },
      { label: '8oz Glasses', value: glasses.toFixed(0) + ' glasses' },
    ]
  }
`

const faqs = [
  { question: 'How much water should I drink per day?', answer: 'The general guideline is 0.5 oz per pound of body weight, or about 2–3 liters for most adults. The "8 glasses a day" rule (64 oz) is a rough approximation. Actual needs depend on body weight, activity level, climate, and diet.' },
  { question: 'Does coffee and tea count toward water intake?', answer: 'Yes. Despite being mildly diuretic, caffeinated beverages still contribute to hydration. Studies show coffee and tea contribute net fluid to daily intake. Water from food (fruits, vegetables, soups) also counts — food provides about 20% of daily fluid needs.' },
  { question: 'What are signs of dehydration?', answer: 'Mild dehydration: thirst, dark yellow urine, reduced performance. Moderate: headache, dizziness, fatigue, dry mouth. Severe (5%+ body water loss): confusion, rapid heartbeat, no urine output. The best indicator is urine color — pale yellow is ideal.' },
  { question: 'Can you drink too much water?', answer: 'Yes — hyponatremia (water intoxication) dilutes blood sodium, causing nausea, headaches, and in severe cases, seizures. This is most common in endurance events when athletes drink large amounts without electrolytes. For normal daily activity, this risk is very low.' },
  { question: 'Does exercise increase water needs?', answer: 'Significantly. You lose 0.5–2 liters per hour of exercise through sweat, depending on intensity and temperature. Add 500ml for every hour of moderate exercise, more in heat or for intense workouts. Check urine color after exercise to gauge if you rehydrated adequately.' },
]
---
<Layout
  title="Water Intake Calculator: Daily Hydration Needs"
  description="Calculate how much water you should drink per day based on weight, activity level, and climate. Free water intake calculator."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Fitness & Health', href: '/calculators/fitness' },
    { name: 'Water Intake Calculator', href: '/calculators/water-intake-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/fitness" class="hover:text-blue-600">Fitness</a><span>›</span>
      <span class="text-gray-900">Water Intake Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Water Intake Calculator"
          description="Find your daily hydration target based on your body weight and lifestyle"
          formulaId="water-intake"
          formulaFn={formulaFn}
          resultLabel="Daily Water Target"
          inputs={[
            { id: 'weight', label: 'Body Weight', type: 'number', placeholder: '160', min: 50, unit: 'lbs', defaultValue: 160 },
            { id: 'unit', label: 'Weight Unit', type: 'select', options: [{ value: 'lbs', label: 'Pounds (lbs)' }, { value: 'kg', label: 'Kilograms (kg)' }], defaultValue: 'lbs' },
            { id: 'activity', label: 'Activity Level', type: 'select', options: [
              { value: 'sedentary', label: 'Sedentary (little exercise)' },
              { value: 'moderate', label: 'Moderate (3–5 days/week)' },
              { value: 'active', label: 'Active (1+ hour/day)' },
              { value: 'very-active', label: 'Very Active (2+ hours/day)' },
            ], defaultValue: 'moderate' },
            { id: 'climate', label: 'Climate', type: 'select', options: [
              { value: 'normal', label: 'Normal / Mild' },
              { value: 'hot', label: 'Hot / Humid' },
            ], defaultValue: 'normal' },
          ]}
          gauge={{
            min: 0, max: 100, unit: '% of 3L target',
            zones: [
              { label: 'Low', color: '#ef4444', from: 0, to: 40 },
              { label: 'Getting There', color: '#f59e0b', from: 40, to: 70 },
              { label: 'Good', color: '#3b82f6', from: 70, to: 90 },
              { label: 'Optimal', color: '#22c55e', from: 90, to: 100 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'Calorie Calculator', href: '/calculators/calorie-calculator' },
            { name: 'TDEE Calculator', href: '/calculators/tdee-calculator' },
            { name: 'BMR Calculator', href: '/calculators/bmr-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Urine Color Guide</h3>
          <div class="space-y-2 text-xs">
            {[['#fffde7','Colorless','Over-hydrated'],['#fff9c4','Pale Yellow','Well hydrated ✓'],['#f9a825','Dark Yellow','Mildly dehydrated'],['#e65100','Amber','Dehydrated'],['#bf360c','Brown','Very dehydrated']].map(([bg, color, status]) => (
              <div class="flex items-center gap-2">
                <div style={`background:${bg};`} class="w-6 h-4 rounded border border-gray-200"></div>
                <span class="font-medium">{color}</span>
                <span class="text-gray-600">— {status}</span>
              </div>
            ))}
          </div>
        </div>
        <div class="bg-green-50 border border-green-200 rounded-xl p-5">
          <h3 class="font-bold text-green-900 mb-2">Hydration Tips</h3>
          <ul class="text-xs text-green-800 space-y-1">
            <li>• Drink a glass immediately upon waking</li>
            <li>• Carry a reusable 1L water bottle</li>
            <li>• Set hourly reminders if needed</li>
            <li>• Add lemon or cucumber for flavor</li>
            <li>• Eat water-rich foods (cucumber, watermelon)</li>
          </ul>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Benefits of Proper Hydration</h2>
        <div class="grid grid-cols-2 gap-3">
          {[
            { icon: '🧠', label: 'Brain Function', detail: 'Even 1% dehydration impairs concentration, reaction time, and short-term memory' },
            { icon: '💪', label: 'Physical Performance', detail: '2–3% dehydration reduces endurance and strength significantly' },
            { icon: '⚡', label: 'Energy Levels', detail: 'Dehydration is a common cause of afternoon energy slumps and headaches' },
            { icon: '🫁', label: 'Digestion', detail: 'Water aids nutrient absorption, prevents constipation, and supports kidney function' },
          ].map(b => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="text-xl mb-1">{b.icon}</div>
              <div class="font-semibold text-gray-800 text-xs mb-1">{b.label}</div>
              <div class="text-xs text-gray-600">{b.detail}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Water Content in Foods</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr>
            <th class="text-left p-2 text-xs font-semibold text-gray-700">Food</th>
            <th class="text-right p-2 text-xs font-semibold text-gray-700">Water Content</th>
          </tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[['Cucumber','96%'],['Celery','95%'],['Watermelon','92%'],['Strawberries','91%'],['Orange','86%'],['Broccoli','89%'],['Banana','75%'],['Avocado','73%']].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right font-medium text-blue-600">{r[1]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</Layout>
''')

write("sleep", '''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const type = inputs.type || 'wake'
  const sleepTime = inputs.sleepTime || '22:30'
  const wakeTime = inputs.wakeTime || '06:30'
  const cycles = parseInt(inputs.cycles) || 5
  const CYCLE = 90 * 60 * 1000
  const FALL_ASLEEP = 15 * 60 * 1000
  if (type === 'wake') {
    const [h, m] = sleepTime.split(':').map(Number)
    const base = new Date()
    base.setHours(h, m, 0, 0)
    const wakeOptions = []
    for (let i = 4; i <= 7; i++) {
      const wake = new Date(base.getTime() + FALL_ASLEEP + i * CYCLE)
      const wh = wake.getHours().toString().padStart(2,'0')
      const wm = wake.getMinutes().toString().padStart(2,'0')
      wakeOptions.push(wh + ':' + wm + ' (' + i + ' cycles / ' + (i * 1.5) + 'h)')
    }
    return {
      value: wakeOptions[2],
      gaugeValue: 75,
      breakdown: ['If you sleep at ' + sleepTime + ':'].concat(wakeOptions),
      stats: [
        { label: 'Optimal Wake (5 cycles)', value: wakeOptions[1] },
        { label: 'Ideal Wake (6 cycles)', value: wakeOptions[2] },
        { label: 'Best Wake (7 cycles)', value: wakeOptions[3] },
        { label: 'Sleep Cycle', value: '90 min' },
      ]
    }
  } else {
    const [h, m] = wakeTime.split(':').map(Number)
    const target = new Date()
    target.setHours(h, m, 0, 0)
    const bedtimes = []
    for (let i = 4; i <= 7; i++) {
      const bed = new Date(target.getTime() - FALL_ASLEEP - i * CYCLE)
      const bh = bed.getHours().toString().padStart(2,'0')
      const bm = bed.getMinutes().toString().padStart(2,'0')
      bedtimes.push(bh + ':' + bm + ' (' + i + ' cycles / ' + (i * 1.5) + 'h)')
    }
    return {
      value: bedtimes[2],
      gaugeValue: 75,
      breakdown: ['To wake at ' + wakeTime + ':'].concat(bedtimes.reverse()),
      stats: [
        { label: 'Bedtime (6 cycles/9h)', value: bedtimes[3] },
        { label: 'Bedtime (6 cycles)', value: bedtimes[2] },
        { label: 'Bedtime (5 cycles)', value: bedtimes[1] },
        { label: 'Bedtime (4 cycles)', value: bedtimes[0] },
      ]
    }
  }
`

const faqs = [
  { question: 'How many hours of sleep do I need?', answer: 'Adults (18–64): 7–9 hours per night. Older adults (65+): 7–8 hours. Teenagers (14–17): 8–10 hours. School-age children (6–13): 9–11 hours. These are average needs — some individuals genuinely function well on 6 or need 10 hours.' },
  { question: 'What is a sleep cycle?', answer: 'A sleep cycle lasts approximately 90 minutes and includes light sleep (N1, N2), deep sleep (N3/slow-wave sleep), and REM sleep. Most people complete 4–6 cycles per night. Waking at the end of a cycle (vs. mid-cycle) dramatically reduces grogginess.' },
  { question: 'Why do I feel groggy even after 8 hours?', answer: 'Sleep inertia — grogginess upon waking — is worst when you wake during deep sleep (N3 stage). Waking at the end of a 90-minute cycle, when sleep is lightest, minimizes this. This is the basis of sleep cycle-based alarm timing.' },
  { question: 'What is REM sleep and why is it important?', answer: 'REM (Rapid Eye Movement) sleep is when most dreaming occurs. It is critical for memory consolidation, emotional processing, and creativity. REM periods lengthen later in the night — a major reason why cutting sleep short (especially skipping the last 1–2 hours) significantly impairs cognitive function.' },
  { question: 'How does screen time affect sleep?', answer: 'Blue light from screens suppresses melatonin production, delaying sleep onset by 1–3 hours. Avoiding screens 1–2 hours before bed, using night mode, or wearing blue-light glasses can help. The stimulating content of social media and news also increases alertness regardless of light.' },
]
---
<Layout
  title="Sleep Calculator: Best Wake-Up & Bedtimes by Sleep Cycles"
  description="Find the best wake-up times or bedtimes based on 90-minute sleep cycles. Wake feeling refreshed instead of groggy. Free sleep calculator."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Fitness & Health', href: '/calculators/fitness' },
    { name: 'Sleep Calculator', href: '/calculators/sleep-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/fitness" class="hover:text-blue-600">Fitness</a><span>›</span>
      <span class="text-gray-900">Sleep Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Sleep Calculator"
          description="Find optimal wake-up times or bedtimes based on 90-minute sleep cycles"
          formulaId="sleep"
          formulaFn={formulaFn}
          resultLabel="Optimal Time"
          inputs={[
            { id: 'type', label: 'I want to find...', type: 'select', options: [
              { value: 'wake', label: 'Best wake-up times (I know when I sleep)' },
              { value: 'bed', label: 'Best bedtime (I know when I wake up)' },
            ], defaultValue: 'wake' },
            { id: 'sleepTime', label: 'Sleep / Lights Out Time', type: 'select', options: [
              '20:00','20:30','21:00','21:30','22:00','22:30','23:00','23:30','00:00','00:30','01:00','01:30','02:00'
            ].map(t => ({ value: t, label: t })), defaultValue: '22:30' },
            { id: 'wakeTime', label: 'Wake-Up Time (if known)', type: 'select', options: [
              '04:00','04:30','05:00','05:30','06:00','06:30','07:00','07:30','08:00','08:30','09:00','09:30','10:00'
            ].map(t => ({ value: t, label: t })), defaultValue: '06:30' },
          ]}
          gauge={{
            min: 0, max: 100, unit: '% optimal',
            zones: [
              { label: '4 cycles (6h)', color: '#f59e0b', from: 0, to: 55 },
              { label: '5 cycles (7.5h)', color: '#3b82f6', from: 55, to: 77 },
              { label: '6 cycles (9h)', color: '#22c55e', from: 77, to: 100 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'BMR Calculator', href: '/calculators/bmr-calculator' },
            { name: 'TDEE Calculator', href: '/calculators/tdee-calculator' },
            { name: 'Age Calculator', href: '/calculators/age-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Sleep Stages (90-min cycle)</h3>
          <div class="space-y-2 text-xs text-blue-800">
            {[['N1 (Light)','1–5 min','Drowsy, easily awakened'],['N2 (Light)','10–60 min','Heart rate slows, sleep spindles'],['N3 (Deep)','20–40 min','Restorative, hardest to wake'],['REM','10–60 min','Dreaming, memory consolidation']].map(([s,d,desc]) => (
              <div class="border-b border-blue-100 pb-1">
                <div class="flex justify-between"><span class="font-medium">{s}</span><span>{d}</span></div>
                <div class="text-blue-600">{desc}</div>
              </div>
            ))}
          </div>
        </div>
        <div class="bg-purple-50 border border-purple-200 rounded-xl p-5">
          <h3 class="font-bold text-purple-900 mb-2">Sleep Needs by Age</h3>
          <div class="space-y-1 text-xs text-purple-800">
            {[['Infants (0–1)','12–16 hours'],['Toddlers (1–3)','11–14 hours'],['Children (6–13)','9–11 hours'],['Teens (14–17)','8–10 hours'],['Adults (18–64)','7–9 hours'],['Older adults (65+)','7–8 hours']].map(([a,h]) => (
              <div class="flex justify-between border-b border-purple-100 pb-1"><span>{a}</span><span class="font-medium">{h}</span></div>
            ))}
          </div>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Effects of Sleep Deprivation</h2>
        <div class="space-y-2">
          {[
            { hours: '1 night short', effect: 'Reduced attention, slower reaction time, increased hunger hormones' },
            { hours: '3–5 days short', effect: 'Significant cognitive impairment, mood instability, immune suppression' },
            { hours: '1–2 weeks short', effect: 'Performance equivalent to 48 hours awake; impairment not perceived' },
            { hours: 'Chronic (months)', effect: 'Increased risk of diabetes, heart disease, obesity, and depression' },
          ].map(e => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-gray-800 text-xs mb-1">{e.hours}</div>
              <div class="text-xs text-gray-600">{e.effect}</div>
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Sleep Hygiene Tips</h2>
        <div class="space-y-2">
          {[
            'Keep a consistent sleep schedule — even on weekends',
            'Make your room dark, cool (65–68°F / 18–20°C), and quiet',
            'Avoid caffeine after 2pm (half-life is 5–7 hours)',
            'No screens 1 hour before bed; use night mode if necessary',
            'Avoid alcohol before bed — it fragments sleep and reduces REM',
            'Exercise regularly but not within 2–3 hours of bedtime',
            'Use your bed only for sleep — not work, TV, or social media',
          ].map(tip => (
            <div class="flex gap-2 text-xs text-gray-600">
              <span class="text-blue-500 mt-0.5">•</span>
              <span>{tip}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
</Layout>
''')

write("one-rep-max", '''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const weight = parseFloat(inputs.weight) || 0
  const reps = parseInt(inputs.reps) || 1
  const unit = inputs.unit || 'lbs'
  if (weight <= 0) throw new Error('Enter weight lifted.')
  if (reps < 1 || reps > 30) throw new Error('Reps must be between 1 and 30.')
  if (reps === 1) {
    return {
      value: weight + ' ' + unit + ' (that IS your 1RM)',
      gaugeValue: 100,
      breakdown: ['Your 1 rep IS your 1RM: ' + weight + ' ' + unit],
      stats: [
        { label: '1RM', value: weight + ' ' + unit },
        { label: '90%', value: Math.round(weight * 0.9) + ' ' + unit },
        { label: '80%', value: Math.round(weight * 0.8) + ' ' + unit },
        { label: '70%', value: Math.round(weight * 0.7) + ' ' + unit },
      ]
    }
  }
  const brzycki = weight * (36 / (37 - reps))
  const epley = weight * (1 + reps / 30)
  const avg = (brzycki + epley) / 2
  const pct = reps >= 10 ? 65 : reps >= 6 ? 80 : 90
  return {
    value: Math.round(avg) + ' ' + unit + ' estimated 1RM',
    gaugeValue: pct,
    breakdown: [
      'Brzycki formula: ' + Math.round(brzycki) + ' ' + unit,
      'Epley formula: ' + Math.round(epley) + ' ' + unit,
      'Average estimate: ' + Math.round(avg) + ' ' + unit,
    ],
    stats: [
      { label: '1RM Estimate', value: Math.round(avg) + ' ' + unit },
      { label: '85% (5-rep zone)', value: Math.round(avg * 0.85) + ' ' + unit },
      { label: '75% (10-rep zone)', value: Math.round(avg * 0.75) + ' ' + unit },
      { label: '65% (15-rep zone)', value: Math.round(avg * 0.65) + ' ' + unit },
    ]
  }
`

const faqs = [
  { question: 'What is a 1 rep max (1RM)?', answer: 'Your 1RM is the maximum weight you can lift for a single repetition with proper form. It is used to set training intensity percentages for strength programs. Testing your true 1RM carries injury risk, so estimating from submaximal lifts is safer.' },
  { question: 'How accurate are 1RM calculators?', answer: 'Most accurate for 1–5 rep sets (within 2–5%). Accuracy decreases for higher rep sets (10+) because the relationship between reps and maximal strength varies by individual, muscle fiber type, and exercise type. Experienced lifters can often handle a higher percentage of their 1RM for multiple reps than beginners.' },
  { question: 'What weight should I use for different rep ranges?', answer: '1RM = 100% | 3 reps ≈ 93% | 5 reps ≈ 87% | 8 reps ≈ 80% | 10 reps ≈ 75% | 12 reps ≈ 70% | 15 reps ≈ 65%. These are guidelines — individual responses vary significantly.' },
  { question: 'Should I actually test my 1RM?', answer: 'Not regularly. True 1RM testing is taxing and carries higher injury risk. Most strength programs use percentage-based training from an estimated or tested 1RM. Test your true 1RM only at the end of training cycles or for competition, with a spotter.' },
  { question: 'Which formula is most accurate — Epley or Brzycki?', answer: 'Neither is universally best. Both are validated formulas that perform similarly for 1–6 rep ranges. Brzycki tends to be more accurate at lower rep counts; Epley can overestimate at very high reps. Averaging both (as this calculator does) improves overall accuracy.' },
]
---
<Layout
  title="One Rep Max Calculator: Estimate Your 1RM"
  description="Estimate your one rep max from any weight and rep count using the Brzycki and Epley formulas. Free 1RM calculator with training percentage chart."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Fitness & Health', href: '/calculators/fitness' },
    { name: 'One Rep Max Calculator', href: '/calculators/one-rep-max-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/fitness" class="hover:text-blue-600">Fitness</a><span>›</span>
      <span class="text-gray-900">One Rep Max Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="One Rep Max Calculator"
          description="Estimate your maximum strength from submaximal lifts using validated formulas"
          formulaId="one-rep-max"
          formulaFn={formulaFn}
          resultLabel="Estimated 1RM"
          inputs={[
            { id: 'weight', label: 'Weight Lifted', type: 'number', placeholder: '225', min: 1, unit: 'lbs', defaultValue: 225 },
            { id: 'reps', label: 'Reps Performed', type: 'number', placeholder: '5', min: 1, max: 30, defaultValue: 5 },
            { id: 'unit', label: 'Weight Unit', type: 'select', options: [{ value: 'lbs', label: 'Pounds (lbs)' }, { value: 'kg', label: 'Kilograms (kg)' }], defaultValue: 'lbs' },
          ]}
          gauge={{
            min: 0, max: 100, unit: '% accuracy',
            zones: [
              { label: '1–3 reps (very accurate)', color: '#22c55e', from: 80, to: 100 },
              { label: '4–6 reps (accurate)', color: '#3b82f6', from: 60, to: 80 },
              { label: '7–10 reps (decent)', color: '#f59e0b', from: 40, to: 60 },
              { label: '10+ reps (rough estimate)', color: '#ef4444', from: 0, to: 40 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'Calorie Calculator', href: '/calculators/calorie-calculator' },
            { name: 'TDEE Calculator', href: '/calculators/tdee-calculator' },
            { name: 'Body Fat Calculator', href: '/calculators/body-fat-calculator' },
            { name: 'Protein Calculator', href: '/calculators/protein-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">1RM Percentage Chart</h3>
          <table class="w-full text-xs">
            <thead><tr class="text-blue-700"><th class="text-left pb-1">% of 1RM</th><th class="text-right pb-1">Approx. Reps</th><th class="text-right pb-1">Training Goal</th></tr></thead>
            <tbody class="text-blue-900">
              {[['95–100%','1–2','Max strength'],['85–92%','3–5','Strength'],['75–85%','6–8','Strength/size'],['65–75%','8–12','Hypertrophy'],['55–65%','12–15','Endurance'],['<55%','15+','Muscular endurance']].map(r => (
                <tr class="border-t border-blue-100"><td class="py-0.5">{r[0]}</td><td class="text-right">{r[1]}</td><td class="text-right">{r[2]}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
        <div class="bg-amber-50 border border-amber-200 rounded-xl p-5">
          <h3 class="font-bold text-amber-900 mb-2">Strength Standards (Bench Press)</h3>
          <div class="space-y-1 text-xs text-amber-800">
            {[['Beginner','<0.5× bodyweight'],['Novice','0.75× bodyweight'],['Intermediate','1× bodyweight'],['Advanced','1.5× bodyweight'],['Elite','2× bodyweight']].map(([l,s]) => (
              <div class="flex justify-between border-b border-amber-100 pb-1"><span>{l}</span><span class="font-medium">{s}</span></div>
            ))}
          </div>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Strength Standards by Lift</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr>
            <th class="text-left p-2 text-xs font-semibold text-gray-700">Lift</th>
            <th class="text-right p-2 text-xs font-semibold text-gray-700">Intermediate (male)</th>
            <th class="text-right p-2 text-xs font-semibold text-gray-700">Intermediate (female)</th>
          </tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[['Squat','1.5× BW','1.0× BW'],['Bench Press','1.0× BW','0.65× BW'],['Deadlift','1.75× BW','1.25× BW'],['Overhead Press','0.75× BW','0.5× BW']].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">How to Safely Test Your 1RM</h2>
        <div class="space-y-2">
          {[
            'Warm up thoroughly — 5–10 min cardio + dynamic stretching',
            'Do progressively heavier warm-up sets (50%, 70%, 80%, 90%)',
            'Rest 3–5 minutes between near-max attempts',
            'Make small jumps (2.5–5%) for each attempt',
            'Use a spotter for barbell lifts; have safety bars set',
            'Stop if form breaks down — technique before weight',
            'Limit true 1RM testing to 2–4 times per year',
          ].map(tip => (
            <div class="flex gap-2 text-xs text-gray-600">
              <span class="text-blue-500 mt-0.5">•</span>
              <span>{tip}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
</Layout>
''')

write("pace", '''---
import Layout from '../../layouts/Layout.astro'
import Calculator from '../../components/Calculator.astro'

const formulaFn = `
  const type = inputs.type || 'pace'
  const distNum = parseFloat(inputs.distance) || 0
  const distUnit = inputs.distUnit || 'miles'
  const timeH = parseInt(inputs.timeH) || 0
  const timeM = parseInt(inputs.timeM) || 0
  const timeS = parseInt(inputs.timeS) || 0
  const paceM = parseInt(inputs.paceMin) || 0
  const paceS = parseInt(inputs.paceSec) || 0
  if (distNum <= 0 && type !== 'time') throw new Error('Enter a distance.')
  const totalSec = timeH * 3600 + timeM * 60 + timeS
  const paceSec = paceM * 60 + paceS
  if (type === 'pace') {
    if (totalSec === 0) throw new Error('Enter a finish time.')
    const pacePerUnitSec = totalSec / distNum
    const pm = Math.floor(pacePerUnitSec / 60)
    const ps = Math.round(pacePerUnitSec % 60)
    const speed = (distNum / (totalSec / 3600))
    return {
      value: pm + ':' + ps.toString().padStart(2,'0') + ' per ' + distUnit,
      gaugeValue: Math.max(0, Math.min(100, 100 - (pacePerUnitSec - 240) / 4)),
      breakdown: ['Pace: ' + pm + ':' + ps.toString().padStart(2,'0') + '/' + distUnit, 'Speed: ' + speed.toFixed(2) + ' ' + distUnit + '/hr'],
      stats: [
        { label: 'Pace', value: pm + ':' + ps.toString().padStart(2,'0') + '/' + distUnit },
        { label: 'Speed', value: speed.toFixed(2) + ' ' + distUnit + '/hr' },
        { label: 'Total Time', value: timeH + 'h ' + timeM + 'm ' + timeS + 's' },
        { label: 'Distance', value: distNum + ' ' + distUnit },
      ]
    }
  } else if (type === 'time') {
    if (paceSec === 0) throw new Error('Enter a pace.')
    const totalT = paceSec * distNum
    const h = Math.floor(totalT / 3600)
    const m = Math.floor((totalT % 3600) / 60)
    const s = Math.round(totalT % 60)
    return {
      value: h + 'h ' + m + 'm ' + s + 's finish time',
      gaugeValue: 70,
      breakdown: ['Distance: ' + distNum + ' ' + distUnit, 'Pace: ' + paceM + ':' + paceS.toString().padStart(2,'0') + '/' + distUnit, 'Finish: ' + h + 'h ' + m + 'm ' + s + 's'],
      stats: [
        { label: 'Finish Time', value: h + ':' + m.toString().padStart(2,'0') + ':' + s.toString().padStart(2,'0') },
        { label: 'Pace', value: paceM + ':' + paceS.toString().padStart(2,'0') + '/' + distUnit },
        { label: 'Hours', value: String(h) },
        { label: 'Minutes', value: String(m) },
      ]
    }
  } else {
    if (totalSec === 0 || paceSec === 0) throw new Error('Enter time and pace.')
    const dist = totalSec / paceSec
    return {
      value: dist.toFixed(2) + ' ' + distUnit,
      gaugeValue: 70,
      breakdown: ['Time: ' + timeH + 'h ' + timeM + 'm ' + timeS + 's', 'Pace: ' + paceM + ':' + paceS.toString().padStart(2,'0') + '/' + distUnit, 'Distance: ' + dist.toFixed(2) + ' ' + distUnit],
      stats: [
        { label: 'Distance', value: dist.toFixed(2) + ' ' + distUnit },
        { label: 'Pace', value: paceM + ':' + paceS.toString().padStart(2,'0') + '/' + distUnit },
        { label: 'Finish Time', value: timeH + 'h ' + timeM + 'm' },
        { label: 'Speed', value: (dist / (totalSec/3600)).toFixed(2) + ' ' + distUnit + '/hr' },
      ]
    }
  }
`

const faqs = [
  { question: 'What is a good running pace?', answer: 'Average recreational runners run 9–11 min/mile (5:35–6:50 min/km). A "good" 5K time is under 25 minutes (8:00/mile). Competitive runners run 5–7 min/mile. Elite marathon pace is ~4:45/mile. Your "good" pace is one that challenges you and improves over time.' },
  { question: 'How do I convert pace to speed?', answer: 'Divide 60 (minutes) by your pace in minutes per mile. Example: 10:00/mile pace = 60 ÷ 10 = 6.0 mph. Or for kilometers: 6:00/km pace = 60 ÷ 6 = 10 km/h. This calculator shows both automatically.' },
  { question: 'What pace should I train at for a marathon?', answer: 'Easy runs: 1–2 minutes slower than goal race pace. Long runs: 60–90 seconds slower than race pace. Tempo runs: about 25–30 seconds faster than race pace. Speed work varies. Most training should be at conversational pace (easy effort).' },
  { question: 'How do I calculate my finish time?', answer: 'Multiply your pace per mile by the race distance in miles. A 10:00/mile pace for a half marathon (13.1 miles) = 131 minutes = 2 hours 11 minutes. Use this calculator\'s "finish time" mode to do this automatically.' },
  { question: 'What is negative splitting and why does it help?', answer: 'Running the second half of a race faster than the first. It is the most efficient racing strategy — going out too fast depletes glycogen and causes lactic acid buildup. Most world records are run as negative splits or even splits. For beginners, aim for even pacing.' },
]
---
<Layout
  title="Pace Calculator: Running Pace, Finish Time & Distance"
  description="Calculate running pace, finish time, or distance for any race. Supports miles and kilometers. Free pace calculator for runners."
  breadcrumbs={[
    { name: 'Home', href: '/' },
    { name: 'Fitness & Health', href: '/calculators/fitness' },
    { name: 'Pace Calculator', href: '/calculators/pace-calculator' },
  ]}
>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
    <nav class="text-xs text-gray-500 mb-6 flex gap-1 items-center flex-wrap">
      <a href="/" class="hover:text-blue-600">Home</a><span>›</span>
      <a href="/calculators/fitness" class="hover:text-blue-600">Fitness</a><span>›</span>
      <span class="text-gray-900">Pace Calculator</span>
    </nav>
    <div class="grid lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <Calculator
          title="Pace Calculator"
          description="Calculate running pace, predict finish time, or find distance covered"
          formulaId="pace"
          formulaFn={formulaFn}
          resultLabel="Result"
          inputs={[
            { id: 'type', label: 'Calculate', type: 'select', options: [
              { value: 'pace', label: 'Pace (from distance + time)' },
              { value: 'time', label: 'Finish Time (from distance + pace)' },
              { value: 'dist', label: 'Distance (from time + pace)' },
            ], defaultValue: 'pace' },
            { id: 'distance', label: 'Distance', type: 'number', placeholder: '5', min: 0.1, step: 0.1, defaultValue: 5 },
            { id: 'distUnit', label: 'Distance Unit', type: 'select', options: [{ value: 'miles', label: 'Miles' }, { value: 'km', label: 'Kilometers' }], defaultValue: 'miles' },
            { id: 'timeH', label: 'Time: Hours', type: 'number', placeholder: '0', min: 0, max: 24, defaultValue: 0 },
            { id: 'timeM', label: 'Time: Minutes', type: 'number', placeholder: '45', min: 0, max: 59, defaultValue: 45 },
            { id: 'timeS', label: 'Time: Seconds', type: 'number', placeholder: '0', min: 0, max: 59, defaultValue: 0 },
            { id: 'paceMin', label: 'Pace: Min/Mile (or km)', type: 'number', placeholder: '9', min: 0, max: 30, defaultValue: 9 },
            { id: 'paceSec', label: 'Pace: Seconds', type: 'number', placeholder: '0', min: 0, max: 59, defaultValue: 0 },
          ]}
          gauge={{
            min: 0, max: 100, unit: '% speed score',
            zones: [
              { label: 'Slow', color: '#94a3b8', from: 0, to: 30 },
              { label: 'Moderate', color: '#3b82f6', from: 30, to: 55 },
              { label: 'Fast', color: '#22c55e', from: 55, to: 80 },
              { label: 'Elite', color: '#f59e0b', from: 80, to: 100 },
            ]
          }}
          faqs={faqs}
          relatedCalcs={[
            { name: 'Running Calorie Calculator', href: '/calculators/running-calorie-calculator' },
            { name: 'Steps to Miles Calculator', href: '/calculators/steps-to-miles-calculator' },
            { name: 'Calories Burned Calculator', href: '/calculators/calories-burned-calculator' },
            { name: 'VO2 Max Calculator', href: '/calculators/vo2max-calculator' },
          ]}
        />
      </div>
      <aside class="space-y-5">
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-5">
          <h3 class="font-bold text-blue-900 mb-3">Race Distance Reference</h3>
          <div class="space-y-1 text-xs text-blue-800">
            {[['1 mile','1.609 km'],['5K','3.107 miles'],['10K','6.214 miles'],['Half Marathon','13.1 miles / 21.1 km'],['Marathon','26.2 miles / 42.2 km'],['50K Ultra','31.1 miles']].map(([race, dist]) => (
              <div class="flex justify-between border-b border-blue-100 pb-1"><span>{race}</span><span class="font-medium">{dist}</span></div>
            ))}
          </div>
        </div>
        <div class="bg-green-50 border border-green-200 rounded-xl p-5">
          <h3 class="font-bold text-green-900 mb-2">Pace Reference</h3>
          <div class="space-y-1 text-xs text-green-800">
            {[['6:00/mi','10.0 mph / 16.1 kph'],['7:30/mi','8.0 mph / 12.9 kph'],['9:00/mi','6.7 mph / 10.7 kph'],['10:00/mi','6.0 mph / 9.7 kph'],['12:00/mi','5.0 mph / 8.0 kph']].map(([p, s]) => (
              <div class="flex justify-between border-b border-green-100 pb-1"><span>{p}</span><span class="font-medium">{s}</span></div>
            ))}
          </div>
        </div>
      </aside>
    </div>
    <div class="mt-12 grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Common Race Finish Times</h2>
        <table class="w-full text-sm border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-50"><tr>
            <th class="text-left p-2 text-xs font-semibold text-gray-700">Race</th>
            <th class="text-right p-2 text-xs font-semibold text-gray-700">Beginner</th>
            <th class="text-right p-2 text-xs font-semibold text-gray-700">Average</th>
            <th class="text-right p-2 text-xs font-semibold text-gray-700">Good</th>
          </tr></thead>
          <tbody class="divide-y divide-gray-100">
            {[['5K','35–45 min','25–35 min','<25 min'],['10K','60–75 min','50–65 min','<50 min'],['Half Marathon','2h30m–3h','2h–2h30m','<2h'],['Marathon','5h–6h','4h–5h','<4h']].map(r => (
              <tr><td class="p-2 text-xs">{r[0]}</td><td class="p-2 text-xs text-right">{r[1]}</td><td class="p-2 text-xs text-right">{r[2]}</td><td class="p-2 text-xs text-right text-green-600">{r[3]}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <h2 class="text-xl font-bold text-gray-900 mb-4">Training Pace Zones</h2>
        <div class="space-y-2">
          {[
            { zone: 'Easy / Recovery', pace: '60–65 sec slower than race pace', purpose: 'Most runs (70–80% of training volume)' },
            { zone: 'Aerobic / Long Run', pace: '45–60 sec slower than race pace', purpose: 'Weekly long run, building base' },
            { zone: 'Tempo / Threshold', pace: '20–30 sec faster than race pace', purpose: 'Raise lactate threshold, 20–40 min efforts' },
            { zone: 'Interval / VO2', pace: '5K race pace or faster', purpose: 'Speed work, short intervals (400m–1mile)' },
          ].map(z => (
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="font-semibold text-gray-800 text-xs mb-1">{z.zone}</div>
              <div class="text-xs text-blue-600 mb-0.5">{z.pace}</div>
              <div class="text-xs text-gray-600">{z.purpose}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
</Layout>
''')

print("\\n✅ Batch 3 done. Written: ideal-weight, macro, water-intake, sleep, one-rep-max, pace")
