import type { ReactNode } from "react";

type CardProps = {
  /** id of the CardTitle inside, so screen readers announce the section by its title */
  labelledBy: string;
  className?: string;
  children: ReactNode;
};

/** The white bordered box every section of the live results page sits in */
export function Card({ labelledBy, className = "", children }: CardProps) {
  return (
    <section
      aria-labelledby={labelledBy}
      className={`rounded-lg border border-border bg-card p-[24px] ${className}`}
    >
      {children}
    </section>
  );
}

type CardTitleProps = {
  id: string;
  children: ReactNode;
};

/** Uppercase section title: "EQUITY CURVE", "CURRENT POSITION" */
export function CardTitle({ id, children }: CardTitleProps) {
  return (
    <h2
      id={id}
      className="text-sm/[13px] font-semibold uppercase tracking-[1px] text-muted-foreground"
    >
      {children}
    </h2>
  );
}
