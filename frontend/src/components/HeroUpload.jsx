export default function HeroUpload() {
  return (
    <section className="grid grid-cols-1 gap-8 lg:grid-cols-2">
      <div className="space-y-6">
        <h1 className="max-w-2xl font-['Hanken_Grotesk'] text-4xl font-bold leading-tight tracking-tight text-[#191c1e] md:text-5xl">
          AI-Powered Insider Threat Detection System
        </h1>

        <p className="max-w-xl text-base leading-7 text-[#515f74]">
          Deploying behavioural analytics to identify high-risk internal
          activity before data breaches occur. Upload employee records for
          immediate predictive analysis.
        </p>

        <label className="group flex cursor-pointer flex-col items-center justify-center space-y-4 rounded-xl border-2 border-dashed border-[#c6c6cd] bg-white p-8 text-center shadow-sm transition-colors hover:border-black">
          <span className="material-symbols-outlined text-4xl text-black">
            upload_file
          </span>

          <div>
            <p className="text-xl font-semibold">
              Upload employee behavioural records
            </p>
            <p className="text-sm text-[#515f74]">
              Drag and drop CSV files here or click to browse
            </p>
          </div>

          <input type="file" accept=".csv" className="hidden" />
        </label>
      </div>

      <div className="glass-panel space-y-4 rounded-xl border-l-4 border-l-[#ba1a1a] p-6 shadow-sm">
        <div className="flex items-start justify-between gap-4">
          <div>
            <span className="rounded border border-[#ba1a1a]/50 bg-[#ffdad6] px-2 py-1 mono text-[10px] font-semibold uppercase tracking-wide text-[#93000a]">
              High Risk Level
            </span>

            <h3 className="mt-2 text-xl font-semibold">
              Example Prediction Result
            </h3>
          </div>

          <div className="text-right mono text-xs">
            <p className="font-bold text-black">CONFIDENCE: 94.2%</p>
          </div>
        </div>

        <div className="rounded border border-[#c6c6cd] bg-[#f2f4f6] p-4">
          <p className="mb-2 mono text-[10px] uppercase tracking-wider text-[#515f74]">
            Behavioural Explanation
          </p>

          <p className="leading-relaxed text-[#191c1e] italic">
            “Unusual behavioural activity detected, including off-hours
            printing, file burning activity, and travel-related indicators. Risk
            profile matches patterns of potential unauthorised data activity.”
          </p>
        </div>

        <div className="grid grid-cols-3 gap-2">
          <div className="h-1 overflow-hidden rounded bg-[#eceef0]">
            <div className="h-full w-full bg-[#ba1a1a]" />
          </div>
          <div className="h-1 overflow-hidden rounded bg-[#eceef0]">
            <div className="h-full w-full bg-[#ba1a1a]" />
          </div>
          <div className="h-1 overflow-hidden rounded bg-[#eceef0]">
            <div className="h-full w-1/2 bg-[#ba1a1a]" />
          </div>
        </div>
      </div>
    </section>
  );
}