import { interpretabilityFeatures } from "../data/dashboardData";

export default function ExplainabilitySection() {
  return (
    <section className="space-y-8">
      <div className="space-y-2 text-center">
        <h2 className="font-['Hanken_Grotesk'] text-3xl font-semibold">
          Explainability Framework
        </h2>

        <p className="text-[#515f74]">
          Transparency in algorithmic decision-making for security compliance.
        </p>
      </div>

      <div className="rounded-2xl border border-[#c6c6cd] bg-white p-1 shadow-md">
        <div className="grid grid-cols-1 items-center gap-12 rounded-xl bg-white p-8 md:grid-cols-2">
          <div className="space-y-6">
            <div className="space-y-2">
              <h3 className="font-['Hanken_Grotesk'] text-3xl font-semibold">
                Model Interpretability
              </h3>

              <p className="leading-7 text-[#515f74]">
                The system uses feature importance and behavioural indicators to
                explain the model’s prediction in human-readable form.
              </p>
            </div>

            <div className="space-y-4">
              {interpretabilityFeatures.map((feature) => (
                <div key={feature.label} className="space-y-1">
                  <div className="flex justify-between mono text-[10px] font-bold uppercase tracking-wider text-[#515f74]">
                    <span>{feature.label}</span>
                    <span className="text-[#ba1a1a]">{feature.impact}</span>
                  </div>

                  <div className="h-2 w-full overflow-hidden rounded-full bg-[#f2f4f6]">
                    <div
                      className="h-full bg-[#ba1a1a]"
                      style={{ width: feature.width }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="flex aspect-square items-center justify-center rounded-lg border border-[#c6c6cd] bg-[#f2f4f6] p-8 shadow-inner">
            <div className="text-center">
              <span className="material-symbols-outlined text-6xl text-[#515f74]">
                monitoring
              </span>
              <p className="mt-4 font-semibold text-[#191c1e]">
                Feature Importance Visualisation
              </p>
              <p className="mt-2 text-sm leading-6 text-[#515f74]">
                Replace this placeholder with your generated feature importance
                chart if required.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}