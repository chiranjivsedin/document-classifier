const Header = () => {
  return (
    <header className="text-center mb-12 animate-fade-in-down">
      <h1 className="text-4xl font-semibold mb-2 bg-gradient-to-r from-violet-400 to-emerald-400 bg-clip-text text-transparent tracking-tight">
        Document Classifier AI
      </h1>
      <p className="text-slate-400 text-lg">
        Upload an invoice, contract, report, ID proof, or purchase order for instant AI analysis.
      </p>
    </header>
  );
};

export default Header;
