import type { Metadata } from "next";
import SpdConfigurator from "@/components/SpdConfigurator";

export const metadata: Metadata = {
  title: "Configurateur SPD",
  description:
    "Répondez à quelques questions sur votre installation pour trouver la bonne famille de parafoudres.",
};

export default function SpdConfiguratorPageFr() {
  return <SpdConfigurator locale="fr" />;
}
