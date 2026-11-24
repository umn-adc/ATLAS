import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/risk/')({
  component: RiskPage,
})

function RiskPage() {
  return (
    <div className="p-6">
        <h1>Risk</h1>
        <p className="text-muted-foreground">Coming soon to a page near you.</p>
    </div>
  )
}
