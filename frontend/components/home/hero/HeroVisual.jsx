import Image from "next/image";
import {
  Route,
  Target,
  Wallet,
} from "lucide-react";

import HeroRouteDecoration from "./HeroRouteDecoration";
import HeroFloatingCard from "./HeroFloatingCard";
import RomeDayCard from "./RomeDayCard";

export default function HeroVisual() {
  return (
    <>
      {/* =========================
          DESKTOP VISUAL
      ========================== */}
      <div className="absolute inset-y-0 right-0 hidden w-[82%] lg:block">
        <Image
          src="/images/home/hero/hero-rome-final.webp"
          alt="Roma Kolezyum manzarası"
          fill
          priority
          sizes="82vw"
          className="object-cover object-center"
        />

        {/* LEFT FADE */}
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(90deg, #FAFAF7 0%, rgba(250,250,247,0.96) 10%, rgba(250,250,247,0.84) 17%, rgba(250,250,247,0.62) 24%, rgba(250,250,247,0.38) 31%, rgba(250,250,247,0.17) 37%, rgba(250,250,247,0.06) 42%, transparent 47%)",
          }}
        />

        {/* DESKTOP ROUTE */}
        <HeroRouteDecoration />

        {/* CARD CLUSTER */}
        <div className="absolute bottom-[7.2%] right-[5.8%] z-20">
          <div className="relative">
            <RomeDayCard />

            {/* %94 Sana Uygun */}
            <HeroFloatingCard
              icon={Target}
              title="%94 Sana Uygun"
              subtitle="Tercihlerinle eşleşiyor"
              className="left-[-70px] top-[36px] z-30"
            />

            {/* Bütçene Uygun */}
            <HeroFloatingCard
              icon={Wallet}
              title="Bütçene Uygun"
              subtitle="Plan sınırları içinde"
              className="right-[-34px] top-[-18px] z-30"
            />

            {/* Rota Optimize Edildi */}
            <HeroFloatingCard
              icon={Route}
              title="Rota Optimize Edildi"
              subtitle="Daha verimli gezi"
              className="right-[-30px] bottom-[-14px] z-30"
            />
          </div>
        </div>
      </div>

      {/* =========================
          MOBILE / TABLET VISUAL
      ========================== */}
      <div className="relative h-[520px] w-full overflow-hidden lg:hidden">
        <Image
          src="/images/home/hero/hero-rome-final.webp"
          alt="Roma Kolezyum manzarası"
          fill
          priority
          sizes="100vw"
          className="object-cover object-center"
        />

        {/* MOBILE FADE */}
        <div
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(180deg, #FAFAF7 0%, rgba(250,250,247,0.05) 14%, transparent 48%, rgba(250,250,247,0.40) 76%, #FAFAF7 100%)",
          }}
        />

        {/* MOBILE ROUTE + PIN + LANDMARK + AI */}
        <HeroRouteDecoration />

        {/* MOBILE PLAN CARD */}
        <div
          className="
            absolute
            bottom-[72px]
            left-1/2
            z-20
            w-[250px]
            -translate-x-1/2
            rounded-[18px]
            border border-white/80
            bg-white/95
            p-3
            shadow-[0_16px_34px_rgba(23,32,51,0.16)]
            backdrop-blur-xl
          "
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-[12px] font-bold text-foreground">
                Roma · Gün 1
              </p>

              <p className="mt-1 text-[9px] text-muted">
                Kişiselleştirilmiş günlük rota
              </p>
            </div>

            <div className="relative h-12 w-12 overflow-hidden rounded-xl">
              <Image
                src="/images/home/hero/hero-rome-final.webp"
                alt="Roma planı"
                fill
                sizes="48px"
                className="object-cover"
              />
            </div>
          </div>

          <div className="mt-3 flex items-center justify-between border-t border-border pt-2.5">
            <div>
              <p className="text-[9px] text-muted">
                09:00
              </p>

              <p className="text-[10px] font-semibold text-foreground">
                Colosseum
              </p>
            </div>

            <div>
              <p className="text-[9px] text-muted">
                11:00
              </p>

              <p className="text-[10px] font-semibold text-foreground">
                Roman Forum
              </p>
            </div>

            <div>
              <p className="text-[9px] text-muted">
                15:00
              </p>

              <p className="text-[10px] font-semibold text-foreground">
                Pantheon
              </p>
            </div>
          </div>
        </div>

        {/* MOBILE SMALL CARDS */}
        <HeroFloatingCard
          icon={Target}
          title="%94 Sana Uygun"
          className="bottom-[212px] left-[8%] z-20"
        />

        <HeroFloatingCard
          icon={Route}
          title="Rota Optimize Edildi"
          className="bottom-[18px] right-[5%] z-20"
        />
      </div>
    </>
  );
}