import { createFileRoute } from '@tanstack/react-router'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { CurrentPosition } from '../../../components/strategy-live/current-position'
import { EquityCurve } from '../../../components/strategy-live/equity-curve'
import { PerformanceOverview } from '../../../components/strategy-live/performance-overview'
import { RecentActivity } from '../../../components/strategy-live/recent-activity'
import { StrategyHeader } from '../../../components/strategy-live/strategy-header'
import { ErrorState } from '../../../components/ui/error-state'
import { Skeleton } from '../../../components/ui/skeleton'
import { DEFAULT_TIME_RANGE, TIME_RANGES, type StrategyAction, type TimeRange } from '@/lib/strategy-live'
import { fetchStrategyLiveResults, sendStrategyAction } from '@/lib/strategy-live-api'

/**
 * Strategy Live Results: how one deployed strategy is doing right now.
 * Design: Figma "ATLAS - Trading Platform", frame "Strategy Live Results".
 */

/** How often the page asks for fresh numbers */
const REFRESH_MS = 5000

type LiveSearch = {
    range?: TimeRange
}

export const Route = createFileRoute('/strategies/$id/live')({
    // Never trust the URL: anything that isn't a known range falls back to the default.
    // The default is left out of the URL so plain links stay clean.
    validateSearch: (search: Record<string, unknown>): LiveSearch => {
        const range = TIME_RANGES.find((option) => option === search.range)

        // Always return the `range` key, even as undefined. The router lays this object
        // over the raw URL search, so leaving the key out would let a bad value through.
        return { range: range === DEFAULT_TIME_RANGE ? undefined : range }
    },
    component: StrategyLivePage,
})

function StrategyLivePage() {
    const { id } = Route.useParams()
    const { range = DEFAULT_TIME_RANGE } = Route.useSearch()
    const navigate = Route.useNavigate()
    const queryClient = useQueryClient()

    const { data, isPending, isError, error, refetch } = useQuery({
        queryKey: ['strategy-live', id, range],
        queryFn: () => fetchStrategyLiveResults(id, range),
        refetchInterval: REFRESH_MS,
        // Keep showing the old chart while a new range loads, but never another strategy's data
        placeholderData: (previous, previousQuery) => {
            return previousQuery?.queryKey[1] === id ? previous : undefined
        },
    })

    const action = useMutation({
        mutationFn: (next: StrategyAction) => sendStrategyAction(id, next),
        onSettled: () => queryClient.invalidateQueries({ queryKey: ['strategy-live', id] }),
    })

    function changeRange(next: TimeRange) {
        void navigate({
            search: { range: next === DEFAULT_TIME_RANGE ? undefined : next },
            replace: true,
        })
    }

    if (isPending) {
        return <LiveResultsSkeleton />
    }

    if (isError) {
        return (
            <div className="p-[24px]">
                <ErrorState
                    title="Couldn't load live results"
                    message={
                        error instanceof Error
                            ? error.message
                            : 'An unexpected error occurred.'
                    }
                    onRetry={() => {
                        void refetch()
                    }}
                />
            </div>
        )
    }

    const { strategy, performance, equityCurve, position, realizedPnl, executionLatencyMs, activity, venue } = data

    return (
        <div className="mx-auto flex w-full max-w-[1127px] flex-col gap-[24px] p-[24px]">
            <StrategyHeader
                strategy={strategy}
                busy={action.isPending}
                onAction={(next) => action.mutate(next)}
            />

            {action.isError && (
                <p role="alert" className="text-sm/[13px] text-loss-foreground">
                    Couldn't {action.variables} the strategy. Check the connection and try again.
                </p>
            )}

            <PerformanceOverview performance={performance} asOf={strategy.updatedAt} />

            <EquityCurve
                strategyName={strategy.name}
                curve={equityCurve}
                range={range}
                onRangeChange={changeRange}
            />

            <div className="grid grid-cols-1 gap-[16px] lg:grid-cols-[minmax(0,384fr)_minmax(0,679fr)]">
                <CurrentPosition
                    position={position}
                    realizedPnl={realizedPnl}
                    executionLatencyMs={executionLatencyMs}
                />
                <RecentActivity
                    symbol={strategy.symbol}
                    activity={activity}
                    asOf={strategy.updatedAt}
                />
            </div>

            <footer className="flex flex-wrap justify-between gap-[8px] text-xs/[12px] text-muted-foreground">
                <p>All values in {equityCurve.currency} · Includes commissions and fees</p>
                <p>Live data · {venue}</p>
            </footer>
        </div>
    )
}

/** Grey boxes in the shape of the page, shown while the first load is in flight */
function LiveResultsSkeleton() {
    return (
        <div className="mx-auto flex w-full max-w-[1127px] flex-col gap-[24px] p-[24px]">
            <div className="flex flex-col gap-[16px]">
                <Skeleton className="h-[13px] w-[86px]" />
                <Skeleton className="h-[31px] w-[220px]" />
                <Skeleton className="h-[13px] w-[290px]" />
            </div>

            <div className="grid grid-cols-2 gap-[16px] lg:grid-cols-4 xl:grid-cols-[256fr_190fr_190fr_190fr_190fr]">
                <Skeleton className="col-span-2 h-[120px] lg:col-span-4 xl:col-span-1" />
                <Skeleton className="h-[120px]" />
                <Skeleton className="h-[120px]" />
                <Skeleton className="h-[120px]" />
                <Skeleton className="h-[120px]" />
            </div>

            <Skeleton className="h-[372px] w-full" />

            <div className="grid grid-cols-1 gap-[16px] lg:grid-cols-[minmax(0,384fr)_minmax(0,679fr)]">
                <Skeleton className="h-[430px]" />
                <Skeleton className="h-[430px]" />
            </div>
        </div>
    )
}
