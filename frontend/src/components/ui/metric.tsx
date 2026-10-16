type MetricProps = {
  label: string;
  value: string;
  tone?: "gain" | "loss";
  badge?: string;
  suffix?: string;
};

export function Metric({
  label,
  value,
  tone,
  badge,
  suffix,
}: MetricProps) {
    return (
    <div>
      <div className="label">{label}</div>

      <div
        className={`flex items-center gap-2 text-lg font-bold
          ${tone === "gain" ?
            "text-gain-foreground" :
            tone === "loss" ?
            "text-loss-foreground" :
            ""
          }
        `}
      >
        {value}

        {badge && (
          <span className="rounded-sm bg-gain-muted px-1.5 py-0.5 text-xs font-semibold text-gain-foreground">
            {badge}
          </span>
        )}

        {suffix && (
          <span className="rounded-sm bg-muted px-1.5 py-0.5 text-xs font-semibold text-muted-foreground">
            {suffix}
          </span>
        )}
      </div>
    </div>
  );
}