import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/monitoring/')({
  component: MonitoringPage,
})

function MonitoringPage() {
  return (
    <div className="p-6">
        <h1>Monitoring</h1>
        <p className="text-muted-foreground">Coming soon to a page near you.</p>
    </div>
  )
}