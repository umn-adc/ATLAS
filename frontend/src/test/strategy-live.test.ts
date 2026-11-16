import { describe, expect, it } from 'vitest';
import { linePath, niceTicks, scaleLinear } from '@/lib/chart';
import { availableActions, groupActivity, riskRange, type ActivityEvent, type Position } from '@/lib/strategy-live';
import { applyMockAction, buildMockLiveResults } from '@/lib/strategy-live.mock';

// The moment shown in the Figma frame: Oct 26 2026, 10:45:04 in New York
const NOW = Date.parse('2026-10-26T14:45:04Z');

function trade(id: string, time: string): ActivityEvent {
    return { kind: 'trade', id, time, side: 'buy', price: 100, quantity: 1, realizedPnl: null };
}

const LONG: Position = {
    symbol: 'ES',
    quantity: 142,
    unit: 'contracts',
    entryPrice: 5623.5,
    markPrice: 5681.25,
    unrealizedPnl: 8234,
    stopLoss: 5580,
    takeProfit: 5750,
};

describe('available actions', () => {
    it('should offer pause, flatten and stop while running', () => {
        expect(availableActions('running')).toEqual(['pause', 'flatten', 'stop']);
    });

    it('should offer resume instead of pause while paused', () => {
        expect(availableActions('paused')).toEqual(['resume', 'flatten', 'stop']);
    });

    it('should offer start and flatten once stopped', () => {
        expect(availableActions('stopped')).toEqual(['start', 'flatten']);
    });

    it('should only offer start when idle', () => {
        expect(availableActions('idle')).toEqual(['start']);
    });
});

describe('group activity', () => {
    it('should split today from everything earlier, newest first', () => {
        const groups = groupActivity(
            [
                trade('old', '2026-10-22T18:15:09Z'),
                trade('today-early', '2026-10-26T13:45:06Z'),
                trade('mid', '2026-10-23T19:30:42Z'),
                trade('today-late', '2026-10-26T14:45:02Z'),
            ],
            NOW,
        );

        expect(groups.map((group) => group.label)).toEqual(['Today · Oct 26', 'Oct 23 – Oct 22']);
        expect(groups[0].events.map((event) => event.id)).toEqual(['today-late', 'today-early']);
        expect(groups[1].events.map((event) => event.id)).toEqual(['mid', 'old']);
    });

    it('should use a single date when the earlier trades share a day', () => {
        const groups = groupActivity([trade('a', '2026-10-23T15:00:00Z'), trade('b', '2026-10-23T19:00:00Z')], NOW);

        expect(groups.map((group) => group.label)).toEqual(['Oct 23']);
    });

    it('should decide "today" in Eastern time, not UTC', () => {
        // 02:00 UTC on Oct 27 is still the evening of Oct 26 in New York
        const groups = groupActivity([trade('evening', '2026-10-27T02:00:00Z')], Date.parse('2026-10-27T03:00:00Z'));

        expect(groups.map((group) => group.label)).toEqual(['Today · Oct 26']);
    });

    it('should return no groups when there is no activity', () => {
        expect(groupActivity([], NOW)).toEqual([]);
    });
});

describe('risk range', () => {
    it('should place entry and mark between the stop and the target for a long', () => {
        const range = riskRange(LONG);

        expect(range?.lowEnd).toBe('stop');
        expect(range?.entry).toBeCloseTo(0.2559, 3);
        expect(range?.mark).toBeCloseTo(0.5956, 3);
    });

    it('should put the target on the left for a short', () => {
        const range = riskRange({ ...LONG, quantity: -142, stopLoss: 5750, takeProfit: 5580 });

        expect(range?.lowEnd).toBe('target');
        expect(range?.entry).toBeCloseTo(0.2559, 3);
    });

    it('should keep the mark on the bar when price runs past a limit', () => {
        expect(riskRange({ ...LONG, markPrice: 5900 })?.mark).toBe(1);
        expect(riskRange({ ...LONG, markPrice: 5500 })?.mark).toBe(0);
    });

    it('should return null when a limit is missing', () => {
        expect(riskRange({ ...LONG, stopLoss: null })).toBeNull();
        expect(riskRange({ ...LONG, takeProfit: null })).toBeNull();
    });
});

describe('nice ticks', () => {
    it('should give the axis from the design for the mock equity range', () => {
        expect(niceTicks(2850000, 2871125)).toEqual([2850000, 2860000, 2870000, 2880000]);
    });

    it('should cover the data on both ends', () => {
        const ticks = niceTicks(-37, 412);

        expect(ticks[0]).toBeLessThanOrEqual(-37);
        expect(ticks[ticks.length - 1]).toBeGreaterThanOrEqual(412);
    });

    it('should not carry floating point noise', () => {
        expect(niceTicks(0.1, 0.35)).toEqual([0.1, 0.2, 0.3, 0.4]);
    });

    it('should still give a range for a flat line', () => {
        const ticks = niceTicks(100, 100);

        expect(ticks.length).toBeGreaterThan(1);
        expect(ticks[0]).toBeLessThan(100);
        expect(ticks[ticks.length - 1]).toBeGreaterThan(100);
    });
});

describe('scale linear and line path', () => {
    it('should map a value from one range onto another', () => {
        expect(scaleLinear(5, [0, 10], [0, 200])).toBe(100);
    });

    it('should flip when the output range is upside down, like a y axis', () => {
        expect(scaleLinear(2880000, [2850000, 2880000], [192, 0])).toBe(0);
    });

    it('should build an SVG path through the points', () => {
        expect(linePath([[0, 0], [10, 5], [20, 2.5]])).toBe('M0,0L10,5L20,2.5');
    });
});

describe('mock live results', () => {
    it('should add up: total P&L is realized plus unrealized', () => {
        const results = buildMockLiveResults('adds-up', '1W', NOW);

        expect(results.performance.totalPnl).toBe(21125);
        expect(results.performance.totalPnl).toBe(results.realizedPnl + (results.position?.unrealizedPnl ?? 0));
    });

    it('should end the curve at starting equity plus total P&L', () => {
        const { equityCurve, performance } = buildMockLiveResults('curve', '1W', NOW);
        const last = equityCurve.points[equityCurve.points.length - 1];

        expect(last.equity).toBe(equityCurve.startingEquity + performance.totalPnl);
    });

    it('should keep trade times fixed between refreshes', () => {
        const first = buildMockLiveResults('stable', '1W', NOW);
        const later = buildMockLiveResults('stable', '1W', NOW + 5000);

        expect(later.activity[0].time).toBe(first.activity[0].time);
        expect(later.strategy.updatedAt).not.toBe(first.strategy.updatedAt);
    });

    it('should follow the control buttons', () => {
        applyMockAction('controls', 'pause', NOW);
        expect(buildMockLiveResults('controls', '1W', NOW).strategy.status).toBe('paused');

        applyMockAction('controls', 'flatten', NOW);
        const flat = buildMockLiveResults('controls', '1W', NOW);
        expect(flat.position).toBeNull();
        expect(flat.realizedPnl).toBe(21125);

        applyMockAction('controls', 'stop', NOW);
        expect(buildMockLiveResults('controls', '1W', NOW).strategy.status).toBe('stopped');
    });
});
