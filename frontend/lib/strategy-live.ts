/**
 * Types and pure helpers for the Strategy Live Results page (/strategies/$id/live).
 *
 * Design: Figma file "ATLAS - Trading Platform", frame "Strategy Live Results".
 * The types describe what the page needs from the backend. All times are ISO 8601 strings,
 * all money is in the account currency, and all rates are decimals (0.64 means 64%).
 */

import { formatMarketDate, marketDayKey } from './format';

/* ---------- Time range ---------- */

export const TIME_RANGES = ['1D', '1W', '1M', '3M', 'ALL'] as const;
export type TimeRange = (typeof TIME_RANGES)[number];
export const DEFAULT_TIME_RANGE: TimeRange = '1W';

/* ---------- Strategy state and controls ---------- */

/** Mirrors the "strategy-actions" component states in Figma */
export type StrategyRunState = 'idle' | 'running' | 'paused' | 'stopped';

export type StrategyAction = 'start' | 'pause' | 'resume' | 'flatten' | 'stop';

/**
 * Lists the controls to show for a strategy, in display order
 * @example availableActions('running') => ['pause', 'flatten', 'stop']
 */
export function availableActions(status: StrategyRunState): StrategyAction[] {
    switch (status) {
        case 'running':
            return ['pause', 'flatten', 'stop'];
        case 'paused':
            return ['resume', 'flatten', 'stop'];
        case 'stopped':
            return ['start', 'flatten'];
        case 'idle':
            return ['start'];
    }
}

/* ---------- Data model ---------- */

export type TradeSide = 'buy' | 'sell';

export type EquityPoint = {
    time: string;
    /** Account equity with the strategy running */
    equity: number;
    /** What the same starting equity would be worth in the benchmark */
    benchmark: number;
};

/** A fill to mark on the equity curve */
export type Execution = {
    time: string;
    side: TradeSide;
};

export type EquityCurve = {
    currency: string;
    startingEquity: number;
    benchmarkLabel: string;
    /** Oldest first */
    points: EquityPoint[];
    executions: Execution[];
};

export type Position = {
    symbol: string;
    /** Signed: positive is long, negative is short */
    quantity: number;
    /** What the quantity counts, e.g. "contracts" or "shares" */
    unit: string;
    entryPrice: number;
    markPrice: number;
    unrealizedPnl: number;
    stopLoss: number | null;
    takeProfit: number | null;
};

export type TradeEvent = {
    kind: 'trade';
    id: string;
    time: string;
    side: TradeSide;
    price: number;
    quantity: number;
    /** null while the trade is still open (nothing has been realized yet) */
    realizedPnl: number | null;
};

export type SkippedSignalEvent = {
    kind: 'skipped';
    id: string;
    time: string;
    reason: string;
};

export type ActivityEvent = TradeEvent | SkippedSignalEvent;

export type StrategySummary = {
    id: string;
    name: string;
    symbol: string;
    broker: string;
    version: string;
    status: StrategyRunState;
    /** When the current live run began, null if it has never run */
    startedAt: string | null;
    /** When this snapshot was produced */
    updatedAt: string;
};

export type Performance = {
    totalPnl: number;
    totalReturn: number;
    dailyPnl: number;
    winRate: number;
    winningTrades: number;
    totalTrades: number;
    /** Negative decimal, e.g. -0.032 */
    maxDrawdown: number;
    sharpe: number;
};

export type StrategyLiveResults = {
    strategy: StrategySummary;
    performance: Performance;
    equityCurve: EquityCurve;
    /** null when the strategy is flat */
    position: Position | null;
    realizedPnl: number;
    executionLatencyMs: number | null;
    /** Newest first */
    activity: ActivityEvent[];
    /** Where prices come from, e.g. "CME Globex" */
    venue: string;
};

/* ---------- Recent activity ---------- */

export type ActivityGroup = {
    label: string;
    events: ActivityEvent[];
};

/**
 * Splits activity into "today" and "everything earlier", newest first, the way the design shows it
 * @param events Activity in any order
 * @param now The current moment, used to decide what counts as today (Eastern time)
 * @example labels => ['Today · Oct 26', 'Oct 23 – Oct 22']
 */
export function groupActivity(events: ActivityEvent[], now: Date | string | number): ActivityGroup[] {
    const sorted = [...events].sort((a, b) => Date.parse(b.time) - Date.parse(a.time));
    const todayKey = marketDayKey(now);

    const today: ActivityEvent[] = [];
    const earlier: ActivityEvent[] = [];
    for (const event of sorted) {
        if (marketDayKey(event.time) === todayKey) {
            today.push(event);
        } else {
            earlier.push(event);
        }
    }

    const groups: ActivityGroup[] = [];

    if (today.length > 0) {
        groups.push({ label: `Today · ${formatMarketDate(now)}`, events: today });
    }

    if (earlier.length > 0) {
        const newest = formatMarketDate(earlier[0].time);
        const oldest = formatMarketDate(earlier[earlier.length - 1].time);
        groups.push({ label: newest === oldest ? newest : `${newest} – ${oldest}`, events: earlier });
    }

    return groups;
}

/* ---------- Stop-loss to take-profit bar ---------- */

export type RiskRange = {
    /** Which limit sits at the left (lower price) end of the bar: the stop for a long, the target for a short */
    lowEnd: 'stop' | 'target';
    /** Where the entry price sits along the bar, from 0 (left) to 1 (right) */
    entry: number;
    /** Where the mark price sits along the bar, kept inside 0 to 1 */
    mark: number;
};

/**
 * Works out where entry and mark sit between the stop-loss and the take-profit
 * @returns null when the position has no stop or no target, since there is no range to draw
 * @example riskRange({ stopLoss: 5580, takeProfit: 5750, entryPrice: 5623.5, markPrice: 5681.25, ... })
 *          => { lowEnd: 'stop', entry: 0.256, mark: 0.596 }
 */
export function riskRange(position: Position): RiskRange | null {
    const { stopLoss, takeProfit, entryPrice, markPrice } = position;

    if (stopLoss === null || takeProfit === null || stopLoss === takeProfit) return null;

    const low = Math.min(stopLoss, takeProfit);
    const high = Math.max(stopLoss, takeProfit);
    const along = (price: number) => Math.min(1, Math.max(0, (price - low) / (high - low)));

    return {
        lowEnd: stopLoss < takeProfit ? 'stop' : 'target',
        entry: along(entryPrice),
        mark: along(markPrice),
    };
}
