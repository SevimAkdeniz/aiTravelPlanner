import Image from "next/image";
import Link from "next/link";
import {
  ArrowRight,
  CalendarDays,
  Clock3,
  Heart,
  MapPin,
  Route,
  Sparkles,
  Wallet,
} from "lucide-react";

const FEATURE_ICONS = {
  sparkle: Sparkles,
  wallet: Wallet,
  heart: Heart,
  calendar: CalendarDays,
  route: Route,
  clock: Clock3,
};

export default function ChoiceCard({
  variant = "recommend",
  title,
  description,
  image,
  href,
  buttonLabel,
  features = [],
}) {
  const isRecommend = variant === "recommend";

  return (
    <article
      className="
        group
        relative
        overflow-hidden
        rounded-[26px]
        border
        border-border
        bg-surface
        p-5
        shadow-card
        transition-all
        duration-300

        hover:-translate-y-1
        hover:shadow-card-hover

        sm:p-6
        lg:p-7
      "
    >
      {/* SOFT DECORATION */}
      <div
        className={`
          pointer-events-none
          absolute
          right-[5%]
          top-[12%]
          h-[210px]
          w-[210px]
          rounded-[45%]

          ${
            isRecommend
              ? "bg-primary-soft/70"
              : "bg-info-soft/80"
          }

          rotate-[-12deg]
          blur-[1px]
        `}
      />

      <div
        className="
          relative
          z-10
          grid
          gap-7

          md:grid-cols-[1fr_230px]
          md:items-center

          lg:grid-cols-[1fr_250px]
        "
      >
        {/* CONTENT */}
        <div>
          {/* ICON */}
          <div
            className={`
              flex
              h-14
              w-14
              items-center
              justify-center
              rounded-full

              ${
                isRecommend
                  ? "bg-primary text-white"
                  : "bg-info-soft text-info"
              }
            `}
          >
            {isRecommend ? (
              <MapPin
                size={27}
                strokeWidth={2.1}
              />
            ) : (
              <CalendarDays
                size={25}
                strokeWidth={2}
              />
            )}
          </div>

          {/* TITLE */}
          <h3
            className="
              mt-6
              text-[27px]
              font-bold
              leading-tight
              tracking-[-0.03em]
              text-foreground

              lg:text-[30px]
            "
          >
            {title}
          </h3>

          {/* DESCRIPTION */}
          <p
            className="
              mt-3
              max-w-[360px]
              text-[14px]
              leading-6
              text-muted

              sm:text-[15px]
            "
          >
            {description}
          </p>

          {/* FEATURES */}
          <ul className="mt-6 space-y-3">
            {features.map((feature) => {
              const Icon =
                FEATURE_ICONS[feature.icon] ||
                Sparkles;

              return (
                <li
                  key={feature.label}
                  className="
                    flex
                    items-center
                    gap-3
                    text-[13px]
                    font-medium
                    text-foreground

                    sm:text-[14px]
                  "
                >
                  <Icon
                    size={18}
                    strokeWidth={1.9}
                    className={
                      isRecommend
                        ? "text-primary"
                        : "text-info"
                    }
                  />

                  {feature.label}
                </li>
              );
            })}
          </ul>
        </div>

        {/* IMAGE */}
        <div
          className="
            relative
            mx-auto
            h-[240px]
            w-full
            max-w-[250px]
            overflow-hidden
            rounded-[24px]
            shadow-sm

            md:mx-0
            md:h-[260px]
          "
        >
          <Image
            src={image}
            alt={title}
            fill
            sizes="(max-width: 768px) 80vw, 250px"
            className="
              object-cover
              transition-transform
              duration-500
              group-hover:scale-[1.03]
            "
          />

          <div className="absolute inset-0 bg-gradient-to-t from-foreground/10 via-transparent to-transparent" />
        </div>
      </div>

      {/* BUTTON */}
      <Link
        href={href}
        className="
          relative
          z-10
          mt-7
          inline-flex
          h-[48px]
          w-full
          items-center
          justify-center
          gap-3
          rounded-[12px]
          bg-primary
          px-6
          text-[14px]
          font-semibold
          text-white
          shadow-button
          transition-all
          duration-300

          hover:-translate-y-0.5
          hover:bg-primary-hover
        "
      >
        {buttonLabel}

        <ArrowRight
          size={17}
          strokeWidth={2}
        />
      </Link>
    </article>
  );
}