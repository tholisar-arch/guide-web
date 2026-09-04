import type { Metadata } from "next";
import SpdConfigurator from "@/components/SpdConfigurator";

export const metadata: Metadata = {
  title: "SPD-configurator",
  description:
    "Beantwoord enkele vragen over uw installatie om de juiste overspanningsbeveiligingsfamilie te vinden.",
};

export default function SpdConfiguratorPageNl() {
  return <SpdConfigurator locale="nl" />;
}
