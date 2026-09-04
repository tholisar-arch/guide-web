import type { Metadata } from "next";
import { getData } from "@/lib/data";
import GuideRoute, { getGuideMetadataFor } from "@/components/GuideRoute";

export const dynamicParams = false;

export function generateStaticParams() {
  return getData("hu").getAllParams();
}

export function generateMetadata({
  params,
}: {
  params: { slug: string[] };
}): Metadata {
  return getGuideMetadataFor("hu", params.slug);
}

export default function GuidePageHu({
  params,
}: {
  params: { slug: string[] };
}) {
  return <GuideRoute locale="hu" segments={params.slug} />;
}
