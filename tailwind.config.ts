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
          50: "#eef6ff",
          100: "#d9ecff",
          200: "#bcdcff",
          300: "#8ec5ff",
          400: "#59a6ff",
          500: "#3184ff",
          600: "#1b63f2",
          700: "#154ddc",
          800: "#173fb0",
          900: "#18398a",
          950: "#132458",
        },
        ink: {
          50: "#f6f7f9",
          100: "#eceef2",
          200: "#d5d9e2",
          300: "#b0b8c8",
          400: "#8590a8",
          500: "#66728c",
          600: "#515b73",
          700: "#434b5e",
          800: "#3a4050",
          900: "#242832",
          950: "#161920",
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
