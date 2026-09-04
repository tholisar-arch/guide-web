import type { Metadata } from "next";
import { getData } from "@/lib/data";
import GuideRoute, { getGuideMetadataFor } from "@/components/GuideRoute";

export const dynamicParams = false;

export function generateStaticParams() {
  return getData("pl").getAllParams();
}

export function generateMetadata({
  params,
}: {
  params: { slug: string[] };
}): Metadata {
  return getGuideMetadataFor("pl", params.slug);
}

export default function GuidePagePl({
  params,
}: {
  params: { slug: string[] };
}) {
  return <GuideRoute locale="pl" segments={params.slug} />;
}
