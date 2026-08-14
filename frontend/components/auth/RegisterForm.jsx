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
  UserRound,
} from "lucide-react";

export default function RegisterForm() {
  const [showPassword, setShowPassword] =
    useState(false);

  const [showConfirmPassword, setShowConfirmPassword] =
    useState(false);

  return (
    <section
      className="
        relative
        flex
        min-h-screen
        w-full
        items-center
        justify-start
        overflow-hidden
        bg-[#FAFAF7]
        px-8
        lg:w-1/2
        lg:pl-[88px]
        lg:pr-[60px]
      "
    >
      {/* BACK HOME */}
      <Link
        href="/"
        className="
          absolute
          right-[90px]
          top-[52px]
          z-20
          flex
          items-center
          gap-3
          text-[15px]
          font-medium
          text-foreground
        "
      >
        <ArrowLeft size={19} />
        Ana Sayfaya Dön
      </Link>

      {/* DOT DECORATION */}
      <div className="absolute right-8 top-8 z-10 grid grid-cols-5 gap-[7px] opacity-35">
        {Array.from({ length: 20 }).map(
          (_, i) => (
            <span
              key={i}
              className="h-[3px] w-[3px] rounded-full bg-primary"
            />
          ),
        )}
      </div>

      {/* CONTENT */}
      <div
        className="
          relative
          z-20
          w-full
          max-w-[500px]
          -translate-y-[2px]
          lg:translate-x-[24px]
        "
      >
        {/* HEADER */}
        <h1 className="text-[40px] font-bold leading-[1.08] tracking-[-0.045em] text-foreground">
          Hesabını oluştur
        </h1>

        <div className="mt-3 h-[3px] w-[50px] bg-primary" />

        <p className="mt-5 text-[16px] leading-7 text-muted">
          Sana özel seyahat planları oluşturmak
          için
          <br />
          birkaç adımda hesabını oluştur.
        </p>

        {/* FORM */}
        <form
          className="mt-4"
          onSubmit={(e) => e.preventDefault()}
        >
          {/* NAME */}
          <div>
            <label
              htmlFor="name"
              className="mb-2 block text-[14px] font-semibold text-foreground"
            >
              Ad Soyad
            </label>

            <div className="relative">
              <UserRound
                size={18}
                className="absolute left-4 top-1/2 -translate-y-1/2 text-[#667085]"
              />

              <input
                id="name"
                type="text"
                placeholder="Adınızı ve soyadınızı girin"
                className="
                  h-[52px]
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

          {/* EMAIL */}
          <div className="mt-3">
            <label
              htmlFor="email"
              className="mb-2 block text-[14px] font-semibold text-foreground"
            >
              E-posta
            </label>

            <div className="relative">
              <Mail
                size={18}
                className="absolute left-4 top-1/2 -translate-y-1/2 text-[#667085]"
              />

              <input
                id="email"
                type="email"
                placeholder="ornek@email.com"
                className="
                  h-[52px]
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

          {/* PASSWORD */}
          <div className="mt-3">
            <label
              htmlFor="password"
              className="mb-2 block text-[14px] font-semibold text-foreground"
            >
              Şifre
            </label>

            <div className="relative">
              <LockKeyhole
                size={18}
                className="absolute left-4 top-1/2 -translate-y-1/2 text-[#667085]"
              />

              <input
                id="password"
                type={
                  showPassword
                    ? "text"
                    : "password"
                }
                placeholder="Şifrenizi oluşturun"
                className="
                  h-[52px]
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
                onClick={() =>
                  setShowPassword(
                    !showPassword,
                  )
                }
                className="absolute right-4 top-1/2 -translate-y-1/2 text-[#667085]"
                aria-label={
                  showPassword
                    ? "Şifreyi gizle"
                    : "Şifreyi göster"
                }
              >
                {showPassword ? (
                  <EyeOff size={19} />
                ) : (
                  <Eye size={19} />
                )}
              </button>
            </div>
          </div>

          {/* CONFIRM PASSWORD */}
          <div className="mt-3">
            <label
              htmlFor="confirmPassword"
              className="mb-2 block text-[14px] font-semibold text-foreground"
            >
              Şifre Tekrar
            </label>

            <div className="relative">
              <LockKeyhole
                size={18}
                className="absolute left-4 top-1/2 -translate-y-1/2 text-[#667085]"
              />

              <input
                id="confirmPassword"
                type={
                  showConfirmPassword
                    ? "text"
                    : "password"
                }
                placeholder="Şifrenizi tekrar girin"
                className="
                  h-[52px]
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
                onClick={() =>
                  setShowConfirmPassword(
                    !showConfirmPassword,
                  )
                }
                className="absolute right-4 top-1/2 -translate-y-1/2 text-[#667085]"
                aria-label={
                  showConfirmPassword
                    ? "Şifreyi gizle"
                    : "Şifreyi göster"
                }
              >
                {showConfirmPassword ? (
                  <EyeOff size={19} />
                ) : (
                  <Eye size={19} />
                )}
              </button>
            </div>
          </div>

          {/* REGISTER BUTTON */}
          <button
            type="submit"
            className="
              mt-4
              flex
              h-[54px]
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
              Kayıt Ol
            </span>

            <ArrowRight size={21} />
          </button>

          {/* DIVIDER */}
          <div className="my-3 flex items-center gap-5">
            <div className="h-px flex-1 bg-border-strong" />

            <span className="text-[14px] text-muted">
              veya
            </span>

            <div className="h-px flex-1 bg-border-strong" />
          </div>

          {/* SOCIAL LOGIN */}
          <div className="space-y-2">
            {/* GOOGLE */}
            <button
              type="button"
              className="
                flex
                h-[52px]
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

            {/* APPLE */}
            <button
              type="button"
              className="
                flex
                h-[52px]
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

        {/* LOGIN */}
        <p className="mt-3 text-center text-[15px] text-muted">
          Zaten hesabın var mı?{" "}
          <Link
            href="/login"
            className="font-semibold text-primary"
          >
            Giriş Yap
          </Link>
        </p>
      </div>

      {/* BOTTOM DECORATION */}
<div
  className="
    pointer-events-none
    absolute
    bottom-0
    left-0
    right-0
    z-[1]
    h-[380px]
    overflow-hidden
  "
  aria-hidden="true"
>
        {/* BOTTOM WAVES */}
<div
  className="
    pointer-events-none
    absolute
    bottom-0
    left-0
    z-[2]
    h-[120px]
    w-[calc(100%-230px)]
    opacity-30
  "
>
  <svg
    className="h-full w-full"
    viewBox="0 0 800 120"
    preserveAspectRatio="none"
    fill="none"
  >
    <path
      d="M0 80 C150 20 240 120 390 70 C540 20 650 110 800 55"
      stroke="#F5B000"
      strokeWidth="1"
    />

    <path
      d="M0 100 C150 40 250 130 400 85 C550 35 650 120 800 75"
      stroke="#F5B000"
      strokeWidth="1"
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
      className="shrink-0"
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