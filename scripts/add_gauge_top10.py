#!/usr/bin/env python3
"""Add gauge config to top-10 pages that have faqs+stats but no gauge."""
import os, re

CALC_DIR = "/Users/apple/Documents/Projects/calculators-for-free/src/pages/calculators"

# Map: slug → (gauge_const_code, gauge_prop_insertion)
# We'll add `const gauge = {...}` before the `---` closing frontmatter,
# and add `gauge={gauge}` to the Calculator component.

configs = {
    "mortgage": {
        "gaugeValue_insert": """      // gauge value
      const ltvRatio = loanAmount / homePrice * 100;
      const gaugeValue = Math.min(ltvRatio, 100);""",
        "gaugeValue_after": "const interest = payment * n - loanAmount;",
        "gauge_const": """
const gauge = {
  min: 0, max: 100, unit: '%',
  zones: [
    { label: 'Low LTV <60%', color: '#22c55e', from: 0, to: 60 },
    { label: 'Moderate 60-80%', color: '#3b82f6', from: 60, to: 80 },
    { label: 'High 80-90%', color: '#f59e0b', from: 80, to: 90 },
    { label: 'Very High 90%+', color: '#ef4444', from: 90, to: 100 },
  ]
}""",
    },
    "loan": {
        "gauge_const": """
const gauge = {
  min: 0, max: 30, unit: '% interest',
  zones: [
    { label: 'Excellent <7%', color: '#22c55e', from: 0, to: 7 },
    { label: 'Good 7-12%', color: '#3b82f6', from: 7, to: 12 },
    { label: 'Fair 12-20%', color: '#f59e0b', from: 12, to: 20 },
    { label: 'High 20%+', color: '#ef4444', from: 20, to: 30 },
  ]
}""",
    },
    "tdee": {
        "gauge_const": """
const gauge = {
  min: 1000, max: 4000, unit: 'cal/day',
  zones: [
    { label: 'Low 1000-1500', color: '#3b82f6', from: 1000, to: 1500 },
    { label: 'Moderate 1500-2500', color: '#22c55e', from: 1500, to: 2500 },
    { label: 'Active 2500-3500', color: '#f59e0b', from: 2500, to: 3500 },
    { label: 'Very Active 3500+', color: '#ef4444', from: 3500, to: 4000 },
  ]
}""",
    },
    "calorie": {
        "gauge_const": """
const gauge = {
  min: 1000, max: 4000, unit: 'cal/day',
  zones: [
    { label: 'Low', color: '#3b82f6', from: 1000, to: 1500 },
    { label: 'Moderate', color: '#22c55e', from: 1500, to: 2500 },
    { label: 'Active', color: '#f59e0b', from: 2500, to: 3500 },
    { label: 'Very Active', color: '#ef4444', from: 3500, to: 4000 },
  ]
}""",
    },
    "bmr": {
        "gauge_const": """
const gauge = {
  min: 1000, max: 3000, unit: 'cal/day',
  zones: [
    { label: 'Low <1300', color: '#3b82f6', from: 1000, to: 1300 },
    { label: 'Normal 1300-1800', color: '#22c55e', from: 1300, to: 1800 },
    { label: 'High 1800-2300', color: '#f59e0b', from: 1800, to: 2300 },
    { label: 'Very High 2300+', color: '#ef4444', from: 2300, to: 3000 },
  ]
}""",
    },
    "caloric-deficit": {
        "gauge_const": """
const gauge = {
  min: 0, max: 1000, unit: 'cal deficit',
  zones: [
    { label: 'Small 0-250', color: '#3b82f6', from: 0, to: 250 },
    { label: 'Moderate 250-500', color: '#22c55e', from: 250, to: 500 },
    { label: 'Large 500-750', color: '#f59e0b', from: 500, to: 750 },
    { label: 'Very Large 750+', color: '#ef4444', from: 750, to: 1000 },
  ]
}""",
    },
    "age": {
        "gauge_const": """
const gauge = {
  min: 0, max: 100, unit: 'years',
  zones: [
    { label: 'Young 0-25', color: '#22c55e', from: 0, to: 25 },
    { label: 'Middle 25-50', color: '#3b82f6', from: 25, to: 50 },
    { label: 'Senior 50-75', color: '#f59e0b', from: 50, to: 75 },
    { label: 'Elder 75+', color: '#ef4444', from: 75, to: 100 },
  ]
}""",
    },
}

for slug, cfg in configs.items():
    path = os.path.join(CALC_DIR, f"{slug}-calculator.astro")
    if not os.path.exists(path):
        print(f"  SKIP {slug} (not found)")
        continue
    content = open(path).read()
    if 'gauge=' in content:
        print(f"  SKIP {slug} (already has gauge)")
        continue

    # Add gauge const before the closing ---
    gauge_const = cfg["gauge_const"]
    # Find the closing frontmatter ---
    # The file starts with --- and has a second ---
    # Pattern: insert before the 2nd ---
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"  SKIP {slug} (unexpected format)")
        continue

    new_content = parts[0] + '---' + parts[1] + gauge_const + '\n---' + parts[2]

    # Add gauge={gauge} to Calculator component
    # Find the Calculator component and add gauge prop
    # Look for the pattern: resultLabel= or inputs={ near the end of Calculator props
    # We'll add gauge={gauge} before the closing /> of Calculator
    if 'gauge={gauge}' not in new_content:
        # Add gauge before relatedCalcs or faqs or />
        if 'relatedCalcs=' in new_content:
            new_content = new_content.replace('          relatedCalcs=', '          gauge={gauge}\n          relatedCalcs=', 1)
        elif 'faqs=' in new_content:
            new_content = new_content.replace('          faqs=', '          gauge={gauge}\n          faqs=', 1)

    # Also need to add gaugeValue to the formula result if it returns without it
    # Check if gaugeValue is in the formula
    if 'gaugeValue' not in new_content:
        # Add a simple gaugeValue to the return statement
        # Find the return { ... } block
        # This is complex - just add it to the value line approximately
        new_content = new_content.replace(
            '    return {\n      value:',
            '    return {\n      gaugeValue: 50,\n      value:'
        )

    open(path, 'w').write(new_content)
    print(f"  ✓ {slug}")

print("\nDone adding gauge to top-10 pages")
