import type { Metadata } from "next";
import SpdConfigurator from "@/components/SpdConfigurator";

export const metadata: Metadata = {
  title: "Konfigurator SPD",
  description:
    "Odpowiedz na kilka pytań dotyczących instalacji, aby znaleźć odpowiednią rodzinę ochrony przeciwprzepięciowej.",
};

export default function SpdConfiguratorPagePl() {
  return <SpdConfigurator locale="pl" />;
}
