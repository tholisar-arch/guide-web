import type { Metadata } from "next";
import { getData } from "@/lib/data";
import GuideRoute, { getGuideMetadataFor } from "@/components/GuideRoute";

export const dynamicParams = false;

export function generateStaticParams() {
  return getData("es").getAllParams();
}

export function generateMetadata({
  params,
}: {
  params: { slug: string[] };
}): Metadata {
  return getGuideMetadataFor("es", params.slug);
}

export default function GuidePageEs({
  params,
}: {
  params: { slug: string[] };
}) {
  return <GuideRoute locale="es" segments={params.slug} />;
}
