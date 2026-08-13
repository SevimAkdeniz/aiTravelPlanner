import Link from "next/link";
import {
  ArrowRight,
  MapPin,
  Sparkles,
} from "lucide-react";

import HeroVisual from "./hero/HeroVisual";

export default function HeroSection() {
  return (
    <section
      className="
        relative
        overflow-hidden
        bg-background
        lg:min-h-[calc(100vh-84px)]
      "
    >
      {/* HERO VISUAL */}
      <HeroVisual />

      {/* CONTENT */}
      <div
        className="
          relative
          z-10
          mx-auto
          flex
          w-full
          items-center

          px-4
          pb-12
          pt-8

          sm:px-8
          sm:pt-10

          lg:min-h-[calc(100vh-84px)]
          lg:px-12
          lg:py-16

          xl:px-14
        "
      >
        <div
          className="
            mx-auto
            w-full
            max-w-[780px]
            text-center

            lg:mx-0
            lg:text-left
          "
        >
          {/* BADGE */}
          <div
            className="
              mb-7
              inline-flex
              items-center
              justify-center
              gap-2
              rounded-full
              bg-primary-soft
              px-4
              py-2
              text-[13px]
              font-medium
              text-primary

              sm:text-[14px]
            "
          >
            <Sparkles
              size={16}
              strokeWidth={2}
            />

            Yapay Zekâ Destekli Seyahat Planlama
          </div>

          {/* TITLE */}
          <h1
            className="
              mx-auto
              max-w-[760px]
              text-[40px]
              font-bold
              leading-[1.08]
              tracking-[-0.045em]
              text-foreground

              sm:text-[48px]

              md:text-[54px]

              lg:mx-0
              lg:text-[56px]

              xl:text-[62px]
            "
          >
            <span className="block lg:whitespace-nowrap">
              Seyahatini Yapay Zekâ ile
            </span>

            <span className="block">
              Sana{" "}
              <span className="text-primary">
                Özel Planla
              </span>
            </span>
          </h1>

          {/* DESCRIPTION */}
          <p
            className="
              mx-auto
              mt-7
              max-w-[590px]
              text-[15px]
              leading-8
              text-muted

              sm:text-[16px]

              md:text-[17px]

              lg:mx-0
            "
          >
            AI Travel Planner, tercihlerini anlar,
            bütçeni gözetir, sana en uygun yerleri
            önerir ve en iyi rotayı oluşturarak
            unutulmaz bir seyahat deneyimi sunar.
          </p>

          {/* CTA BUTTONS */}
          <div
            className="
              mx-auto
              mt-14
              flex
              w-full
              max-w-[450px]
              flex-col
              items-center
              justify-center
              gap-3

              sm:mt-16
              sm:flex-row

              lg:mx-0
              lg:mt-9
              lg:max-w-none
              lg:justify-start
              lg:gap-4
            "
          >
            {/* PRIMARY */}
            <Link
              href="/planner"
              className="
                inline-flex
                h-[54px]
                w-full
                items-center
                justify-center
                gap-3
                rounded-[14px]
                bg-primary
                px-7
                text-[15px]
                font-semibold
                text-white
                shadow-button
                transition-all
                duration-300

                hover:-translate-y-0.5
                hover:bg-primary-hover

                sm:w-auto

                lg:h-[56px]
                lg:text-[16px]
              "
            >
              <Sparkles size={17} />

              Seyahatimi Planla

              <ArrowRight size={16} />
            </Link>

            {/* SECONDARY */}
            <Link
              href="/recommendations"
              className="
                inline-flex
                h-[54px]
                w-full
                items-center
                justify-center
                gap-3
                rounded-[14px]
                border
                border-primary
                bg-surface
                px-7
                text-[15px]
                font-semibold
                text-foreground
                transition-all
                duration-300

                hover:-translate-y-0.5
                hover:bg-primary-soft

                sm:w-auto

                lg:h-[56px]
                lg:text-[16px]
              "
            >
              <MapPin
                size={18}
                className="text-primary"
              />

              Bana Yer Öner
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}