import type { Metadata } from "next";
import SpdConfigurator from "@/components/SpdConfigurator";

export const metadata: Metadata = {
  title: "SPD-konfigurátor",
  description:
    "Válaszoljon néhány kérdésre az Ön rendszeréről, hogy megtalálja a megfelelő túlfeszültségvédelmi termékcsaládot.",
};

export default function SpdConfiguratorPageHu() {
  return <SpdConfigurator locale="hu" />;
}
