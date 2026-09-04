import type { Metadata } from "next";
import HomeContent from "@/components/HomeContent";
import { t } from "@/lib/i18n";

export const metadata: Metadata = {
  title: t("de").metaSiteTitle,
  description: t("de").metaSiteDescription,
};

export default function HomePageDe() {
  return <HomeContent locale="de" />;
}
