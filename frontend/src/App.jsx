import { useState, useRef } from 'react';
import './index.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isDragActive, setIsDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelection(e.target.files[0]);
    }
  };

  const handleFileSelection = (selectedFile) => {
    // Only accept PDF, JPEG, PNG
    const validTypes = ['application/pdf', 'image/jpeg', 'image/png'];
    if (!validTypes.includes(selectedFile.type)) {
      setError("Please upload a PDF, JPEG, or PNG file.");
      return;
    }
    
    setFile(selectedFile);
    setResult(null);
    setError(null);
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  const classifyDocument = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/classify', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        let errMsg = `Server returned ${response.status}: ${response.statusText}`;
        try {
            const errBody = await response.json();
            if (errBody.detail) errMsg = errBody.detail;
        } catch(e) {}
        throw new Error(errMsg);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setError("Failed to classify document. " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatCategory = (category) => {
    if (!category) return '';
    return category.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  };

  return (
    <div className="max-w-[1000px] mx-auto p-8 w-full">
      <header className="text-center mb-12 animate-fade-in-down">
        <h1 className="text-4xl font-semibold mb-2 bg-gradient-to-r from-violet-400 to-emerald-400 bg-clip-text text-transparent tracking-tight">
          Document Classifier AI
        </h1>
        <p className="text-slate-400 text-lg">
          Upload an invoice, contract, report, ID proof, or purchase order for instant AI analysis.
        </p>
      </header>

      <main>
        <div className="bg-slate-800/70 backdrop-blur-xl border border-white/10 rounded-2xl shadow-md">
          <div className="p-8">
            <div 
              className={`group w-full p-16 border-2 border-dashed border-white/10 rounded-2xl flex flex-col items-center justify-center cursor-pointer transition-all duration-300 bg-slate-900/40 hover:border-violet-500 hover:bg-violet-500/5 ${isDragActive ? 'border-violet-500 bg-violet-500/5 -translate-y-0.5' : ''}`}
              onDragEnter={handleDragEnter}
              onDragLeave={handleDragLeave}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              onClick={triggerFileInput}
            >
              <input 
                type="file" 
                ref={fileInputRef} 
                onChange={handleFileChange} 
                className="hidden" 
                accept="application/pdf,image/jpeg,image/png" 
              />
              <svg className="w-16 h-16 mb-4 text-violet-500 transition-transform duration-300 group-hover:scale-110" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <div className="text-xl font-medium mb-2">
                {isDragActive ? 'Drop file here!' : 'Drag & drop a document here'}
              </div>
              <div className="text-slate-400 text-sm">or click to browse files (PDF, JPEG, PNG)</div>
            </div>

            {error && (
              <div className="mt-4 p-4 text-red-500 bg-red-500/10 rounded-lg border border-red-500/30">
                <strong className="font-semibold">Error:</strong> {error}
              </div>
            )}

            {file && (
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
                  onClick={classifyDocument}
                  disabled={loading}
                >
                  {loading ? 'Analyzing...' : 'Classify Document'}
                </button>
              </div>
            )}
          </div>
        </div>

        {loading && (
          <div className="flex flex-col items-center justify-center p-12 animate-fade-in">
            <div className="w-10 h-10 border-[3px] border-violet-500/30 rounded-full border-t-violet-500 animate-spin mb-4"></div>
            <h3 className="font-semibold text-lg tracking-tight">Analyzing with Gemma3...</h3>
            <p className="text-slate-400 mt-2">Extracting text and running neural classification</p>
          </div>
        )}

        {result && !loading && (
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
        )}
      </main>
    </div>
  );
}

export default App;
