import type { Metadata } from "next";
import HomeContent from "@/components/HomeContent";
import { t } from "@/lib/i18n";

export const metadata: Metadata = {
  title: t("pt").metaSiteTitle,
  description: t("pt").metaSiteDescription,
};

export default function HomePagePt() {
  return <HomeContent locale="pt" />;
}
