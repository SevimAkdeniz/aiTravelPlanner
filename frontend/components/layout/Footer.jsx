import Link from "next/link";
import {
  Mail,
  Globe2,
  Heart,
  Sparkles,
} from "lucide-react";

export default function Footer() {
  return (
    <footer className="px-4 pb-4 pt-14 sm:px-6 lg:px-8">
      <div className="mx-auto w-full rounded-[24px] border border-border bg-surface px-6 py-7 shadow-xs sm:px-8 lg:px-10">
        {/* TOP */}
        <div
          className="
            grid grid-cols-2
            gap-x-6 gap-y-10
            border-b border-border
            pb-8
            text-center

            md:grid-cols-2
            md:text-left

            lg:grid-cols-[1.5fr_1fr_1fr_1fr_1fr]
            lg:gap-x-10
          "
        >
          {/* BRAND */}
          <div className="col-span-2 mx-auto max-w-[320px] md:mx-0 lg:col-span-1">
            <Link
              href="/"
              className="flex items-center justify-center gap-3 md:justify-start"
            >
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-foreground text-primary shadow-sm">
                <Sparkles size={22} strokeWidth={2} />
              </div>

              <span className="text-[22px] font-bold tracking-[-0.03em] text-foreground">
                AI Travel Planner
              </span>
            </Link>

            <p className="mt-4 text-[14px] leading-6 text-muted">
              Yapay zekâ ile kişiselleştirilmiş seyahat
              planları oluşturmanın en akıllı yolu.
            </p>

            {/* SOCIAL */}
            <div className="mt-6 flex items-center justify-center gap-3 md:justify-start">
              <SocialLink href="#" label="Instagram">
                <span className="text-[15px] font-semibold">
                  ◎
                </span>
              </SocialLink>

              <SocialLink href="#" label="Facebook">
                <span className="text-[17px] font-semibold">
                  f
                </span>
              </SocialLink>

              <SocialLink href="#" label="X">
                <span className="text-[16px] font-medium">
                  𝕏
                </span>
              </SocialLink>

              <SocialLink
                href="mailto:hello@aitravelplanner.com"
                label="E-posta"
              >
                <Mail size={18} />
              </SocialLink>
            </div>
          </div>

          {/* KEŞFET */}
          <FooterColumn
            title="Keşfet"
            links={[
              ["Ana Sayfa", "/"],
              ["Bana Yer Öner", "/recommendations"],
              ["Seyahatimi Planla", "/planner"],
              ["Planlarım", "/plans"],
            ]}
          />

          {/* ÜRÜN */}
          <FooterColumn
            title="Ürün"
            links={[
              ["Nasıl Çalışır?", "#how-it-works"],
              ["Özellikler", "#features"],
              ["AI Önerileri", "/recommendations"],
              ["Planlarım", "/plans"],
            ]}
          />

          {/* DESTEK */}
          <FooterColumn
            title="Destek"
            links={[
              ["SSS", "/faq"],
              ["Yardım Merkezi", "/help"],
              ["İletişim", "/contact"],
              ["Geri Bildirim", "/feedback"],
            ]}
          />

          {/* ŞİRKET */}
          <FooterColumn
            title="Şirket"
            links={[
              ["Hakkımızda", "#about"],
              ["Kariyer", "/careers"],
              ["Gizlilik Politikası", "/privacy"],
              ["Kullanım Koşulları", "/terms"],
            ]}
          />
        </div>

        {/* BOTTOM */}
        <div
          className="
            flex flex-col
            items-center
            gap-4
            pt-6
            text-center
            text-[13px]
            text-muted

            md:flex-row
            md:justify-between
            md:text-left
          "
        >
          <p>
            © 2026 AI Travel Planner. Tüm hakları saklıdır.
          </p>

          <div className="flex items-center justify-center gap-2">
            <Heart
              size={17}
              strokeWidth={1.8}
              className="text-primary"
            />

            <span>
              Seyahat et, keşfet, ilham al.
            </span>
          </div>

          <div className="flex items-center justify-center gap-2">
            <Globe2
              size={17}
              strokeWidth={1.8}
            />

            <span>
              Dünyayı keşfetmenin en akıllı yolu.
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}

function FooterColumn({ title, links }) {
  return (
    <div className="text-center md:text-left">
      <h3 className="relative inline-block text-[14px] font-semibold text-foreground">
        {title}

        <span
          className="
            absolute
            -bottom-2
            left-1/2
            h-[2px]
            w-7
            -translate-x-1/2
            rounded-full
            bg-primary

            md:left-0
            md:translate-x-0
          "
        />
      </h3>

      <ul className="mt-5 space-y-2.5">
        {links.map(([label, href]) => (
          <li key={label}>
            <Link
              href={href}
              className="
                text-[13px]
                leading-5
                text-muted
                transition-colors
                hover:text-primary
              "
            >
              {label}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

function SocialLink({
  href,
  label,
  children,
}) {
  return (
    <Link
      href={href}
      aria-label={label}
      className="
        flex h-9 w-9
        items-center justify-center
        rounded-full
        border border-border
        bg-surface
        text-foreground
        shadow-sm
        transition-all duration-200
        hover:-translate-y-0.5
        hover:border-primary/40
        hover:text-primary
      "
    >
      {children}
    </Link>
  );
}