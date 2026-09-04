import type { Metadata } from "next";
import XrefSearch from "@/components/XrefSearch";

export const metadata: Metadata = {
  title: "Kreuzreferenzsuche",
  description:
    "Finden Sie die entsprechende Mersen-Referenz zu einer Wettbewerber-Artikelnummer, oder sehen Sie die bekannten Kreuzreferenzen einer Mersen-Referenz.",
};

export default function XrefPageDe() {
  return <XrefSearch locale="de" />;
}
