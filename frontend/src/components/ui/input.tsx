import * as React from "react"

import { cn } from "@/lib/utils"

function Input({ className, type, ...props }: React.ComponentProps<"input">) {
  return (
    <input
      type={type}
      data-slot="input"
      className={cn(
        "file:text-foreground placeholder:text-muted-foreground/50 selection:bg-accent/20 selection:text-foreground h-10 w-full min-w-0 rounded-xl border border-border/60 bg-background px-4 py-2 text-sm font-light shadow-xs transition-all duration-200 outline-none file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-40",
        "focus-visible:border-accent/50 focus-visible:ring-2 focus-visible:ring-accent/20",
        "aria-invalid:ring-destructive/30 aria-invalid:border-destructive/50",
        className
      )}
      {...props}
    />
  )
}

export { Input }
