"use client";

import { usePathname } from "next/navigation";
import { getData } from "@/lib/data";
import type { ChapterSelector, SelectorNavNode } from "@/lib/types";
import CategoryRow from "@/components/CategoryRow";
import { Home, ArrowLeftRight, Sliders } from "lucide-react";
import Link from "next/link";
import { localeFromPathname, localeHref, t } from "@/lib/i18n";

function SelectorGroupRow({
  locale,
  catSlug,
  node,
  level,
}: {
  locale: "en" | "fr";
  catSlug: string;
  node: SelectorNavNode;
  level: number;
}) {
  if (node.type === "leaves") return null;
  return (
    <>
      {node.children.map((child) => (
        <CategoryRow
          key={child.slug}
          href={localeHref(locale, `/guide/selector/${catSlug}/${child.slug}`)}
          title={child.title}
          level={level}
        />
      ))}
    </>
  );
}

export default function Sidebar() {
  const pathname = usePathname();
  const locale = localeFromPathname(pathname ?? "/");
  const dict = t(locale);
  const { nav } = getData(locale);
  const selector = nav.chapters.find(
    (c) => c.slug === "selector"
  ) as ChapterSelector;

  return (
    <nav className="flex h-full flex-col gap-1 overflow-y-auto no-scrollbar px-2 py-4 text-sm">
      <Link
        href={localeHref(locale, "/")}
        className="mb-2 flex items-center gap-2 rounded-md px-2 py-1.5 font-medium text-ink-800 hover:bg-ink-100 dark:text-ink-100 dark:hover:bg-ink-800"
      >
        <Home size={15} />
        {dict.guideHome}
      </Link>

      <Link
        href={localeHref(locale, "/xref")}
        className="mb-2 flex items-center gap-2 rounded-md px-2 py-1.5 font-medium text-ink-800 hover:bg-ink-100 dark:text-ink-100 dark:hover:bg-ink-800"
      >
        <ArrowLeftRight size={15} />
        {dict.crossReferenceSearch}
      </Link>

      <CategoryRow
        href={localeHref(locale, "/guide/selector")}
        title={selector.title}
        defaultOpen
        level={0}
        bold
      >
        {selector.categories.map((cat) => (
          <CategoryRow
            key={cat.slug}
            href={localeHref(locale, `/guide/selector/${cat.slug}`)}
            title={cat.title}
            level={1}
          >
            {cat.nav.type === "group" ? (
              <SelectorGroupRow
                locale={locale}
                catSlug={cat.slug}
                node={cat.nav}
                level={2}
              />
            ) : undefined}
          </CategoryRow>
        ))}
      </CategoryRow>

      <Link
        href={localeHref(locale, "/spd-configurator")}
        className="mt-2 flex items-center gap-2 rounded-md px-2 py-1.5 font-medium text-ink-800 hover:bg-ink-100 dark:text-ink-100 dark:hover:bg-ink-800"
      >
        <Sliders size={15} />
        {dict.spdConfigurator}
      </Link>
    </nav>
  );
}
