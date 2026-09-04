import type { Metadata } from "next";
import SendRequest from "@/components/SendRequest";

export const metadata: Metadata = {
  title: "Aanvraag versturen",
  description:
    "Neem contact op met uw lokale Mersen-team over een product of project.",
};

export default function SendRequestPageNl() {
  return <SendRequest locale="nl" />;
}
