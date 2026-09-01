import { nav } from "@/lib/data";
import type {
  ChapterAbout,
  ChapterSelector,
  ChapterMarkets,
  ChapterKnowledge,
  SelectorNavNode,
} from "@/lib/types";
import CategoryRow from "@/components/CategoryRow";
import { Home } from "lucide-react";
import Link from "next/link";

function SelectorGroupRow({
  catSlug,
  node,
  level,
}: {
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
          href={`/guide/selector/${catSlug}/${child.slug}`}
          title={child.title}
          count={child.count}
          level={level}
        />
      ))}
    </>
  );
}

export default function Sidebar() {
  const about = nav.chapters.find((c) => c.slug === "about") as ChapterAbout;
  const selector = nav.chapters.find(
    (c) => c.slug === "selector"
  ) as ChapterSelector;
  const markets = nav.chapters.find(
    (c) => c.slug === "markets"
  ) as ChapterMarkets;
  const knowledge = nav.chapters.find(
    (c) => c.slug === "knowledge"
  ) as ChapterKnowledge;

  return (
    <nav className="flex h-full flex-col gap-1 overflow-y-auto no-scrollbar px-2 py-4 text-sm">
      <Link
        href="/"
        className="mb-2 flex items-center gap-2 rounded-md px-2 py-1.5 font-medium text-ink-800 hover:bg-ink-100 dark:text-ink-100 dark:hover:bg-ink-800"
      >
        <Home size={15} />
        Guide Home
      </Link>

      <CategoryRow href="/guide/about" title={about.title} level={0}>
        {about.items.map((it) => (
          <CategoryRow
            key={it.slug}
            href={`/guide/${it.slug}`}
            title={it.title}
            level={1}
          />
        ))}
      </CategoryRow>

      <CategoryRow
        href="/guide/selector"
        title={selector.title}
        count={selector.categories.reduce((s, c) => s + c.count, 0)}
        defaultOpen
        level={0}
      >
        {selector.categories.map((cat) => (
          <CategoryRow
            key={cat.slug}
            href={`/guide/selector/${cat.slug}`}
            title={cat.title}
            count={cat.count}
            level={1}
          >
            {cat.nav.type === "group" ? (
              <SelectorGroupRow
                catSlug={cat.slug}
                node={cat.nav}
                level={2}
              />
            ) : undefined}
          </CategoryRow>
        ))}
      </CategoryRow>

      <CategoryRow href="/guide/markets" title={markets.title} level={0}>
        {markets.items.map((it) => (
          <CategoryRow
            key={it.slug}
            href={`/guide/${it.slug}`}
            title={it.title}
            level={1}
          />
        ))}
      </CategoryRow>

      <CategoryRow href="/guide/knowledge" title={knowledge.title} level={0}>
        {knowledge.items.map((it) => (
          <CategoryRow
            key={it.slug}
            href={`/guide/${it.slug}`}
            title={it.title}
            level={1}
          />
        ))}
      </CategoryRow>
    </nav>
  );
}
