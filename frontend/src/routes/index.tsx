import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/') ({
    component: OverviewPage,
})

function OverviewPage() {
  return (
    <div className="p-6">
        <h1>Overview</h1>
        <p className="text-muted-foreground">Coming soon to a page near you.</p>
    </div>
  )
}