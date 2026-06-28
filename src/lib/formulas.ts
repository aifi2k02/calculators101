export interface CalcResult {
  value: string
  breakdown?: string[]
}

// ── MORTGAGE ──────────────────────────────────────────────────────────────
export function mortgage(principal: number, annualRate: number, years: number): CalcResult {
  if (principal <= 0 || annualRate < 0 || years <= 0) throw new Error('Please enter valid positive values.')
  const r = annualRate / 100 / 12
  const n = years * 12
  const monthly = r === 0
    ? principal / n
    : (principal * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1)
  const total = monthly * n
  const interest = total - principal
  return {
    value: `$${monthly.toFixed(2)}`,
    breakdown: [
      `Total payment: $${total.toFixed(2)}`,
      `Total interest: $${interest.toFixed(2)}`,
      `Principal: $${principal.toLocaleString()}`,
    ],
  }
}

// ── BMI ───────────────────────────────────────────────────────────────────
export function bmi(weightKg: number, heightCm: number): CalcResult {
  if (weightKg <= 0 || heightCm <= 0) throw new Error('Please enter valid weight and height.')
  const heightM = heightCm / 100
  const bmiVal = weightKg / (heightM * heightM)
  let category = ''
  if (bmiVal < 18.5) category = 'Underweight'
  else if (bmiVal < 25) category = 'Normal weight'
  else if (bmiVal < 30) category = 'Overweight'
  else category = 'Obese'
  return {
    value: bmiVal.toFixed(1),
    breakdown: [`Category: ${category}`],
  }
}

// ── TIP ───────────────────────────────────────────────────────────────────
export function tip(billAmount: number, tipPercent: number, numPeople: number): CalcResult {
  if (billAmount <= 0) throw new Error('Bill amount must be greater than 0.')
  const people = Math.max(1, numPeople)
  const tipAmount = (billAmount * tipPercent) / 100
  const total = billAmount + tipAmount
  const perPerson = total / people
  return {
    value: `$${perPerson.toFixed(2)}`,
    breakdown: [
      `Tip amount: $${tipAmount.toFixed(2)}`,
      `Total bill: $${total.toFixed(2)}`,
      `Per person: $${perPerson.toFixed(2)}`,
    ],
  }
}

// ── PERCENTAGE ────────────────────────────────────────────────────────────
export function percentage(value: number, total: number): CalcResult {
  if (total === 0) throw new Error('Total cannot be zero.')
  const pct = (value / total) * 100
  return {
    value: `${pct.toFixed(2)}%`,
    breakdown: [`${value} is ${pct.toFixed(2)}% of ${total}`],
  }
}

// ── AGE ───────────────────────────────────────────────────────────────────
export function age(birthDateStr: string): CalcResult {
  const birth = new Date(birthDateStr)
  if (isNaN(birth.getTime())) throw new Error('Please enter a valid birth date.')
  const now = new Date()
  let years = now.getFullYear() - birth.getFullYear()
  let months = now.getMonth() - birth.getMonth()
  let days = now.getDate() - birth.getDate()
  if (days < 0) { months--; days += new Date(now.getFullYear(), now.getMonth(), 0).getDate() }
  if (months < 0) { years--; months += 12 }
  const totalDays = Math.floor((now.getTime() - birth.getTime()) / 86400000)
  return {
    value: `${years} years`,
    breakdown: [
      `${years} years, ${months} months, ${days} days`,
      `Total days lived: ${totalDays.toLocaleString()}`,
    ],
  }
}

// ── COMPOUND INTEREST ─────────────────────────────────────────────────────
export function compoundInterest(principal: number, rate: number, years: number, n: number): CalcResult {
  if (principal <= 0 || rate < 0 || years <= 0) throw new Error('Please enter valid values.')
  const amount = principal * Math.pow(1 + rate / 100 / n, n * years)
  const interest = amount - principal
  return {
    value: `$${amount.toFixed(2)}`,
    breakdown: [
      `Principal: $${principal.toLocaleString()}`,
      `Interest earned: $${interest.toFixed(2)}`,
      `Total amount: $${amount.toFixed(2)}`,
    ],
  }
}

// ── GPA ───────────────────────────────────────────────────────────────────
export function gpa(grades: { grade: string; credits: number }[]): CalcResult {
  const gradeMap: Record<string, number> = {
    'A+': 4.0, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D+': 1.3, 'D': 1.0, 'D-': 0.7,
    'F': 0.0,
  }
  let totalPoints = 0, totalCredits = 0
  for (const { grade, credits } of grades) {
    const pts = gradeMap[grade.toUpperCase()]
    if (pts === undefined) throw new Error(`Unknown grade: ${grade}`)
    totalPoints += pts * credits
    totalCredits += credits
  }
  if (totalCredits === 0) throw new Error('Total credits cannot be zero.')
  const result = totalPoints / totalCredits
  return {
    value: result.toFixed(2),
    breakdown: [`Total credits: ${totalCredits}`, `Grade points: ${totalPoints.toFixed(1)}`],
  }
}

// ── LOAN ──────────────────────────────────────────────────────────────────
export function loan(principal: number, annualRate: number, months: number): CalcResult {
  if (principal <= 0 || months <= 0) throw new Error('Please enter valid values.')
  const r = annualRate / 100 / 12
  const monthly = r === 0
    ? principal / months
    : (principal * r * Math.pow(1 + r, months)) / (Math.pow(1 + r, months) - 1)
  const total = monthly * months
  const interest = total - principal
  return {
    value: `$${monthly.toFixed(2)}`,
    breakdown: [
      `Total repayment: $${total.toFixed(2)}`,
      `Total interest: $${interest.toFixed(2)}`,
    ],
  }
}

// ── CALORIE (BMR — Mifflin-St Jeor) ──────────────────────────────────────
export function calorie(weightKg: number, heightCm: number, age: number, sex: 'male' | 'female', activity: number): CalcResult {
  if (weightKg <= 0 || heightCm <= 0 || age <= 0) throw new Error('Please enter valid values.')
  const bmr = sex === 'male'
    ? 10 * weightKg + 6.25 * heightCm - 5 * age + 5
    : 10 * weightKg + 6.25 * heightCm - 5 * age - 161
  const tdee = bmr * activity
  return {
    value: `${Math.round(tdee)} kcal`,
    breakdown: [
      `BMR: ${Math.round(bmr)} kcal/day`,
      `Maintenance calories: ${Math.round(tdee)} kcal/day`,
      `For weight loss: ${Math.round(tdee - 500)} kcal/day`,
      `For weight gain: ${Math.round(tdee + 500)} kcal/day`,
    ],
  }
}

// ── DATE DIFFERENCE ───────────────────────────────────────────────────────
export function dateDiff(startStr: string, endStr: string): CalcResult {
  const start = new Date(startStr)
  const end = new Date(endStr)
  if (isNaN(start.getTime()) || isNaN(end.getTime())) throw new Error('Please enter valid dates.')
  const diffMs = Math.abs(end.getTime() - start.getTime())
  const days = Math.floor(diffMs / 86400000)
  const weeks = Math.floor(days / 7)
  const months = Math.abs(
    (end.getFullYear() - start.getFullYear()) * 12 + (end.getMonth() - start.getMonth())
  )
  return {
    value: `${days} days`,
    breakdown: [
      `${weeks} weeks and ${days % 7} days`,
      `Approximately ${months} months`,
    ],
  }
}
