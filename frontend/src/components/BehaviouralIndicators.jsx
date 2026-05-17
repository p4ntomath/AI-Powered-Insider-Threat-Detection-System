import { indicators } from "../data/dashboardData";

export default function BehaviouralIndicators() {
  return (
    <section className="space-y-6">
      <h2 className="font-['Hanken_Grotesk'] text-3xl font-semibold">
        Key Behavioural Indicators
      </h2>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4 lg:grid-cols-5">
        {indicators.map((indicator) => (
          <div
            key={indicator.label}
            className="flex cursor-default flex-col items-center gap-3 rounded-xl border border-[#c6c6cd] bg-white p-4 text-center shadow-sm transition-colors hover:border-black"
          >
            <span className="material-symbols-outlined text-3xl text-[#515f74]">
              {indicator.icon}
            </span>

            <span className="mono text-[10px] font-semibold uppercase tracking-wider text-[#191c1e]">
              {indicator.label}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}