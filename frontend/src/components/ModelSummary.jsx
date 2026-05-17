import { modelMetrics } from "../data/dashboardData";

export default function ModelSummary() {
  return (
    <section id="model-summary" className="space-y-6">
      <div className="flex items-center gap-3 border-b border-[#c6c6cd] pb-4">
        <span className="material-symbols-outlined text-black">analytics</span>
        <h2 className="font-['Hanken_Grotesk'] text-3xl font-semibold tracking-tight">
          Model Architecture: Random Forest Classifier
        </h2>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {modelMetrics.map((metric) => (
          <div
            key={metric.label}
            className="rounded-xl border border-[#c6c6cd] bg-white p-5 shadow-sm transition-shadow hover:shadow-md"
          >
            <p className="mb-1 mono text-xs font-semibold uppercase tracking-wider text-[#515f74]">
              {metric.label}
            </p>

            <p className="text-3xl font-bold text-black">{metric.value}</p>

            <p className="mt-2 text-xs leading-5 text-[#515f74]">
              {metric.description}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}