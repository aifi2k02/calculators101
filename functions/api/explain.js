// POST /api/explain — free AI reasoning via Cloudflare Workers AI.
// Guardrails: (1) cache by input hash, (2) soft per-IP rate limit, (3) deterministic fallback.

const MODEL = '@cf/meta/llama-3.1-8b-instruct-fp8'
const RATE_LIMIT = 30          // requests per IP per window
const RATE_WINDOW = 3600       // seconds (1 hour)
const CACHE_TTL = 86400        // cache identical explanations for 24h

async function sha256(str) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str))
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('')
}

function fallbackText(result, breakdown) {
  const steps = (breakdown || []).filter(l => l && l !== '—')
  if (steps.length) return 'Here is how this result was reached:\n\n• ' + steps.join('\n• ')
  return 'Result: ' + (result || 'see above')
}

// Soft fixed-window rate limiter backed by the Cache API (no KV binding required).
async function rateLimited(ip) {
  try {
    const cache = caches.default
    const bucket = Math.floor(Date.now() / 1000 / RATE_WINDOW)
    const key = new Request(`https://rl.internal/${ip}/${bucket}`)
    const hit = await cache.match(key)
    const count = hit ? parseInt(await hit.text(), 10) || 0 : 0
    if (count >= RATE_LIMIT) return true
    await cache.put(key, new Response(String(count + 1), {
      headers: { 'Cache-Control': `max-age=${RATE_WINDOW}` },
    }))
    return false
  } catch {
    return false // never let the limiter break the endpoint
  }
}

export async function onRequestPost({ request, env }) {
  const json = (obj, status = 200) =>
    new Response(JSON.stringify(obj), { status, headers: { 'Content-Type': 'application/json' } })

  let body
  try {
    body = await request.json()
  } catch {
    return json({ explanation: null, error: 'invalid_json' }, 400)
  }

  const title = String(body.title || 'Calculator').slice(0, 120)
  const result = String(body.result || '').slice(0, 200)
  const inputs = body.inputs && typeof body.inputs === 'object' ? body.inputs : {}
  const breakdown = Array.isArray(body.breakdown) ? body.breakdown.slice(0, 20).map(s => String(s).slice(0, 200)) : []
  const source = fallbackText(result, breakdown)

  // If the AI binding is missing, degrade gracefully to the deterministic steps.
  if (!env.AI) return json({ explanation: source, source: 'fallback' })

  const inputStr = Object.entries(inputs).map(([k, v]) => `${k}: ${v}`).join(', ').slice(0, 500)
  const payloadKey = await sha256(JSON.stringify({ title, result, inputStr, breakdown }))
  const cache = caches.default
  const cacheKey = new Request(`https://ai-explain.internal/${payloadKey}`)

  // 1) Cache: identical calculation → cached explanation, zero neurons spent.
  try {
    const cached = await cache.match(cacheKey)
    if (cached) {
      const data = await cached.json()
      return json({ explanation: data.explanation, source: 'cache' })
    }
  } catch { /* ignore cache read errors */ }

  // 2) Rate limit per IP (soft).
  const ip = request.headers.get('CF-Connecting-IP') || 'anon'
  if (await rateLimited(ip)) {
    return json({ explanation: source, source: 'rate_limited' })
  }

  // 3) Ask the model, with the deterministic steps as grounding.
  const system = 'You explain the result of an online calculator to a general audience. ' +
    'Use ONLY the numbers and steps provided — never invent figures. ' +
    'Write 2 short paragraphs of plain English: what the result means, then what the person might do with it. ' +
    'Be warm and clear. No markdown headings, no bullet lists, under 130 words.'
  const user = `Calculator: ${title}\nInputs: ${inputStr}\nResult: ${result}\n` +
    `Calculation steps:\n${breakdown.join('\n')}`

  try {
    const ai = await env.AI.run(MODEL, {
      messages: [{ role: 'system', content: system }, { role: 'user', content: user }],
      max_tokens: 320,
      temperature: 0.3,
    })
    const explanation = (ai && (ai.response || ai.result))?.trim()
    if (!explanation) return json({ explanation: source, source: 'fallback' })

    // Store in cache for future identical requests.
    try {
      await cache.put(cacheKey, new Response(JSON.stringify({ explanation }), {
        headers: { 'Content-Type': 'application/json', 'Cache-Control': `max-age=${CACHE_TTL}` },
      }))
    } catch { /* ignore cache write errors */ }

    return json({ explanation, source: 'ai' })
  } catch (e) {
    // Quota exhausted or model error → deterministic fallback, never a broken button.
    return json({ explanation: source, source: 'fallback' })
  }
}
