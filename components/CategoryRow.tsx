"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ChevronRight } from "lucide-react";
import type { ReactNode, MouseEvent } from "react";

export default function CategoryRow({
  href,
  title,
  count,
  children,
  defaultOpen = false,
  level = 0,
}: {
  href: string;
  title: string;
  count?: number;
  children?: ReactNode;
  defaultOpen?: boolean;
  level?: number;
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
        className={`flex items-center justify-between gap-2 rounded-md px-2 py-1.5 text-sm hover:bg-ink-100 dark:hover:bg-ink-800 ${
          isActive
            ? "bg-brand-50 text-brand-700 font-medium dark:bg-brand-950 dark:text-brand-300"
            : "text-ink-700 dark:text-ink-200"
        }`}
        style={{ paddingLeft: 8 + level * 12 }}
      >
        <span className="truncate">{title}</span>
        {typeof count === "number" && (
          <span className="shrink-0 text-xs text-ink-400">{count}</span>
        )}
      </Link>
    );
  }

  return (
    <details open={open} className="group/details">
      <summary
        className={`flex cursor-pointer list-none items-center justify-between gap-2 rounded-md px-2 py-1.5 text-sm hover:bg-ink-100 dark:hover:bg-ink-800 [&::-webkit-details-marker]:hidden ${
          isActive
            ? "bg-brand-50 text-brand-700 font-medium dark:bg-brand-950 dark:text-brand-300"
            : "text-ink-700 dark:text-ink-200"
        }`}
        style={{ paddingLeft: 8 + level * 12 }}
      >
        <Link href={href} onClick={stop} className="min-w-0 flex-1 truncate">
          {title}
        </Link>
        <span className="flex shrink-0 items-center gap-1.5 text-xs text-ink-400">
          {typeof count === "number" && <span>{count}</span>}
          <ChevronRight
            size={14}
            className="transition-transform group-open/details:rotate-90"
          />
        </span>
      </summary>
      <div>{children}</div>
    </details>
  );
}
