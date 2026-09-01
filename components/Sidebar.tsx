import { nav } from "@/lib/data";
import type { ChapterSelector, SelectorNavNode } from "@/lib/types";
import CategoryRow from "@/components/CategoryRow";
import { Home, ArrowLeftRight, Sliders } from "lucide-react";
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
          level={level}
        />
      ))}
    </>
  );
}

export default function Sidebar() {
  const selector = nav.chapters.find(
    (c) => c.slug === "selector"
  ) as ChapterSelector;

  return (
    <nav className="flex h-full flex-col gap-1 overflow-y-auto no-scrollbar px-2 py-4 text-sm">
      <Link
        href="/"
        className="mb-2 flex items-center gap-2 rounded-md px-2 py-1.5 font-medium text-ink-800 hover:bg-ink-100 dark:text-ink-100 dark:hover:bg-ink-800"
      >
        <Home size={15} />
        Guide Home
      </Link>

      <Link
        href="/xref"
        className="mb-2 flex items-center gap-2 rounded-md px-2 py-1.5 font-medium text-ink-800 hover:bg-ink-100 dark:text-ink-100 dark:hover:bg-ink-800"
      >
        <ArrowLeftRight size={15} />
        Cross Reference Search
      </Link>

      <CategoryRow href="/guide/selector" title={selector.title} defaultOpen level={0}>
        {selector.categories.map((cat) => (
          <CategoryRow
            key={cat.slug}
            href={`/guide/selector/${cat.slug}`}
            title={cat.title}
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

      <Link
        href="/spd-configurator"
        className="mt-2 flex items-center gap-2 rounded-md px-2 py-1.5 font-medium text-ink-800 hover:bg-ink-100 dark:text-ink-100 dark:hover:bg-ink-800"
      >
        <Sliders size={15} />
        SPD Configurator
      </Link>
    </nav>
  );
}
