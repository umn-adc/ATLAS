/**
 * Small math helpers for hand-drawn SVG charts. No chart library needed for a line chart.
 */

/**
 * Picks round axis values that cover a range of data
 * @param min The smallest value in the data
 * @param max The largest value in the data
 * @param targetCount Roughly how many ticks to aim for
 * @returns Evenly spaced round numbers, the first at or below min and the last at or above max
 * @example niceTicks(2850000, 2871125) => [2850000, 2860000, 2870000, 2880000]
 */
export function niceTicks(min: number, max: number, targetCount = 4): number[] {
    if (!Number.isFinite(min) || !Number.isFinite(max)) return [0, 1];

    // A flat line still needs some height to be drawn against
    if (min === max) {
        const pad = min === 0 ? 1 : Math.abs(min) * 0.01;
        min -= pad;
        max += pad;
    }

    const roughStep = (max - min) / Math.max(1, targetCount - 1);
    const magnitude = 10 ** Math.floor(Math.log10(roughStep));
    const fraction = roughStep / magnitude;

    let niceFraction = 10;
    if (fraction <= 1) {
        niceFraction = 1;
    } else if (fraction <= 2) {
        niceFraction = 2;
    } else if (fraction <= 5) {
        niceFraction = 5;
    }

    const step = niceFraction * magnitude;
    const first = Math.floor(min / step) * step;
    const count = Math.round((Math.ceil(max / step) * step - first) / step);

    const ticks: number[] = [];
    for (let i = 0; i <= count; i++) {
        // toPrecision trims floating point noise like 0.30000000000000004
        ticks.push(Number((first + i * step).toPrecision(12)));
    }

    return ticks;
}

/**
 * Maps a value from one range onto another, like a ruler
 * @example scaleLinear(5, [0, 10], [0, 200]) => 100
 */
export function scaleLinear(value: number, domain: [number, number], range: [number, number]): number {
    const [d0, d1] = domain;
    const [r0, r1] = range;

    if (d0 === d1) return (r0 + r1) / 2;

    return r0 + ((value - d0) / (d1 - d0)) * (r1 - r0);
}

/**
 * Builds the `d` attribute for an SVG path that connects points with straight lines
 * @example linePath([[0, 0], [10, 5]]) => 'M0,0L10,5'
 */
export function linePath(points: Array<[number, number]>): string {
    return points.map(([x, y], index) => `${index === 0 ? 'M' : 'L'}${round(x)},${round(y)}`).join('');
}

function round(value: number): number {
    return Math.round(value * 100) / 100;
}
