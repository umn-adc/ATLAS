# ATLAS Frontend

React 19 + TypeScript + Vite, using [TanStack Router](https://tanstack.com/router) for file-based, type-safe routing and [TanStack Query](https://tanstack.com/query) for server state.

## Getting started

```bash
bun install
bun dev        # http://localhost:5173
```

Run the FastAPI backend on port 8000 alongside it. In dev, Vite proxies `/api/*` to `http://127.0.0.1:8000`, so call the backend with relative paths like `fetch('/api/strategies')`.

## Scripts

| Command         | What it does                     |
| --------------- | -------------------------------- |
| `bun dev`       | Start the dev server             |
| `bun run build` | Typecheck and build to `dist/`   |
| `bun run lint`  | Lint with oxlint                 |

Run `bun run lint && bun run build` before opening a PR.

## Routing

Routes are files in `src/routes/`. The file path is the URL:

| File                              | URL               |
| --------------------------------- | ----------------- |
| `src/routes/index.tsx`            | `/`               |
| `src/routes/about.tsx`            | `/about`          |
| `src/routes/strategies/index.tsx` | `/strategies`     |
| `src/routes/strategies/$id.tsx`   | `/strategies/:id` |

- `src/routes/__root.tsx` is the layout that wraps every page (header, footer, 404).
- Each route file must export `const Route = createFileRoute(...)`. The path string is filled in automatically, so don't edit it by hand.
- Use `<Link to="...">` for navigation. Links are type-checked, so a typo'd route fails the build.
- Keep filter/view state in the URL with `validateSearch` (see `src/routes/strategies/index.tsx` for the pattern).

### `src/routeTree.gen.ts`

This file is **generated** by the router plugin whenever the dev server or build runs, and it is **committed** so a fresh clone builds without extra steps. Don't edit it by hand, since your changes will be overwritten. If it looks stale, restart `bun dev`.
