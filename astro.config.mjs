// @ts-check
import tailwindcss from "@tailwindcss/vite";
import { defineConfig, fontProviders } from "astro/config";

// Vercel sets this on every deployment, including previews.
const productionHost = process.env.VERCEL_PROJECT_PRODUCTION_URL;

export default defineConfig({
  site: productionHost ? `https://${productionHost}` : "http://localhost:4321",
  // One page, so inlining the CSS removes a render-blocking request at no caching cost.
  build: { inlineStylesheets: "always" },
  fonts: [
    {
      provider: fontProviders.fontsource(),
      name: "Funnel Display",
      cssVariable: "--font-funnel-display",
      weights: [400],
      styles: ["normal"],
      subsets: ["latin"],
    },
    {
      provider: fontProviders.fontsource(),
      name: "Funnel Sans",
      cssVariable: "--font-funnel-sans",
      weights: [400, 500],
      styles: ["normal"],
      subsets: ["latin"],
    },
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});
