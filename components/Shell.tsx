"use client";

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import Link from "next/link";
import { Menu, X } from "lucide-react";
import Image from "next/image";
import type { ReactNode } from "react";
import SearchBox from "@/components/SearchBox";

export default function Shell({
  sidebar,
  children,
}: {
  sidebar: ReactNode;
  children: ReactNode;
}) {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-40 flex h-14 items-center gap-3 border-b border-ink-200 bg-white/90 px-3 backdrop-blur dark:border-ink-800 dark:bg-ink-950/90 sm:px-4">
        <button
          onClick={() => setOpen((v) => !v)}
          className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md text-ink-600 hover:bg-ink-100 lg:hidden dark:text-ink-300 dark:hover:bg-ink-800"
          aria-label="Open menu"
        >
          {open ? <X size={19} /> : <Menu size={19} />}
        </button>
        <Link href="/" className="flex shrink-0 items-center gap-3">
          <span className="flex h-8 items-center rounded-md bg-white px-1.5 shadow-card dark:shadow-none">
            <Image
              src="/brand/mersen-logo.png"
              alt="Mersen"
              width={84}
              height={32}
              className="h-5 w-auto"
              priority
            />
          </span>
          <span className="hidden h-5 w-px bg-ink-200 sm:block dark:bg-ink-800" />
          <span className="hidden text-sm font-medium tracking-tight text-ink-800 sm:block dark:text-ink-50">
            Selection Guide{" "}
            <span className="font-normal text-ink-400">2026 Europe</span>
          </span>
        </Link>
        <div className="ml-auto flex flex-1 items-center justify-end gap-2 sm:flex-none sm:w-80">
          <SearchBox />
        </div>
      </header>

      <div className="mx-auto flex w-full max-w-[1500px] flex-1">
        <div
          className={`fixed inset-0 z-30 bg-black/30 transition-opacity lg:hidden ${
            open ? "opacity-100" : "pointer-events-none opacity-0"
          }`}
          onClick={() => setOpen(false)}
        />
        <aside
          className={`fixed inset-y-0 left-0 z-30 w-72 -translate-x-full border-r border-ink-200 bg-white pt-14 transition-transform lg:static lg:z-0 lg:h-[calc(100vh-3.5rem)] lg:translate-x-0 lg:pt-0 dark:border-ink-800 dark:bg-ink-950 ${
            open ? "translate-x-0" : ""
          }`}
        >
          <div className="sticky top-14 h-[calc(100vh-3.5rem)] lg:top-0">
            {sidebar}
          </div>
        </aside>
        <main className="min-w-0 flex-1">{children}</main>
      </div>
    </div>
  );
}
