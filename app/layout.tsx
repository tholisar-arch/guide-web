import type { Metadata } from "next";
import "./globals.css";
import Shell from "@/components/Shell";
import Sidebar from "@/components/Sidebar";

export const metadata: Metadata = {
  title: {
    default: "Selection Guide 2026 Europe | Mersen Electrical Protection",
    template: "%s | Selection Guide 2026 Europe",
  },
  description:
    "Guide interactif de sélection des produits de protection électrique : fusibles basse et moyenne tension, fusibles ultra-rapides, parafoudres et solutions photovoltaïques.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr" suppressHydrationWarning>
      <body className="bg-white text-ink-800 dark:bg-ink-950 dark:text-ink-100">
        <Shell sidebar={<Sidebar />}>{children}</Shell>
      </body>
    </html>
  );
}
