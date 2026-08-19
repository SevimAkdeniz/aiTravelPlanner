import {
  Compass,
  MapPin,
} from "lucide-react";

const ROUTE_COLOR = "#F5B000";

export default function ChoiceRouteDecoration() {
  return (
    <div
      className="
        pointer-events-none
        absolute
        inset-x-0
        top-[110px]
        hidden
        h-[230px]
        overflow-hidden
        lg:block
      "
      aria-hidden="true"
    >
      {/* LEFT ROUTE */}
      <svg
        viewBox="0 0 600 230"
        className="absolute left-0 top-0 h-full w-[40%]"
        fill="none"
        aria-hidden="true"
      >
        <path
          d="
            M -10 210
            C 70 190, 95 150, 75 110
            C 55 70, 85 35, 135 45
            C 180 54, 205 85, 240 72
            C 270 60, 295 52, 330 66
          "
          stroke={ROUTE_COLOR}
          strokeWidth="2"
          strokeLinecap="round"
          strokeDasharray="6 10"
        />
      </svg>

      {/* RIGHT ROUTE */}
      <svg
        viewBox="0 0 600 230"
        className="absolute right-0 top-0 h-full w-[40%]"
        fill="none"
        aria-hidden="true"
      >
        <path
          d="
            M 600 190
            C 540 180, 500 165, 475 138
            C 450 110, 470 76, 510 82
            C 548 88, 545 42, 510 44
            C 470 46, 440 50, 410 68
          "
          stroke={ROUTE_COLOR}
          strokeWidth="2"
          strokeLinecap="round"
          strokeDasharray="6 10"
        />
      </svg>

      {/* LEFT ICON */}
      <div
        className="
          absolute
          left-[14%]
          top-[8%]
          flex h-12 w-12
          items-center justify-center
          rounded-full
          border border-primary/20
          bg-background
          text-primary
          shadow-[0_8px_24px_rgba(23,32,51,0.10)]
        "
      >
        <MapPin
          size={22}
          strokeWidth={2}
        />
      </div>

      {/* RIGHT ICON */}
      <div
        className="
          absolute
          right-[14%]
          top-[8%]
          flex h-12 w-12
          items-center justify-center
          rounded-full
          border border-primary/20
          bg-background
          text-primary
          shadow-[0_8px_24px_rgba(23,32,51,0.10)]
        "
      >
        <Compass
          size={22}
          strokeWidth={2}
        />
      </div>
    </div>
  );
}