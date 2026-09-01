"use client";

import { useState } from "react";
import Link from "next/link";
import { ChevronLeft, ChevronRight, ExternalLink, RotateCcw, Sliders } from "lucide-react";
import { SPD_NODES, SPD_START } from "@/lib/spd-configurator";

export default function SpdConfigurator() {
  const [path, setPath] = useState<string[]>([SPD_START]);
  const currentId = path[path.length - 1];
  const node = SPD_NODES[currentId];

  function choose(to: string) {
    setPath((p) => [...p, to]);
  }

  function goBack() {
    setPath((p) => (p.length > 1 ? p.slice(0, -1) : p));
  }

  function reset() {
    setPath([SPD_START]);
  }

  const breadcrumb = path
    .slice(0, -1)
    .map((id) => SPD_NODES[id]?.title)
    .filter(Boolean);

  return (
    <div className="mx-auto max-w-2xl px-4 py-10">
      <div className="mb-2 flex items-center gap-2 text-brand-600 dark:text-brand-400">
        <Sliders size={18} />
        <span className="text-xs font-semibold uppercase tracking-wide">
          SPD Configurator
        </span>
      </div>
      <h1 className="mb-2 text-2xl font-bold text-ink-900 dark:text-white">
        Find the right surge protection device
      </h1>
      <p className="mb-6 text-sm text-ink-500 dark:text-ink-400">
        Answer a few questions about your installation to reach the right
        Surge Protection product family.
      </p>

      {breadcrumb.length > 0 && (
        <p className="mb-4 text-xs text-ink-400">
          {breadcrumb.join(" → ")}
        </p>
      )}

      <div className="rounded-xl border border-ink-200 bg-white p-5 dark:border-ink-800 dark:bg-ink-900">
        <h2 className="mb-4 text-lg font-semibold text-ink-800 dark:text-ink-100">
          {node.title}
        </h2>
        <div className="space-y-2">
          {node.options.map((opt) =>
            opt.to ? (
              <button
                key={opt.label}
                onClick={() => choose(opt.to as string)}
                className="flex w-full items-center justify-between rounded-lg border border-ink-200 px-4 py-3 text-left text-sm text-ink-700 transition hover:border-brand-300 hover:bg-brand-50 dark:border-ink-700 dark:text-ink-200 dark:hover:bg-brand-950"
              >
                {opt.label}
                <ChevronRight size={16} className="shrink-0 text-ink-400" />
              </button>
            ) : opt.external ? (
              <a
                key={opt.label}
                href={opt.href}
                target="_blank"
                rel="noopener noreferrer"
                className="flex w-full items-center justify-between rounded-lg border border-ink-200 px-4 py-3 text-left text-sm text-ink-700 transition hover:border-brand-300 hover:bg-brand-50 dark:border-ink-700 dark:text-ink-200 dark:hover:bg-brand-950"
              >
                {opt.label}
                <ExternalLink size={16} className="shrink-0 text-ink-400" />
              </a>
            ) : (
              <Link
                key={opt.label}
                href={opt.href as string}
                className="flex w-full items-center justify-between rounded-lg border border-brand-200 bg-brand-50 px-4 py-3 text-left text-sm font-medium text-brand-700 transition hover:border-brand-300 hover:bg-brand-100 dark:border-brand-900 dark:bg-brand-950 dark:text-brand-300 dark:hover:bg-brand-900"
              >
                {opt.label}
                <ChevronRight size={16} className="shrink-0" />
              </Link>
            )
          )}
        </div>
      </div>

      <div className="mt-4 flex items-center gap-3">
        {path.length > 1 && (
          <button
            onClick={goBack}
            className="flex items-center gap-1.5 rounded-lg border border-ink-200 px-3 py-1.5 text-sm text-ink-600 hover:border-brand-300 hover:bg-brand-50 dark:border-ink-800 dark:text-ink-300 dark:hover:bg-brand-950"
          >
            <ChevronLeft size={15} />
            Back
          </button>
        )}
        {path.length > 1 && (
          <button
            onClick={reset}
            className="flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm text-ink-400 hover:text-ink-600 dark:hover:text-ink-200"
          >
            <RotateCcw size={14} />
            Start over
          </button>
        )}
      </div>
    </div>
  );
}
