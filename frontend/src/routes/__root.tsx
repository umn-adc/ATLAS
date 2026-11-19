import { createRootRoute, Outlet } from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools'
import AppShell from '../components/app-shell'

export const Route = createRootRoute({
	component: RootLayout,
	notFoundComponent: () => <div>Page not found</div>, // can change to fancy 404 page
	//create errorComponent later
})

function RootLayout() {
    return (
        <>
			<AppShell>
				<Outlet/> {/*This is the hole child that routes render into*/}
			</AppShell>
			{import.meta.env.DEV && <TanStackRouterDevtools position="bottom-right"/>}
        </>
    )
}