/**
 * Mock data for the Strategy Live Results page. The numbers match the Figma frame.
 *
 * Only strategy-live-api.ts imports this. Delete the file once the backend serves live results.
 *
 * The timeline is pinned to the moment the page first asks for data, so trades and the
 * curve stay put between refreshes while "Updated ... ago" keeps ticking like a live feed.
 */

import type { ActivityEvent, EquityPoint, Execution, StrategyAction, StrategyLiveResults, StrategyRunState, TimeRange, TradeSide } from './strategy-live';

const SECOND = 1000;
const MINUTE = 60 * SECOND;
const HOUR = 60 * MINUTE;
const DAY = 24 * HOUR;

const STARTING_EQUITY = 2_850_000;
const UNREALIZED_PNL = 8_234;
const REALIZED_PNL = 12_891;

/** Dollars above starting equity at each step of the curve, read off the Figma vector */
const EQUITY_OFFSETS = [
    0, 475, 125, 1825, 1600, 2675, 2075, 4775, 4025, 5000, 4525, 5975, 5725, 7575, 6600, 7325, 6475,
    8675, 8425, 10025, 9400, 10625, 9775, 11975, 11350, 12575, 11725, 13550, 13050, 15400, 14275, 14900, 13675, 15625,
    15275, 17225, 16350, 17950, 17350, 18425, 17100, 17950, 19425, 18700, 20525, 19775, 21125, 19775, 20775, 20275, 21125,
];

/** The same for the buy-and-hold benchmark */
const BENCHMARK_OFFSETS = [
    0, 550, 775, 475, 150, 850, 1550, 1325, 1100, 1725, 2350, 2200, 2025, 2975, 3900, 3275, 2650,
    2975, 3275, 3750, 4225, 3975, 3750, 4525, 5300, 5000, 4700, 5625, 6550, 6175, 5775, 6100, 6400, 6800,
    7200, 6800, 6400, 7275, 8125, 7800, 7500, 8275, 9050, 8675, 8275, 9225, 10150, 9925, 9700, 10150, 10625,
];

/** Which steps of the curve have a fill marked on them */
const EXECUTION_STEPS: Array<{ step: number; side: TradeSide }> = [
    { step: 7, side: 'buy' },
    { step: 16, side: 'sell' },
    { step: 19, side: 'buy' },
    { step: 32, side: 'sell' },
    { step: 35, side: 'buy' },
    { step: 47, side: 'sell' },
];

/**
 * How much history each range button covers. The curve keeps the same shape for every
 * range (it is mock data), only the dates under it change. 1W is 6 days so the axis reads
 * as 7 daily labels, like the design.
 */
const RANGE_SPAN: Record<TimeRange, number> = {
    '1D': DAY,
    '1W': 6 * DAY,
    '1M': 30 * DAY,
    '3M': 90 * DAY,
    ALL: 180 * DAY,
};

/** Recent activity, as "how long before the pinned moment" so it always looks recent */
const ACTIVITY: Array<{ ago: number } & (
    | { kind: 'trade'; side: TradeSide; price: number; quantity: number; realizedPnl: number | null }
    | { kind: 'skipped'; reason: string }
)> = [
    { ago: 2 * SECOND, kind: 'trade', side: 'buy', price: 5623.5, quantity: 142, realizedPnl: null },
    { ago: 15 * MINUTE + 4 * SECOND, kind: 'skipped', reason: 'Signal skipped – low volume' },
    { ago: 29 * MINUTE + 46 * SECOND, kind: 'trade', side: 'sell', price: 5620.25, quantity: 15, realizedPnl: -562.5 },
    { ago: 59 * MINUTE + 58 * SECOND, kind: 'trade', side: 'buy', price: 5621, quantity: 15, realizedPnl: null },
    { ago: 2 * DAY + 19 * HOUR + 14 * MINUTE + 22 * SECOND, kind: 'trade', side: 'sell', price: 5618.75, quantity: 20, realizedPnl: 3250 },
    { ago: 2 * DAY + 23 * HOUR + 44 * MINUTE + 53 * SECOND, kind: 'trade', side: 'buy', price: 5615.5, quantity: 20, realizedPnl: null },
    { ago: 3 * DAY + 20 * HOUR + 29 * MINUTE + 55 * SECOND, kind: 'trade', side: 'sell', price: 5612.25, quantity: 10, realizedPnl: 1225 },
    // Older than what the card shows by default, so "View all" has something to reveal
    { ago: 3 * DAY + 22 * HOUR + 5 * MINUTE + 12 * SECOND, kind: 'trade', side: 'buy', price: 5609.75, quantity: 10, realizedPnl: null },
    { ago: 4 * DAY + 1 * HOUR + 30 * MINUTE, kind: 'skipped', reason: 'Signal skipped – spread too wide' },
    { ago: 4 * DAY + 20 * HOUR + 40 * MINUTE + 31 * SECOND, kind: 'trade', side: 'sell', price: 5604.5, quantity: 12, realizedPnl: 2140 },
    { ago: 4 * DAY + 23 * HOUR + 10 * MINUTE + 8 * SECOND, kind: 'trade', side: 'buy', price: 5598.25, quantity: 12, realizedPnl: null },
];

/* ---------- Per-strategy state, so the control buttons do something ---------- */

type MockSession = {
    /** The moment the timeline is pinned to */
    anchor: number;
    status: StrategyRunState;
    flat: boolean;
};

const sessions = new Map<string, MockSession>();

function getSession(strategyId: string, now: number): MockSession {
    let session = sessions.get(strategyId);

    if (!session) {
        session = { anchor: now, status: 'running', flat: false };
        sessions.set(strategyId, session);
    }

    return session;
}

export function applyMockAction(strategyId: string, action: StrategyAction, now: number): void {
    const session = getSession(strategyId, now);

    switch (action) {
        case 'start':
        case 'resume':
            session.status = 'running';
            break;
        case 'pause':
            session.status = 'paused';
            break;
        case 'stop':
            session.status = 'stopped';
            break;
        case 'flatten':
            session.flat = true;
            break;
    }
}

/* ---------- Snapshot ---------- */

export function buildMockLiveResults(strategyId: string, range: TimeRange, now: number): StrategyLiveResults {
    const session = getSession(strategyId, now);
    const iso = (time: number) => new Date(time).toISOString();

    const lastStep = EQUITY_OFFSETS.length - 1;
    const stepTime = (step: number) => session.anchor - RANGE_SPAN[range] * (1 - step / lastStep);

    const points: EquityPoint[] = EQUITY_OFFSETS.map((offset, step) => ({
        time: iso(stepTime(step)),
        equity: STARTING_EQUITY + offset,
        benchmark: STARTING_EQUITY + BENCHMARK_OFFSETS[step],
    }));

    const executions: Execution[] = EXECUTION_STEPS.map(({ step, side }) => ({
        time: iso(stepTime(step)),
        side,
    }));

    const activity: ActivityEvent[] = ACTIVITY.map(({ ago, ...event }, index) => ({
        ...event,
        id: `mock-${index}`,
        time: iso(session.anchor - ago),
    }));

    return {
        strategy: {
            id: strategyId,
            name: 'MomentumAlpha',
            symbol: 'ES',
            broker: 'IBKR',
            version: 'v2.4.1-8f2a',
            status: session.status,
            startedAt: iso(session.anchor - (3 * DAY + 4 * HOUR + 10 * MINUTE)),
            updatedAt: iso(now),
        },
        performance: {
            totalPnl: UNREALIZED_PNL + REALIZED_PNL,
            totalReturn: (UNREALIZED_PNL + REALIZED_PNL) / STARTING_EQUITY,
            dailyPnl: 8_234,
            winRate: 0.64,
            winningTrades: 32,
            totalTrades: 50,
            maxDrawdown: -0.032,
            sharpe: 2.1,
        },
        equityCurve: {
            currency: 'USD',
            startingEquity: STARTING_EQUITY,
            benchmarkLabel: 'Buy & Hold ES',
            points,
            executions,
        },
        position: session.flat
            ? null
            : {
                  symbol: 'ES',
                  quantity: 142,
                  unit: 'contracts',
                  entryPrice: 5623.5,
                  markPrice: 5681.25,
                  unrealizedPnl: UNREALIZED_PNL,
                  stopLoss: 5580,
                  takeProfit: 5750,
              },
        // Flattening turns the open profit into realized profit
        realizedPnl: session.flat ? REALIZED_PNL + UNREALIZED_PNL : REALIZED_PNL,
        executionLatencyMs: 2.3,
        activity,
        venue: 'CME Globex',
    };
}
