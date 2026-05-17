import { testingExamples } from "../data/dashboardData";

export default function TestingExamples() {
  return (
    <section className="space-y-6">
      <h2 className="font-['Hanken_Grotesk'] text-3xl font-semibold">
        Testing Examples
      </h2>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        {testingExamples.map((example) => (
          <div
            key={example.type}
            className="space-y-3 rounded-xl border border-[#c6c6cd] bg-white p-6 shadow-sm"
          >
            <div className="flex items-center justify-between gap-4">
              <span
                className={`rounded border px-2 py-0.5 mono text-[10px] font-semibold uppercase tracking-wider ${example.badgeClass}`}
              >
                {example.type}
              </span>

              <span className="mono text-xs text-[#515f74]">
                CONFIDENCE: {example.confidence}
              </span>
            </div>

            <p className="leading-6 text-[#191c1e]">{example.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}