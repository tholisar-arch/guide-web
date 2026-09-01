import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          // Mersen orange, sampled from the official logo mark
          50: "#fff4ee",
          100: "#ffe4d6",
          200: "#ffc7ac",
          300: "#ffa378",
          400: "#ff7a45",
          500: "#ff5112",
          600: "#e8430a",
          700: "#c23608",
          800: "#9c2e0e",
          900: "#7e2a10",
          950: "#451205",
        },
        ink: {
          // neutral slate tuned toward Mersen's dark petrol/teal chrome
          50: "#f5f7f8",
          100: "#eaeef0",
          200: "#d3dade",
          300: "#adb9c0",
          400: "#82919c",
          500: "#62717d",
          600: "#4d5b66",
          700: "#404b54",
          800: "#363f47",
          900: "#23292e",
          950: "#15191c",
        },
      },
      fontFamily: {
        sans: [
          "Segoe UI",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "Roboto",
          "Helvetica Neue",
          "Arial",
          "sans-serif",
        ],
      },
      boxShadow: {
        card: "0 1px 2px rgba(16,24,40,0.06), 0 1px 3px rgba(16,24,40,0.08)",
      },
    },
  },
  plugins: [],
};

export default config;
