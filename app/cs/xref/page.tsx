import type { Metadata } from "next";
import XrefSearch from "@/components/XrefSearch";

export const metadata: Metadata = {
  title: "Vyhledávání křížových referencí",
  description:
    "Najděte odpovídající referenci Mersen ke katalogovému číslu konkurence, nebo si prohlédněte známé křížové reference k referenci Mersen.",
};

export default function XrefPageCs() {
  return <XrefSearch locale="cs" />;
}
