import type { ReactNode } from "react"
import * as DropdownMenu from "@radix-ui/react-dropdown-menu"
import { Check, ChevronDown } from "lucide-react"
import { Button } from "../../../components/ui/button"

type FilterOption = {
  label: string
  value: string
}

type FilterSelectProps = {
  label: string
  value: string
  options: FilterOption[]
  onChange: (value: string) => void
  icon?: ReactNode
}

function FilterSelect({
  label,
  value,
  options,
  onChange,
  icon,
}: FilterSelectProps) {
  const selectedOption = options.find(
    (option) => option.value === value
  )

  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <Button
          variant="outline"
          size="sm"
          className="h-7 gap-1.5 rounded-md border-input px-2.5 text-[11px]"
        >
          {icon}
          <span>
            {label}: {selectedOption?.label ?? value}
          </span>
          <ChevronDown
            className="size-3 text-muted-foreground"
            aria-hidden="true"
          />
        </Button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content
          align="start"
          sideOffset={4}
          className="z-50 min-w-36 rounded-md border border-border bg-popover p-1 text-xs text-popover-foreground shadow-md"
        >
          <DropdownMenu.RadioGroup
            value={value}
            onValueChange={onChange}
          >
            {options.map((option) => (
              <DropdownMenu.RadioItem
                key={option.value}
                value={option.value}
                className="relative flex cursor-pointer items-center rounded-sm py-1.5 pr-8 pl-2 outline-none select-none hover:bg-accent focus:bg-accent"
              >
                {option.label}

                <DropdownMenu.ItemIndicator className="absolute right-2">
                  <Check className="size-3" />
                </DropdownMenu.ItemIndicator>
              </DropdownMenu.RadioItem>
            ))}
          </DropdownMenu.RadioGroup>
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  )
}

export { FilterSelect }