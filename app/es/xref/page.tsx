import type { Metadata } from "next";
import XrefSearch from "@/components/XrefSearch";

export const metadata: Metadata = {
  title: "Búsqueda por referencia de la competencia",
  description:
    "Encuentre la referencia Mersen equivalente a una referencia de la competencia, o consulte las referencias cruzadas conocidas de una referencia Mersen.",
};

export default function XrefPageEs() {
  return <XrefSearch locale="es" />;
}
