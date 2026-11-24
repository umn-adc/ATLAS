import * as React from "react"
import { Search } from "lucide-react"
import { Input } from "../../../components/ui/input"
import { cn } from "cn"

type SearchInputProps = Omit<
  React.ComponentProps<"input">,
  "value" | "onChange"
> & {
  value: string
  onChange: (value: string) => void
}

function SearchInput({
  value,
  onChange,
  className,
  placeholder = "Search...",
  ...props
}: SearchInputProps) {
  return (
    <div className="relative flex h-7 w-full items-center">
      <Search
        className="pointer-events-none absolute left-2.5 size-3.5 text-muted-foreground"
        aria-hidden="true"
      />

      <Input
        {...props}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        className={cn("h-7 rounded-md pl-8 text-[11px]", className)}
      />
    </div>
  )
}

export { SearchInput }