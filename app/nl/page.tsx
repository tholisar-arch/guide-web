import type { Metadata } from "next";
import HomeContent from "@/components/HomeContent";
import { t } from "@/lib/i18n";

export const metadata: Metadata = {
  title: t("nl").metaSiteTitle,
  description: t("nl").metaSiteDescription,
};

export default function HomePageNl() {
  return <HomeContent locale="nl" />;
}
