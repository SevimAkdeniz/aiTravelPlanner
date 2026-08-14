import Image from "next/image";
import Link from "next/link";
import {
  MapPin,
  Sparkles,
  Wallet,
} from "lucide-react";

const features = [
  {
    icon: Sparkles,
    line1: "Kişiselleştirilmiş",
    line2: "Öneriler",
  },
  {
    icon: MapPin,
    line1: "Akıllı",
    line2: "Rotalar",
  },
  {
    icon: Wallet,
    line1: "Bütçe Dostu",
    line2: "Planlama",
  },
];

export default function AuthVisual() {
  return (
    <section className="relative hidden min-h-screen overflow-hidden lg:block lg:w-1/2">
      {/* BACKGROUND IMAGE */}
      <Image
        src="/images/auth/login-rome-bg-v4.png"
        alt="Roma manzarası"
        fill
        priority
        className="object-cover"
        style={{
          objectPosition: "15% center",
        }}
      />

      {/* VERY SUBTLE DARK LAYER */}
      <div className="absolute inset-0 z-[1] bg-[#172033]/[0.04]" />

      {/* ORGANIC TRANSPARENT WHITE SHAPE */}
      <div className="pointer-events-none absolute inset-0 z-[2]">
        <svg
          className="h-full w-full"
          viewBox="0 0 900 1080"
          preserveAspectRatio="none"
          aria-hidden="true"
        >
          <path
            d="
              M 0 0
              H 430

              C 515 0,
                575 18,
                620 58

              C 665 98,
                690 155,
                695 230

              C 700 310,
                690 395,
                670 485

              C 650 575,
                620 665,
                575 755

              C 535 835,
                490 905,
                425 960

              C 360 1015,
                275 1045,
                165 1062

              C 105 1072,
                50 1077,
                0 1080

              Z
            "
            fill="rgba(250, 248, 243, 0.28)"
          />
        </svg>
      </div>

      {/* LOGO */}
      <Link
        href="/"
        className="
          absolute
          left-[4.5%]
          top-[7%]
          z-20
          flex
          items-center
          gap-4
        "
      >
        <div className="flex h-12 w-12 items-center justify-center text-primary">
          <Sparkles
            size={34}
            strokeWidth={1.9}
          />
        </div>

        <span className="text-[28px] font-bold tracking-[-0.04em] text-foreground">
          AI Travel Planner
        </span>
      </Link>

      {/* MAIN CONTENT */}
      <div
        className="
          absolute
          left-[5.5%]
          top-[23%]
          z-20
          w-[540px]
        "
      >
        <h1
          className="
            text-[72px]
            font-bold
            leading-[0.96]
            tracking-[-0.06em]
            text-foreground
          "
        >
          <span className="text-primary">
            Roma
          </span>{" "}
          seni
          <br />
          bekliyor.
        </h1>

        <p className="mt-7 text-[20px] leading-8 text-[#344054]">
          Rotanı{" "}
          <span className="font-medium text-primary">
            yapay zekâ
          </span>{" "}
          senin için şekillendirsin.
        </p>

        {/* FEATURE CARDS */}
        <div className="mt-9 flex gap-3">
          {features.map((item) => {
            const Icon = item.icon;

            return (
              <div
                key={item.line1}
                className="
                  flex
                  h-[54px]
                  items-center
                  gap-2.5
                  rounded-[14px]
                  bg-white/95
                  px-3.5
                  shadow-[0_6px_18px_rgba(23,32,51,0.07)]
                "
              >
                <div
                  className="
                    flex
                    h-8
                    w-8
                    shrink-0
                    items-center
                    justify-center
                    rounded-full
                    bg-primary-soft
                    text-primary
                  "
                >
                  <Icon
                    size={17}
                    strokeWidth={2}
                  />
                </div>

                <div className="whitespace-nowrap text-[12px] font-medium leading-[1.15] text-foreground">
                  <div>{item.line1}</div>
                  <div>{item.line2}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* ROUTE DECORATION */}
      <div
        className="
          pointer-events-none
          absolute
          right-[6%]
          top-[28%]
          z-20
          h-[380px]
          w-[170px]
        "
      >
        <svg
          viewBox="0 0 170 380"
          className="absolute inset-0 h-full w-full"
          fill="none"
          aria-hidden="true"
        >
          <path
            d="
              M 118 28
              C 78 58, 66 96, 86 130
              C 108 168, 121 206, 101 242
              C 82 277, 63 304, 36 330
            "
            stroke="#F5B000"
            strokeWidth="2.5"
            strokeDasharray="8 10"
            strokeLinecap="round"
          />
        </svg>

        {/* TOP PIN */}
        <div className="absolute right-[26px] top-[8px] flex h-10 w-10 items-center justify-center rounded-full bg-white shadow-[0_8px_24px_rgba(23,32,51,0.10)]">
          <MapPin
            size={18}
            className="text-primary"
          />
        </div>

        {/* BOTTOM PIN */}
        <div className="absolute bottom-[26px] left-[18px] flex h-11 w-11 items-center justify-center rounded-full bg-primary text-white shadow-[0_12px_24px_rgba(245,176,0,0.28)]">
          <MapPin size={20} />
        </div>
      </div>

      {/* AI ROUTE CARD */}
      <div
        className="
          absolute
          bottom-[9%]
          left-[6%]
          z-20
          w-[205px]
          rounded-[18px]
          bg-white
          px-4
          py-3.5
          shadow-[0_14px_34px_rgba(23,32,51,0.14)]
        "
      >
        <div className="flex items-center gap-2.5">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-primary-soft text-primary">
            <Sparkles size={17} />
          </div>

          <div>
            <p className="text-[14px] font-semibold text-foreground">
              AI Rotası Hazır
            </p>

            <p className="mt-0.5 text-[12px] text-muted">
              Roma · Sana Özel
            </p>
          </div>
        </div>

        <div className="mt-3 h-[4px] overflow-hidden rounded-full bg-[#EADFB7]">
          <div className="h-full w-[72%] rounded-full bg-primary" />
        </div>

        <div className="mt-2.5 flex items-center gap-1">
          <span className="text-[12px] font-bold text-primary">
            %94
          </span>

          <span className="text-[12px] text-muted">
            Sana Uygun
          </span>
        </div>
      </div>
    </section>
  );
}