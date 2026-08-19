import {
  Sparkles,
} from "lucide-react";
import CitySilhouette from "./main-choice/CitySilhouette";
import ChoiceCard from "./main-choice/ChoiceCard";
import ChoiceRouteDecoration from "./main-choice/ChoiceRouteDecoration";
import TrustBar from "./main-choice/TrustBar";

const CURRENT_IMAGE =
  "/images/home/hero/hero-rome-final.webp";

export default function MainChoiceSection() {
  return (
    <section
      className="
        relative
        overflow-hidden
        bg-background
        px-5
        py-16

        sm:px-8
        sm:py-20

        lg:px-10
        lg:py-24

        xl:px-12
      "
    >
      {/* ROUTE DECORATION */}
      <ChoiceRouteDecoration />

      <div
        className="
          relative
          z-10
          mx-auto
          w-full
          max-w-[1280px]
        "
      >
        {/* HEADER */}
        <div className="mx-auto max-w-[720px] text-center">
          <div
            className="
              inline-flex
              items-center
              gap-2
              rounded-full
              bg-primary-soft
              px-4
              py-2
              text-[13px]
              font-medium
              text-primary
            "
          >
            <Sparkles
              size={15}
              strokeWidth={2}
            />

            Sana Özel, Senin Rotaların
          </div>

          <h2
            className="
              mt-5
              text-[34px]
              font-bold
              leading-[1.12]
              tracking-[-0.04em]
              text-foreground

              sm:text-[42px]

              lg:text-[50px]
            "
          >
            Bugün nasıl yardımcı olalım?
          </h2>

          <p
            className="
              mx-auto
              mt-4
              max-w-[580px]
              text-[15px]
              leading-7
              text-muted

              sm:text-[16px]
            "
          >
            Keşfetmek istediğin yerleri bul,
            planını oluştur. Tercihlerine en uygun
            deneyimi birlikte tasarlayalım.
          </p>
        </div>

        {/* CHOICE CARDS */}
        <div
          className="
            mx-auto
            mt-12
            grid
            w-full
            max-w-[1240px]
            gap-6

            lg:grid-cols-2
            lg:gap-8
          "
        >
          <ChoiceCard
            variant="recommend"
            title="Bana Yer Öner"
            description="İlgi alanlarına, bütçene ve seyahat tarzına uygun en iyi yerleri keşfet."
            image={CURRENT_IMAGE}
            href="/recommendations"
            buttonLabel="Yer Önerilerini Keşfet"
            features={[
              {
                icon: "sparkle",
                label: "Kişiye özel öneriler",
              },
              {
                icon: "wallet",
                label: "Bütçene uygun seçenekler",
              },
              {
                icon: "heart",
                label: "İlgi alanlarına göre filtreleme",
              },
            ]}
          />

          <ChoiceCard
            variant="plan"
            title="Seyahatimi Planla"
            description="Tarihlerini, bütçeni ve tercihlerini gir, AI sana mükemmel planını oluştursun."
            image={CURRENT_IMAGE}
            href="/planner"
            buttonLabel="Planını Oluştur"
            features={[
              {
                icon: "calendar",
                label: "Gün gün planlama",
              },
              {
                icon: "route",
                label: "Rota optimizasyonu",
              },
              {
                icon: "clock",
                label: "Zaman ve mesafe dengesi",
              },
            ]}
          />
        </div>

        {/* TRUST BAR */}
        <TrustBar />
      </div>



      {/* SOFT BOTTOM DECORATION */}
      <div
        className="
          pointer-events-none
          absolute
          bottom-0
          left-1/2
          h-[110px]
          w-[120%]
          -translate-x-1/2
          bg-gradient-to-t
          from-primary-soft/40
          to-transparent
        "
      />
    </section>
  );
}