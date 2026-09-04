import type { Metadata } from "next";
import SendRequest from "@/components/SendRequest";

export const metadata: Metadata = {
  title: "Kérés küldése",
  description:
    "Vegye fel a kapcsolatot a helyi Mersen csapattal egy termékkel vagy projekttel kapcsolatban.",
};

export default function SendRequestPageHu() {
  return <SendRequest locale="hu" />;
}
