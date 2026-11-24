import { useId, type ReactNode } from "react";

type PanelProps = {
  title: string;
  children: ReactNode;
  badge?: ReactNode;
  actions?: ReactNode;
  padded?: boolean;
};

export function Panel({
  title,
  children,
  badge,
  actions,
  padded = false,
}: PanelProps) {
  const titleId = useId();

  return (
    <section
      aria-labelledby={titleId}
      className="overflow-hidden rounded-lg border border-border bg-card"
    >
      <div className="flex items-center gap-2 border-b border-border px-4 py-3">
        <h2 id={titleId} className="label">
          {title}
        </h2>

        {badge}

        <div className="ml-auto flex items-center gap-2">
          {actions}
        </div>
      </div>

      <div className={padded ? "p-4" : ""}>
        {children}
      </div>
    </section>
  );
}