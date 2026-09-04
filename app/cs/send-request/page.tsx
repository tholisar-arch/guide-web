import type { Metadata } from "next";
import SendRequest from "@/components/SendRequest";

export const metadata: Metadata = {
  title: "Odeslat poptávku",
  description:
    "Kontaktujte místní tým Mersen ohledně produktu nebo projektu.",
};

export default function SendRequestPageCs() {
  return <SendRequest locale="cs" />;
}
