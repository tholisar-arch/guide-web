import type { Metadata } from "next";
import XrefSearch from "@/components/XrefSearch";

export const metadata: Metadata = {
  title: "Ricerca per riferimento concorrente",
  description:
    "Trova il riferimento Mersen equivalente a un codice concorrente, oppure consulta i riferimenti incrociati noti di un codice Mersen.",
};

export default function XrefPageIt() {
  return <XrefSearch locale="it" />;
}
