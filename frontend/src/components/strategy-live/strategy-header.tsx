import { Link } from "@tanstack/react-router";
import { ArrowLeft, Layers2, Pause, Play, Square, type LucideIcon } from "lucide-react";
import { useNow } from "@/hooks/use-now";
import { formatDuration } from "@/lib/format";
import {
  availableActions,
  type StrategyAction,
  type StrategySummary,
} from "@/lib/strategy-live";

type StrategyHeaderProps = {
  strategy: StrategySummary;
  /** Disables the controls while a previous action is still being sent */
  busy: boolean;
  onAction: (action: StrategyAction) => void;
};

const NEUTRAL = "border-border bg-card text-foreground hover:bg-accent";

/**
 * Label, icon and colors for each control. Destructive ones are outlined in their warning color.
 *
 * Brand purple uses the raw primary-* palette (like the sidebar does) because the semantic
 * `primary` token is currently overridden to near-black by the shadcn block in index.css.
 */
const ACTIONS: Record<StrategyAction, { label: string; Icon: LucideIcon; className: string }> = {
  start: {
    label: "Start",
    Icon: Play,
    className:
      "border-primary-600 bg-primary-600 text-white hover:border-primary-700 hover:bg-primary-700 dark:border-primary-500 dark:bg-primary-500",
  },
  resume: { label: "Resume", Icon: Play, className: NEUTRAL },
  pause: { label: "Pause", Icon: Pause, className: NEUTRAL },
  flatten: {
    label: "Flatten",
    Icon: Layers2,
    className: "border-warning bg-card text-warning-foreground hover:bg-warning-muted",
  },
  stop: {
    label: "Stop",
    Icon: Square,
    className: "border-loss bg-card text-loss-foreground hover:bg-loss-muted",
  },
};

export function StrategyHeader({ strategy, busy, onAction }: StrategyHeaderProps) {
  return (
    <header className="flex flex-col gap-[16px]">
      <Link
        to="/strategies"
        search={{ status: "all", page: 1 }}
        className="inline-flex items-center gap-[6px] self-start text-sm/[13px] text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="size-[12px]" aria-hidden="true" />
        All strategies
      </Link>

      <div className="flex flex-wrap items-center justify-between gap-[16px]">
        <div className="flex flex-col gap-[8px]">
          <h1 className="text-[26px]/[31px] font-semibold tracking-[-0.8px] text-foreground">
            {strategy.name}
          </h1>
          <StrategyMeta strategy={strategy} />
        </div>

        <div className="flex flex-wrap gap-[8px]">
          {availableActions(strategy.status).map((action) => {
            const { label, Icon, className } = ACTIONS[action];

            return (
              <button
                key={action}
                type="button"
                disabled={busy}
                onClick={() => onAction(action)}
                className={`inline-flex h-[36px] items-center gap-[8px] rounded-lg border px-[12px] text-md/[15px] font-medium transition-colors disabled:pointer-events-none disabled:opacity-50 ${className}`}
              >
                <Icon className="size-[14px]" aria-hidden="true" />
                {label}
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
}

/**
 * "ES · IBKR · v2.4.1-8f2a · Live for 3d 4h · Updated 2s ago"
 *
 * Kept as its own component because it re-renders every second to keep the
 * durations fresh, and the rest of the page shouldn't have to.
 */
function StrategyMeta({ strategy }: { strategy: StrategySummary }) {
  const now = useNow();

  const parts = [
    strategy.symbol,
    strategy.broker,
    strategy.version,
    runLabel(strategy, now),
    updatedLabel(strategy.updatedAt, now),
  ];

  return (
    <p className="text-sm/[13px] text-muted-foreground">{parts.join(" · ")}</p>
  );
}

function runLabel(strategy: StrategySummary, now: number): string {
  switch (strategy.status) {
    case "running":
      return strategy.startedAt
        ? `Live for ${formatDuration(now - Date.parse(strategy.startedAt))}`
        : "Live";
    case "paused":
      return "Paused";
    case "stopped":
      return "Stopped";
    case "idle":
      return "Not running";
  }
}

function updatedLabel(updatedAt: string, now: number): string {
  const elapsed = now - Date.parse(updatedAt);

  return elapsed < 1000 ? "Updated just now" : `Updated ${formatDuration(elapsed)} ago`;
}
