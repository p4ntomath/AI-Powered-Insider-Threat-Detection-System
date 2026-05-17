export default function Header() {
  return (
    <header className="fixed top-0 z-50 flex h-16 w-full items-center justify-between border-b border-[#c6c6cd] bg-white px-6 md:px-8">
      <nav className="hidden h-full items-center gap-8 md:flex">
        <a
          href="#"
          className="flex h-full items-center border-b-2 border-black font-bold text-black"
        >
          System Overview
        </a>

        <a
          href="#model-summary"
          className="flex h-full items-center px-2 font-medium text-[#515f74] transition-colors hover:text-black"
        >
          Metrics
        </a>

        <a
          href="#evaluation"
          className="flex h-full items-center px-2 font-medium text-[#515f74] transition-colors hover:text-black"
        >
          Evaluation
        </a>
      </nav>

      <div className="mono text-xs font-bold uppercase tracking-widest text-black">
        COS720 Prototype
      </div>
    </header>
  );
}