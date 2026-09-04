import type { Metadata } from "next";
import { getData } from "@/lib/data";
import GuideRoute, { getGuideMetadataFor } from "@/components/GuideRoute";

export const dynamicParams = false;

export function generateStaticParams() {
  return getData("cs").getAllParams();
}

export function generateMetadata({
  params,
}: {
  params: { slug: string[] };
}): Metadata {
  return getGuideMetadataFor("cs", params.slug);
}

export default function GuidePageCs({
  params,
}: {
  params: { slug: string[] };
}) {
  return <GuideRoute locale="cs" segments={params.slug} />;
}
