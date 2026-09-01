import Image from "next/image";
import Link from "next/link";
import { ChevronLeft } from "lucide-react";
import type { ReactNode } from "react";

export default function SelectorFrame({
  title,
  backHref,
  children,
}: {
  title: string;
  backHref?: string;
  children: ReactNode;
}) {
  return (
    <div className="mx-auto max-w-5xl px-4 py-6 sm:py-8">
      <div className="overflow-hidden rounded-xl border border-ink-200 shadow-card dark:border-ink-800">
        <div className="relative flex items-center gap-4 border-b border-ink-200 bg-white pr-4 dark:border-ink-800 dark:bg-ink-900">
          <div className="relative hidden h-[52px] w-[140px] shrink-0 overflow-hidden sm:block sm:h-[64px] sm:w-[168px]">
            <Image
              src="/brand/selector-banner.webp"
              alt=""
              fill
              className="object-cover"
              priority
            />
          </div>
          <h1 className="min-w-0 flex-1 truncate py-3 text-lg font-bold uppercase tracking-wide text-ink-700 sm:text-2xl dark:text-ink-100">
            {title}
          </h1>
          <div className="relative hidden h-6 w-28 shrink-0 sm:block sm:h-7 sm:w-32">
            <Image
              src="/brand/mersen-logo.png"
              alt="Mersen"
              fill
              className="object-contain object-right"
            />
          </div>
        </div>

        {backHref && (
          <div className="flex justify-end bg-white px-4 pt-3 dark:bg-ink-900">
            <Link
              href={backHref}
              className="flex items-center gap-1.5 rounded-full border border-ink-300 px-3 py-1 text-xs font-medium text-ink-600 hover:border-brand-400 hover:text-brand-600 dark:border-ink-700 dark:text-ink-300 dark:hover:text-brand-400"
            >
              <ChevronLeft size={13} />
              Back
            </Link>
          </div>
        )}

        <div className="bg-white px-4 py-5 dark:bg-ink-900 sm:px-6 sm:py-6">
          {children}
        </div>
      </div>
    </div>
  );
}
