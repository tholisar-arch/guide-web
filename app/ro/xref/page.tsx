import type { Metadata } from "next";
import XrefSearch from "@/components/XrefSearch";

export const metadata: Metadata = {
  title: "Căutare referințe încrucișate",
  description:
    "Găsiți referința Mersen echivalentă unui cod al concurenței sau consultați referințele încrucișate cunoscute ale unei referințe Mersen.",
};

export default function XrefPageRo() {
  return <XrefSearch locale="ro" />;
}
