import { createRootRoute, Outlet, Link } from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools'
import AppShell from '../components/app-shell'
import { ErrorState } from '../components/ui/error-state'
export const Route = createRootRoute({
    component: RootLayout,

    notFoundComponent: () => (
        <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 text-center">
            <h1 className="text-6xl font-bold">404</h1>
            <h2 className="text-xl font-semibold">Page not found</h2>
            <p className="text-muted-foreground">
                The page you're looking for doesn't exist.
            </p>
            <Link
                to="/"
                className="rounded-md bg-[#400DE7] px-4 py-2 text-white hover:opacity-90"
            >
                Back to Overview
            </Link>
        </div>
    ),

    errorComponent: ({ error, reset }) => (
        <ErrorState
            title="Something went wrong"
            message={error instanceof Error ? error.message : "An unexpected error occurred."}
            onRetry={reset}
        />
    ),
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