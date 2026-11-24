import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/backtesting/')({
  component: BacktestingPage,
})

function BacktestingPage() {
  return (
    <div className="p-6">
        <h1>Backtesting</h1>
        <p className="text-muted-foreground">Coming soon to a page near you.</p>
    </div>
  )
}