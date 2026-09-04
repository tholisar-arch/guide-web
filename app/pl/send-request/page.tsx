import type { Metadata } from "next";
import SendRequest from "@/components/SendRequest";

export const metadata: Metadata = {
  title: "Wyślij zapytanie",
  description:
    "Skontaktuj się z lokalnym zespołem Mersen w sprawie produktu lub projektu.",
};

export default function SendRequestPagePl() {
  return <SendRequest locale="pl" />;
}
