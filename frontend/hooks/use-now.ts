import { useEffect, useState } from 'react'

/**
 * Returns the current time and re-renders the component on a timer,
 * for labels like "Updated 2s ago" that go stale on their own.
 */
export function useNow(intervalMs = 1000): number {
    const [now, setNow] = useState(() => Date.now())

    useEffect(() => {
        const id = setInterval(() => setNow(Date.now()), intervalMs)

        return () => clearInterval(id)
    }, [intervalMs])

    return now
}
