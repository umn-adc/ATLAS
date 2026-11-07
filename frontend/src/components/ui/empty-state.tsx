import type { ReactNode } from "react";

type EmptyStateProps = {
  icon?: ReactNode;
  title: string;
  description: string;
  action?: ReactNode;
};

export function EmptyState({
  icon,
  title,
  description,
  action,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 rounded-lg border border-dashed p-8 text-center">
      {icon && (
        <div className="text-muted-foreground">
          {icon}
        </div>
      )}

      <h2 className="text-lg font-semibold">{title}</h2>

      <p className="max-w-md text-sm text-muted-foreground">
        {description}
      </p>

      {action && <div>{action}</div>}
    </div>
  );
}