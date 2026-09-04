import type { Metadata } from "next";
import XrefSearch from "@/components/XrefSearch";

export const metadata: Metadata = {
  title: "Kereszthivatkozás-kereső",
  description:
    "Keresse meg a megfelelő Mersen referenciát egy versenytárs cikkszámához, vagy tekintse meg egy Mersen referencia ismert kereszthivatkozásait.",
};

export default function XrefPageHu() {
  return <XrefSearch locale="hu" />;
}
