import type { Metadata } from "next";
import XrefSearch from "@/components/XrefSearch";

export const metadata: Metadata = {
  title: "Cross Reference Search",
  description:
    "Find the equivalent Mersen reference for a competitor part number, or look up a Mersen reference's known cross references.",
};

export default function XrefPage() {
  return <XrefSearch locale="en" />;
}
