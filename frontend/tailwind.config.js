/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        space: "#0B0F1A",
        neon: "#9C27B0",
        electric: "#00E5FF",
        platinum: "#E0E0E0",
        graphite: "#1F2633",
      },
      fontFamily: {
        sans: ['Arial', 'ui-sans-serif', 'system-ui'],
        mono: ['Courier New', 'ui-monospace', 'monospace'],
      },
    },
  },
  plugins: [],
}
