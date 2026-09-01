"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

export default function ActiveLink({
  href,
  children,
  className = "",
  activeClassName = "",
}: {
  href: string;
  children: ReactNode;
  className?: string;
  activeClassName?: string;
}) {
  const pathname = usePathname();
  const isActive = pathname === href;
  return (
    <Link
      href={href}
      className={`${className} ${isActive ? activeClassName : ""}`}
      aria-current={isActive ? "page" : undefined}
    >
      {children}
    </Link>
  );
}
