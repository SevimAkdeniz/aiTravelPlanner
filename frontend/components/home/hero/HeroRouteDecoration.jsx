import {
  Landmark,
  MapPin,
  Sparkles,
} from "lucide-react";

const ROUTE_COLOR = "#F5B000";
const ROUTE_SOFT = "#FFF1C7";

export default function HeroRouteDecoration() {
  return (
    <>
      {/* =====================================================
          DESKTOP
          BURAYA DOKUNMADIM
      ====================================================== */}
      <div
        className="
          pointer-events-none
          absolute
          left-[33%]
          top-[28%]
          z-[6]
          hidden
          h-[360px]
          w-[840px]
          lg:block
        "
      >
        {/* SOL ROTA */}
        <svg
          viewBox="0 0 840 360"
          className="absolute inset-0 h-full w-full overflow-visible"
          fill="none"
          aria-hidden="true"
        >
          <path
            d="
              M 78 270
              C 26 235, 20 180, 58 148
              C 94 118, 145 118, 188 138
              C 210 148, 232 147, 254 141
              C 268 137, 280 135, 292 135
            "
            stroke={ROUTE_COLOR}
            strokeWidth="2.8"
            strokeLinecap="round"
            strokeDasharray="7 10"
          />
        </svg>

        {/* SAĞ ÜST ÇIKIŞ */}
        <svg
          viewBox="0 0 840 360"
          className="absolute inset-0 h-full w-full overflow-visible"
          fill="none"
          aria-hidden="true"
        >
          <path
            d="
              M 845 160
              C 925 140, 930 20, 880 -42
            "
            stroke={ROUTE_COLOR}
            strokeWidth="2.8"
            strokeLinecap="round"
            strokeDasharray="7 10"
          />
        </svg>

        {/* LANDMARK */}
        <div
          className="
            absolute
            left-[148px]
            top-[118px]
            flex h-12 w-12
            items-center justify-center
            rounded-full
            border border-white/85
            bg-white/95
            shadow-[0_10px_26px_rgba(23,32,51,0.14)]
          "
        >
          <Landmark
            size={22}
            strokeWidth={2}
            style={{ color: ROUTE_COLOR }}
          />
        </div>

        {/* PIN */}
        <div
          className="
            absolute
            left-[54px]
            top-[246px]
            flex h-14 w-14
            items-center justify-center
            rounded-full
            shadow-[0_12px_30px_rgba(245,176,0,0.28)]
          "
          style={{ backgroundColor: ROUTE_COLOR }}
        >
          <MapPin
            size={27}
            strokeWidth={2.2}
            className="text-white"
          />
        </div>

        {/* AI ÖNERİSİ */}
        <div
          className="
            absolute
            left-[800px]
            top-[-90px]
            flex min-w-[160px]
            items-center gap-2.5
            rounded-[16px]
            border border-white/85
            bg-white/95
            px-4 py-3
            shadow-[0_8px_22px_rgba(23,32,51,0.10)]
            backdrop-blur-md
          "
        >
          <div
            className="
              flex h-7 w-7
              shrink-0
              items-center justify-center
              rounded-full
            "
            style={{ backgroundColor: ROUTE_SOFT }}
          >
            <Sparkles
              size={14}
              strokeWidth={2}
              style={{ color: ROUTE_COLOR }}
            />
          </div>

          <div>
            <p className="whitespace-nowrap text-[10.5px] font-semibold leading-none text-foreground">
              AI Önerisi
            </p>

            <p className="mt-1 whitespace-nowrap text-[8.5px] leading-4 text-muted">
              Akıllı rota eşleşmesi
            </p>
          </div>
        </div>
      </div>

      {/* =====================================================
          MOBILE
          SADECE BU KISIM YENİ
      ====================================================== */}
      <div
        className="
          pointer-events-none
          absolute
          inset-0
          z-[6]
          lg:hidden
        "
      >
{/* MOBİL SOL ROTA */}
<svg
  viewBox="0 0 390 520"
  preserveAspectRatio="none"
  className="absolute inset-0 h-full w-full"
  fill="none"
  aria-hidden="true"
>
  <path
    d="
      M 88 225
      C 116 190, 150 178, 184 186
      C 192 188, 198 192, 204 196
    "
    stroke={ROUTE_COLOR}
    strokeWidth="2.4"
    strokeLinecap="round"
    strokeDasharray="6 9"
  />
</svg>

{/* MOBİL SAĞ ROTA */}
<svg
  viewBox="0 0 390 520"
  preserveAspectRatio="none"
  className="absolute inset-0 h-full w-full"
  fill="none"
  aria-hidden="true"
>
  <path
    d="
      M 324 138
      C 334 130, 340 120, 344 108
    "
    stroke={ROUTE_COLOR}
    strokeWidth="2.4"
    strokeLinecap="round"
    strokeDasharray="6 9"
  />
</svg>

        {/* MOBİL PIN */}
        {/* MOBİL PIN */}
        <div
          className="
    absolute
    left-[17%]
    top-[40%]
    flex h-9 w-9
    items-center justify-center
    rounded-full
    shadow-[0_8px_20px_rgba(245,176,0,0.24)]
  "
          style={{ backgroundColor: ROUTE_COLOR }}
        >
          <MapPin
            size={18}
            strokeWidth={2.1}
            className="text-white"
          />
        </div>

        {/* MOBİL LANDMARK */}
        <div
          className="
    absolute
    left-[39%]
    top-[31%]
    flex h-9 w-9
    items-center justify-center
    rounded-full
    border border-white/85
    bg-white/95
    shadow-[0_8px_18px_rgba(23,32,51,0.11)]
  "
        >
          <Landmark
            size={16}
            strokeWidth={2}
            style={{ color: ROUTE_COLOR }}
          />
        </div>

        {/* MOBİL AI ÖNERİSİ */}
        <div
          className="
            absolute
            right-[5%]
            top-[12%]
            flex items-center gap-2
            rounded-[14px]
            border border-white/85
            bg-white/95
            px-3 py-2.5
            shadow-[0_8px_20px_rgba(23,32,51,0.10)]
            backdrop-blur-md
          "
        >
          <div
            className="
              flex h-6 w-6
              shrink-0
              items-center justify-center
              rounded-full
            "
            style={{ backgroundColor: ROUTE_SOFT }}
          >
            <Sparkles
              size={12}
              strokeWidth={2}
              style={{ color: ROUTE_COLOR }}
            />
          </div>

          <div>
            <p className="whitespace-nowrap text-[9.5px] font-semibold leading-none text-foreground">
              AI Önerisi
            </p>

            <p className="mt-1 whitespace-nowrap text-[7.5px] text-muted">
              Akıllı rota eşleşmesi
            </p>
          </div>
        </div>
      </div>
    </>
  );
}