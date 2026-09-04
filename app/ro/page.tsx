import type { Metadata } from "next";
import HomeContent from "@/components/HomeContent";
import { t } from "@/lib/i18n";

export const metadata: Metadata = {
  title: t("ro").metaSiteTitle,
  description: t("ro").metaSiteDescription,
};

export default function HomePageRo() {
  return <HomeContent locale="ro" />;
}
