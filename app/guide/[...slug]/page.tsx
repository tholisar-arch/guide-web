import { notFound } from "next/navigation";
import type { Metadata } from "next";
import Link from "next/link";
import {
  getAllParams,
  getPageBySlug,
  getPageByNumber,
  getListingChain,
  resolveListing,
  countLeaves,
  flattenLeaves,
} from "@/lib/data";
import type { ChapterAbout, ChapterMarkets, ChapterKnowledge } from "@/lib/types";
import LeafPageView from "@/components/LeafPageView";
import Breadcrumbs from "@/components/Breadcrumbs";
import GroupCards from "@/components/GroupCards";
import LeafFilterList from "@/components/LeafFilterList";
import ThumbCard from "@/components/ThumbCard";

export const dynamicParams = false;

export function generateStaticParams() {
  return getAllParams();
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
      { title: "Accueil", href: "/" },
      ...chainToCrumbs(chain, false),
      { title: entry.title },
    ];
    const parentHref = chain.length
      ? chain[chain.length - 1].href
      : "/";
    return (
      <LeafPageView entry={entry} crumbs={crumbs} parentHref={parentHref} />
    );
  }

  const listing = resolveListing(segments);
  if (!listing) notFound();

  const chain = getListingChain(segments);
  const crumbs = [
    { title: "Accueil", href: "/" },
    ...chainToCrumbs(chain, true),
  ];

  if (listing.kind === "chapter") {
    const chapter = listing.chapter;

    if (chapter.slug === "about") {
      const c = chapter as ChapterAbout;
      return (
        <div className="mx-auto max-w-6xl px-4 py-8">
          <Breadcrumbs items={crumbs} />
          <h1 className="mb-6 mt-3 text-2xl font-bold text-ink-900 dark:text-white">
            {c.title}
          </h1>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {c.items.map((it) => {
              const p = getPageByNumber(it.page);
              return (
                <ThumbCard
                  key={it.slug}
                  href={`/guide/${it.slug}`}
                  title={it.title}
                  image={p?.screenshot ?? ""}
                />
              );
            })}
          </div>
        </div>
      );
    }

    if (chapter.slug === "selector") {
      const c = chapter;
      return (
        <div className="mx-auto max-w-6xl px-4 py-8">
          <Breadcrumbs items={crumbs} />
          <h1 className="mb-2 mt-3 text-2xl font-bold text-ink-900 dark:text-white">
            {c.title}
          </h1>
          <p className="mb-6 max-w-2xl text-sm text-ink-500 dark:text-ink-400">
            Parcourez l&apos;ensemble des familles de produits de protection
            électrique : fusibles, parafoudres et solutions photovoltaïques.
          </p>
          {c.overview.length > 0 && (
            <div className="mb-6">
              {c.overview.map((it) => (
                <Link
                  key={it.slug}
                  href={`/guide/${it.slug}`}
                  className="text-sm font-medium text-brand-600 hover:underline dark:text-brand-400"
                >
                  {it.title} &rarr;
                </Link>
              ))}
            </div>
          )}
          <GroupCards
            items={c.categories.map((cat) => ({
              title: cat.title,
              href: `/guide/selector/${cat.slug}`,
              count: cat.count,
            }))}
          />
        </div>
      );
    }

    if (chapter.slug === "markets") {
      const c = chapter as ChapterMarkets;
      return (
        <div className="mx-auto max-w-6xl px-4 py-8">
          <Breadcrumbs items={crumbs} />
          <h1 className="mb-6 mt-3 text-2xl font-bold text-ink-900 dark:text-white">
            {c.title}
          </h1>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {c.items.map((it) => {
              const p = getPageByNumber(it.page);
              return (
                <ThumbCard
                  key={it.slug}
                  href={`/guide/${it.slug}`}
                  title={it.title}
                  image={p?.screenshot ?? ""}
                />
              );
            })}
          </div>
        </div>
      );
    }

    // knowledge
    const c = chapter as ChapterKnowledge;
    return (
      <div className="mx-auto max-w-4xl px-4 py-8">
        <Breadcrumbs items={crumbs} />
        <h1 className="mb-6 mt-3 text-2xl font-bold text-ink-900 dark:text-white">
          {c.title}
        </h1>
        <LeafFilterList items={c.items} />
      </div>
    );
  }

  // category or subgroup
  const title =
    listing.kind === "category"
      ? listing.category.title
      : listing.pathTitles[listing.pathTitles.length - 1];
  const total = countLeaves(listing.node);

  return (
    <div className="mx-auto max-w-6xl px-4 py-8">
      <Breadcrumbs items={crumbs} />
      <h1 className="mb-1 mt-3 text-2xl font-bold text-ink-900 dark:text-white">
        {title}
      </h1>
      <p className="mb-6 text-sm text-ink-500 dark:text-ink-400">
        {total} référence{total > 1 ? "s" : ""} de produits
      </p>
      {listing.node.type === "group" ? (
        <GroupCards
          items={listing.node.children.map((child) => ({
            title: child.title,
            href: `/guide/${segments.join("/")}/${child.slug}`,
            count: child.count,
          }))}
        />
      ) : (
        <LeafFilterList items={flattenLeaves(listing.node)} />
      )}
    </div>
  );
}
