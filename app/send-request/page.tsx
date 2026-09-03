import type { Metadata } from "next";
import SendRequest from "@/components/SendRequest";

export const metadata: Metadata = {
  title: "Send a Request",
  description:
    "Compose an email right from the site: recipient, subject, and message.",
};

export default function SendRequestPage() {
  return <SendRequest locale="en" />;
}
