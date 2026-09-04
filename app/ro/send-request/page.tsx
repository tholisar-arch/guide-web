import type { Metadata } from "next";
import SendRequest from "@/components/SendRequest";

export const metadata: Metadata = {
  title: "Trimiteți o solicitare",
  description:
    "Contactați echipa Mersen locală în legătură cu un produs sau un proiect.",
};

export default function SendRequestPageRo() {
  return <SendRequest locale="ro" />;
}
