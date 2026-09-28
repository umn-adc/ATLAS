import { createFileRoute } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'

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
    const { data, isPending } = useQuery({
        queryKey: ['strategies', status, page],
        queryFn: () =>
            fetch(`/api/strategies?status=${status}&page=${page}`).then((r)=>
            r.json()),
    })

    if (isPending) return <div>Loading...</div>
    return <pre>{JSON.stringify(data, null, 2)}</pre>
}
