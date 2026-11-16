/**
 * Data access for the Strategy Live Results page.
 *
 * The backend has no live results endpoints yet, so both functions answer from mock data.
 * This file is the only place that knows that. Once the endpoints exist, replace each body
 * with the fetch call in its comment and delete strategy-live.mock.ts. The page and its
 * components only depend on the types in strategy-live.ts.
 */

import { applyMockAction, buildMockLiveResults } from './strategy-live.mock';
import type { StrategyAction, StrategyLiveResults, TimeRange } from './strategy-live';

/** Loads everything the page shows for one strategy */
export async function fetchStrategyLiveResults(strategyId: string, range: TimeRange): Promise<StrategyLiveResults> {
    // const response = await fetch(`/api/strategies/${strategyId}/live?range=${range}`);
    // if (!response.ok) {
    //     throw new Error(`Failed to load live results (${response.status})`);
    // }
    // return response.json();

    return buildMockLiveResults(strategyId, range, Date.now());
}

/** Asks the backend to start, pause, resume, flatten or stop a strategy */
export async function sendStrategyAction(strategyId: string, action: StrategyAction): Promise<void> {
    // const response = await fetch(`/api/strategies/${strategyId}/actions`, {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({ action }),
    // });
    // if (!response.ok) {
    //     throw new Error(`Failed to ${action} strategy (${response.status})`);
    // }

    applyMockAction(strategyId, action, Date.now());
}
