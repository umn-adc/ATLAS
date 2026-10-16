import { createFileRoute } from '@tanstack/react-router'

// THIS IS A THROWAWAY FILE TO DEMONSTRATE ROUTING, DELETE OR MODIFY WHEN NEEDED

export const Route = createFileRoute('/deployments/')({
  component: DeploymentsPage,
})

function DeploymentsPage() {
  return (
    <div className="p-6">
        <h1>Deployments</h1>
        <p className="text-muted-foreground">Coming soon to a page near you.</p>
    </div>
  )
}
