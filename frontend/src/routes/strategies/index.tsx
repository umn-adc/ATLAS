
import { createFileRoute } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'
import { Skeleton } from '../../components/ui/skeleton'
import { ErrorState } from '../../components/ui/error-state'

const STATUSES = ['all', 'active', 'archived'] as const

type StrategySearch = {
    status: (typeof STATUSES)[number]
    page: number
}

export const Route = createFileRoute('/strategies/')({
    // Never trust the URL: fall back to defaults on anything malformed
    validateSearch: (search: Record<string, unknown>): StrategySearch => {
        const status = STATUSES.find((s) => s === search.status) ?? 'all'
        const page = Number(search.page)
        return {
            status,
            page: Number.isInteger(page) && page > 0 ? page : 1,
        }
    },
    component: StrategiesPage,
})

function StrategiesPage() {
    const { status, page } = Route.useSearch()

    const { data, isPending, isError, error, refetch } = useQuery({
        queryKey: ['strategies', status, page],
        queryFn: async () => {
            const response = await fetch(
                `/api/strategies?status=${status}&page=${page}`
            )

            if (!response.ok) {
                throw new Error(`Failed to load strategies (${response.status})`)
            }

            return response.json()
        },
    })

    if (isPending) {
        return (
            <div className="space-y-4 p-6">
                <Skeleton className="h-8 w-48" />
                <Skeleton className="h-4 w-72" />
                <div className="space-y-3">
                    <Skeleton className="h-16 w-full" />
                    <Skeleton className="h-16 w-full" />
                    <Skeleton className="h-16 w-full" />
                </div>
            </div>
        )
    }

    if (isError) {
        return (
            <ErrorState
                title="Couldn't load strategies"
                message={
                    error instanceof Error
                        ? error.message
                        : 'An unexpected error occurred.'
                }
                onRetry={() => {
                    void refetch()
                }}
            />
        )
    }

    return <pre>{JSON.stringify(data, null, 2)}</pre>
}
