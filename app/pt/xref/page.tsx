import type { Metadata } from "next";
import XrefSearch from "@/components/XrefSearch";

export const metadata: Metadata = {
  title: "Pesquisa por referência concorrente",
  description:
    "Encontre a referência Mersen equivalente a uma referência da concorrência, ou consulte as referências cruzadas conhecidas de uma referência Mersen.",
};

export default function XrefPagePt() {
  return <XrefSearch locale="pt" />;
}
