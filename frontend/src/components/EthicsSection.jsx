export default function EthicsSection() {
  return (
    <section className="space-y-6 rounded-xl border border-[#c6c6cd] bg-[#f2f4f6] p-8">
      <div className="flex items-center gap-3">
        <span className="material-symbols-outlined text-[#ba1a1a]">gavel</span>
        <h2 className="font-['Hanken_Grotesk'] text-3xl font-semibold">
          Ethics & Protocol Limitations
        </h2>
      </div>

      <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
        <div className="space-y-4">
          <p className="text-lg font-bold text-[#191c1e]">
            Prototype Disclaimer
          </p>

          <p className="leading-7 text-[#515f74]">
            This system is an academic prototype. Predictions should support
            further human investigation and should not be treated as proof of
            malicious intent.
          </p>
        </div>

        <div className="space-y-4">
          <p className="text-lg font-bold text-[#191c1e]">
            Human-in-the-Loop Requirement
          </p>

          <ul className="space-y-3">
            <li className="flex items-start gap-3">
              <span className="material-symbols-outlined mt-0.5 text-[18px] text-black">
                check_circle
              </span>
              <span className="text-[#515f74]">
                All high-risk alerts must be reviewed by a human analyst before
                any action is taken.
              </span>
            </li>

            <li className="flex items-start gap-3">
              <span className="material-symbols-outlined mt-0.5 text-[18px] text-black">
                check_circle
              </span>
              <span className="text-[#515f74]">
                Data ingestion must comply with GDPR, POPIA, and local labour
                privacy laws.
              </span>
            </li>

            <li className="flex items-start gap-3">
              <span className="material-symbols-outlined mt-0.5 text-[18px] text-black">
                check_circle
              </span>
              <span className="text-[#515f74]">
                Model bias audits should be conducted before real-world
                deployment.
              </span>
            </li>
          </ul>
        </div>
      </div>
    </section>
  );
}