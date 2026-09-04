import type { Metadata } from "next";
import SendRequest from "@/components/SendRequest";

export const metadata: Metadata = {
  title: "Enviar una solicitud",
  description:
    "Póngase en contacto con su equipo local de Mersen sobre un producto o proyecto.",
};

export default function SendRequestPageEs() {
  return <SendRequest locale="es" />;
}
