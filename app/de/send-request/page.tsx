import type { Metadata } from "next";
import SendRequest from "@/components/SendRequest";

export const metadata: Metadata = {
  title: "Anfrage senden",
  description:
    "Nehmen Sie Kontakt mit Ihrem lokalen Mersen-Team zu einem Produkt oder Projekt auf.",
};

export default function SendRequestPageDe() {
  return <SendRequest locale="de" />;
}
