export default function HeroFloatingCard({
  icon: Icon,
  title,
  subtitle,
  className = "",
}) {
  return (
    <div
      className={`
        absolute
        flex items-center gap-1.5
        rounded-[14px]
        border border-white/80
        bg-white/94
        px-2 py-1.5
        shadow-[0_6px_16px_rgba(23,32,51,0.10)]
        backdrop-blur-md
        ${className}
      `}
    >
      <div className="flex h-5.5 w-5.5 shrink-0 items-center justify-center rounded-full bg-primary-soft text-primary">
        <Icon size={11} strokeWidth={2} />
      </div>

      <div>
        <p className="text-[9px] font-semibold leading-none text-foreground">
          {title}
        </p>

        {subtitle && (
          <p className="mt-0.5 text-[7.5px] leading-3 text-muted">
            {subtitle}
          </p>
        )}
      </div>
    </div>
  );
}