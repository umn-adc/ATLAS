import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/data/')({
  component: DataPage,
})

function DataPage() {
  return (
    <div className="p-6">
        <h1>Data</h1>
        <p className="text-muted-foreground">Coming soon to a page near you.</p>
    </div>
  )
}