import {
  Bot,
  LockKeyhole,
  ShieldCheck,
  Smile,
} from "lucide-react";

const ITEMS = [
  {
    icon: ShieldCheck,
    title: "Güvenilir Kaynaklar",
    description:
      "Güncel ve güvenilir verilerle öneriler sunarız.",
  },
  {
    icon: Bot,
    title: "AI Destekli",
    description:
      "Yapay zekâ ile kişiselleştirilmiş seyahat deneyimi.",
  },
  {
    icon: Smile,
    title: "%94 Eşleşme",
    description:
      "Öneriler tercihlerinle yüksek uyum sağlar.",
  },
  {
    icon: LockKeyhole,
    title: "Verilerin Güvende",
    description:
      "Kişisel verilerin gizliliği bizim önceliğimizdir.",
  },
];

export default function TrustBar() {
  return (
    <div
      className="
        mx-auto
        mt-10
        grid
        max-w-[1050px]
        gap-0
        overflow-hidden
        rounded-[20px]
        border
        border-border
        bg-surface
        shadow-sm

        sm:grid-cols-2

        lg:grid-cols-4
      "
    >
      {ITEMS.map(
        ({
          icon: Icon,
          title,
          description,
        }) => (
          <div
            key={title}
            className="
              flex
              gap-3
              border-b
              border-border
              p-5

              sm:[&:nth-child(odd)]:border-r

              lg:border-b-0
              lg:border-r
              lg:last:border-r-0
              lg:[&:nth-child(odd)]:border-r
            "
          >
            <div
              className="
                flex
                h-10
                w-10
                shrink-0
                items-center
                justify-center
                rounded-full
                bg-primary-soft
                text-primary
              "
            >
              <Icon
                size={19}
                strokeWidth={1.9}
              />
            </div>

            <div>
              <p className="text-[13px] font-semibold text-foreground">
                {title}
              </p>

              <p className="mt-1 text-[11px] leading-4.5 text-muted">
                {description}
              </p>
            </div>
          </div>
        ),
      )}
    </div>
  );
}