import { cn } from "cn"

type SegmentedControlOption = {
  label: string
  value: string
}

type SegmentedControlProps = {
  options: SegmentedControlOption[]
  value: string
  onChange: (value: string) => void
  className?: string
}

function SegmentedControl({
  options,
  value,
  onChange,
  className,
}: SegmentedControlProps) {
  return (
    <div
      role="radiogroup"
      className={cn(
        "inline-flex h-7 items-center gap-0.5 rounded-md border border-input bg-muted p-0.5",
        className
      )}
    >
      {options.map((option) => {
        const isSelected = option.value === value

        return (
          <button
            key={option.value}
            type="button"
            role="radio"
            aria-checked={isSelected}
            tabIndex={isSelected ? 0 : -1}
            onClick={() => onChange(option.value)}
            onKeyDown={(event) => {
              const currentIndex = options.findIndex(
                (item) => item.value === value
              )

              let nextIndex = currentIndex

              if (event.key === "ArrowRight" || event.key === "ArrowDown") {
                nextIndex = (currentIndex + 1) % options.length
              } else if (
                event.key === "ArrowLeft" ||
                event.key === "ArrowUp"
              ) {
                nextIndex =
                  (currentIndex - 1 + options.length) % options.length
              } else {
                return
              }

              event.preventDefault()
              onChange(options[nextIndex].value)

              const nextButton = event.currentTarget.parentElement
                ?.querySelectorAll<HTMLButtonElement>('[role="radio"]')[
                nextIndex
              ]

              nextButton?.focus()
            }}
            className={cn(
              "h-full rounded-sm px-2 text-[10px] font-medium transition-colors outline-none focus-visible:ring-2 focus-visible:ring-ring",
              isSelected
                ? "bg-primary text-primary-foreground shadow-sm"
                : "text-muted-foreground hover:text-foreground"
            )}
          >
            {option.label}
          </button>
        )
      })}
    </div>
  )
}

export { SegmentedControl }