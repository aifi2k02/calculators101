export interface CalcEntry {
  name: string
  href: string
  description: string
  icon: string
  live: boolean
}

export interface Category {
  slug: string
  name: string
  icon: string
  color: string
  bgClass: string
  borderClass: string
  textClass: string
  description: string
  metaDescription: string
  intro: string
  faqs: { question: string; answer: string }[]
  calculators: CalcEntry[]
}

export const categories: Category[] = [
  {
    slug: 'financial',
    name: 'Financial',
    icon: '💰',
    color: 'blue',
    bgClass: 'bg-blue-50',
    borderClass: 'border-blue-200',
    textClass: 'text-blue-700',
    description: 'Mortgage, loan, investment, and money calculators',
    metaDescription: 'Free financial calculators for mortgage, loans, compound interest, retirement, savings, and more. Make smarter money decisions with accurate, instant results.',
    intro: 'Make confident financial decisions with our free calculators. From figuring out your monthly mortgage payment to seeing how your savings grow with compound interest — every tool is instant, accurate, and requires no sign-up.',
    faqs: [
      { question: 'Are these financial calculators accurate?', answer: 'Yes. Each calculator uses the same formulas used by banks and financial institutions. Results are for informational purposes — always confirm major financial decisions with a licensed advisor.' },
      { question: 'Can I use these for home buying?', answer: 'Absolutely. The Mortgage Calculator shows your monthly payment and total interest, the Loan Calculator covers personal and auto loans, and the Compound Interest Calculator shows how savings and investments grow over time.' },
      { question: 'What is the most popular financial calculator?', answer: 'The Mortgage Calculator is the most-used, followed by the Loan Calculator and Compound Interest Calculator.' },
    ],
    calculators: [
      { name: 'Mortgage Calculator', href: '/calculators/mortgage-calculator', description: 'Monthly payment, total interest, and amortization', icon: '🏠', live: true },
      { name: 'Loan Calculator', href: '/calculators/loan-calculator', description: 'Monthly payments for any personal or auto loan', icon: '💳', live: true },
      { name: 'Business Loan Calculator', href: '/calculators/business-loan-calculator', description: 'Payment, interest, and true APR for business financing', icon: '🏢', live: true },
      { name: 'Student Loan Calculator', href: '/calculators/student-loan-calculator', description: 'Payment, interest, and payoff with extra payments', icon: '🎓', live: true },
      { name: 'Personal Loan Calculator', href: '/calculators/personal-loan-calculator', description: 'Payment and true APR including origination fees', icon: '🏦', live: true },
      { name: 'Mortgage Payoff Calculator', href: '/calculators/mortgage-payoff-calculator', description: 'Interest and years saved by paying extra', icon: '🏠', live: true },
      { name: 'Compound Interest Calculator', href: '/calculators/compound-interest-calculator', description: 'See how investments grow over time', icon: '📈', live: true },
      { name: 'Savings Calculator', href: '/calculators/savings-calculator', description: 'How long until you reach your savings goal', icon: '🏦', live: true },
      { name: 'Retirement Calculator', href: '/calculators/retirement-calculator', description: 'Project your nest egg and monthly retirement income', icon: '🎯', live: true },
      { name: 'Social Security Calculator', href: '/calculators/social-security-calculator', description: 'Estimate your monthly benefit by income and claiming age', icon: '🏛️', live: true },
      { name: 'Investment Calculator', href: '/calculators/investment-calculator', description: 'Future value of investments with contributions', icon: '📊', live: true },
      { name: 'Auto Loan Calculator', href: '/calculators/auto-loan-calculator', description: 'Monthly car payment with trade-in and down payment', icon: '🚗', live: true },
      { name: 'Interest Calculator', href: '/calculators/interest-calculator', description: 'Simple or compound interest on any amount', icon: '💵', live: true },
      { name: 'Credit Card Payoff', href: '/calculators/credit-card-calculator', description: 'Time and interest to pay off credit card debt', icon: '💳', live: true },
      { name: 'Debt Payoff Calculator', href: '/calculators/debt-payoff-calculator', description: 'Payoff timeline with extra payment analysis', icon: '📉', live: true },
      { name: 'Debt Consolidation Calculator', href: '/calculators/debt-consolidation-calculator', description: 'Combine debts into one lower-rate loan and see savings', icon: '🔗', live: true },
      { name: 'Inflation Calculator', href: '/calculators/inflation-calculator', description: 'Purchasing power over time', icon: '📋', live: true },
      { name: 'ROI Calculator', href: '/calculators/roi-calculator', description: 'Return on investment percentage and multiple', icon: '📈', live: true },
      { name: 'Salary Calculator', href: '/calculators/salary-calculator', description: 'Convert between hourly, annual, monthly pay', icon: '💼', live: true },
      { name: 'Budget Calculator', href: '/calculators/budget-calculator', description: '50/30/20 budget planning tool', icon: '📒', live: true },
      { name: 'Net Worth Calculator', href: '/calculators/net-worth-calculator', description: 'Total assets minus liabilities', icon: '💰', live: true },
      { name: 'Amortization Calculator', href: '/calculators/amortization-calculator', description: 'Full loan amortization schedule', icon: '📋', live: true },
      { name: 'House Affordability Calculator', href: '/calculators/house-affordability-calculator', description: 'How much home can you afford?', icon: '🏡', live: true },
      { name: 'Refinance Calculator', href: '/calculators/refinance-calculator', description: 'Monthly savings and break-even point', icon: '🔄', live: true },
      { name: 'Down Payment Calculator', href: '/calculators/down-payment-calculator', description: 'Down payment needed and savings timeline', icon: '🏦', live: true },
      { name: 'Paycheck Calculator', href: '/calculators/paycheck-calculator', description: 'Federal taxes, Social Security, and Medicare withholding', icon: '💵', live: true },
      { name: '401k Calculator', href: '/calculators/401k-calculator', description: 'Project your 401k balance at retirement', icon: '💼', live: true },
      { name: 'Rent vs Buy Calculator', href: '/calculators/rent-vs-buy-calculator', description: 'Compare true cost of renting vs buying', icon: '🏠', live: true },
      { name: 'Currency Converter', href: '/calculators/currency-calculator', description: 'Convert between 24 major currencies', icon: '💱', live: true },
      { name: 'APR Calculator', href: '/calculators/apr-calculator', description: 'True annual percentage rate including fees', icon: '📊', live: true },
      { name: 'Car Lease Calculator', href: '/calculators/car-lease-calculator', description: 'Monthly lease payment with money factor', icon: '🚗', live: true },
      { name: 'Home Equity Calculator', href: '/calculators/home-equity-calculator', description: 'Equity, LTV, and HELOC borrowing power', icon: '🏠', live: true },
      { name: 'CD Calculator', href: '/calculators/cd-calculator', description: 'Certificate of deposit interest and maturity value', icon: '🏦', live: true },
      { name: 'Stock Profit Calculator', href: '/calculators/stock-profit-calculator', description: 'Profit, loss, and ROI on any stock trade', icon: '📈', live: true },
      { name: 'Break-Even Calculator', href: '/calculators/break-even-calculator', description: 'Units and revenue needed to cover all costs', icon: '⚖️', live: true },
      { name: 'Markup Calculator', href: '/calculators/markup-calculator', description: 'Markup %, selling price, and gross margin', icon: '🏷️', live: true },
      { name: 'Mortgage Points Calculator', href: '/calculators/mortgage-points-calculator', description: 'Break-even and savings from discount points', icon: '📋', live: true },
      { name: 'Income Tax Calculator', href: '/calculators/income-tax-calculator', description: '2024 federal tax by bracket, effective rate, and marginal rate', icon: '🧾', live: true },
      { name: 'Depreciation Calculator', href: '/calculators/depreciation-calculator', description: 'Straight-line and double-declining asset depreciation', icon: '📉', live: true },
      { name: 'Roth IRA Calculator', href: '/calculators/roth-ira-calculator', description: 'Tax-free retirement balance vs Traditional IRA', icon: '💰', live: true },
      { name: 'PMI Calculator', href: '/calculators/pmi-calculator', description: 'Monthly PMI cost and payoff timeline', icon: '🏠', live: true },
      { name: 'Emergency Fund Calculator', href: '/calculators/emergency-fund-calculator', description: 'Target savings and timeline to build safety net', icon: '🏦', live: true },
      { name: 'FIRE Calculator', href: '/calculators/fire-calculator', description: 'Financial independence number and years to FIRE', icon: '🔥', live: true },
      { name: 'Capital Gains Tax Calculator', href: '/calculators/capital-gains-calculator', description: 'Federal tax on short-term and long-term gains', icon: '📈', live: true },
      { name: 'Annuity Calculator', href: '/calculators/annuity-calculator', description: 'Future value or required payment for regular contributions', icon: '📊', live: true },
      { name: 'Dividend Calculator', href: '/calculators/dividend-calculator', description: 'Dividend yield, income, and DRIP reinvestment projections', icon: '💹', live: true },
      { name: 'Rule of 72 Calculator', href: '/calculators/rule-of-72-calculator', description: 'How long to double an investment at any rate', icon: '⏱️', live: true },
      { name: 'NPV Calculator', href: '/calculators/npv-calculator', description: 'Net Present Value — should you take this investment?', icon: '📉', live: true },
      { name: 'Escrow Calculator', href: '/calculators/escrow-calculator', description: 'Monthly escrow and total PITI mortgage payment', icon: '🏠', live: true },
      { name: 'Payback Period Calculator', href: '/calculators/payback-period-calculator', description: 'How long until your investment pays for itself', icon: '⏳', live: true },
      { name: 'DCA Calculator', href: '/calculators/dca-calculator', description: 'Dollar cost averaging — project returns from monthly investing', icon: '📅', live: true },
      { name: 'Debt-to-Income Calculator', href: '/calculators/debt-to-income-calculator', description: 'DTI ratio for mortgage and loan qualification', icon: '⚖️', live: true },
      { name: 'Bond Yield Calculator', href: '/calculators/bond-yield-calculator', description: 'Yield to maturity (YTM) and fair bond price', icon: '📊', live: true },
      { name: 'College Savings Calculator', href: '/calculators/college-savings-calculator', description: '529 plan projections and college funding gap', icon: '🎓', live: true },
      { name: 'Crypto Profit Calculator', href: '/calculators/crypto-calculator', description: 'Profit, ROI, and return multiple for any crypto trade', icon: '₿', live: true },
      { name: 'Hourly to Salary Calculator', href: '/calculators/hourly-to-salary-calculator', description: 'Convert an hourly wage to weekly, monthly, and annual pay', icon: '💵', live: true },
      { name: 'Overtime Calculator', href: '/calculators/overtime-calculator', description: 'Overtime pay at 1.5× or 2× plus total weekly earnings', icon: '⏰', live: true },
      { name: 'Wedding Budget Calculator', href: '/calculators/wedding-budget-calculator', description: 'Break down your wedding budget by category', icon: '💒', live: true },
      { name: 'Tax Refund Calculator', href: '/calculators/tax-refund-calculator', description: 'Estimate your 2026 federal refund or balance due', icon: '💵', live: true },
      { name: '1099 / Freelancer Tax Calculator', href: '/calculators/1099-tax-calculator', description: 'Self-employment + income tax and quarterly set-aside', icon: '🧾', live: true },
      { name: 'Quarterly Estimated Tax Calculator', href: '/calculators/quarterly-tax-calculator', description: 'Per-quarter payments and all four IRS due dates', icon: '📆', live: true },
      { name: 'Self-Employment Tax Calculator', href: '/calculators/self-employment-tax-calculator', description: 'Social Security + Medicare on freelance earnings', icon: '🧮', live: true },
      { name: 'Content Creator Tax Calculator', href: '/calculators/creator-tax-calculator', description: 'Taxes on sponsorships, ads, affiliate, and merch', icon: '🎥', live: true },
      { name: 'Pay Raise Calculator', href: '/calculators/pay-raise-calculator', description: 'What your raise is really worth after tax and inflation', icon: '📈', live: true },
      { name: 'Cost of Living Raise Calculator', href: '/calculators/cost-of-living-raise-calculator', description: 'The raise you need to keep up with inflation', icon: '🛒', live: true },
      { name: 'Bonus Tax Calculator', href: '/calculators/bonus-tax-calculator', description: 'Take-home bonus after 22% withholding, FICA, and state tax', icon: '🎉', live: true },
      { name: 'Commission Calculator', href: '/calculators/commission-calculator', description: 'Sales commission and total pay from rate, base, and quota', icon: '🤝', live: true },
      { name: 'Influencer Earnings Calculator', href: '/calculators/creator-earnings-calculator', description: 'Estimated pay per sponsored post and per month', icon: '🌟', live: true },
      { name: 'Freelance Rate Calculator', href: '/calculators/freelance-rate-calculator', description: 'The hourly rate to charge to hit your income goal', icon: '💻', live: true },
      { name: 'Side Hustle Calculator', href: '/calculators/side-hustle-calculator', description: 'Real profit and true hourly rate after costs and tax', icon: '🚀', live: true },
      { name: 'Coast FIRE Calculator', href: '/calculators/coast-fire-calculator', description: 'The amount to invest now to coast to retirement', icon: '🏝️', live: true },
      { name: 'Nurse Pay Calculator', href: '/calculators/nurse-pay-calculator', description: 'Real pay with night & weekend shift differentials', icon: '🩺', live: true },
      { name: 'Present Value Calculator', href: '/calculators/present-value-calculator', description: 'What a future sum of money is worth today', icon: '⏮️', live: true },
      { name: 'Future Value Calculator', href: '/calculators/future-value-calculator', description: 'What a lump sum plus deposits grows to over time', icon: '⏭️', live: true },
      { name: 'Simple Interest Calculator', href: '/calculators/simple-interest-calculator', description: 'Interest and total using I = P × r × t', icon: '📈', live: true },
      { name: 'Percent Off Calculator', href: '/calculators/percent-off-calculator', description: 'Sale price and savings on any discount', icon: '🏷️', live: true },
    ],
  },
  {
    slug: 'fitness',
    name: 'Fitness & Health',
    icon: '🏃',
    color: 'green',
    bgClass: 'bg-green-50',
    borderClass: 'border-green-200',
    textClass: 'text-green-700',
    description: 'BMI, calorie, TDEE, and health calculators',
    metaDescription: 'Free fitness and health calculators for BMI, calories, TDEE, body fat, macros, and more. Science-based results, instantly.',
    intro: 'Track your health and reach your fitness goals with our science-backed calculators. Whether you want to know your BMI, calculate your daily calorie needs, or plan your macros — our tools use clinically validated formulas to give you accurate results.',
    faqs: [
      { question: 'What formula is used for BMI?', answer: 'BMI = weight (kg) ÷ height² (m²). This is the standard formula from the World Health Organization. For imperial units, BMI = (weight in lbs × 703) ÷ height² (in²).' },
      { question: 'What formula is used for calorie calculation?', answer: 'We use the Mifflin-St Jeor equation, which is considered the most accurate for most adults. It factors in your age, sex, weight, height, and activity level.' },
      { question: 'Are these health calculators suitable for medical advice?', answer: 'These calculators are informational tools. Always consult a healthcare professional or registered dietitian for personalized medical or nutritional advice.' },
    ],
    calculators: [
      { name: 'BMI Calculator', href: '/calculators/bmi-calculator', description: 'Body Mass Index with weight category', icon: '⚖️', live: true },
      { name: 'Calorie Calculator', href: '/calculators/calorie-calculator', description: 'Daily calorie needs based on your goals', icon: '🥗', live: true },
      { name: 'TDEE Calculator', href: '/calculators/tdee-calculator', description: 'Total daily energy expenditure by activity level', icon: '🔥', live: true },
      { name: 'Body Fat Calculator', href: '/calculators/body-fat-calculator', description: 'Body fat % using the US Navy method', icon: '📏', live: true },
      { name: 'Ideal Weight Calculator', href: '/calculators/ideal-weight-calculator', description: 'Ideal weight range using 4 clinical formulas', icon: '🎯', live: true },
      { name: 'Macro Calculator', href: '/calculators/macro-calculator', description: 'Daily protein, carb, and fat targets', icon: '🥩', live: true },
      { name: 'Carbohydrate Calculator', href: '/calculators/carbohydrate-calculator', description: 'Daily carb grams from calories and diet split', icon: '🍞', live: true },
      { name: 'Heart Rate Calculator', href: '/calculators/heart-rate-calculator', description: 'Max HR and training zones by age', icon: '❤️', live: true },
      { name: 'Target Heart Rate Calculator', href: '/calculators/target-heart-rate-calculator', description: 'Max HR and training zones (Karvonen) by age', icon: '🎯', live: true },
      { name: 'Water Intake Calculator', href: '/calculators/water-intake-calculator', description: 'Daily water needs by weight and activity', icon: '💧', live: true },
      { name: 'Due Date Calculator', href: '/calculators/due-date-calculator', description: 'Pregnancy due date from LMP or conception', icon: '🤰', live: true },
      { name: 'Ovulation Calculator', href: '/calculators/ovulation-calculator', description: 'Fertile window and ovulation date', icon: '📅', live: true },
      { name: 'Pace Calculator', href: '/calculators/pace-calculator', description: 'Running pace, finish time, or distance', icon: '🏃', live: true },
      { name: 'Sleep Calculator', href: '/calculators/sleep-calculator', description: 'Best time to sleep or wake up', icon: '😴', live: true },
      { name: 'Calories Burned Calculator', href: '/calculators/calories-burned-calculator', description: 'Calories burned for 20+ activities', icon: '🔥', live: true },
      { name: 'Protein Calculator', href: '/calculators/protein-calculator', description: 'Daily protein needs by weight and goal', icon: '🥩', live: true },
      { name: 'Waist-to-Hip Ratio Calculator', href: '/calculators/waist-hip-calculator', description: 'WHR, body shape, and cardiovascular health risk', icon: '📏', live: true },
      { name: 'One Rep Max Calculator', href: '/calculators/one-rep-max-calculator', description: 'Estimate 1RM and training weights from any set', icon: '🏋️', live: true },
      { name: 'BAC Calculator', href: '/calculators/bac-calculator', description: 'Blood alcohol content using Widmark formula', icon: '🍺', live: true },
      { name: 'BMR Calculator', href: '/calculators/bmr-calculator', description: 'Basal metabolic rate — Mifflin-St Jeor & Harris-Benedict', icon: '🔥', live: true },
      { name: 'Lean Body Mass Calculator', href: '/calculators/lean-body-mass-calculator', description: 'Weight minus fat using Boer formula or body fat %', icon: '💪', live: true },
      { name: 'Caloric Deficit Calculator', href: '/calculators/caloric-deficit-calculator', description: 'Daily calorie target and weight loss timeline', icon: '🥗', live: true },
      { name: 'Steps to Miles Calculator', href: '/calculators/steps-to-miles-calculator', description: 'Convert steps to distance and calories burned', icon: '👟', live: true },
      { name: 'Pregnancy Weight Gain Calculator', href: '/calculators/pregnancy-weight-calculator', description: 'IOM-recommended weight gain by pre-pregnancy BMI', icon: '🤰', live: true },
      { name: 'VO2 Max Calculator', href: '/calculators/vo2max-calculator', description: 'Estimate aerobic capacity from 3 test methods', icon: '🏃', live: true },
      { name: 'Keto Calculator', href: '/calculators/keto-calculator', description: 'Personalized keto macros: fat, protein, and carbs', icon: '🥑', live: true },
      { name: 'Body Surface Area Calculator', href: '/calculators/body-surface-area-calculator', description: 'BSA in m² using 4 validated medical formulas', icon: '📏', live: true },
      { name: 'Running Calorie Calculator', href: '/calculators/running-calorie-calculator', description: 'Calories burned running by weight and distance', icon: '🏃', live: true },
      { name: 'Intermittent Fasting Calculator', href: '/calculators/intermittent-fasting-calculator', description: 'Eating window, fasting window, and meal schedule', icon: '⏱️', live: true },
      { name: 'Army Body Fat Calculator', href: '/calculators/army-body-fat-calculator', description: 'Military tape-test body fat and AR 600-9 pass limits', icon: '🎖️', live: true },
      { name: 'Life Expectancy Calculator', href: '/calculators/life-expectancy-calculator', description: 'Estimate your lifespan from age, sex, and lifestyle', icon: '⏳', live: true },
    ],
  },
  {
    slug: 'math',
    name: 'Math',
    icon: '📐',
    color: 'purple',
    bgClass: 'bg-purple-50',
    borderClass: 'border-purple-200',
    textClass: 'text-purple-700',
    description: 'Percentage, fraction, algebra, and number calculators',
    metaDescription: 'Free math calculators for percentage, fractions, averages, area, volume, triangles, ratios, and more. Fast and accurate for students and professionals.',
    intro: 'From quick percentage calculations to complex geometry — our math calculators cover everything students, teachers, and professionals need. All results show step-by-step breakdowns so you understand the "how" behind every answer.',
    faqs: [
      { question: 'How do I calculate a percentage?', answer: 'There are three common percentage problems: (1) X% of Y — multiply Y by X/100. (2) X is what % of Y — divide X by Y and multiply by 100. (3) Percentage change — divide the difference by the original value and multiply by 100.' },
      { question: 'What math calculators are available?', answer: 'Percentage, average/statistics, fractions, ratios, area, volume, triangle, and exponent calculators are all live. More are being added regularly.' },
      { question: 'Are these calculators good for students?', answer: 'Yes. Every calculator shows a step-by-step breakdown of the calculation, making it easy to learn the formula, not just the answer.' },
    ],
    calculators: [
      { name: 'Percentage Calculator', href: '/calculators/percentage-calculator', description: 'Percent of, percent change, and what percent', icon: '📊', live: true },
      { name: 'Average Calculator', href: '/calculators/average-calculator', description: 'Mean, median, mode, and standard deviation', icon: '📉', live: true },
      { name: 'Fraction Calculator', href: '/calculators/fraction-calculator', description: 'Add, subtract, multiply, and divide fractions', icon: '½', live: true },
      { name: 'Ratio Calculator', href: '/calculators/ratio-calculator', description: 'Simplify ratios or solve proportions', icon: '⚖️', live: true },
      { name: 'Area Calculator', href: '/calculators/area-calculator', description: 'Area of squares, rectangles, circles, triangles', icon: '⬜', live: true },
      { name: 'Volume Calculator', href: '/calculators/volume-calculator', description: 'Volume of 3D shapes — cubes, spheres, cylinders', icon: '📦', live: true },
      { name: 'Surface Area Calculator', href: '/calculators/surface-area-calculator', description: 'Surface area of cubes, spheres, cylinders & cones', icon: '📐', live: true },
      { name: 'Triangle Calculator', href: '/calculators/triangle-calculator', description: 'Area, sides, and angles via Pythagorean theorem', icon: '📐', live: true },
      { name: 'Exponent Calculator', href: '/calculators/exponent-calculator', description: 'Any base raised to any power', icon: '🔢', live: true },
      { name: 'Square Root Calculator', href: '/calculators/square-root-calculator', description: 'Square roots, cube roots, squares, and cubes', icon: '√', live: true },
      { name: 'Logarithm Calculator', href: '/calculators/logarithm-calculator', description: 'Log base 10, natural log, or any custom base', icon: 'log', live: true },
      { name: 'LCM & GCD Calculator', href: '/calculators/lcm-gcd-calculator', description: 'Least common multiple and greatest common divisor', icon: '🔢', live: true },
      { name: 'Random Number Generator', href: '/calculators/random-number-calculator', description: 'Random numbers in any range', icon: '🎲', live: true },
      { name: 'Binary Converter', href: '/calculators/binary-calculator', description: 'Convert between binary, decimal, hex, and octal', icon: '01', live: true },
      { name: 'Quadratic Calculator', href: '/calculators/quadratic-calculator', description: 'Solve ax² + bx + c = 0 with roots and vertex', icon: '📐', live: true },
      { name: 'Matrix Calculator', href: '/calculators/matrix-calculator', description: 'Add, multiply, determinant & inverse (2×2 to 4×4)', icon: '🔢', live: true },
      { name: 'Unit Converter', href: '/calculators/unit-converter-calculator', description: 'Convert length, weight, volume, temperature, speed', icon: '⚖️', live: true },
      { name: 'Scientific Notation', href: '/calculators/scientific-notation-calculator', description: 'Convert to and from scientific notation', icon: '🔬', live: true },
      { name: 'Combination Calculator', href: '/calculators/combination-calculator', description: 'Combinations C(n,r) and permutations P(n,r)', icon: '🔢', live: true },
      { name: 'Permutation Calculator', href: '/calculators/permutation-calculator', description: 'Permutations nPr — ordered arrangements of r from n', icon: '🔢', live: true },
      { name: 'Factorial Calculator', href: '/calculators/factorial-calculator', description: 'Calculate n! with multiplication steps', icon: '!', live: true },
      { name: 'Prime Number Calculator', href: '/calculators/prime-calculator', description: 'Check if a number is prime or find the nth prime', icon: '🔢', live: true },
      { name: 'Significant Figures Calculator', href: '/calculators/sig-figs-calculator', description: 'Count sig figs and round to any precision', icon: '🔬', live: true },
      { name: 'Slope Calculator', href: '/calculators/slope-calculator', description: 'Slope, distance, midpoint, and line equation', icon: '📐', live: true },
      { name: 'Rounding Calculator', href: '/calculators/rounding-calculator', description: 'Round to decimal places with floor, ceil, or truncate', icon: '🔢', live: true },
      { name: 'Modulo Calculator', href: '/calculators/modulo-calculator', description: 'Remainder after division — a mod b', icon: '%', live: true },
      { name: 'Z-Score Calculator', href: '/calculators/z-score-calculator', description: 'Standard score and percentile for normal distributions', icon: '📊', live: true },
      { name: 'Percentage Error Calculator', href: '/calculators/percentage-error-calculator', description: 'Percent error between experimental and theoretical values', icon: '🔬', live: true },
      { name: 'Circle Calculator', href: '/calculators/circle-calculator', description: 'Area, circumference, diameter, and radius from any input', icon: '⭕', live: true },
      { name: 'Law of Cosines Calculator', href: '/calculators/law-of-cosines-calculator', description: 'Solve any triangle from SSS or SAS', icon: '📐', live: true },
      { name: 'Angle Converter', href: '/calculators/angle-converter-calculator', description: 'Convert between degrees, radians, gradians, and arc minutes', icon: '🔄', live: true },
      { name: 'Distance Formula Calculator', href: '/calculators/distance-calculator', description: 'Distance and midpoint between two points in 2D or 3D', icon: '📏', live: true },
      { name: 'Number Base Converter', href: '/calculators/number-base-calculator', description: 'Convert between binary, decimal, hex, octal, and any base 2–36', icon: '🔢', live: true },
      { name: 'Tank Volume Calculator', href: '/calculators/tank-volume-calculator', description: 'Capacity of cylinder, rectangular, and oval tanks in gallons or liters', icon: '🛢️', live: true },
      { name: 'Basic Calculator', href: '/calculators/basic-calculator', description: 'Fast online calculator for add, subtract, multiply, divide', icon: '🧮', live: true },
      { name: 'Scientific Calculator', href: '/calculators/scientific-calculator', description: 'Trig, logs, exponents, roots & constants with full order of operations', icon: '🧪', live: true },
      { name: 'Standard Deviation Calculator', href: '/calculators/standard-deviation-calculator', description: 'Standard deviation, variance & mean (sample or population)', icon: '📊', live: true },
      { name: 'Mean, Median, Mode Calculator', href: '/calculators/mean-median-mode-calculator', description: 'Mean, median, mode, and range for any data set', icon: '📈', live: true },
      { name: 'Probability Calculator', href: '/calculators/probability-calculator', description: 'Single and two-event probability with and/or/not', icon: '🎲', live: true },
      { name: 'Pythagorean Theorem Calculator', href: '/calculators/pythagorean-theorem-calculator', description: 'Solve a² + b² = c² for any right-triangle side', icon: '📐', live: true },
      { name: 'Number Sequence Calculator', href: '/calculators/number-sequence-calculator', description: 'nth term & sum of arithmetic or geometric sequences', icon: '🔢', live: true },
      { name: 'Confidence Interval Calculator', href: '/calculators/confidence-interval-calculator', description: 'Confidence interval & margin of error for a mean', icon: '📏', live: true },
      { name: 'Sample Size Calculator', href: '/calculators/sample-size-calculator', description: 'How many people to survey for a reliable result', icon: '👥', live: true },
      { name: 'Half-Life Calculator', href: '/calculators/half-life-calculator', description: 'Remaining amount, decay constant & mean lifetime', icon: '☢️', live: true },
    ],
  },
  {
    slug: 'other',
    name: 'Other',
    icon: '⚙️',
    color: 'amber',
    bgClass: 'bg-amber-50',
    borderClass: 'border-amber-200',
    textClass: 'text-amber-700',
    description: 'Age, date, GPA, tip, discount, and everyday calculators',
    metaDescription: 'Free everyday calculators for age, date differences, GPA, tip splitting, discounts, sales tax, grades, and more.',
    intro: 'Everyday calculations made effortless. Find your exact age, split a restaurant bill, calculate your GPA, convert Roman numerals, or figure out your final exam score — all in seconds, with no sign-up required.',
    faqs: [
      { question: 'How does the Age Calculator work?', answer: 'Enter your date of birth and the calculator computes your exact age in years, months, and days, plus total days lived, total weeks, and your next birthday countdown.' },
      { question: 'How is GPA calculated?', answer: 'GPA = Total grade points ÷ Total credit hours. Grade points are assigned per letter grade (A=4.0, B=3.0, etc.) and weighted by the credit hours for each course.' },
      { question: 'Can I calculate days between any two dates?', answer: 'Yes. The Date Calculator supports any date range and also lets you add or subtract days from a date to find a future or past date.' },
    ],
    calculators: [
      { name: 'Age Calculator', href: '/calculators/age-calculator', description: 'Exact age in years, months, days, and weeks', icon: '🎂', live: true },
      { name: 'Date Calculator', href: '/calculators/date-calculator', description: 'Days between dates or add/subtract days', icon: '📅', live: true },
      { name: 'GPA Calculator', href: '/calculators/gpa-calculator', description: 'Semester GPA from course grades and credits', icon: '🎓', live: true },
      { name: 'Tip Calculator', href: '/calculators/tip-calculator', description: 'Tip amount and bill split per person', icon: '🍽️', live: true },
      { name: 'Discount Calculator', href: '/calculators/discount-calculator', description: 'Sale price after discount or find % off', icon: '🏷️', live: true },
      { name: 'Sales Tax Calculator', href: '/calculators/sales-tax-calculator', description: 'Add or reverse-calculate sales tax', icon: '🧾', live: true },
      { name: 'Grade Calculator', href: '/calculators/grade-calculator', description: 'Overall grade from multiple scores', icon: '📝', live: true },
      { name: 'Final Grade Calculator', href: '/calculators/final-grade-calculator', description: 'Score needed on final exam', icon: '🎯', live: true },
      { name: 'Time Calculator', href: '/calculators/time-calculator', description: 'Time difference, add hours, convert minutes', icon: '⏱️', live: true },
      { name: 'Roman Numeral Converter', href: '/calculators/roman-numeral-calculator', description: 'Convert numbers to/from Roman numerals', icon: 'Ⅷ', live: true },
      { name: 'Speed Calculator', href: '/calculators/speed-calculator', description: 'Calculate speed, distance, or time', icon: '⚡', live: true },
      { name: 'Fuel Cost Calculator', href: '/calculators/fuel-cost-calculator', description: 'Total fuel cost for any trip', icon: '⛽', live: true },
      { name: 'Electricity Cost Calculator', href: '/calculators/electricity-calculator', description: 'Monthly cost to run any appliance', icon: '💡', live: true },
      { name: 'Word Count Calculator', href: '/calculators/word-count-calculator', description: 'Word count, reading time, and text stats', icon: '📝', live: true },
      { name: 'Password Generator', href: '/calculators/password-calculator', description: 'Strong random passwords with entropy score', icon: '🔒', live: true },
      { name: 'Paint Calculator', href: '/calculators/paint-calculator', description: 'Gallons of paint needed for a room', icon: '🎨', live: true },
      { name: 'Concrete Calculator', href: '/calculators/concrete-calculator', description: 'Cubic yards and bags for slabs, columns, footings', icon: '🧱', live: true },
      { name: 'Gravel Calculator', href: '/calculators/gravel-calculator', description: 'Cubic yards and tons of gravel for any area', icon: '🪨', live: true },
      { name: 'Military Time Converter', href: '/calculators/military-time-calculator', description: 'Convert between 12-hour and 24-hour time', icon: '🕐', live: true },
      { name: 'Days Until Calculator', href: '/calculators/days-until-calculator', description: 'Countdown to any future or past date', icon: '📅', live: true },
      { name: 'Height Converter', href: '/calculators/height-converter-calculator', description: 'Convert cm to feet/inches and vice versa', icon: '📏', live: true },
      { name: 'Zodiac Sign Calculator', href: '/calculators/zodiac-calculator', description: 'Western sun sign, element, and Chinese zodiac', icon: '⭐', live: true },
      { name: 'Numerology Calculator', href: '/calculators/numerology-calculator', description: 'Life Path Number and Destiny Number', icon: '🔮', live: true },
      { name: 'Color Converter', href: '/calculators/color-converter-calculator', description: 'Convert between HEX, RGB, and HSL color codes', icon: '🎨', live: true },
      { name: 'Number to Words Converter', href: '/calculators/number-to-words-calculator', description: 'Convert any number to English words', icon: '🔤', live: true },
      { name: 'GST / VAT Calculator', href: '/calculators/gst-vat-calculator', description: 'Add or remove GST, VAT, or any consumption tax', icon: '🧾', live: true },
      { name: 'Love Calculator', href: '/calculators/love-calculator', description: 'Fun compatibility score for any two names', icon: '💕', live: true },
      { name: 'Dog Age Calculator', href: '/calculators/dog-age-calculator', description: 'Dog years to human years by breed size', icon: '🐕', live: true },
      { name: 'Cooking Measurement Converter', href: '/calculators/cooking-calculator', description: 'Convert cups, tablespoons, ounces, grams, and more', icon: '🥄', live: true },
      { name: 'Shoe Size Converter', href: '/calculators/shoe-size-calculator', description: 'Convert shoe sizes between US, UK, EU, and cm', icon: '👟', live: true },
      { name: 'Roof Pitch Calculator', href: '/calculators/roof-pitch-calculator', description: 'Pitch, angle, slope, and rafter length', icon: '🏠', live: true },
      { name: 'Time Card Calculator', href: '/calculators/time-card-calculator', description: 'Total work hours from clock-in and clock-out with breaks', icon: '⏱️', live: true },
      { name: 'Gas Mileage Calculator', href: '/calculators/gas-mileage-calculator', description: 'MPG, cost per mile, and trip fuel cost', icon: '⛽', live: true },
      { name: 'Tile Calculator', href: '/calculators/tile-calculator', description: 'Number of tiles and boxes needed for any room', icon: '🧱', live: true },
      { name: 'Mulch Calculator', href: '/calculators/mulch-calculator', description: 'Cubic yards and bags of mulch for any bed', icon: '🌱', live: true },
      { name: 'Roofing Calculator', href: '/calculators/roofing-calculator', description: 'Roof area, squares, and shingle bundles by pitch', icon: '🏠', live: true },
      { name: 'Carbon Footprint Calculator', href: '/calculators/carbon-footprint-calculator', description: 'Estimate your annual CO₂ emissions in tons', icon: '🌍', live: true },
      { name: 'Pizza Calculator', href: '/calculators/pizza-calculator', description: 'How many pizzas to order for any party size', icon: '🍕', live: true },
      { name: 'Subscription Cost Calculator', href: '/calculators/subscription-cost-calculator', description: 'The true lifetime cost of your subscriptions', icon: '💸', live: true },
      { name: 'Screen Time Calculator', href: '/calculators/screen-time-calculator', description: 'How many years of your life you spend on screens', icon: '📱', live: true },
      { name: 'Hash Calculator', href: '/calculators/hash-calculator', description: 'Generate MD5, SHA-1, SHA-256 & SHA-512 hashes from text', icon: '🔐', live: true },
      { name: 'Business Days Calculator', href: '/calculators/business-days-calculator', description: 'Working days between two dates, excluding weekends', icon: '📆', live: true },
      { name: 'Day of the Week Calculator', href: '/calculators/day-of-week-calculator', description: 'What day of the week any date falls on', icon: '🗓️', live: true },
      { name: 'Week Number Calculator', href: '/calculators/week-number-calculator', description: 'The ISO week number for any date', icon: '📅', live: true },
      { name: 'Time Zone Converter', href: '/calculators/time-zone-converter', description: 'Convert time between world time zones, DST-accurate', icon: '🌐', live: true },
      { name: 'Sunrise & Sunset Calculator', href: '/calculators/sunrise-sunset-calculator', description: 'Sunrise, sunset, and day length for any location', icon: '🌅', live: true },
      { name: 'Moon Phase Calculator', href: '/calculators/moon-phase-calculator', description: 'Moon phase, illumination, and next full moon', icon: '🌙', live: true },
      { name: 'Wind Chill Calculator', href: '/calculators/wind-chill-calculator', description: 'How cold it really feels, via the official NWS formula', icon: '🥶', live: true },
      { name: 'BTU Calculator', href: '/calculators/btu-calculator', description: 'Cooling BTUs a room needs — AC sizing', icon: '❄️', live: true },
      { name: 'Heat Index Calculator', href: '/calculators/heat-index-calculator', description: 'How hot it really feels, from temperature and humidity', icon: '🥵', live: true },
      { name: 'Dew Point Calculator', href: '/calculators/dew-point-calculator', description: 'Dew point and comfort level from temp and humidity', icon: '💧', live: true },
      { name: 'Density Calculator', href: '/calculators/density-calculator', description: 'Density from mass and volume in any units', icon: '⚖️', live: true },
      { name: 'Base64 Calculator', href: '/calculators/base64-calculator', description: 'Encode text to Base64 or decode it back (UTF-8 safe)', icon: '🔤', live: true },
      { name: 'URL Encode Calculator', href: '/calculators/url-encode-calculator', description: 'Percent-encode text for URLs or decode it back', icon: '🔗', live: true },
      { name: 'IP Subnet Calculator', href: '/calculators/ip-subnet-calculator', description: 'Network, broadcast, mask & usable hosts from CIDR', icon: '🌐', live: true },
      { name: 'Ohm’s Law Calculator', href: '/calculators/ohms-law-calculator', description: 'Solve volts, amps, ohms & watts from any two', icon: '⚡', live: true },
      { name: 'Square Footage Calculator', href: '/calculators/square-footage-calculator', description: 'Area from length × width, plus material cost', icon: '📐', live: true },
    ],
  },
]

export function getCategoryBySlug(slug: string): Category | undefined {
  return categories.find(c => c.slug === slug)
}

// ─── Topical silos: SEO clustering for internal linking. URLs are UNCHANGED. ───
// Each calculator keeps its flat /calculators/{slug} URL; silos only drive
// related-link clustering, hub pages, and breadcrumbs.
export interface SiloMeta { id: string; name: string; hubs: string[] }

export const silos: SiloMeta[] = [
  { id: 'loans', name: 'Loans & Mortgage', hubs: ['Mortgage & Home', 'Auto & Personal Loans', 'Debt & Credit'] },
  { id: 'invest', name: 'Investing & Retirement', hubs: ['Retirement', 'Investing & Returns', 'Savings & Wealth'] },
  { id: 'tax', name: 'Taxes', hubs: ['Income & Sales Tax', 'Business & Self-Employed Tax', 'Refunds & Deductions'] },
  { id: 'pay', name: 'Income & Pay', hubs: ['Salary & Wages', 'Raises & Bonuses', 'Gig & Creator Economy'] },
  { id: 'budget', name: 'Budget & Spending', hubs: ['Everyday Money', 'Bills & Running Costs'] },
  { id: 'body', name: 'Body & Weight', hubs: ['Body Composition', 'Weight Goals'] },
  { id: 'nutri', name: 'Nutrition & Diet', hubs: ['Calories & Macros', 'Diets & Food'] },
  { id: 'exer', name: 'Exercise & Cardio', hubs: ['Running & Cardio', 'Strength & Vitals'] },
  { id: 'health', name: 'Health & Life', hubs: ['Pregnancy & Cycle', 'Wellness & Body'] },
  { id: 'math', name: 'Core Math', hubs: ['Arithmetic', 'Algebra', 'Geometry', 'Grades & GPA'] },
  { id: 'stats', name: 'Stats & Numbers', hubs: ['Statistics', 'Number Systems', 'Developer Tools'] },
  { id: 'date', name: 'Date & Time', hubs: ['Dates', 'Time'] },
  { id: 'home', name: 'Home & DIY', hubs: ['Construction', 'Materials'] },
  { id: 'sci', name: 'Science & Weather', hubs: ['Weather', 'Physics & Space'] },
  { id: 'fun', name: 'Fun & Lifestyle', hubs: ['Fun', 'Utilities'] },
]

// slug (href without the /calculators/ prefix) → its silo + hub
export const siloAssignments: Record<string, { silo: string; hub: string }> = {
  // Loans & Mortgage
  'mortgage-calculator': { silo: 'loans', hub: 'Mortgage & Home' },
  'loan-calculator': { silo: 'loans', hub: 'Auto & Personal Loans' },
  'auto-loan-calculator': { silo: 'loans', hub: 'Auto & Personal Loans' },
  'business-loan-calculator': { silo: 'loans', hub: 'Auto & Personal Loans' },
  'student-loan-calculator': { silo: 'loans', hub: 'Auto & Personal Loans' },
  'personal-loan-calculator': { silo: 'loans', hub: 'Auto & Personal Loans' },
  'mortgage-payoff-calculator': { silo: 'loans', hub: 'Mortgage & Home' },
  'interest-calculator': { silo: 'loans', hub: 'Debt & Credit' },
  'credit-card-calculator': { silo: 'loans', hub: 'Debt & Credit' },
  'debt-payoff-calculator': { silo: 'loans', hub: 'Debt & Credit' },
  'debt-consolidation-calculator': { silo: 'loans', hub: 'Debt & Credit' },
  'amortization-calculator': { silo: 'loans', hub: 'Mortgage & Home' },
  'house-affordability-calculator': { silo: 'loans', hub: 'Mortgage & Home' },
  'refinance-calculator': { silo: 'loans', hub: 'Mortgage & Home' },
  'down-payment-calculator': { silo: 'loans', hub: 'Mortgage & Home' },
  'rent-vs-buy-calculator': { silo: 'loans', hub: 'Mortgage & Home' },
  'apr-calculator': { silo: 'loans', hub: 'Auto & Personal Loans' },
  'car-lease-calculator': { silo: 'loans', hub: 'Auto & Personal Loans' },
  'home-equity-calculator': { silo: 'loans', hub: 'Mortgage & Home' },
  'mortgage-points-calculator': { silo: 'loans', hub: 'Mortgage & Home' },
  'pmi-calculator': { silo: 'loans', hub: 'Mortgage & Home' },
  'escrow-calculator': { silo: 'loans', hub: 'Mortgage & Home' },
  'debt-to-income-calculator': { silo: 'loans', hub: 'Debt & Credit' },
  'simple-interest-calculator': { silo: 'loans', hub: 'Debt & Credit' },
  // Investing & Retirement
  'compound-interest-calculator': { silo: 'invest', hub: 'Investing & Returns' },
  'savings-calculator': { silo: 'invest', hub: 'Savings & Wealth' },
  'retirement-calculator': { silo: 'invest', hub: 'Retirement' },
  'investment-calculator': { silo: 'invest', hub: 'Investing & Returns' },
  'roi-calculator': { silo: 'invest', hub: 'Investing & Returns' },
  'net-worth-calculator': { silo: 'invest', hub: 'Savings & Wealth' },
  '401k-calculator': { silo: 'invest', hub: 'Retirement' },
  'social-security-calculator': { silo: 'invest', hub: 'Retirement' },
  'cd-calculator': { silo: 'invest', hub: 'Investing & Returns' },
  'stock-profit-calculator': { silo: 'invest', hub: 'Investing & Returns' },
  'roth-ira-calculator': { silo: 'invest', hub: 'Retirement' },
  'emergency-fund-calculator': { silo: 'invest', hub: 'Savings & Wealth' },
  'fire-calculator': { silo: 'invest', hub: 'Savings & Wealth' },
  'lcm-gcd-calculator': { silo: 'math', hub: 'Arithmetic' },
  'annuity-calculator': { silo: 'invest', hub: 'Retirement' },
  'dividend-calculator': { silo: 'invest', hub: 'Investing & Returns' },
  'rule-of-72-calculator': { silo: 'invest', hub: 'Investing & Returns' },
  'npv-calculator': { silo: 'invest', hub: 'Investing & Returns' },
  'payback-period-calculator': { silo: 'invest', hub: 'Investing & Returns' },
  'dca-calculator': { silo: 'invest', hub: 'Investing & Returns' },
  'bond-yield-calculator': { silo: 'invest', hub: 'Investing & Returns' },
  'college-savings-calculator': { silo: 'invest', hub: 'Retirement' },
  'crypto-calculator': { silo: 'invest', hub: 'Investing & Returns' },
  'coast-fire-calculator': { silo: 'invest', hub: 'Savings & Wealth' },
  'present-value-calculator': { silo: 'invest', hub: 'Investing & Returns' },
  'future-value-calculator': { silo: 'invest', hub: 'Investing & Returns' },
  // Taxes
  'inflation-calculator': { silo: 'invest', hub: 'Investing & Returns' },
  'break-even-calculator': { silo: 'tax', hub: 'Refunds & Deductions' },
  'markup-calculator': { silo: 'tax', hub: 'Refunds & Deductions' },
  'income-tax-calculator': { silo: 'tax', hub: 'Income & Sales Tax' },
  'capital-gains-calculator': { silo: 'tax', hub: 'Income & Sales Tax' },
  'sales-tax-calculator': { silo: 'tax', hub: 'Income & Sales Tax' },
  'depreciation-calculator': { silo: 'tax', hub: 'Refunds & Deductions' },
  'gst-vat-calculator': { silo: 'tax', hub: 'Income & Sales Tax' },
  'tax-refund-calculator': { silo: 'tax', hub: 'Refunds & Deductions' },
  '1099-tax-calculator': { silo: 'tax', hub: 'Business & Self-Employed Tax' },
  'quarterly-tax-calculator': { silo: 'tax', hub: 'Business & Self-Employed Tax' },
  'self-employment-tax-calculator': { silo: 'tax', hub: 'Business & Self-Employed Tax' },
  'creator-tax-calculator': { silo: 'tax', hub: 'Business & Self-Employed Tax' },
  'bonus-tax-calculator': { silo: 'tax', hub: 'Refunds & Deductions' },
  'business-days-calculator': { silo: 'date', hub: 'Dates' },
  // Income & Pay
  'salary-calculator': { silo: 'pay', hub: 'Salary & Wages' },
  'paycheck-calculator': { silo: 'pay', hub: 'Salary & Wages' },
  'hourly-to-salary-calculator': { silo: 'pay', hub: 'Salary & Wages' },
  'overtime-calculator': { silo: 'pay', hub: 'Salary & Wages' },
  'time-card-calculator': { silo: 'pay', hub: 'Salary & Wages' },
  'pay-raise-calculator': { silo: 'pay', hub: 'Raises & Bonuses' },
  'cost-of-living-raise-calculator': { silo: 'pay', hub: 'Raises & Bonuses' },
  'commission-calculator': { silo: 'pay', hub: 'Salary & Wages' },
  'subscription-cost-calculator': { silo: 'pay', hub: 'Gig & Creator Economy' },
  'screen-time-calculator': { silo: 'pay', hub: 'Gig & Creator Economy' },
  'creator-earnings-calculator': { silo: 'pay', hub: 'Gig & Creator Economy' },
  'freelance-rate-calculator': { silo: 'pay', hub: 'Gig & Creator Economy' },
  'side-hustle-calculator': { silo: 'pay', hub: 'Gig & Creator Economy' },
  'nurse-pay-calculator': { silo: 'pay', hub: 'Raises & Bonuses' },
  // Budget & Spending
  'budget-calculator': { silo: 'budget', hub: 'Everyday Money' },
  'currency-calculator': { silo: 'budget', hub: 'Everyday Money' },
  'tip-calculator': { silo: 'budget', hub: 'Everyday Money' },
  'discount-calculator': { silo: 'budget', hub: 'Everyday Money' },
  'fuel-cost-calculator': { silo: 'budget', hub: 'Bills & Running Costs' },
  'electricity-calculator': { silo: 'budget', hub: 'Bills & Running Costs' },
  'wedding-budget-calculator': { silo: 'budget', hub: 'Everyday Money' },
  'gas-mileage-calculator': { silo: 'budget', hub: 'Bills & Running Costs' },
  'percent-off-calculator': { silo: 'budget', hub: 'Everyday Money' },
  // Body & Weight
  'bmi-calculator': { silo: 'body', hub: 'Body Composition' },
  'tdee-calculator': { silo: 'body', hub: 'Weight Goals' },
  'body-fat-calculator': { silo: 'body', hub: 'Body Composition' },
  'ideal-weight-calculator': { silo: 'body', hub: 'Weight Goals' },
  'waist-hip-calculator': { silo: 'body', hub: 'Body Composition' },
  'bmr-calculator': { silo: 'body', hub: 'Body Composition' },
  'lean-body-mass-calculator': { silo: 'body', hub: 'Body Composition' },
  'caloric-deficit-calculator': { silo: 'body', hub: 'Weight Goals' },
  'pregnancy-weight-calculator': { silo: 'body', hub: 'Weight Goals' },
  'body-surface-area-calculator': { silo: 'body', hub: 'Body Composition' },
  'army-body-fat-calculator': { silo: 'body', hub: 'Body Composition' },
  // Nutrition & Diet
  'calorie-calculator': { silo: 'nutri', hub: 'Calories & Macros' },
  'macro-calculator': { silo: 'nutri', hub: 'Calories & Macros' },
  'carbohydrate-calculator': { silo: 'nutri', hub: 'Calories & Macros' },
  'water-intake-calculator': { silo: 'nutri', hub: 'Calories & Macros' },
  'calories-burned-calculator': { silo: 'nutri', hub: 'Calories & Macros' },
  'protein-calculator': { silo: 'nutri', hub: 'Calories & Macros' },
  'keto-calculator': { silo: 'nutri', hub: 'Diets & Food' },
  'intermittent-fasting-calculator': { silo: 'nutri', hub: 'Diets & Food' },
  'cooking-calculator': { silo: 'nutri', hub: 'Diets & Food' },
  'pizza-calculator': { silo: 'nutri', hub: 'Diets & Food' },
  // Exercise & Cardio
  'heart-rate-calculator': { silo: 'exer', hub: 'Running & Cardio' },
  'target-heart-rate-calculator': { silo: 'exer', hub: 'Running & Cardio' },
  'pace-calculator': { silo: 'exer', hub: 'Running & Cardio' },
  'sleep-calculator': { silo: 'exer', hub: 'Strength & Vitals' },
  'one-rep-max-calculator': { silo: 'exer', hub: 'Strength & Vitals' },
  'bac-calculator': { silo: 'exer', hub: 'Strength & Vitals' },
  'speed-calculator': { silo: 'exer', hub: 'Running & Cardio' },
  'steps-to-miles-calculator': { silo: 'exer', hub: 'Running & Cardio' },
  'vo2max-calculator': { silo: 'exer', hub: 'Running & Cardio' },
  'running-calorie-calculator': { silo: 'exer', hub: 'Running & Cardio' },
  'distance-calculator': { silo: 'exer', hub: 'Running & Cardio' },
  // Health & Life
  'due-date-calculator': { silo: 'health', hub: 'Pregnancy & Cycle' },
  'ovulation-calculator': { silo: 'health', hub: 'Pregnancy & Cycle' },
  'height-converter-calculator': { silo: 'health', hub: 'Wellness & Body' },
  'shoe-size-calculator': { silo: 'health', hub: 'Wellness & Body' },
  'carbon-footprint-calculator': { silo: 'health', hub: 'Wellness & Body' },
  'life-expectancy-calculator': { silo: 'health', hub: 'Wellness & Body' },
  // Core Math
  'percentage-calculator': { silo: 'math', hub: 'Arithmetic' },
  'average-calculator': { silo: 'math', hub: 'Arithmetic' },
  'fraction-calculator': { silo: 'math', hub: 'Arithmetic' },
  'ratio-calculator': { silo: 'math', hub: 'Arithmetic' },
  'area-calculator': { silo: 'math', hub: 'Geometry' },
  'surface-area-calculator': { silo: 'math', hub: 'Geometry' },
  'volume-calculator': { silo: 'math', hub: 'Geometry' },
  'triangle-calculator': { silo: 'math', hub: 'Geometry' },
  'exponent-calculator': { silo: 'math', hub: 'Arithmetic' },
  'square-root-calculator': { silo: 'math', hub: 'Arithmetic' },
  'logarithm-calculator': { silo: 'math', hub: 'Arithmetic' },
  'quadratic-calculator': { silo: 'math', hub: 'Algebra' },
  'matrix-calculator': { silo: 'math', hub: 'Algebra' },
  'factorial-calculator': { silo: 'math', hub: 'Arithmetic' },
  'slope-calculator': { silo: 'math', hub: 'Algebra' },
  'rounding-calculator': { silo: 'math', hub: 'Arithmetic' },
  'modulo-calculator': { silo: 'math', hub: 'Arithmetic' },
  'gpa-calculator': { silo: 'math', hub: 'Grades & GPA' },
  'grade-calculator': { silo: 'math', hub: 'Grades & GPA' },
  'final-grade-calculator': { silo: 'math', hub: 'Grades & GPA' },
  'percentage-error-calculator': { silo: 'math', hub: 'Arithmetic' },
  'circle-calculator': { silo: 'math', hub: 'Geometry' },
  'law-of-cosines-calculator': { silo: 'math', hub: 'Geometry' },
  'angle-converter-calculator': { silo: 'math', hub: 'Geometry' },
  'basic-calculator': { silo: 'math', hub: 'Arithmetic' },
  'scientific-calculator': { silo: 'math', hub: 'Arithmetic' },
  'pythagorean-theorem-calculator': { silo: 'math', hub: 'Geometry' },
  'number-sequence-calculator': { silo: 'math', hub: 'Algebra' },
  'square-footage-calculator': { silo: 'math', hub: 'Geometry' },
  // Stats & Numbers
  'random-number-calculator': { silo: 'stats', hub: 'Number Systems' },
  'binary-calculator': { silo: 'stats', hub: 'Number Systems' },
  'scientific-notation-calculator': { silo: 'stats', hub: 'Number Systems' },
  'combination-calculator': { silo: 'stats', hub: 'Statistics' },
  'permutation-calculator': { silo: 'stats', hub: 'Statistics' },
  'prime-calculator': { silo: 'stats', hub: 'Number Systems' },
  'sig-figs-calculator': { silo: 'stats', hub: 'Number Systems' },
  'roman-numeral-calculator': { silo: 'stats', hub: 'Number Systems' },
  'password-calculator': { silo: 'stats', hub: 'Developer Tools' },
  'z-score-calculator': { silo: 'stats', hub: 'Statistics' },
  'color-converter-calculator': { silo: 'stats', hub: 'Developer Tools' },
  'number-to-words-calculator': { silo: 'stats', hub: 'Number Systems' },
  'number-base-calculator': { silo: 'stats', hub: 'Number Systems' },
  'hash-calculator': { silo: 'stats', hub: 'Developer Tools' },
  'standard-deviation-calculator': { silo: 'stats', hub: 'Statistics' },
  'mean-median-mode-calculator': { silo: 'stats', hub: 'Statistics' },
  'probability-calculator': { silo: 'stats', hub: 'Statistics' },
  'confidence-interval-calculator': { silo: 'stats', hub: 'Statistics' },
  'sample-size-calculator': { silo: 'stats', hub: 'Statistics' },
  'base64-calculator': { silo: 'stats', hub: 'Developer Tools' },
  'url-encode-calculator': { silo: 'stats', hub: 'Developer Tools' },
  'ip-subnet-calculator': { silo: 'stats', hub: 'Developer Tools' },
  // Home & DIY
  'unit-converter-calculator': { silo: 'home', hub: 'Materials' },
  'paint-calculator': { silo: 'home', hub: 'Materials' },
  'concrete-calculator': { silo: 'home', hub: 'Construction' },
  'gravel-calculator': { silo: 'home', hub: 'Materials' },
  'roof-pitch-calculator': { silo: 'home', hub: 'Construction' },
  'tank-volume-calculator': { silo: 'home', hub: 'Construction' },
  'tile-calculator': { silo: 'home', hub: 'Materials' },
  'mulch-calculator': { silo: 'home', hub: 'Materials' },
  'roofing-calculator': { silo: 'home', hub: 'Construction' },
  // Date & Time
  'age-calculator': { silo: 'date', hub: 'Dates' },
  'date-calculator': { silo: 'date', hub: 'Dates' },
  'time-calculator': { silo: 'date', hub: 'Time' },
  'military-time-calculator': { silo: 'date', hub: 'Time' },
  'days-until-calculator': { silo: 'date', hub: 'Dates' },
  'day-of-week-calculator': { silo: 'date', hub: 'Dates' },
  'week-number-calculator': { silo: 'date', hub: 'Dates' },
  'time-zone-converter': { silo: 'date', hub: 'Time' },
  // Fun & Lifestyle
  'word-count-calculator': { silo: 'fun', hub: 'Utilities' },
  'zodiac-calculator': { silo: 'fun', hub: 'Fun' },
  'numerology-calculator': { silo: 'fun', hub: 'Fun' },
  'love-calculator': { silo: 'fun', hub: 'Fun' },
  'dog-age-calculator': { silo: 'fun', hub: 'Fun' },
  // Science & Weather
  'sunrise-sunset-calculator': { silo: 'sci', hub: 'Physics & Space' },
  'moon-phase-calculator': { silo: 'sci', hub: 'Physics & Space' },
  'wind-chill-calculator': { silo: 'sci', hub: 'Weather' },
  'btu-calculator': { silo: 'sci', hub: 'Physics & Space' },
  'heat-index-calculator': { silo: 'sci', hub: 'Weather' },
  'dew-point-calculator': { silo: 'sci', hub: 'Weather' },
  'half-life-calculator': { silo: 'sci', hub: 'Physics & Space' },
  'density-calculator': { silo: 'sci', hub: 'Physics & Space' },
  'ohms-law-calculator': { silo: 'sci', hub: 'Physics & Space' },
}

// Flat slug → entry lookup, built once from the category lists above.
const _bySlug: Record<string, CalcEntry> = Object.fromEntries(
  categories.flatMap(c => c.calculators).map(e => [e.href.replace('/calculators/', ''), e])
)

// Flat slug → its registry category (the real category page it lives under).
const _catOf: Record<string, { slug: string; name: string }> = Object.fromEntries(
  categories.flatMap(c =>
    c.calculators.map(e => [e.href.replace('/calculators/', ''), { slug: c.slug, name: c.name }])
  )
)

function _slugOf(href: string): string {
  return href.replace('/calculators/', '').replace(/^\/+|\/+$/g, '')
}

export function getSiloOf(href: string): { silo: string; hub: string } | undefined {
  return siloAssignments[_slugOf(href)]
}

export function getSiloMeta(id: string): SiloMeta | undefined {
  return silos.find(s => s.id === id)
}

/**
 * Related calculators for a page, scoped to its topical silo.
 * Order: same hub first (tightest match), then rest of the silo. Only ever
 * returns live, existing pages — never invents a URL.
 */
export function getRelated(href: string, limit = 6): { name: string; href: string }[] {
  const slug = _slugOf(href)
  const me = siloAssignments[slug]
  if (!me) return []
  const others = Object.entries(siloAssignments).filter(
    ([s]) => s !== slug && _bySlug[s]?.live
  )
  const sameHub = others.filter(([, v]) => v.silo === me.silo && v.hub === me.hub)
  const sameSilo = others.filter(([, v]) => v.silo === me.silo && v.hub !== me.hub)
  return [...sameHub, ...sameSilo]
    .slice(0, limit)
    .map(([s]) => ({ name: _bySlug[s].name, href: _bySlug[s].href }))
}

/**
 * Breadcrumb trail for a calculator page, with the topical silo as a tier:
 *   Home › {Category} › {Silo} › {Calculator}
 * The category tier is the calculator's real registry category. The silo tier
 * links to that category page with a #{siloId} anchor (repoint to a dedicated
 * hub page once those exist). Returns [] for non-calculator URLs.
 */
export function getBreadcrumbs(href: string): { name: string; href: string }[] {
  const slug = _slugOf(href)
  const entry = _bySlug[slug]
  const cat = _catOf[slug]
  const a = siloAssignments[slug]
  if (!entry || !cat || !a) return []
  const meta = getSiloMeta(a.silo)
  const hub = getSiloHub(a.silo)
  const siloHref = hub ? `/calculators/${hub.slug}` : `/calculators/${cat.slug}#${a.silo}`
  return [
    { name: 'Home', href: '/' },
    { name: cat.name, href: `/calculators/${cat.slug}` },
    { name: meta ? meta.name : a.silo, href: siloHref },
    { name: entry.name, href: entry.href },
  ]
}

// ─── Silo hub pages: rankable landing pages at /calculators/{slug}/ that ───
// aggregate a topical cluster and target its head keyword. Additive: no
// existing URL changes. The breadcrumb silo tier links here.
export interface SiloHub {
  id: string          // matches a silo id in `silos`
  slug: string        // URL slug under /calculators/
  parentCat: string   // registry category slug this cluster sits under
  title: string       // H1 + SEO title base
  description: string // meta description
  intro: string
  faqs: { question: string; answer: string }[]
}

export const siloHubs: SiloHub[] = [
  {
    id: 'loans', slug: 'loans', parentCat: 'financial',
    title: 'Loan & Mortgage Calculators',
    description: 'Free loan and mortgage calculators — monthly payments, amortization, refinancing, auto loans, home affordability, and debt payoff. Instant, accurate, no sign-up.',
    intro: 'Everything you need to plan borrowing and pay down debt. Estimate a mortgage payment, run a full amortization schedule, compare refinancing, size an auto or personal loan, and build a debt-payoff plan — all in one place.',
    faqs: [
      { question: 'Which loan calculator should I start with?', answer: 'For a home, start with the Mortgage Calculator for your monthly payment, then House Affordability to see your budget and Amortization to view the full payoff schedule. For a car, use the Auto Loan Calculator; for cards and other debt, use the Debt Payoff Calculator.' },
      { question: 'Are these calculators accurate?', answer: 'Yes — they use the standard amortization formula banks and lenders use. Results are estimates for planning; your actual rate and payment depend on your lender, credit score, and local taxes.' },
    ],
  },
  {
    id: 'invest', slug: 'investing', parentCat: 'financial',
    title: 'Investment & Retirement Calculators',
    description: 'Free investment and retirement calculators — compound interest, 401k, Roth IRA, FIRE, ROI, dividends, and future value. Project your growth instantly.',
    intro: 'Model how your money grows and plan for retirement. Project compound interest and future value, run 401k and Roth IRA scenarios, find your FIRE number, and measure returns with ROI, dividend, and net-worth tools.',
    faqs: [
      { question: 'How do I project my retirement savings?', answer: 'Use the 401k or Retirement Calculator to project your balance from contributions, employer match, and expected return. The FIRE and Coast FIRE calculators show the number you need to retire early.' },
      { question: 'What return rate should I assume?', answer: 'A common long-run assumption for a diversified stock portfolio is 6–7% after inflation, but returns vary year to year. Try a range of rates to see best- and worst-case outcomes.' },
    ],
  },
  {
    id: 'tax', slug: 'taxes', parentCat: 'financial',
    title: 'Tax Calculators',
    description: 'Free tax calculators — income tax, sales tax, capital gains, self-employment, 1099, quarterly estimates, and tax refund. Estimate what you owe in seconds.',
    intro: 'Estimate what you owe and what you keep. Calculate federal income tax by bracket, sales tax and VAT, capital gains, self-employment and 1099 taxes, quarterly estimates, and your expected refund.',
    faqs: [
      { question: 'Can these calculators file my taxes?', answer: 'No — they are estimation tools to help you plan and set money aside. Use them to understand your likely bill, then file with the IRS or a tax professional.' },
      { question: 'Which calculator is right for freelancers?', answer: 'Use the 1099 / Freelancer Tax Calculator and the Self-Employment Tax Calculator together, then the Quarterly Estimated Tax Calculator to plan your four IRS payments.' },
    ],
  },
  {
    id: 'pay', slug: 'income', parentCat: 'financial',
    title: 'Paycheck & Income Calculators',
    description: 'Free paycheck and income calculators — take-home pay, salary vs hourly, overtime, raises, bonuses, commission, and freelance rates. Know your real pay.',
    intro: 'Understand your real earnings. Convert salary to hourly, estimate take-home pay after withholding, calculate overtime and commission, and see what a raise, bonus, or freelance rate is actually worth.',
    faqs: [
      { question: 'How do I find my take-home pay?', answer: 'Use the Paycheck Calculator to estimate net pay after federal tax, Social Security, and Medicare. For hourly work, start with Hourly to Salary, then add Overtime.' },
      { question: 'What is my raise really worth?', answer: 'The Pay Raise Calculator shows your increase after tax, and the Cost of Living Raise Calculator shows the raise you need just to keep up with inflation.' },
    ],
  },
  {
    id: 'budget', slug: 'budgeting', parentCat: 'financial',
    title: 'Budgeting & Spending Calculators',
    description: 'Free budgeting calculators — 50/30/20 budget, tips, discounts, currency, fuel cost, and subscription spending. Take control of your money.',
    intro: 'Plan your spending and catch waste. Build a 50/30/20 budget, split a tip, work out discounts and currency conversions, estimate fuel and driving costs, and see the true lifetime cost of your subscriptions.',
    faqs: [
      { question: 'What is the 50/30/20 budget?', answer: 'It splits after-tax income into 50% needs, 30% wants, and 20% savings and debt payoff. The Budget Calculator applies it to your income automatically.' },
      { question: 'How can these tools save me money?', answer: 'The Subscription Cost Calculator reveals recurring spend you may have forgotten, while the Fuel Cost and Discount calculators help with everyday decisions.' },
    ],
  },
  {
    id: 'body', slug: 'body-weight', parentCat: 'fitness',
    title: 'Body Fat & Weight Calculators',
    description: 'Free body composition calculators — BMI, body fat %, BMR, TDEE, ideal weight, and lean body mass. Science-based formulas, instant results.',
    intro: 'Measure and track your body composition. Calculate BMI, body fat percentage, basal metabolic rate, ideal weight range, and lean body mass using clinically validated formulas.',
    faqs: [
      { question: 'Is BMI or body fat percentage better?', answer: 'BMI is a fast screening tool but does not distinguish muscle from fat. For a fuller picture, pair it with the Body Fat and Lean Body Mass calculators, especially if you are muscular.' },
      { question: 'What is BMR and why does it matter?', answer: 'Basal metabolic rate is the calories your body burns at rest. It is the starting point for setting calorie targets — use the BMR Calculator, then TDEE for your daily total.' },
    ],
  },
  {
    id: 'nutri', slug: 'nutrition', parentCat: 'fitness',
    title: 'Nutrition & Diet Calculators',
    description: 'Free nutrition calculators — daily calories, macros, protein, keto, intermittent fasting, and water intake. Plan your diet with confidence.',
    intro: 'Dial in your diet. Calculate daily calorie needs, macro and protein targets, keto ratios, an intermittent fasting schedule, and how much water to drink for your body and goals.',
    faqs: [
      { question: 'How many calories should I eat?', answer: 'Start with the Calorie Calculator for your maintenance level, then adjust for your goal. The Caloric Deficit Calculator shows a target and timeline for weight loss.' },
      { question: 'How much protein do I need?', answer: 'The Protein Calculator recommends a daily target based on your weight, activity, and goal — generally higher for those building muscle or losing fat.' },
    ],
  },
  {
    id: 'exer', slug: 'exercise', parentCat: 'fitness',
    title: 'Exercise & Cardio Calculators',
    description: 'Free exercise calculators — calories burned, running pace, VO2 max, heart rate zones, one-rep max, and steps to miles. Train smarter.',
    intro: 'Get more from your training. Estimate calories burned, running pace and finish time, VO2 max, heart-rate zones, and your one-rep max, and convert steps to miles and distance.',
    faqs: [
      { question: 'How do I find my training heart-rate zones?', answer: 'The Heart Rate Calculator estimates your maximum heart rate and target zones by age, so you can train at the right intensity for endurance or fat burning.' },
      { question: 'What is a one-rep max and why calculate it?', answer: 'Your one-rep max is the most weight you can lift once. The One Rep Max Calculator estimates it from any set so you can program training weights without maxing out.' },
    ],
  },
  {
    id: 'health', slug: 'health', parentCat: 'fitness',
    title: 'Health & Wellness Calculators',
    description: 'Free health calculators — pregnancy due date, ovulation, life expectancy, height converter, and shoe size. Simple, science-based tools.',
    intro: 'Everyday health and wellness tools. Estimate a pregnancy due date and fertile window, project life expectancy from lifestyle, and convert height and shoe sizes.',
    faqs: [
      { question: 'How accurate is the due date calculator?', answer: 'It uses the standard method (280 days from your last period, or from conception) that clinicians use for an estimated due date. Only about 1 in 20 babies arrive on the exact date.' },
      { question: 'Are these medical tools?', answer: 'No — they are informational estimates. For personal medical decisions, always consult a qualified healthcare professional.' },
    ],
  },
  {
    id: 'math', slug: 'core-math', parentCat: 'math',
    title: 'Arithmetic, Algebra & Geometry Calculators',
    description: 'Free math calculators — percentages, fractions, exponents, square roots, quadratic equations, area, volume, triangles, and GPA. Step-by-step results.',
    intro: 'Solve everyday and school math fast. Work with percentages, fractions, exponents and roots, quadratic equations, geometry (area, volume, triangles, circles), and grades and GPA.',
    faqs: [
      { question: 'Do these calculators show the steps?', answer: 'Many, including the Quadratic, Fraction, and Percentage calculators, show the breakdown so you can follow and learn the method, not just the answer.' },
      { question: 'Which calculator handles geometry?', answer: 'Use the Area, Volume, Circle, and Triangle calculators for shapes, and the Pythagorean Theorem and Law of Cosines calculators for triangle sides and angles.' },
    ],
  },
  {
    id: 'stats', slug: 'statistics', parentCat: 'math',
    title: 'Statistics & Number Calculators',
    description: 'Free statistics calculators — mean, median, mode, standard deviation, z-score, probability, confidence interval, plus binary, hex, and dev tools.',
    intro: 'Crunch data and convert numbers. Calculate mean, median, mode, standard deviation, z-scores, probability, and confidence intervals, and work with binary, number bases, hashes, and other developer tools.',
    faqs: [
      { question: 'Which calculator finds standard deviation?', answer: 'The Standard Deviation Calculator computes both sample and population standard deviation, plus variance and the mean, from any list of numbers.' },
      { question: 'Can I convert between number systems?', answer: 'Yes — use the Binary, Number Base, and Scientific Notation calculators to convert between decimal, binary, hexadecimal, and more.' },
    ],
  },
  {
    id: 'date', slug: 'date-time', parentCat: 'other',
    title: 'Date & Time Calculators',
    description: 'Free date and time calculators — age, date difference, business days, day of week, week number, time zones, and countdowns. DST-accurate.',
    intro: 'Work with dates and time precisely. Calculate your age, the difference between two dates, business days, the day of the week for any date, ISO week numbers, time-zone conversions, and days until an event.',
    faqs: [
      { question: 'How does the business days calculator work?', answer: 'It counts working days between two dates, excluding weekends, so you can plan deadlines and delivery windows accurately.' },
      { question: 'Are time-zone conversions daylight-saving accurate?', answer: 'Yes — the Time Zone Converter uses the official IANA time-zone database, so it applies the correct offset and DST rules for the exact date you choose.' },
    ],
  },
  {
    id: 'home', slug: 'home-diy', parentCat: 'other',
    title: 'Home & DIY Calculators',
    description: 'Free home and DIY calculators — concrete, paint, tile, mulch, square footage, roof pitch, and tank volume. Estimate materials before you buy.',
    intro: 'Plan projects and buy the right amount of materials. Estimate concrete, paint, tile, and mulch quantities, measure square footage, work out roof pitch, and calculate tank volume.',
    faqs: [
      { question: 'How do I estimate materials for a project?', answer: 'Enter your area or dimensions and the calculator returns the quantity you need — for example bags of concrete, gallons of paint, or boxes of tile — plus a bit of guidance on waste allowance.' },
      { question: 'What is square footage used for?', answer: 'Square footage drives most material and cost estimates. Use the Square Footage Calculator first, then feed the result into the paint, tile, or flooring estimate.' },
    ],
  },
  {
    id: 'sci', slug: 'science', parentCat: 'other',
    title: 'Science & Weather Calculators',
    description: 'Free science calculators — wind chill, heat index, dew point, half-life, Ohm’s law, and moon phase. Physics, chemistry, and weather made simple.',
    intro: 'Physics, chemistry, and weather in one place. Calculate wind chill, heat index, and dew point with official formulas, work out half-life and Ohm’s law, and check the moon phase and sunrise or sunset.',
    faqs: [
      { question: 'Which formulas do the weather calculators use?', answer: 'The Wind Chill and Heat Index calculators use the official U.S. National Weather Service formulas, so results match what forecasters report.' },
      { question: 'What can I use Ohm’s law calculator for?', answer: 'It solves for voltage, current, resistance, or power when you know any two — handy for electronics, wiring, and physics homework.' },
    ],
  },
  {
    id: 'fun', slug: 'lifestyle', parentCat: 'other',
    title: 'Fun & Lifestyle Calculators',
    description: 'Free fun calculators — love compatibility, numerology, zodiac sign, dog age, and word count. Playful tools for everyday curiosity.',
    intro: 'Just-for-fun and everyday-curiosity tools. Check love compatibility, numerology, and your zodiac sign, convert your dog’s age to human years, and count words in any text.',
    faqs: [
      { question: 'Are the fun calculators serious?', answer: 'The love, numerology, and zodiac tools are for entertainment. Others, like the Word Count and Dog Age calculators, give genuinely useful results.' },
      { question: 'How does the dog age calculator work?', answer: 'It converts your dog’s age to human-equivalent years using a modern formula that accounts for breed size, rather than the old “multiply by seven” rule.' },
    ],
  },
]

export function getSiloHub(id: string): SiloHub | undefined {
  return siloHubs.find(s => s.id === id)
}

export function getSiloHubBySlug(slug: string): SiloHub | undefined {
  return siloHubs.find(s => s.slug === slug)
}

// Calculators in a silo, grouped by hub, in the hub order declared in `silos`.
export function getSiloCalculators(id: string): { hub: string; items: CalcEntry[] }[] {
  const meta = getSiloMeta(id)
  if (!meta) return []
  const inSilo = Object.entries(siloAssignments).filter(([, v]) => v.silo === id)
  return meta.hubs
    .map(hub => ({
      hub,
      items: inSilo
        .filter(([, v]) => v.hub === hub)
        .map(([s]) => _bySlug[s])
        .filter(Boolean),
    }))
    .filter(g => g.items.length > 0)
}

// A category page's own calculators, grouped into silo sections (silo order),
// each linking to its hub page. Used to give category pages topical structure
// and top-down links into the hubs.
export function getCategorySilos(
  catSlug: string
): { id: string; name: string; hubSlug: string; items: CalcEntry[] }[] {
  const cat = getCategoryBySlug(catSlug)
  if (!cat) return []
  return silos
    .map(s => {
      const hub = getSiloHub(s.id)
      const items = cat.calculators.filter(
        e => siloAssignments[e.href.replace('/calculators/', '')]?.silo === s.id
      )
      return { id: s.id, name: s.name, hubSlug: hub ? hub.slug : cat.slug, items }
    })
    .filter(g => g.items.length > 0)
}
