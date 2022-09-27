/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ["'Inter', sans-serif"],
      },
      colors: {
        primary: '#00c0d7',
        background: '#242528',
      },
    },
  },
  plugins: [],
};
