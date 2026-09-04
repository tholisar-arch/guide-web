import type { Metadata } from "next";
import SpdConfigurator from "@/components/SpdConfigurator";

export const metadata: Metadata = {
  title: "Configurador SPD",
  description:
    "Responda a algumas perguntas sobre a sua instalação para encontrar a família de proteção contra sobretensões adequada.",
};

export default function SpdConfiguratorPagePt() {
  return <SpdConfigurator locale="pt" />;
}
