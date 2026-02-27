"use client"

import type React from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"

import { cn } from "@/lib/utils"

type NavItem = {
  href: string
  label: string
}

const NAV_ITEMS: NavItem[] = [
  { href: "/", label: "Home" },
  { href: "/upload", label: "Upload" },
  { href: "/results", label: "Candidates" },
  { href: "/analytics", label: "Analytics" },
  { href: "/graph", label: "Graph" },
]

function isActive(pathname: string, href: string) {
  if (href === "/") return pathname === "/"
  return pathname === href || pathname.startsWith(`${href}/`)
}

export default function AppNav({
  rightSlot,
  className,
}: {
  rightSlot?: React.ReactNode
  className?: string
}) {
  const pathname = usePathname()

  return (
    <header className={cn("flex items-center justify-between gap-6", className)}>
      <Link href="/" className="flex items-center gap-2 group cursor-pointer">
        <div className="size-10 bg-brutal-black flex items-center justify-center rounded-xl text-white shadow-hard group-hover:rotate-6 transition-transform">
          <span className="material-symbols-outlined text-2xl">auto_awesome</span>
        </div>
        <span className="text-xl font-black uppercase tracking-tighter">ResumeRanker</span>
      </Link>

      <nav className="hidden md:flex items-center gap-2">
        {NAV_ITEMS.map((item) => {
          const active = isActive(pathname, item.href)
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "brutalist-button text-xs py-2",
                active && "brutalist-button-primary",
              )}
            >
              {item.label}
            </Link>
          )
        })}
      </nav>

      <div className="flex items-center gap-3">
        {rightSlot}
        <div className="md:hidden flex items-center gap-2">
          <Link href="/upload" className="brutalist-button text-xs py-2">
            Upload
          </Link>
          <Link href="/results" className="brutalist-button-primary text-xs py-2">
            Results
          </Link>
        </div>
      </div>
    </header>
  )
}

