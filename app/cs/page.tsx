import type { Metadata } from "next";
import HomeContent from "@/components/HomeContent";
import { t } from "@/lib/i18n";

export const metadata: Metadata = {
  title: t("cs").metaSiteTitle,
  description: t("cs").metaSiteDescription,
};

export default function HomePageCs() {
  return <HomeContent locale="cs" />;
}
