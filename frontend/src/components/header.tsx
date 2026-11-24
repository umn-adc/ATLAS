import { useEffect, useState } from "react";
import { Metric } from "./ui/metric";
import { SidebarTrigger } from "@/components/ui/sidebar";

const MOCK_ACCOUNT = {
  nav: "$2,847,392",
  dailyPnl: "+$14,729",
  dailyPnlBadge: "+0.52%",
  grossExposure: "68.4%",
  netExposure: "+12.3%",
  activeStrategies: "7",
  totalStrategies: "9",
};

function Clock() {
  const [now, setNow] = useState(() => new Date());

  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000);

    return () => clearInterval(id);
  }, []);

  return (
    <span className="text-sm font-medium tabular-nums text-muted-foreground">
      {now.toLocaleTimeString("en-US", {
        timeZone: "America/New_York",
        hour12: false,
      })}{" "}
      ET
    </span>
  );
}

export default function Header() {
  return (
    <header className="flex items-center justify-between border-b bg-card px-6 py-3">
      <div className="w-full flex items-center justify-start sm:gap-4 md:gap-8 lg:gap-16 xl:gap-24">
        <div className="rounded-[50%] bg-muted cursor-pointer">
          <SidebarTrigger className="p-4" />
        </div>

        <Metric
          label="NAV"
          value={MOCK_ACCOUNT.nav}
        />

        <Metric
          label="Daily P&L"
          value={MOCK_ACCOUNT.dailyPnl}
          tone="gain"
          badge={MOCK_ACCOUNT.dailyPnlBadge}
        />

        <Metric
          label="Gross Exposure"
          value={MOCK_ACCOUNT.grossExposure}
        />

        <Metric
          label="Net Exposure"
          value={MOCK_ACCOUNT.netExposure}
          tone="gain"
        />

        <Metric
          label="Active Strategies"
          value={MOCK_ACCOUNT.activeStrategies}
          suffix={`of ${MOCK_ACCOUNT.totalStrategies}`}
        />
      </div>

      <div className="w-full flex items-center justify-end gap-4">
        <div className="h-full flex items-center gap-2">
          <span className="size-2 rounded-full bg-gain animate-pulse" />
          <span className="label">LIVE</span>
        </div>

        <Clock />
      </div>
    </header>
  )
}