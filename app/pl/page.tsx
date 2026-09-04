import type { Metadata } from "next";
import HomeContent from "@/components/HomeContent";
import { t } from "@/lib/i18n";

export const metadata: Metadata = {
  title: t("pl").metaSiteTitle,
  description: t("pl").metaSiteDescription,
};

export default function HomePagePl() {
  return <HomeContent locale="pl" />;
}
