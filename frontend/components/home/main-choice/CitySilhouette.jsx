export default function CitySilhouette() {
  return (
    <div
      className="
        pointer-events-none
        absolute
        inset-x-0
        bottom-0
        h-[120px]
        overflow-hidden
        opacity-45

        sm:h-[140px]
        lg:h-[165px]
      "
      aria-hidden="true"
    >
      <svg
        viewBox="0 0 1440 180"
        preserveAspectRatio="none"
        className="h-full w-full"
        fill="none"
      >
        {/* SOFT GROUND */}
        <path
          d="
            M 0 150
            C 180 130, 340 138, 500 148
            C 690 158, 860 150, 1040 142
            C 1200 134, 1320 138, 1440 148
            L 1440 180
            L 0 180
            Z
          "
          fill="#F7D98A"
          opacity="0.32"
        />

        {/* LEFT BUILDINGS */}
        <path
          d="
            M 0 145
            L 36 145
            L 36 118
            L 48 118
            L 48 92
            L 58 92
            L 58 118
            L 76 118
            L 76 136

            L 110 136
            L 110 105
            L 124 105
            L 124 86
            L 134 86
            L 134 105
            L 150 105
            L 150 142

            L 188 142
            L 188 123
            L 212 123
            L 212 98
            L 224 98
            L 224 80
            L 234 80
            L 234 98
            L 248 98
            L 248 142
          "
          stroke="#E8B53D"
          strokeWidth="2"
          opacity="0.32"
        />

        {/* CENTER DOME */}
        <path
          d="
            M 340 146
            L 340 118
            L 366 118

            C 368 96, 382 82, 400 82
            C 418 82, 432 96, 434 118

            L 460 118
            L 460 146

            M 395 82
            L 395 66
            M 405 82
            L 405 66
            M 400 66
            L 400 56
          "
          stroke="#E8B53D"
          strokeWidth="2"
          opacity="0.36"
        />

        {/* CENTER BRIDGE */}
        <path
          d="
            M 520 148
            C 560 120, 605 120, 645 148

            M 645 148
            C 685 120, 730 120, 770 148
          "
          stroke="#E8B53D"
          strokeWidth="2"
          opacity="0.28"
        />

        {/* RIGHT BUILDINGS */}
        <path
          d="
            M 900 146
            L 900 112
            L 920 112
            L 920 96
            L 934 96
            L 934 112
            L 954 112
            L 954 146

            L 1000 146
            L 1000 124
            L 1022 124
            L 1022 102
            L 1032 102
            L 1032 124
            L 1050 124
            L 1050 146
          "
          stroke="#E8B53D"
          strokeWidth="2"
          opacity="0.30"
        />

        {/* COLOSSEUM-LIKE DECORATION */}
        <path
          d="
            M 1190 146
            L 1190 105

            C 1210 92, 1250 88, 1290 96
            C 1322 102, 1342 114, 1350 128

            L 1350 146

            M 1208 118
            L 1332 118

            M 1210 132
            L 1338 132
          "
          stroke="#E8B53D"
          strokeWidth="2"
          opacity="0.34"
        />

        {/* COLOSSEUM ARCHES */}
        <g
          stroke="#E8B53D"
          strokeWidth="1.5"
          opacity="0.28"
        >
          <path d="M 1210 146 Q 1218 128 1226 146" />
          <path d="M 1234 146 Q 1242 128 1250 146" />
          <path d="M 1258 146 Q 1266 128 1274 146" />
          <path d="M 1282 146 Q 1290 128 1298 146" />
          <path d="M 1306 146 Q 1314 128 1322 146" />
        </g>
      </svg>
    </div>
  );
}