import type { APIRoute } from 'astro'
import siteConfig from '../lib/siteConfig'

export const GET: APIRoute = () => {
  const { allowIndexing, siteUrl } = siteConfig

  const content = allowIndexing
    ? `User-agent: *\nAllow: /\n\nSitemap: ${siteUrl}/sitemap.xml\n`
    : `User-agent: *\nDisallow: /\n`

  return new Response(content, {
    headers: { 'Content-Type': 'text/plain' },
  })
}
