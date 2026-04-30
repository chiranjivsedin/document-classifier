import { useState, useRef } from 'react';

const Dropzone = ({ onFileSelect, error }) => {
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
      onFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onFileSelect(e.target.files[0]);
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  return (
    <>
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
    </>
  );
};

export default Dropzone;
