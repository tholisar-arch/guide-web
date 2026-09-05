import { FileText } from "lucide-react";
import type { ResourceLink } from "@/lib/types";
import { t, type Locale } from "@/lib/i18n";

export default function ResourceLinks({
  links,
  locale,
}: {
  links: ResourceLink[];
  locale: Locale;
}) {
  if (!links.length) return null;
  const dict = t(locale);

  return (
    <div className="mt-6 rounded-2xl border border-ink-200 bg-ink-50/60 p-5 dark:border-ink-800 dark:bg-ink-900/40">
      <h2 className="mb-3 text-xs font-semibold uppercase tracking-wide text-ink-500 dark:text-ink-400">
        {dict.documentation}
      </h2>
      <ul className="space-y-2">
        {links.map((link, i) => (
          <li key={i}>
            <a
              href={link.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-sm text-brand-600 transition-colors hover:text-brand-700 hover:underline dark:text-brand-400 dark:hover:text-brand-300"
            >
              <FileText size={14} className="shrink-0" />
              {link.label}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
