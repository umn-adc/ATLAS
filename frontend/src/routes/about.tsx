import { createFileRoute } from '@tanstack/react-router'

// THIS IS A THROWAWAY FILE TO DEMONSTRATE ROUTING, DELETE OR MODIFY WHEN NEEDED

export const Route = createFileRoute('/about')({
  component: About,
})

function About() {
  return <div>Hello "/about"!</div>
}
