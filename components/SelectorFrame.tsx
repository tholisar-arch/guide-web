import Link from "next/link";
import { ChevronLeft } from "lucide-react";
import type { ReactNode } from "react";
import { t, type Locale } from "@/lib/i18n";

export default function SelectorFrame({
  backHref,
  locale,
  topLeft,
  children,
}: {
  backHref?: string;
  locale: Locale;
  topLeft?: ReactNode;
  children: ReactNode;
}) {
  const dict = t(locale);
  return (
    <div className="mx-auto max-w-5xl px-4 py-6 sm:py-8">
      {(backHref || topLeft) && (
        <div className="mb-4 flex items-center justify-between gap-3">
          <div>{topLeft}</div>
          {backHref && (
            <Link
              href={backHref}
              className="flex shrink-0 items-center gap-1.5 rounded-full border border-ink-300 px-3 py-1 text-xs font-medium text-ink-600 hover:border-brand-400 hover:text-brand-600 dark:border-ink-700 dark:text-ink-300 dark:hover:text-brand-400"
            >
              <ChevronLeft size={13} />
              {dict.back}
            </Link>
          )}
        </div>
      )}

      {children}
    </div>
  );
}
