import { FileText } from "lucide-react";
import type { ResourceLink } from "@/lib/types";

export default function ResourceLinks({ links }: { links: ResourceLink[] }) {
  if (!links.length) return null;

  return (
    <div className="mt-6 rounded-xl border border-ink-200 p-4 dark:border-ink-800">
      <h2 className="mb-3 text-sm font-semibold text-ink-700 dark:text-ink-200">
        Documentation
      </h2>
      <ul className="space-y-2">
        {links.map((link, i) => (
          <li key={i}>
            <a
              href={link.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-sm text-brand-600 hover:underline dark:text-brand-400"
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
