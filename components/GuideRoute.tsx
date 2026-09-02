import { notFound } from "next/navigation";
import { getData } from "@/lib/data";
import type { ChapterSelector } from "@/lib/types";
import LeafPageView from "@/components/LeafPageView";
import Breadcrumbs from "@/components/Breadcrumbs";
import GroupCards from "@/components/GroupCards";
import LeafFilterList from "@/components/LeafFilterList";
import SelectorFrame from "@/components/SelectorFrame";
import { localeHref, t, type Locale } from "@/lib/i18n";

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

export function getGuideMetadataFor(locale: Locale, segments: string[]) {
  const data = getData(locale);
  const full = segments.join("/");
  const entry = data.getPageBySlug(full);
  if (entry) {
    return {
      title: entry.title,
      description: entry.text.slice(0, 160) || entry.title,
    };
  }
  const listing = data.resolveListing(segments);
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

export default function GuideRoute({
  locale,
  segments,
}: {
  locale: Locale;
  segments: string[];
}) {
  const data = getData(locale);
  const dict = t(locale);
  const full = segments.join("/");

  const entry = data.getPageBySlug(full);
  if (entry) {
    const parentSegments = segments.slice(0, -1);
    const chain = data.getListingChain(parentSegments);
    const crumbs = [
      { title: dict.home, href: localeHref(locale, "/") },
      ...chainToCrumbs(chain, false).map((c) => ({
        ...c,
        href: c.href ? localeHref(locale, c.href) : undefined,
      })),
      { title: entry.title },
    ];
    const parentHref = chain.length
      ? localeHref(locale, chain[chain.length - 1].href)
      : localeHref(locale, "/");
    return (
      <LeafPageView
        entry={entry}
        crumbs={crumbs}
        parentHref={parentHref}
        locale={locale}
      />
    );
  }

  const listing = data.resolveListing(segments);
  if (!listing) notFound();

  const chain = data.getListingChain(segments);
  const crumbs = [
    { title: dict.home, href: localeHref(locale, "/") },
    ...chainToCrumbs(chain, true).map((c) => ({
      ...c,
      href: c.href ? localeHref(locale, c.href) : undefined,
    })),
  ];
  const backHref =
    segments.length > 1
      ? localeHref(locale, "/guide/" + segments.slice(0, -1).join("/"))
      : undefined;

  if (listing.kind === "chapter") {
    const c = listing.chapter as ChapterSelector;
    return (
      <SelectorFrame backHref={backHref} locale={locale}>
        <Breadcrumbs items={crumbs} />
        <h1 className="mb-2 mt-3 text-2xl font-bold text-ink-900 dark:text-white">
          {c.title}
        </h1>
        <p className="mb-6 max-w-2xl text-sm text-ink-500 dark:text-ink-400">
          {dict.productFamiliesDesc}
        </p>
        <GroupCards
          items={c.categories.map((cat) => ({
            title: cat.title,
            href: localeHref(locale, `/guide/selector/${cat.slug}`),
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
    <SelectorFrame backHref={backHref} locale={locale}>
      <Breadcrumbs items={crumbs} />
      <h1 className="mb-6 mt-3 text-2xl font-bold text-ink-900 dark:text-white">
        {title}
      </h1>
      {listing.node.type === "group" ? (
        <GroupCards
          items={listing.node.children.map((child) => ({
            title: child.title,
            href: localeHref(locale, `/guide/${segments.join("/")}/${child.slug}`),
          }))}
        />
      ) : (
        <LeafFilterList
          locale={locale}
          items={data.flattenLeaves(listing.node).map((it) => ({
            ...it,
            title: stripKnownPrefix(it.title, listing.pathTitles.join(" - ")),
          }))}
        />
      )}
    </SelectorFrame>
  );
}
