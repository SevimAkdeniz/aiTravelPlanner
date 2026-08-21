"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import {
    ArrowLeft,
    ArrowRight,
    Eye,
    EyeOff,
    LockKeyhole,
    Mail,
  } from "lucide-react";

export default function LoginForm() {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <section
  className="
    relative
    flex
    min-h-[100dvh]
    w-full
    items-start
    justify-center
    overflow-x-hidden
    overflow-y-auto
    bg-[#FAFAF7]
    px-5
    pb-28
    pt-24

    sm:px-8
    sm:pt-28

    lg:min-h-screen
    lg:w-1/2
    lg:items-center
    lg:justify-start
    lg:overflow-hidden
    lg:pb-0
    lg:pl-[88px]
    lg:pr-[60px]
    lg:pt-0
  "
>
      {/* Back Home */}
      <Link
  href="/"
  className="
    absolute
    left-5
    top-7
    z-30
    flex
    items-center
    gap-2
    text-[14px]
    font-medium
    text-foreground

    sm:left-8

    lg:left-auto
    lg:right-[90px]
    lg:top-[52px]
    lg:gap-3
    lg:text-[15px]
  "
>
  <ArrowLeft size={19} />
  Ana Sayfaya Dön
</Link>

      {/* Dot decoration */}
      <div className="absolute right-8 top-8 z-10 hidden grid-cols-5 gap-[7px] opacity-35 lg:grid">
        {Array.from({ length: 20 }).map((_, i) => (
          <span
            key={i}
            className="h-[3px] w-[3px] rounded-full bg-primary"
          />
        ))}
      </div>

      {/* FORM CONTENT */}
      <div
  className="
    relative
    z-20
    w-full
    max-w-[500px]

    lg:translate-x-[24px]
    lg:-translate-y-[2px]
  "
>
        {/* Header */}
        <h1
  className="
    text-[36px]
    font-bold
    leading-[1.08]
    tracking-[-0.045em]
    text-foreground

    sm:text-[40px]
    lg:text-[44px]
  "
>
  Tekrar hoş geldin
</h1>

        <div className="mt-4 h-[3px] w-[50px] bg-primary" />

        <p className="mt-5 text-[15px] leading-6 text-muted sm:text-[16px] sm:leading-7 lg:text-[17px]">
  Seyahat planlarına devam etmek için
  <br className="hidden sm:block" />
  {" "}
  hesabına giriş yap.
</p>

        {/* Form */}
        <form
          className="mt-7"
          onSubmit={(e) => e.preventDefault()}
        >
          {/* Email */}
          <div>
            <label
              htmlFor="email"
              className="mb-2 block text-[15px] font-semibold text-foreground"
            >
              E-posta
            </label>

            <div className="relative">
              <Mail
                size={19}
                className="absolute left-4 top-1/2 -translate-y-1/2 text-[#667085]"
              />

              <input
                id="email"
                type="email"
                placeholder="ornek@email.com"
                className="
                  h-[58px]
                  w-full
                  rounded-xl
                  border
                  border-border-strong
                  bg-white
                  pl-12
                  pr-4
                  text-[15px]
                  text-foreground
                  outline-none
                  transition
                  placeholder:text-subtle
                  focus:border-primary
                "
              />
            </div>
          </div>

          {/* Password */}
          <div className="mt-5">
            <label
              htmlFor="password"
              className="mb-2 block text-[15px] font-semibold text-foreground"
            >
              Şifre
            </label>

            <div className="relative">
              <LockKeyhole
                size={19}
                className="absolute left-4 top-1/2 -translate-y-1/2 text-[#667085]"
              />

              <input
                id="password"
                type={showPassword ? "text" : "password"}
                placeholder="Şifrenizi girin"
                className="
                  h-[60px]
                  w-full
                  rounded-xl
                  border
                  border-border-strong
                  bg-white
                  pl-12
                  pr-12
                  text-[15px]
                  text-foreground
                  outline-none
                  transition
                  placeholder:text-subtle
                  focus:border-primary
                "
              />

              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-[#667085]"
              >
                {showPassword ? (
                  <EyeOff size={20} />
                ) : (
                  <Eye size={20} />
                )}
              </button>
            </div>

            <div className="mt-2 flex justify-end">
              <Link
                href="#"
                className="text-[14px] font-medium text-primary"
              >
                Şifremi Unuttum
              </Link>
            </div>
          </div>

          {/* Login */}
          <button
            type="submit"
            className="
              mt-4
              flex
              h-[60px]
              w-full
              items-center
              justify-center
              rounded-xl
              bg-primary
              px-5
              text-[16px]
              font-semibold
              text-white
              shadow-button
              transition
              hover:bg-primary-hover
            "
          >
            <span className="mx-auto">
              Giriş Yap
            </span>

            <ArrowRight size={21} />
          </button>

          {/* Divider */}
          <div className="my-5 flex items-center gap-5">
            <div className="h-px flex-1 bg-border-strong" />

            <span className="text-[14px] text-muted">
              veya
            </span>

            <div className="h-px flex-1 bg-border-strong" />
          </div>

          {/* Social Login */}
<div className="space-y-3">
  {/* Google */}
  <button
    type="button"
    className="
      flex
      h-[60px]
      w-full
      items-center
      justify-center
      gap-3
      rounded-xl
      border
      border-border-strong
      bg-white
      text-[15px]
      font-medium
      text-foreground
      transition
      hover:bg-[#F8F8F6]
    "
  >
    <GoogleIcon />
    Google ile Devam Et
  </button>

  {/* Apple */}
<button
  type="button"
  className="
    flex
    h-[60px]
    w-full
    items-center
    justify-center
    gap-3
    rounded-xl
    border
    border-border-strong
    bg-white
    text-[15px]
    font-medium
    text-foreground
    transition
    hover:bg-[#F8F8F6]
  "
>
  <AppleIcon />
  Apple ile Devam Et
</button>
</div>
        </form>

        {/* Register */}
        <p className="mt-8 text-center text-[15px] text-muted">
          Henüz hesabın yok mu?{" "}
          <Link
            href="/register"
            className="font-semibold text-primary"
          >
            Kayıt Ol
          </Link>
        </p>
      </div>

     {/* BOTTOM WAVES */}
<div
  className="
    pointer-events-none
    absolute
    bottom-[14px]
    left-0
    z-[2]

    h-[78px]
    w-[76%]
    opacity-[0.38]

    sm:bottom-[10px]
    sm:h-[88px]
    sm:w-[78%]
    sm:opacity-[0.36]

    lg:bottom-0
    lg:h-[120px]
    lg:w-[calc(100%_-_230px)]
    lg:opacity-30
  "
  aria-hidden="true"
>
  <svg
    className="h-full w-full"
    viewBox="0 0 800 120"
    preserveAspectRatio="none"
    fill="none"
  >
    <path
      d="
        M0 78
        C140 52 230 94 355 74
        C485 53 590 91 700 70
        C742 62 772 58 800 55
      "
      stroke="#F5B000"
      strokeWidth="1.35"
      strokeLinecap="round"
    />

    <path
      d="
        M0 101
        C145 73 250 111 375 91
        C500 72 600 108 710 90
        C750 84 778 81 800 79
      "
      stroke="#F5B000"
      strokeWidth="1.35"
      strokeLinecap="round"
    />
  </svg>
</div>

      {/* COLOSSEUM LINE DECORATION */}
      <div
        className="
          pointer-events-none
          absolute
          bottom-[20px]
          right-[-48px]
          z-[1]
          h-[330px]
          w-[270px]
          opacity-[0.55]
        "
        aria-hidden="true"
      >
        <Image
  src="/images/auth/colosseum-line.png"
  alt=""
  fill
  className="object-contain object-bottom"
/>
      </div>
    </section>
  );
}

function GoogleIcon() {
  return (
    <svg
      width="19"
      height="19"
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <path
        fill="#4285F4"
        d="M21.6 12.23c0-.71-.06-1.4-.18-2.06H12v3.9h5.38a4.6 4.6 0 0 1-2 3.02v2.51h3.24c1.9-1.75 2.98-4.34 2.98-7.37Z"
      />

      <path
        fill="#34A853"
        d="M12 22c2.7 0 4.98-.9 6.64-2.4l-3.24-2.51c-.9.6-2.05.96-3.4.96-2.6 0-4.81-1.76-5.6-4.13H3.05v2.6A10 10 0 0 0 12 22Z"
      />

      <path
        fill="#FBBC05"
        d="M6.4 13.92A6.03 6.03 0 0 1 6.08 12c0-.67.11-1.32.32-1.92v-2.6H3.05A10 10 0 0 0 2 12c0 1.61.38 3.14 1.05 4.52l3.35-2.6Z"
      />

      <path
        fill="#EA4335"
        d="M12 5.95c1.47 0 2.8.51 3.84 1.5l2.88-2.89C16.97 2.93 14.7 2 12 2a10 10 0 0 0-8.95 5.48l3.35 2.6C7.19 7.71 9.4 5.95 12 5.95Z"
      />
    </svg>
  );
}
function AppleIcon() {
    return (
      <svg
        width="20"
        height="20"
        viewBox="0 0 24 24"
        aria-hidden="true"
        className="shrink-0"
      >
        <path
          fill="currentColor"
          d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.79 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.53 4.09ZM12.03 7.25C11.88 5.02 13.69 3.18 15.77 3c.29 2.58-2.34 4.5-3.74 4.25Z"
        />
      </svg>
    );
  }