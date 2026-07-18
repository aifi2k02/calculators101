// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://supercalculator.xyz',
  // Cloudflare Pages serves directory output at trailing-slash URLs and 308-redirects
  // non-slash → slash. Match that so canonicals/links point at the real served URL.
  trailingSlash: 'always',
  vite: {
    plugins: [tailwindcss()]
  }
});