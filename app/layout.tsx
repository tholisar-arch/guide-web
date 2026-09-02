import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Shell from "@/components/Shell";
import Sidebar from "@/components/Sidebar";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "Selection Guide 2026 Europe | Mersen Electrical Protection",
    template: "%s | Selection Guide 2026 Europe",
  },
  description:
    "Interactive selection guide for electrical protection products: low and medium voltage fuses, high-speed fuses, surge protection devices, and photovoltaic solutions.",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning className={inter.variable}>
      <body className="bg-white font-sans text-ink-800 antialiased dark:bg-ink-950 dark:text-ink-100">
        <Shell sidebar={<Sidebar />}>{children}</Shell>
      </body>
    </html>
  );
}
