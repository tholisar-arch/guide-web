import type { Metadata } from "next";
import XrefSearch from "@/components/XrefSearch";

export const metadata: Metadata = {
  title: "Recherche par référence concurrente",
  description:
    "Trouvez la référence Mersen équivalente à une référence concurrente, ou consultez les références croisées connues d'une référence Mersen.",
};

export default function XrefPageFr() {
  return <XrefSearch locale="fr" />;
}
