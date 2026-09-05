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
          // neutral slate tuned toward Mersen's dark petrol/teal chrome,
          // with the 50 and 950 ends nudged toward apple.com's near-white
          // page ground and true near-black text/surfaces.
          50: "#fafbfb",
          100: "#eaeef0",
          200: "#d3dade",
          300: "#adb9c0",
          400: "#82919c",
          500: "#62717d",
          600: "#4d5b66",
          700: "#404b54",
          800: "#363f47",
          900: "#23292e",
          950: "#0c0e10",
        },
      },
      fontFamily: {
        sans: [
          "var(--font-inter)",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "Arial",
          "sans-serif",
        ],
      },
      // A rounder, softer scale than Tailwind's defaults -- since every
      // component already uses rounded-md/lg/xl/2xl, bumping the scale
      // here reshapes the whole site's corners without touching each
      // className individually.
      borderRadius: {
        md: "0.625rem",
        lg: "0.875rem",
        xl: "1.25rem",
        "2xl": "1.5rem",
        "3xl": "2rem",
      },
      boxShadow: {
        // Soft, multi-stop "elevation" shadows -- diffuse enough to read
        // as depth (Apple-style) rather than the flat 1px hairline a
        // Swiss/enterprise-tool surface usually gets.
        card: "0 1px 2px rgba(15,23,42,0.04), 0 1px 1px rgba(15,23,42,0.03)",
        "card-hover":
          "0 8px 24px -8px rgba(15,23,42,0.16), 0 2px 8px -2px rgba(15,23,42,0.06)",
        elevated:
          "0 20px 48px -12px rgba(15,23,42,0.18), 0 4px 16px -4px rgba(15,23,42,0.08)",
        glow: "0 8px 30px -6px rgba(255,81,18,0.35)",
      },
      transitionDuration: {
        DEFAULT: "220ms",
      },
      transitionTimingFunction: {
        // A gentle "ease-out-expo" curve -- the deceleration feel behind
        // most macOS/iOS interface motion, used here as the sitewide
        // default so every bare `transition` picks it up.
        DEFAULT: "cubic-bezier(0.16, 1, 0.3, 1)",
      },
      backgroundImage: {
        "glow-orange":
          "radial-gradient(60% 60% at 50% 0%, rgba(255,81,18,0.16) 0%, rgba(255,81,18,0) 70%)",
      },
    },
  },
  plugins: [],
};

export default config;
