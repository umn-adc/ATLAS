import { useEffect, useId, useMemo, useRef, useState, type PointerEvent } from "react";
import { linePath, niceTicks, scaleLinear } from "@/lib/chart";
import { formatCurrency, formatMarketDate, formatMarketTime, formatNumber } from "@/lib/format";
import {
  TIME_RANGES,
  type EquityCurve as EquityCurveData,
  type EquityPoint,
  type TimeRange,
  type TradeSide,
} from "@/lib/strategy-live";
import { Card, CardTitle } from "./card";

type EquityCurveProps = {
  strategyName: string;
  curve: EquityCurveData;
  range: TimeRange;
  onRangeChange: (range: TimeRange) => void;
};

/* Chart layout in px, straight from the Figma frame */
const AXIS_WIDTH = 64; // value labels on the left
const AXIS_GAP = 16;
const PLOT_LEFT = AXIS_WIDTH + AXIS_GAP;
const LATEST_LABEL_GUTTER = 135; // room right of the line for the latest value label
const GRID_HEIGHT = 192; // top grid line to bottom grid line
const PLOT_HEIGHT = 208; // the area fill runs a little past the bottom grid line
const CHART_HEIGHT = 232; // plot + gap + time labels
const MARKER_OFFSET = 8; // how far a buy/sell arrow sits from the line

const DAY = 86_400_000;

export function EquityCurve({ strategyName, curve, range, onRangeChange }: EquityCurveProps) {
  const titleId = useId();

  return (
    <Card labelledBy={titleId} className="flex flex-col gap-[24px]">
      <div className="flex flex-wrap items-center justify-between gap-[12px]">
        <div className="flex items-center gap-[12px]">
          <CardTitle id={titleId}>Equity curve</CardTitle>
          <span className="text-xs/[12px] text-muted-foreground">{curve.currency}</span>
        </div>

        <div
          role="radiogroup"
          aria-label="Time range"
          className="flex gap-[4px] rounded-lg bg-muted p-[4px]"
        >
          {TIME_RANGES.map((option) => {
            const selected = option === range;
            const tone = selected
              ? "bg-primary-600 font-semibold text-white dark:bg-primary-500"
              : "text-muted-foreground hover:text-foreground";

            return (
              <button
                key={option}
                type="button"
                role="radio"
                aria-checked={selected}
                onClick={() => onRangeChange(option)}
                className={`h-[24px] w-[36px] rounded-lg text-xs/[12px] transition-colors ${tone}`}
              >
                {option}
              </button>
            );
          })}
        </div>
      </div>

      <Chart strategyName={strategyName} curve={curve} />

      <div className="flex flex-wrap items-center justify-between gap-x-[24px] gap-y-[8px] text-xs/[12px] text-muted-foreground">
        <ul className="flex flex-wrap items-center gap-x-[24px] gap-y-[8px]">
          <li className="flex items-center gap-[6px]">
            <span className="h-[2px] w-[16px] bg-primary-600 dark:bg-primary-400" />
            {strategyName}
          </li>
          <li className="flex items-center gap-[6px]">
            <span className="h-[2px] w-[16px] bg-muted-foreground" />
            {curve.benchmarkLabel}
          </li>
          <li className="flex items-center gap-[6px]">
            <span className="text-gain-foreground">▲</span>
            Buy
          </li>
          <li className="flex items-center gap-[6px]">
            <span className="text-loss-foreground">▼</span>
            Sell
          </li>
        </ul>

        <p>Starting equity {formatCurrency(curve.startingEquity)}</p>
      </div>
    </Card>
  );
}

/* ---------- The plot ---------- */

type Geometry = {
  /** Screen position of every point, same order as curve.points */
  equity: Array<[number, number]>;
  benchmark: Array<[number, number]>;
  valueTicks: Array<{ label: string; y: number }>;
  timeTicks: Array<{ label: string; x: number }>;
  markers: Array<{ side: TradeSide; x: number; y: number }>;
  plotRight: number;
};

function Chart({ strategyName, curve }: { strategyName: string; curve: EquityCurveData }) {
  const gradientId = useId();
  const [containerRef, width] = useElementWidth<HTMLDivElement>();
  const [hoverIndex, setHoverIndex] = useState<number | null>(null);

  // null until the container has been measured, or when there is nothing to draw yet
  const geometry = useMemo(() => buildGeometry(curve, width), [curve, width]);

  const { points } = curve;
  const hasHistory = points.length >= 2;

  function handlePointerMove(event: PointerEvent<SVGRectElement>) {
    const svg = event.currentTarget.ownerSVGElement;
    if (!geometry || !svg) return;

    const pointerX = event.clientX - svg.getBoundingClientRect().left;

    let nearest = 0;
    let nearestDistance = Infinity;
    geometry.equity.forEach(([x], index) => {
      const distance = Math.abs(x - pointerX);
      if (distance < nearestDistance) {
        nearest = index;
        nearestDistance = distance;
      }
    });

    setHoverIndex(nearest);
  }

  // The data can change under the pointer, so make sure the hovered point still exists
  const hovered = geometry && hoverIndex !== null && hoverIndex < points.length ? hoverIndex : null;

  return (
    <div ref={containerRef} className="relative" style={{ height: CHART_HEIGHT }}>
      {!hasHistory && (
        <p className="flex h-full items-center justify-center text-center text-sm/[13px] text-muted-foreground">
          No equity history yet. The curve appears once the strategy has run for a while.
        </p>
      )}

      {geometry && (
        <svg
          width={width}
          height={CHART_HEIGHT}
          role="img"
          aria-label={describeCurve(strategyName, curve)}
          className="block overflow-visible"
        >
          <defs>
            <linearGradient
              id={gradientId}
              x1="0"
              y1="0"
              x2="0"
              y2="1"
              className="text-lavender dark:text-primary-900/60"
            >
              <stop offset="0" stopColor="currentColor" stopOpacity="1" />
              <stop offset="1" stopColor="currentColor" stopOpacity="0.09" />
            </linearGradient>
          </defs>

          {geometry.valueTicks.map((tick) => (
            <g key={tick.label}>
              <line
                x1={PLOT_LEFT}
                x2={width}
                y1={tick.y}
                y2={tick.y}
                className="stroke-chart-grid"
                shapeRendering="crispEdges"
              />
              <text
                x={0}
                y={tick.y}
                dominantBaseline="central"
                className="fill-muted-foreground text-xs"
              >
                {tick.label}
              </text>
            </g>
          ))}

          {geometry.timeTicks.map((tick) => (
            <text
              key={tick.x}
              x={tick.x}
              y={CHART_HEIGHT - 2}
              className="fill-muted-foreground text-xs"
            >
              {tick.label}
            </text>
          ))}

          <path d={areaPath(geometry.equity)} fill={`url(#${gradientId})`} />

          <path
            d={linePath(geometry.benchmark)}
            fill="none"
            strokeWidth={1.5}
            strokeDasharray="5 5"
            className="stroke-muted-foreground"
          />

          <path
            d={linePath(geometry.equity)}
            fill="none"
            strokeWidth={2.5}
            strokeLinecap="round"
            strokeLinejoin="round"
            className="stroke-primary-600 dark:stroke-primary-400"
          />

          {geometry.markers.map((marker, index) => (
            <path
              key={index}
              d={markerPath(marker.side, marker.x, marker.y)}
              className={marker.side === "buy" ? "fill-gain" : "fill-loss"}
            />
          ))}

          <LatestValue
            x={geometry.equity[points.length - 1][0]}
            y={geometry.equity[points.length - 1][1]}
            label={formatNumber(points[points.length - 1].equity)}
          />

          {hovered !== null && (
            <g pointerEvents="none">
              <line
                x1={geometry.equity[hovered][0]}
                x2={geometry.equity[hovered][0]}
                y1={0}
                y2={PLOT_HEIGHT}
                className="stroke-muted-foreground"
                strokeDasharray="2 3"
              />
              <circle
                cx={geometry.benchmark[hovered][0]}
                cy={geometry.benchmark[hovered][1]}
                r={3}
                strokeWidth={1.5}
                className="fill-muted-foreground stroke-card"
              />
              <circle
                cx={geometry.equity[hovered][0]}
                cy={geometry.equity[hovered][1]}
                r={4}
                strokeWidth={2}
                className="fill-primary-600 stroke-card dark:fill-primary-400"
              />
            </g>
          )}

          {/* Invisible sheet over the plot that tracks the pointer */}
          <rect
            x={PLOT_LEFT}
            y={0}
            width={geometry.plotRight - PLOT_LEFT}
            height={PLOT_HEIGHT}
            fill="transparent"
            onPointerMove={handlePointerMove}
            onPointerLeave={() => setHoverIndex(null)}
          />
        </svg>
      )}

      {geometry && hovered !== null && (
        <PointTooltip
          point={points[hovered]}
          strategyName={strategyName}
          benchmarkLabel={curve.benchmarkLabel}
          x={geometry.equity[hovered][0]}
          chartWidth={width}
        />
      )}
    </div>
  );
}

/** One sentence for screen readers, since they can't see the line */
function describeCurve(strategyName: string, curve: EquityCurveData): string {
  const first = curve.points[0];
  const last = curve.points[curve.points.length - 1];

  return (
    `${strategyName} equity went from ${formatNumber(first.equity)} to ${formatNumber(last.equity)} ` +
    `between ${formatMarketDate(first.time)} and ${formatMarketDate(last.time)}. ` +
    `${curve.benchmarkLabel} ended at ${formatNumber(last.benchmark)}.`
  );
}

/** The dot at the end of the line and the label next to it */
function LatestValue({ x, y, label }: { x: number; y: number; label: string }) {
  const labelWidth = Math.max(84, label.length * 6 + 30);
  const labelLeft = x + 12;

  return (
    <g>
      <rect
        x={labelLeft}
        y={y - 12}
        width={labelWidth}
        height={24}
        rx={8}
        className="fill-lavender dark:fill-primary-900"
      />
      <text
        x={labelLeft + labelWidth / 2}
        y={y}
        textAnchor="middle"
        dominantBaseline="central"
        className="fill-primary-600 text-xs font-semibold dark:fill-lavender"
      >
        {label}
      </text>
      <circle
        cx={x}
        cy={y}
        r={4}
        strokeWidth={2}
        className="fill-primary-600 stroke-card dark:fill-primary-400"
      />
    </g>
  );
}

type PointTooltipProps = {
  point: EquityPoint;
  strategyName: string;
  benchmarkLabel: string;
  x: number;
  chartWidth: number;
};

function PointTooltip({ point, strategyName, benchmarkLabel, x, chartWidth }: PointTooltipProps) {
  // Open towards whichever side has more room
  const position = x < chartWidth / 2 ? { left: x + 12 } : { right: chartWidth - x + 12 };

  return (
    <div
      className="pointer-events-none absolute top-0 z-10 flex min-w-[168px] flex-col gap-[4px] rounded-md bg-tooltip px-[10px] py-[8px] text-xs/[14px] text-tooltip-foreground shadow-md"
      style={position}
    >
      <p className="font-medium">
        {formatMarketDate(point.time)} · {formatMarketTime(point.time, false)} ET
      </p>
      <p className="flex justify-between gap-[16px]">
        <span>{strategyName}</span>
        <span className="font-semibold">{formatNumber(point.equity)}</span>
      </p>
      <p className="flex justify-between gap-[16px]">
        <span>{benchmarkLabel}</span>
        <span className="font-semibold">{formatNumber(point.benchmark)}</span>
      </p>
    </div>
  );
}

/* ---------- Geometry ---------- */

/** Turns the data into screen coordinates for a chart of the given width */
function buildGeometry(curve: EquityCurveData, width: number): Geometry | null {
  const { points, executions } = curve;

  if (width === 0 || points.length < 2) return null;

  // On narrow screens the latest value label gets just enough room to fit
  const gutter = width < 560 ? 100 : LATEST_LABEL_GUTTER;
  const plotRight = Math.max(PLOT_LEFT + 40, width - gutter);

  const times = points.map((point) => Date.parse(point.time));
  const timeDomain: [number, number] = [times[0], times[times.length - 1]];
  const toX = (time: number) => scaleLinear(time, timeDomain, [PLOT_LEFT, plotRight]);

  let lowest = Infinity;
  let highest = -Infinity;
  for (const point of points) {
    lowest = Math.min(lowest, point.equity, point.benchmark);
    highest = Math.max(highest, point.equity, point.benchmark);
  }

  const ticks = niceTicks(lowest, highest);
  const valueDomain: [number, number] = [ticks[0], ticks[ticks.length - 1]];
  const toY = (value: number) => scaleLinear(value, valueDomain, [GRID_HEIGHT, 0]);

  const equity = points.map((point, index): [number, number] => [toX(times[index]), toY(point.equity)]);
  const benchmark = points.map((point, index): [number, number] => [toX(times[index]), toY(point.benchmark)]);

  const valueTicks = ticks.map((value) => ({ label: formatNumber(value), y: toY(value) }));

  // Fewer time labels when there is less room for them
  const plotWidth = plotRight - PLOT_LEFT;
  let segments = 2;
  if (plotWidth >= 600) {
    segments = 6;
  } else if (plotWidth >= 300) {
    segments = 3;
  }

  const span = timeDomain[1] - timeDomain[0];
  const step = span / segments;
  const timeTicks = [];
  for (let i = 0; i <= segments; i++) {
    const time = timeDomain[0] + i * step;
    timeTicks.push({ label: timeTickLabel(time, step, span), x: toX(time) });
  }

  const markers = [];
  for (const execution of executions) {
    const time = Date.parse(execution.time);
    if (time < timeDomain[0] || time > timeDomain[1]) continue;

    markers.push({
      side: execution.side,
      x: toX(time),
      y: toY(equityAt(points, times, time)),
    });
  }

  return { equity, benchmark, valueTicks, timeTicks, markers, plotRight };
}

/** Dates when ticks are a day or more apart, clock times when they are closer together */
function timeTickLabel(time: number, step: number, span: number): string {
  if (step >= DAY) return formatMarketDate(time);
  if (span <= DAY) return formatMarketTime(time, false);

  return `${formatMarketDate(time)} ${formatMarketTime(time, false)}`;
}

/** Equity at any moment, reading between the two nearest points */
function equityAt(points: EquityPoint[], times: number[], time: number): number {
  for (let i = 1; i < points.length; i++) {
    if (time <= times[i]) {
      const progress = (time - times[i - 1]) / (times[i] - times[i - 1]);

      return points[i - 1].equity + progress * (points[i].equity - points[i - 1].equity);
    }
  }

  return points[points.length - 1].equity;
}

/** The line, closed down to the bottom of the plot so it can be filled */
function areaPath(line: Array<[number, number]>): string {
  const firstX = line[0][0];
  const lastX = line[line.length - 1][0];

  return `${linePath(line)}L${lastX},${PLOT_HEIGHT}L${firstX},${PLOT_HEIGHT}Z`;
}

/** Buys are an up arrow under the line, sells a down arrow above it */
function markerPath(side: TradeSide, x: number, y: number): string {
  const direction = side === "buy" ? 1 : -1;
  const tip = y + direction * MARKER_OFFSET;
  const base = tip + direction * 8;

  return `M${x},${tip}L${x - 4.5},${base}L${x + 4.5},${base}Z`;
}

/** Tracks an element's width so the SVG can be redrawn to fit it */
function useElementWidth<T extends HTMLElement>() {
  const ref = useRef<T>(null);
  const [width, setWidth] = useState(0);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const observer = new ResizeObserver(([entry]) => {
      setWidth(Math.round(entry.contentRect.width));
    });
    observer.observe(element);

    return () => observer.disconnect();
  }, []);

  return [ref, width] as const;
}
