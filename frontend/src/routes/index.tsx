import { useQuery } from '@tanstack/react-query'
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/') ({
    component: OverviewPage,
})

function OverviewPage() {
  const { data, isPending, isError, error, refetch } = useQuery({
      queryKey: ['health'],
      queryFn: async () => {
          const response = await fetch(
              `/api/health`
          )

          if (!response.ok) {
              throw new Error(`Failed to load health status (${response.status})`)
          }

          return response.json()
      },
  })

  return (
    <div className="p-6">
        <h1>Overview</h1>
        <p className="text-muted-foreground">Coming soon to a page near you.</p>

        {isPending && <p>Loading...</p>}
        {isError && <p className="text-destructive">Error: {error.message}</p>}
        {data && (
            <div>
                <h2>Health Status</h2>
                <p>{JSON.stringify(data)}</p>
            </div>
        )}

        {data && <p>Boomzinghow</p>}
    </div>
  )
}