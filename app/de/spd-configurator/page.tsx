import type { Metadata } from "next";
import SpdConfigurator from "@/components/SpdConfigurator";

export const metadata: Metadata = {
  title: "SPD-Konfigurator",
  description:
    "Beantworten Sie einige Fragen zu Ihrer Anlage, um die passende Überspannungsschutz-Produktfamilie zu finden.",
};

export default function SpdConfiguratorPageDe() {
  return <SpdConfigurator locale="de" />;
}
