import type { Metadata } from "next";
import { getData } from "@/lib/data";
import GuideRoute, { getGuideMetadataFor } from "@/components/GuideRoute";

export const dynamicParams = false;

export function generateStaticParams() {
  return getData("fr").getAllParams();
}

export function generateMetadata({
  params,
}: {
  params: { slug: string[] };
}): Metadata {
  return getGuideMetadataFor("fr", params.slug);
}

export default function GuidePageFr({
  params,
}: {
  params: { slug: string[] };
}) {
  return <GuideRoute locale="fr" segments={params.slug} />;
}
