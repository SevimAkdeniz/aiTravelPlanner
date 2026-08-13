import Image from "next/image";
import { Star } from "lucide-react";

export default function RomeDayCard() {
  return (
    <div
      className="
        w-[248px]
        rounded-[18px]
        border border-white/75
        bg-white/95
        p-3
        shadow-[0_14px_30px_rgba(23,32,51,0.16)]
        backdrop-blur-xl
      "
    >
      {/* HEADER + THUMB */}
      <div className="grid grid-cols-[1fr_56px] items-start gap-2">
        <div>
          <h3 className="text-[12.5px] font-bold tracking-[-0.02em] text-foreground">
            Roma · Gün 1
          </h3>
        </div>

       <div className="relative mt-[8px] h-[66px] w-[56px] overflow-hidden rounded-[14px]">
  <Image
    src="/images/home/hero/hero-rome-final.webp"
    alt="Roma küçük önizleme"
    fill
    sizes="56px"
    className="object-cover"
  />
</div>
      </div>

      {/* LIST */}
      <div className="mt-1 border-t border-border pt-2">
        <div className="space-y-2">
          <div className="grid grid-cols-[36px_8px_1fr] items-start gap-2">
            <p className="text-[9.5px] text-foreground">09:00</p>
            <span className="mt-[4px] h-1.5 w-1.5 rounded-full bg-primary" />
            <div>
              <p className="text-[10.5px] font-semibold leading-4 text-foreground">
                Colosseum
              </p>
              <p className="mt-0.5 text-[9px] leading-3 text-muted">
                Tarihi keşfet
              </p>
            </div>
          </div>

          <div className="grid grid-cols-[36px_8px_1fr] items-start gap-2">
            <p className="text-[9.5px] text-foreground">11:00</p>
            <span className="mt-[4px] h-1.5 w-1.5 rounded-full bg-primary" />
            <div>
              <p className="text-[10.5px] font-semibold leading-4 text-foreground">
                Roman Forum
              </p>
              <p className="mt-0.5 text-[9px] leading-3 text-muted">
                Antik Roma'nın merkezi
              </p>
            </div>
          </div>

          <div className="grid grid-cols-[36px_8px_1fr] items-start gap-2">
            <p className="text-[9.5px] text-foreground">13:00</p>
            <span className="mt-[4px] h-1.5 w-1.5 rounded-full bg-primary" />
            <div>
              <p className="text-[10.5px] font-semibold leading-4 text-foreground">
                Öğle Yemeği
              </p>
              <p className="mt-0.5 text-[9px] leading-3 text-muted">
                Yerel lezzetleri dene
              </p>
            </div>
          </div>

          <div className="grid grid-cols-[36px_8px_1fr] items-start gap-2">
            <p className="text-[9.5px] text-foreground">15:00</p>
            <span className="mt-[4px] h-1.5 w-1.5 rounded-full bg-primary" />
            <div>
              <p className="text-[10.5px] font-semibold leading-4 text-foreground">
                Pantheon
              </p>
              <p className="mt-0.5 text-[9px] leading-3 text-muted">
                Etkileyici mimari
              </p>
            </div>
          </div>

          <div className="grid grid-cols-[36px_8px_1fr] items-start gap-2">
            <p className="text-[9.5px] text-foreground">17:00</p>
            <span className="mt-[4px] h-1.5 w-1.5 rounded-full bg-primary" />
            <div>
              <p className="text-[10.5px] font-semibold leading-4 text-foreground">
                Trevi Çeşmesi
              </p>
              <p className="mt-0.5 text-[9px] leading-3 text-muted">
                Dileklerini tut
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* FOOT */}
      <div className="mt-2.5 rounded-[12px] bg-[#FFF4D6] px-2.5 py-2">
        <div className="flex items-center gap-1.5 text-primary">
          <Star size={11} fill="currentColor" />
          <span className="text-[9.5px] font-medium">%94 Sana Uygun</span>
        </div>
      </div>
    </div>
  );
}