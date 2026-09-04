import type { Metadata } from "next";
import SendRequest from "@/components/SendRequest";

export const metadata: Metadata = {
  title: "Invia una richiesta",
  description:
    "Contatta il team Mersen del tuo paese per un prodotto o un progetto.",
};

export default function SendRequestPageIt() {
  return <SendRequest locale="it" />;
}
