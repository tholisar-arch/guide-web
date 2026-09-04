import type { Metadata } from "next";
import XrefSearch from "@/components/XrefSearch";

export const metadata: Metadata = {
  title: "Wyszukiwarka zamienników",
  description:
    "Znajdź odpowiednik Mersen dla numeru katalogowego konkurencji lub sprawdź znane zamienniki dla referencji Mersen.",
};

export default function XrefPagePl() {
  return <XrefSearch locale="pl" />;
}
