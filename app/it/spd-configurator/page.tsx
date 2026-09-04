import type { Metadata } from "next";
import SpdConfigurator from "@/components/SpdConfigurator";

export const metadata: Metadata = {
  title: "Configuratore SPD",
  description:
    "Rispondi ad alcune domande sul tuo impianto per trovare la famiglia di scaricatori di sovratensione più adatta.",
};

export default function SpdConfiguratorPageIt() {
  return <SpdConfigurator locale="it" />;
}
