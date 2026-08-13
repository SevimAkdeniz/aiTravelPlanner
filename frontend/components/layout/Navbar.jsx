"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  Menu,
  X,
  Sparkles,
  UserRound,
} from "lucide-react";

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 24);
    };

    handleScroll();

    window.addEventListener("scroll", handleScroll, {
      passive: true,
    });

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <header
      className={`
        sticky top-0 z-50 w-full
        transition-all duration-300 ease-out
        ${
          scrolled
            ? "bg-surface/90 shadow-[0_8px_30px_rgba(23,32,51,0.08)] backdrop-blur-xl"
            : "bg-surface"
        }
      `}
    >
      {/* NAVBAR */}
      <div
        className={`
          flex w-full items-center justify-between
          border-b border-border
          px-5 sm:px-8 lg:px-12
          transition-all duration-300 ease-out
          ${scrolled ? "h-[68px]" : "h-[84px]"}
        `}
      >
        {/* LOGO */}
        <Link
          href="/"
          className="flex shrink-0 items-center gap-3"
        >
          {/* Logo Icon */}
          <div
            className={`
              relative flex items-center justify-center
              transition-all duration-300 ease-out
              ${scrolled ? "h-8 w-7" : "h-10 w-9"}
            `}
          >
            <div
              className={`
                absolute rotate-45
                rounded-[50%_50%_50%_14%]
                bg-primary
                shadow-[0_6px_16px_rgba(245,176,0,0.20)]
                transition-all duration-300 ease-out
                ${
                  scrolled
                    ? "h-7 w-7"
                    : "h-8 w-8"
                }
              `}
            />

            <Sparkles
              strokeWidth={2.2}
              className={`
                relative z-10 -translate-y-[1px]
                text-white
                transition-all duration-300 ease-out
                ${
                  scrolled
                    ? "h-[13px] w-[13px]"
                    : "h-[15px] w-[15px]"
                }
              `}
            />
          </div>

          {/* Logo Text */}
          <span
            className={`
              font-bold tracking-[-0.03em] text-foreground
              transition-all duration-300 ease-out
              ${
                scrolled
                  ? "text-[18px] sm:text-[19px]"
                  : "text-[19px] sm:text-[22px]"
              }
            `}
          >
            AI Travel Planner
          </span>
        </Link>

        {/* DESKTOP NAVIGATION */}
        <nav className="hidden h-full items-center gap-10 lg:flex">
          <Link
            href="/"
            className="relative flex h-full items-center text-[15px] font-medium text-primary"
          >
            Ana Sayfa

            <span
              className={`
                absolute bottom-0 left-1/2
                -translate-x-1/2
                rounded-full bg-primary
                transition-all duration-300
                ${
                  scrolled
                    ? "h-[2px] w-[58px]"
                    : "h-[3px] w-[68px]"
                }
              `}
            />
          </Link>

          <Link
            href="#how-it-works"
            className="flex h-full items-center text-[15px] font-medium text-foreground transition-colors hover:text-primary"
          >
            Nasıl Çalışır?
          </Link>

          <Link
            href="/plans"
            className="flex h-full items-center text-[15px] font-medium text-foreground transition-colors hover:text-primary"
          >
            Planlarım
          </Link>

          <Link
            href="#about"
            className="flex h-full items-center text-[15px] font-medium text-foreground transition-colors hover:text-primary"
          >
            Hakkımızda
          </Link>
        </nav>

        {/* DESKTOP ACTIONS */}
        <div className="hidden items-center gap-7 lg:flex">
          <Link
            href="/login"
            className="flex items-center gap-2 text-[15px] font-medium text-foreground transition-colors hover:text-primary"
          >
            <UserRound
              size={20}
              strokeWidth={1.8}
            />

            Giriş Yap
          </Link>

          <Link
            href="/planner"
            className={`
              flex items-center gap-2.5
              rounded-[14px]
              bg-primary
              font-semibold text-white
              shadow-button
              transition-all duration-300 ease-out
              hover:-translate-y-[1px]
              hover:bg-primary-hover
              ${
                scrolled
                  ? "h-10 px-5 text-[14px]"
                  : "h-12 px-7 text-[15px]"
              }
            `}
          >
            <Sparkles
              size={scrolled ? 15 : 17}
              strokeWidth={2}
            />

            Seyahatimi Planla
          </Link>
        </div>

        {/* MOBILE BUTTON */}
<button
  type="button"
  aria-label={mobileMenuOpen ? "Menüyü kapat" : "Menüyü aç"}
  aria-expanded={mobileMenuOpen}
  onClick={() => setMobileMenuOpen((prev) => !prev)}
  className="
    relative
    flex h-10 w-10
    items-center justify-center
    rounded-xl
    text-foreground
    transition-all duration-300 ease-out
    hover:bg-primary-soft
    hover:text-primary
    active:scale-95
    lg:hidden
  "
>
  <span className="relative block h-5 w-5">
    {/* MENU ICON */}
    <Menu
      size={20}
      strokeWidth={1.8}
      className={`
        absolute inset-0
        transition-all duration-300 ease-out
        ${
          mobileMenuOpen
            ? "scale-75 rotate-90 opacity-0"
            : "scale-100 rotate-0 opacity-100"
        }
      `}
    />

    {/* CLOSE ICON */}
    <X
      size={20}
      strokeWidth={1.8}
      className={`
        absolute inset-0
        transition-all duration-300 ease-out
        ${
          mobileMenuOpen
            ? "scale-100 rotate-0 opacity-100"
            : "scale-75 -rotate-90 opacity-0"
        }
      `}
    />
  </span>
</button>
      </div>

      {/* MOBILE MENU */}
      <div
        className={`
          absolute left-0 top-full w-full
          overflow-hidden
          border-b border-border
          bg-surface/95
          backdrop-blur-xl
          transition-all duration-300 ease-out
          lg:hidden
          ${
            mobileMenuOpen
              ? "max-h-[520px] translate-y-0 opacity-100 shadow-card"
              : "pointer-events-none max-h-0 -translate-y-2 opacity-0"
          }
        `}
      >
        <nav className="flex flex-col px-5 py-5 sm:px-8">
          <Link
            href="/"
            onClick={() => setMobileMenuOpen(false)}
            className="border-b border-border py-4 text-[15px] font-semibold text-primary"
          >
            Ana Sayfa
          </Link>

          <Link
            href="#how-it-works"
            onClick={() => setMobileMenuOpen(false)}
            className="border-b border-border py-4 text-[15px] font-medium text-foreground transition-colors hover:text-primary"
          >
            Nasıl Çalışır?
          </Link>

          <Link
            href="/plans"
            onClick={() => setMobileMenuOpen(false)}
            className="border-b border-border py-4 text-[15px] font-medium text-foreground transition-colors hover:text-primary"
          >
            Planlarım
          </Link>

          <Link
            href="#about"
            onClick={() => setMobileMenuOpen(false)}
            className="border-b border-border py-4 text-[15px] font-medium text-foreground transition-colors hover:text-primary"
          >
            Hakkımızda
          </Link>

          <Link
            href="/login"
            onClick={() => setMobileMenuOpen(false)}
            className="flex items-center gap-2 border-b border-border py-4 text-[15px] font-medium text-foreground transition-colors hover:text-primary"
          >
            <UserRound
              size={19}
              strokeWidth={1.8}
            />

            Giriş Yap
          </Link>

          <Link
            href="/planner"
            onClick={() => setMobileMenuOpen(false)}
            className="
              mt-5 flex h-12
              items-center justify-center gap-2
              rounded-xl
              bg-primary
              px-5
              text-[15px] font-semibold text-white
              shadow-button
              transition-all
              hover:bg-primary-hover
            "
          >
            <Sparkles size={17} />

            Seyahatimi Planla
          </Link>
        </nav>
      </div>
    </header>
  );
}