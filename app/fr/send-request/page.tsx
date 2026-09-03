import type { Metadata } from "next";
import SendRequest from "@/components/SendRequest";

export const metadata: Metadata = {
  title: "Envoyer une demande",
  description:
    "Rédigez un e-mail directement depuis le site : destinataire, objet et message.",
};

export default function SendRequestPageFr() {
  return <SendRequest locale="fr" />;
}
