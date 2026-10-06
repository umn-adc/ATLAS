import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/settings/')({
  component: SettingsPage,
})

function SettingsPage() {
  return (
    <div className="p-6">
        <h1>Settings</h1>
        <p className="text-muted-foreground">Coming soon to a page near you.</p>
    </div>
  )
}
