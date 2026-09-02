import type { Metadata } from "next";
import SpdConfigurator from "@/components/SpdConfigurator";

export const metadata: Metadata = {
  title: "SPD Configurator",
  description:
    "Answer a few questions about your installation to find the right Surge Protection Device family.",
};

export default function SpdConfiguratorPage() {
  return <SpdConfigurator locale="en" />;
}
