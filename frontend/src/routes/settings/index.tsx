import { createFileRoute } from '@tanstack/react-router'
import { useTheme } from '../../../hooks/use-theme.ts'

export const Route = createFileRoute('/settings/')({
  component: SettingsPage,
})

function SettingsPage() {
  const { theme, setTheme } = useTheme();
  return (
    <div className="p-6">
        <h1>Settings</h1>
        <div className="text-lg"><br></br><br></br>
        <h2>Appearance</h2>
          <label><input type='radio' checked={theme=='light'} onClick={() => setTheme('light')}></input> Light</label><br></br>
          <label><input type='radio' checked={theme=='dark'} onClick={() => setTheme('dark')}></input> Dark</label><br></br>
          <label><input type='radio' checked={theme=='sys'} onClick={() => setTheme('sys')}></input> System</label>
        </div>
    </div>
  )
}
