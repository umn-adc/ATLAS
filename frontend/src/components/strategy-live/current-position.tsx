import { useId } from "react";
import { formatNumber, formatPnl, formatSignedNumber, minusSign, pnlTone } from "@/lib/format";
import { riskRange, type Position, type RiskRange } from "@/lib/strategy-live";
import { Card, CardTitle } from "./card";

type CurrentPositionProps = {
  /** null when the strategy holds nothing */
  position: Position | null;
  realizedPnl: number;
  executionLatencyMs: number | null;
};

const TONE_CLASS = {
  gain: "text-gain-foreground",
  loss: "text-loss-foreground",
  neutral: "text-foreground",
} as const;

export function CurrentPosition({ position, realizedPnl, executionLatencyMs }: CurrentPositionProps) {
  const titleId = useId();
  const range = position ? riskRange(position) : null;

  return (
    <Card labelledBy={titleId} className="flex flex-col gap-[24px]">
      <CardTitle id={titleId}>Current position</CardTitle>

      {position ? (
        <>
          <p className="flex items-center gap-[8px]">
            <span className="text-2xl/[24px] font-semibold text-foreground">{position.symbol}</span>
            <span className="text-base/[16px] text-foreground">
              · {minusSign(formatSignedNumber(position.quantity))}
            </span>
            <span className="text-xs/[12px] text-muted-foreground">{position.unit}</span>
          </p>

          <dl className="grid grid-cols-2 gap-x-[24px]">
            <PositionMetric label="Entry" value={formatNumber(position.entryPrice, 2)} />
            <PositionMetric label="Mark" value={formatNumber(position.markPrice, 2)} />
          </dl>

          <dl className="grid grid-cols-2 gap-x-[24px] border-y border-border py-[16px]">
            <PnlMetric label="Unrealized P&L" value={position.unrealizedPnl} />
            <PnlMetric label="Realized P&L" value={realizedPnl} />
          </dl>

          {range ? (
            <RiskRangeBar position={position} range={range} />
          ) : (
            <RiskLimits position={position} lowEnd="stop" />
          )}
        </>
      ) : (
        <>
          <p className="flex items-baseline gap-[8px]">
            <span className="text-2xl/[24px] font-semibold text-foreground">Flat</span>
            <span className="text-xs/[12px] text-muted-foreground">no open position</span>
          </p>

          <dl className="border-y border-border py-[16px]">
            <PnlMetric label="Realized P&L" value={realizedPnl} />
          </dl>
        </>
      )}

      <dl className="flex items-baseline justify-between">
        <dt className="text-xs/[12px] text-muted-foreground">Execution latency</dt>
        <dd className="text-sm/[13px] text-foreground">
          {executionLatencyMs === null ? "—" : `${executionLatencyMs.toFixed(1)}ms`}
        </dd>
      </dl>
    </Card>
  );
}

function PositionMetric({ label, value, tone = "text-foreground" }: { label: string; value: string; tone?: string }) {
  return (
    <div className="flex flex-col gap-[8px]">
      <dt className="text-sm/[13px] text-muted-foreground">{label}</dt>
      <dd className={`text-2xl/[24px] font-medium tracking-[-0.5px] ${tone}`}>{value}</dd>
    </div>
  );
}

function PnlMetric({ label, value }: { label: string; value: number }) {
  return (
    <PositionMetric label={label} value={minusSign(formatPnl(value))} tone={TONE_CLASS[pnlTone(value)]} />
  );
}

/**
 * The bar from stop-loss to take-profit, showing where entry and the current mark sit.
 * Red runs from the stop to entry (losing ground), green from entry to the target.
 * For a short the bar is mirrored: the target is the lower price, so it sits on the left.
 */
function RiskRangeBar({ position, range }: { position: Position; range: RiskRange }) {
  const entryPercent = range.entry * 100;
  const markPercent = range.mark * 100;

  const stopOnLeft = range.lowEnd === "stop";
  const leftTone = stopOnLeft ? "bg-loss-border" : "bg-gain-border";
  const rightTone = stopOnLeft ? "bg-gain-border" : "bg-loss-border";

  return (
    <div className="flex flex-col gap-[12px]">
      {/* The label follows the dot, but stops at the edges so it never hangs outside the card */}
      <div className="relative h-[16px]">
        <span
          className="absolute top-0 -translate-x-1/2 whitespace-nowrap text-xs/[12px] font-medium text-foreground"
          style={{ left: `clamp(36px, ${markPercent}%, calc(100% - 36px))` }}
        >
          Mark {formatNumber(position.markPrice, 2)}
        </span>
      </div>

      <div className="relative h-[6px]" aria-hidden="true">
        <div
          className={`absolute inset-y-0 left-0 rounded-full ${leftTone}`}
          style={{ width: `${entryPercent}%` }}
        />
        <div
          className={`absolute inset-y-0 right-0 rounded-full ${rightTone}`}
          style={{ width: `${100 - entryPercent}%` }}
        />
        <div
          className="absolute top-[-3px] h-[12px] w-[2px] -translate-x-1/2 bg-muted-foreground"
          style={{ left: `${entryPercent}%` }}
        />
        <div
          className="absolute top-1/2 size-[14px] -translate-x-1/2 -translate-y-1/2 rounded-full border-[3px] border-card bg-primary-600 dark:bg-primary-400"
          style={{ left: `${markPercent}%` }}
        />
      </div>

      <RiskLimits position={position} lowEnd={range.lowEnd} />
    </div>
  );
}

/** Stop-loss and take-profit prices, with the lower-priced one on the left */
function RiskLimits({ position, lowEnd }: { position: Position; lowEnd: "stop" | "target" }) {
  const stop = { label: "Stop-loss", price: position.stopLoss, tone: "text-loss-foreground" };
  const target = { label: "Take-profit", price: position.takeProfit, tone: "text-gain-foreground" };

  const left = lowEnd === "stop" ? stop : target;
  const right = lowEnd === "stop" ? target : stop;

  return (
    <dl className="flex justify-between">
      <RiskLimit {...left} align="items-start" />
      <RiskLimit {...right} align="items-end" />
    </dl>
  );
}

type RiskLimitProps = {
  label: string;
  price: number | null;
  tone: string;
  align: "items-start" | "items-end";
};

function RiskLimit({ label, price, tone, align }: RiskLimitProps) {
  return (
    <div className={`flex flex-col gap-[4px] ${align}`}>
      <dt className="text-xs/[12px] text-muted-foreground">{label}</dt>
      <dd className={`text-sm/[13px] font-medium ${price === null ? "text-muted-foreground" : tone}`}>
        {price === null ? "—" : formatNumber(price, 2)}
      </dd>
    </div>
  );
}
