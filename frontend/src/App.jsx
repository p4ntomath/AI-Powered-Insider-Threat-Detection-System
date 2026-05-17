import Header from "./components/Header";
import HeroUpload from "./components/HeroUpload";
import ModelSummary from "./components/ModelSummary";
import InferencePipeline from "./components/InferencePipeline";
import BehaviouralIndicators from "./components/BehaviouralIndicators";
import TestingExamples from "./components/TestingExamples";
import ConfusionMatrixSection from "./components/ConfusionMatrixSection";
import ExplainabilitySection from "./components/ExplainabilitySection";
import EthicsSection from "./components/EthicsSection";
import Footer from "./components/Footer";

export default function App() {
  return (
    <div className="min-h-screen bg-[#f7f9fb] text-[#191c1e]">
      <Header />

      <main className="mx-auto max-w-7xl space-y-16 px-6 pb-20 pt-24 md:px-8">
        <HeroUpload />
        <ModelSummary />
        <InferencePipeline />
        <BehaviouralIndicators />
        <TestingExamples />
        <ConfusionMatrixSection />
        <ExplainabilitySection />
        <EthicsSection />
      </main>

      <Footer />
    </div>
  );
}