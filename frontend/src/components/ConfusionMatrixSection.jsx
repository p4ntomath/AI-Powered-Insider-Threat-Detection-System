import { confusionMatrix } from "../data/dashboardData";

export default function ConfusionMatrixSection() {
  return (
    <section
      id="evaluation"
      className="grid grid-cols-1 items-start gap-8 lg:grid-cols-3"
    >
      <div className="space-y-6 lg:col-span-2">
        <h2 className="font-['Hanken_Grotesk'] text-3xl font-semibold">
          Confusion Matrix Analysis
        </h2>

        <div className="overflow-x-auto rounded-xl border border-[#c6c6cd] bg-white shadow-sm">
          <table className="zebra-table w-full text-left">
            <thead className="bg-[#e6e8ea] mono text-[10px] uppercase tracking-wider text-[#515f74]">
              <tr>
                <th className="border-b border-[#c6c6cd] p-4">
                  Actual / Predicted
                </th>
                <th className="border-b border-[#c6c6cd] p-4">
                  Predicted Normal
                </th>
                <th className="border-b border-[#c6c6cd] p-4">
                  Predicted Malicious
                </th>
              </tr>
            </thead>

            <tbody className="mono text-sm">
              <tr>
                <td className="border-r border-[#c6c6cd] bg-[#f2f4f6] p-4 mono text-[10px] uppercase tracking-wider text-[#515f74]">
                  Actual Normal
                </td>
                <td className="p-4 font-bold text-[#191c1e]">
                  {confusionMatrix.trueNormal} (TN)
                </td>
                <td className="p-4 text-[#515f74]">
                  {confusionMatrix.falsePositive} (FP)
                </td>
              </tr>

              <tr>
                <td className="border-r border-[#c6c6cd] bg-[#f2f4f6] p-4 mono text-[10px] uppercase tracking-wider text-[#515f74]">
                  Actual Malicious
                </td>
                <td className="p-4 text-[#515f74]">
                  {confusionMatrix.falseNegative} (FN)
                </td>
                <td className="p-4 font-bold text-[#ba1a1a]">
                  {confusionMatrix.trueMalicious} (TP)
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div className="space-y-4 rounded-xl border border-[#c6c6cd] bg-white p-6 shadow-sm">
        <div className="flex items-center gap-2 text-black">
          <span className="material-symbols-outlined">info</span>
          <span className="font-['Hanken_Grotesk'] text-xl font-semibold">
            Why Recall and F1-Score Matter
          </span>
        </div>

        <p className="leading-7 text-[#515f74]">
          In insider threat detection, recall is important because a false
          negative means malicious behaviour was missed. However, precision is
          also important because false positives may lead to unnecessary
          investigation. The F1-score is useful because it balances precision
          and recall, which is especially important for imbalanced insider
          threat data.
        </p>

        <ul className="space-y-2 mono text-xs text-black">
          <li>• Minimises unobserved threats</li>
          <li>• Optimises security response</li>
          <li>• Validates detection sensitivity</li>
        </ul>
      </div>
    </section>
  );
}