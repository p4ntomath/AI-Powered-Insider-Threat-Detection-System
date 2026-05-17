import { pipelineSteps } from "../data/dashboardData";

export default function InferencePipeline() {
  return (
    <section className="space-y-12">
      <h2 className="text-center font-['Hanken_Grotesk'] text-3xl font-semibold">
        Inference Pipeline
      </h2>

      <div className="relative flex flex-col items-center justify-between gap-8 md:flex-row md:gap-4">
        <div className="absolute left-0 top-6 -z-10 hidden h-px w-full bg-[#c6c6cd] md:block" />

        {pipelineSteps.map((step) => (
          <div
            key={step.number}
            className="flex max-w-[220px] flex-col items-center space-y-4 bg-[#f7f9fb] px-4 text-center"
          >
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-black font-bold text-white">
              {step.number}
            </div>

            <div className="space-y-1">
              <p className="font-bold text-[#191c1e]">{step.title}</p>
              <p className="text-xs leading-5 text-[#515f74]">
                {step.description}
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}