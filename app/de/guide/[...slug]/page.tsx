import type { Metadata } from "next";
import { getData } from "@/lib/data";
import GuideRoute, { getGuideMetadataFor } from "@/components/GuideRoute";

export const dynamicParams = false;

export function generateStaticParams() {
  return getData("de").getAllParams();
}

export function generateMetadata({
  params,
}: {
  params: { slug: string[] };
}): Metadata {
  return getGuideMetadataFor("de", params.slug);
}

export default function GuidePageDe({
  params,
}: {
  params: { slug: string[] };
}) {
  return <GuideRoute locale="de" segments={params.slug} />;
}
