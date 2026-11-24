import type { ReactNode } from "react";
import { formatMarketDate, formatPercent, formatPnl, minusSign, pnlTone } from "@/lib/format";
import type { Performance } from "@/lib/strategy-live";

type PerformanceOverviewProps = {
  performance: Performance;
  /** When the numbers were produced, used for the "Today · Oct 26" caption */
  asOf: string;
};

const TONE_CLASS = {
  gain: "text-gain-foreground",
  loss: "text-loss-foreground",
  neutral: "text-foreground",
} as const;

/**
 * formatSignedPercent() in lib/format refuses anything above 100%, which a
 * long-running strategy's total return can exceed, so this one has no ceiling.
 */
function formatReturn(value: number): string {
  return Intl.NumberFormat("en-US", {
    style: "percent",
    maximumFractionDigits: 2,
    signDisplay: "exceptZero",
  }).format(value);
}

export function PerformanceOverview({ performance, asOf }: PerformanceOverviewProps) {
  const totalTone = TONE_CLASS[pnlTone(performance.totalPnl)];
  const dailyTone = TONE_CLASS[pnlTone(performance.dailyPnl)];

  return (
    <dl
      aria-label="Performance overview"
      className="grid grid-cols-2 gap-[16px] lg:grid-cols-4 xl:grid-cols-[256fr_190fr_190fr_190fr_190fr]"
    >
      <MetricCard
        label="Total P&L"
        className="col-span-2 lg:col-span-4 xl:col-span-1"
        caption="Since strategy launch"
      >
        <span className={`flex flex-wrap items-baseline gap-x-[8px] ${totalTone}`}>
          <span className="text-[30px]/[36px] font-semibold tracking-[-1px]">
            {minusSign(formatPnl(performance.totalPnl))}
          </span>
          <span className="text-md/[15px] font-medium">
            ({minusSign(formatReturn(performance.totalReturn))})
          </span>
        </span>
      </MetricCard>

      <MetricCard label="Daily P&L" caption={`Today · ${formatMarketDate(asOf)}`}>
        <MetricValue className={dailyTone}>
          {minusSign(formatPnl(performance.dailyPnl))}
        </MetricValue>
      </MetricCard>

      <MetricCard
        label="Win rate"
        caption={`${performance.winningTrades}/${performance.totalTrades} trades`}
      >
        <MetricValue>{formatPercent(performance.winRate, 0)}</MetricValue>
      </MetricCard>

      <MetricCard label="Max drawdown" caption="Peak to trough">
        <MetricValue>{minusSign(formatPercent(performance.maxDrawdown, 1))}</MetricValue>
      </MetricCard>

      <MetricCard label="Sharpe" caption="Risk-adjusted return">
        <MetricValue>{performance.sharpe.toFixed(2)}</MetricValue>
      </MetricCard>
    </dl>
  );
}

type MetricCardProps = {
  label: string;
  caption: string;
  className?: string;
  children: ReactNode;
};

function MetricCard({ label, caption, className = "", children }: MetricCardProps) {
  return (
    <div
      className={`flex flex-col gap-[10px] rounded-lg border border-border bg-card p-[16px] ${className}`}
    >
      <dt className="text-lg/[17px] uppercase tracking-[0.7px] text-muted-foreground">
        {label}
      </dt>
      <dd>{children}</dd>
      <dd className="text-xs/[12px] text-muted-foreground">{caption}</dd>
    </div>
  );
}

function MetricValue({ className = "text-foreground", children }: { className?: string; children: ReactNode }) {
  return (
    <span className={`block text-[24px]/[29px] font-semibold tracking-[-0.6px] ${className}`}>
      {children}
    </span>
  );
}
