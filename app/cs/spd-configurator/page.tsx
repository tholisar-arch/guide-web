import type { Metadata } from "next";
import SpdConfigurator from "@/components/SpdConfigurator";

export const metadata: Metadata = {
  title: "Konfigurátor SPD",
  description:
    "Odpovězte na několik otázek o vaší instalaci a najděte správnou řadu přepěťových ochran.",
};

export default function SpdConfiguratorPageCs() {
  return <SpdConfigurator locale="cs" />;
}
