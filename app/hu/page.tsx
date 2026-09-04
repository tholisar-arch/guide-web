import type { Metadata } from "next";
import HomeContent from "@/components/HomeContent";
import { t } from "@/lib/i18n";

export const metadata: Metadata = {
  title: t("hu").metaSiteTitle,
  description: t("hu").metaSiteDescription,
};

export default function HomePageHu() {
  return <HomeContent locale="hu" />;
}
