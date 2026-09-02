import Link from "next/link";
import { ChevronLeft } from "lucide-react";
import type { ReactNode } from "react";

export default function SelectorFrame({
  backHref,
  children,
}: {
  backHref?: string;
  children: ReactNode;
}) {
  return (
    <div className="mx-auto max-w-5xl px-4 py-6 sm:py-8">
      {backHref && (
        <div className="mb-4 flex justify-end">
          <Link
            href={backHref}
            className="flex items-center gap-1.5 rounded-full border border-ink-300 px-3 py-1 text-xs font-medium text-ink-600 hover:border-brand-400 hover:text-brand-600 dark:border-ink-700 dark:text-ink-300 dark:hover:text-brand-400"
          >
            <ChevronLeft size={13} />
            Back
          </Link>
        </div>
      )}

      {children}
    </div>
  );
}
