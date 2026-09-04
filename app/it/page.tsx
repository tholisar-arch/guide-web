import type { Metadata } from "next";
import HomeContent from "@/components/HomeContent";
import { t } from "@/lib/i18n";

export const metadata: Metadata = {
  title: t("it").metaSiteTitle,
  description: t("it").metaSiteDescription,
};

export default function HomePageIt() {
  return <HomeContent locale="it" />;
}
