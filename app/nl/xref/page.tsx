import type { Metadata } from "next";
import XrefSearch from "@/components/XrefSearch";

export const metadata: Metadata = {
  title: "Kruisreferentie zoeken",
  description:
    "Vind de bijbehorende Mersen-referentie voor een concurrerend artikelnummer, of bekijk de bekende kruisreferenties van een Mersen-referentie.",
};

export default function XrefPageNl() {
  return <XrefSearch locale="nl" />;
}
