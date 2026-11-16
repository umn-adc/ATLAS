import { useId, useState } from "react";
import { formatMarketTime, formatNumber, formatPnl, minusSign, pnlTone } from "@/lib/format";
import {
  groupActivity,
  type ActivityEvent,
  type ActivityGroup,
  type SkippedSignalEvent,
  type TradeEvent,
} from "@/lib/strategy-live";
import { Card, CardTitle } from "./card";

type RecentActivityProps = {
  symbol: string;
  /** Trades and skipped signals, in any order */
  activity: ActivityEvent[];
  /** When the data was produced. Decides which rows count as "today" */
  asOf: string;
};

/** How many rows the card shows before "View all" */
const DEFAULT_ROWS = 7;

const SIDE_BADGE = {
  buy: "bg-gain-muted text-gain-foreground",
  sell: "bg-loss-muted text-loss-foreground",
} as const;

const TONE_CLASS = {
  gain: "text-gain-foreground",
  loss: "text-loss-foreground",
  neutral: "text-foreground",
} as const;

const HEADING = "h-[28px] pb-[16px] align-top text-xs/[12px] font-normal text-muted-foreground";

export function RecentActivity({ symbol, activity, asOf }: RecentActivityProps) {
  const titleId = useId();
  const [expanded, setExpanded] = useState(false);

  const newestFirst = [...activity].sort((a, b) => Date.parse(b.time) - Date.parse(a.time));
  const visible = expanded ? newestFirst : newestFirst.slice(0, DEFAULT_ROWS);
  const groups = groupActivity(visible, asOf);

  return (
    <Card labelledBy={titleId} className="flex flex-col gap-[16px]">
      <div className="flex items-center justify-between gap-[12px]">
        <CardTitle id={titleId}>Recent activity</CardTitle>
        <span className="text-xs/[12px] text-muted-foreground">{symbol} · All times ET</span>
      </div>

      {groups.length === 0 ? (
        <p className="py-[24px] text-sm/[13px] text-muted-foreground">
          No trades or signals yet. They show up here as the strategy runs.
        </p>
      ) : (
        <ActivityTable groups={groups} />
      )}

      {/* There is no trade history page yet, so "View all" opens the rest of the list in place */}
      {newestFirst.length > DEFAULT_ROWS && (
        <button
          type="button"
          aria-expanded={expanded}
          onClick={() => setExpanded(!expanded)}
          className="self-start text-sm/[13px] font-medium text-primary-600 hover:underline dark:text-primary-400"
        >
          {expanded ? "Show less" : "View all →"}
        </button>
      )}
    </Card>
  );
}

function ActivityTable({ groups }: { groups: ActivityGroup[] }) {
  return (
    // On a phone the table keeps its column widths and scrolls sideways inside the card
    <div className="overflow-x-auto">
      <table className="w-full min-w-[400px] table-fixed border-collapse text-left">
        <colgroup>
          <col className="w-[112px]" />
          <col className="w-[72px]" />
          <col />
          <col className="w-[48px]" />
          <col className="w-[96px]" />
        </colgroup>

        <thead>
          <tr className="border-b border-border">
            <th scope="col" className={HEADING}>Time</th>
            <th scope="col" className={HEADING}>Side</th>
            <th scope="col" className={`${HEADING} text-right`}>Price</th>
            <th scope="col" className={`${HEADING} text-right`}>Qty</th>
            <th scope="col" className={`${HEADING} text-right`}>P&L</th>
          </tr>
        </thead>

        {groups.map((group) => (
          <tbody key={group.label}>
            <tr>
              <th
                scope="rowgroup"
                colSpan={5}
                className="h-[24px] text-2xs/[11px] font-normal uppercase tracking-[0.5px] text-muted-foreground"
              >
                {group.label}
              </th>
            </tr>

            {group.events.map((event) =>
              event.kind === "trade" ? (
                <TradeRow key={event.id} trade={event} />
              ) : (
                <SkippedSignalRow key={event.id} signal={event} />
              ),
            )}
          </tbody>
        ))}
      </table>
    </div>
  );
}

function TradeRow({ trade }: { trade: TradeEvent }) {
  return (
    <tr className="border-b border-border text-sm/[13px]">
      <td className="h-[36px] text-muted-foreground">{formatMarketTime(trade.time)}</td>
      <td>
        <span
          className={`inline-block rounded-lg px-[8px] py-[4px] text-2xs/[11px] font-semibold uppercase ${SIDE_BADGE[trade.side]}`}
        >
          {trade.side}
        </span>
      </td>
      <td className="text-right text-foreground">{formatNumber(trade.price, 2)}</td>
      <td className="text-right text-foreground">{formatNumber(trade.quantity)}</td>
      <td className="text-right font-medium">
        {trade.realizedPnl === null ? (
          <span className="text-muted-foreground">—</span>
        ) : (
          <span className={TONE_CLASS[pnlTone(trade.realizedPnl)]}>
            {minusSign(formatPnl(trade.realizedPnl))}
          </span>
        )}
      </td>
    </tr>
  );
}

function SkippedSignalRow({ signal }: { signal: SkippedSignalEvent }) {
  return (
    <tr className="border-b border-border text-sm/[13px] text-muted-foreground">
      <td className="h-[32px]">{formatMarketTime(signal.time)}</td>
      <td colSpan={4} className="italic">
        {signal.reason}
      </td>
    </tr>
  );
}
