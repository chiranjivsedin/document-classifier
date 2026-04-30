import { formatCategory } from '../utils/formatters';

const ClassificationResult = ({ result }) => {
  return (
    <div className="bg-slate-800/70 backdrop-blur-xl border border-white/10 rounded-2xl shadow-md mt-8 animate-slide-up">
      <div className="border-b border-white/10 p-6 flex justify-between items-center">
        <h2 className="font-semibold text-2xl tracking-tight">Classification Results</h2>
        <div className="inline-flex items-center px-4 py-2 rounded-full font-semibold text-lg capitalize bg-violet-500/15 text-violet-300 border border-violet-500/30">
          {formatCategory(result.predicted_class)}
        </div>
      </div>
      
      <div className="p-6">
        <div className="mt-6">
          <div className="flex justify-between mb-2 font-medium text-slate-400">
            <span>Confidence Score</span>
            <span>{Math.round(result.confidence * 100)}%</span>
          </div>
          <div className="w-full h-2 bg-black/30 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-violet-500 to-emerald-500 rounded-full transition-all duration-1000 ease-[cubic-bezier(0.4,0,0.2,1)]" 
              style={{ width: `${Math.round(result.confidence * 100)}%` }}
            ></div>
          </div>
        </div>

        <div className="mt-6 p-5 bg-black/20 rounded-lg border-l-4 border-violet-500">
          <div className="text-sm text-slate-400 uppercase tracking-wider mb-2">AI Reasoning</div>
          <div className="leading-relaxed text-[1.05rem]">{result.reason}</div>
        </div>

        <div className="flex gap-6 mt-6 text-sm text-slate-400">
          <div className="flex items-center gap-2">
            <svg className="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Extraction Route: {result.route}
          </div>
          <div className="flex items-center gap-2">
            <svg className="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            OCR Used: {result.ocr_used ? 'Yes' : 'No'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClassificationResult;
