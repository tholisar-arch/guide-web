import type { Metadata } from "next";
import SendRequest from "@/components/SendRequest";

export const metadata: Metadata = {
  title: "Enviar um pedido",
  description:
    "Entre em contacto com a sua equipa Mersen local sobre um produto ou projeto.",
};

export default function SendRequestPagePt() {
  return <SendRequest locale="pt" />;
}
