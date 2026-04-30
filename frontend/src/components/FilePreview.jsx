import { formatFileSize } from '../utils/formatters';

const FilePreview = ({ file, loading, onClassify }) => {
  return (
    <div className="mt-8 p-6 flex items-center justify-between animate-slide-up">
      <div className="flex items-center gap-4">
        <svg className="text-violet-500 w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <div>
          <div className="font-medium">{file.name}</div>
          <div className="text-slate-400 text-sm">{formatFileSize(file.size)}</div>
        </div>
      </div>
      <button 
        className="bg-violet-500 text-white border-none py-3 px-6 rounded-lg font-semibold text-base cursor-pointer transition-all duration-200 hover:bg-violet-600 hover:-translate-y-[1px] hover:shadow-[0_4px_12px_rgba(139,92,246,0.3)] disabled:opacity-70 disabled:cursor-not-allowed" 
        onClick={onClassify}
        disabled={loading}
      >
        {loading ? 'Analyzing...' : 'Classify Document'}
      </button>
    </div>
  );
};

export default FilePreview;
