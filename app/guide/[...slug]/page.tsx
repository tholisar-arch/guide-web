import { notFound } from "next/navigation";
import type { Metadata } from "next";
import {
  getAllParams,
  getPageBySlug,
  getListingChain,
  resolveListing,
  flattenLeaves,
} from "@/lib/data";
import type { ChapterSelector } from "@/lib/types";
import LeafPageView from "@/components/LeafPageView";
import Breadcrumbs from "@/components/Breadcrumbs";
import GroupCards from "@/components/GroupCards";
import LeafFilterList from "@/components/LeafFilterList";
import SelectorFrame from "@/components/SelectorFrame";

export const dynamicParams = false;

export function generateStaticParams() {
  return getAllParams();
}

function stripKnownPrefix(title: string, prefix: string): string {
  if (!prefix || title === prefix) return title;
  const withDash = prefix + " - ";
  return title.startsWith(withDash) ? title.slice(withDash.length) : title;
}

function chainToCrumbs(chain: { title: string; href: string }[], dropLastHref = true) {
  return chain.map((c, i) => ({
    title: c.title,
    href: dropLastHref && i === chain.length - 1 ? undefined : c.href,
  }));
}

export function generateMetadata({
  params,
}: {
  params: { slug: string[] };
}): Metadata {
  const full = params.slug.join("/");
  const entry = getPageBySlug(full);
  if (entry) {
    return {
      title: entry.title,
      description: entry.text.slice(0, 160) || entry.title,
    };
  }
  const listing = resolveListing(params.slug);
  if (listing) {
    const title =
      listing.kind === "chapter"
        ? listing.chapter.title
        : listing.kind === "category"
        ? listing.category.title
        : listing.pathTitles[listing.pathTitles.length - 1];
    return { title };
  }
  return {};
}

export default function GuidePage({
  params,
}: {
  params: { slug: string[] };
}) {
  const segments = params.slug;
  const full = segments.join("/");

  const entry = getPageBySlug(full);
  if (entry) {
    const parentSegments = segments.slice(0, -1);
    const chain = getListingChain(parentSegments);
    const crumbs = [
      { title: "Home", href: "/" },
      ...chainToCrumbs(chain, false),
      { title: entry.title },
    ];
    const parentHref = chain.length ? chain[chain.length - 1].href : "/";
    return (
      <LeafPageView entry={entry} crumbs={crumbs} parentHref={parentHref} />
    );
  }

  const listing = resolveListing(segments);
  if (!listing) notFound();

  const chain = getListingChain(segments);
  const crumbs = [{ title: "Home", href: "/" }, ...chainToCrumbs(chain, true)];
  const backHref =
    segments.length > 1 ? "/guide/" + segments.slice(0, -1).join("/") : undefined;

  if (listing.kind === "chapter") {
    const c = listing.chapter as ChapterSelector;
    return (
      <SelectorFrame backHref={backHref}>
        <Breadcrumbs items={crumbs} />
        <h1 className="mb-2 mt-3 text-2xl font-bold text-ink-900 dark:text-white">
          {c.title}
        </h1>
        <p className="mb-6 max-w-2xl text-sm text-ink-500 dark:text-ink-400">
          Browse the full range of electrical protection product families:
          fuses, surge protection devices, and photovoltaic solutions.
        </p>
        <GroupCards
          items={c.categories.map((cat) => ({
            title: cat.title,
            href: `/guide/selector/${cat.slug}`,
          }))}
        />
      </SelectorFrame>
    );
  }

  // category or subgroup
  const title =
    listing.kind === "category"
      ? listing.category.title
      : listing.pathTitles[listing.pathTitles.length - 1];

  return (
    <SelectorFrame backHref={backHref}>
      <Breadcrumbs items={crumbs} />
      <h1 className="mb-6 mt-3 text-2xl font-bold text-ink-900 dark:text-white">
        {title}
      </h1>
      {listing.node.type === "group" ? (
        <GroupCards
          items={listing.node.children.map((child) => ({
            title: child.title,
            href: `/guide/${segments.join("/")}/${child.slug}`,
          }))}
        />
      ) : (
        <LeafFilterList
          items={flattenLeaves(listing.node).map((it) => ({
            ...it,
            title: stripKnownPrefix(it.title, listing.pathTitles.join(" - ")),
          }))}
        />
      )}
    </SelectorFrame>
  );
}
