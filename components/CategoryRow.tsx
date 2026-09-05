"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ChevronRight } from "lucide-react";
import type { ReactNode, MouseEvent } from "react";

export default function CategoryRow({
  href,
  title,
  children,
  defaultOpen = false,
  level = 0,
  bold = false,
}: {
  href: string;
  title: string;
  children?: ReactNode;
  defaultOpen?: boolean;
  level?: number;
  bold?: boolean;
}) {
  const pathname = usePathname();
  const isActive = pathname === href;
  const containsActive = children != null && pathname?.startsWith(href + "/");
  const open = defaultOpen || isActive || containsActive;

  function stop(e: MouseEvent) {
    e.stopPropagation();
  }

  if (!children) {
    return (
      <Link
        href={href}
        onClick={stop}
        className={`flex items-center gap-2 rounded-lg py-1.5 pr-2 text-sm transition-colors ${
          isActive
            ? "bg-brand-50 font-medium text-brand-700 dark:bg-brand-950/60 dark:text-brand-300"
            : "text-ink-700 hover:bg-ink-100 dark:text-ink-200 dark:hover:bg-ink-800"
        }`}
        style={{ paddingLeft: 8 + level * 12 }}
      >
        <span className={`truncate ${bold ? "font-medium" : ""}`} title={title}>{title}</span>
      </Link>
    );
  }

  return (
    <details open={open} className="group/details">
      <summary
        className={`flex cursor-pointer list-none items-center justify-between gap-2 rounded-lg py-1.5 pr-2 text-sm transition-colors [&::-webkit-details-marker]:hidden ${
          isActive
            ? "bg-brand-50 font-medium text-brand-700 dark:bg-brand-950/60 dark:text-brand-300"
            : "text-ink-700 hover:bg-ink-100 dark:text-ink-200 dark:hover:bg-ink-800"
        }`}
        style={{ paddingLeft: 8 + level * 12 }}
      >
        <Link
          href={href}
          onClick={stop}
          title={title}
          className={`min-w-0 flex-1 truncate ${bold ? "font-medium" : ""}`}
        >
          {title}
        </Link>
        <ChevronRight
          size={14}
          className="shrink-0 text-ink-400 transition-transform group-open/details:rotate-90"
        />
      </summary>
      <div>{children}</div>
    </details>
  );
}
