import type { Metadata } from "next";
import SpdConfigurator from "@/components/SpdConfigurator";

export const metadata: Metadata = {
  title: "Configurator SPD",
  description:
    "Răspundeți la câteva întrebări despre instalația dumneavoastră pentru a găsi familia potrivită de protecție la supratensiuni.",
};

export default function SpdConfiguratorPageRo() {
  return <SpdConfigurator locale="ro" />;
}
