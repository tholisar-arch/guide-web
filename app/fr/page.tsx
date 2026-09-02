import type { Metadata } from "next";
import HomeContent from "@/components/HomeContent";
import { t } from "@/lib/i18n";

export const metadata: Metadata = {
  title: t("fr").metaSiteTitle,
  description: t("fr").metaSiteDescription,
};

export default function HomePageFr() {
  return <HomeContent locale="fr" />;
}
