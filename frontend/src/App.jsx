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

  // Replace underscores and capitalize first letter for display
  const formatCategory = (category) => {
    if (!category) return '';
    return category.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  };

  return (
    <div className="container">
      <header className="header">
        <h1>Document Classifier AI</h1>
        <p>Upload an invoice, contract, report, ID proof, or purchase order for instant AI analysis.</p>
      </header>

      <main>
        <div className="glass-panel">
          <div style={{ padding: '2rem' }}>
            <div 
              className={`dropzone ${isDragActive ? 'active' : ''}`}
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
                style={{ display: 'none' }} 
                accept="application/pdf,image/jpeg,image/png" 
              />
              <svg className="dropzone-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <div className="dropzone-text">
                {isDragActive ? 'Drop file here!' : 'Drag & drop a document here'}
              </div>
              <div className="dropzone-subtext">or click to browse files (PDF, JPEG, PNG)</div>
            </div>

            {error && (
              <div style={{ color: 'var(--error)', marginTop: '1rem', padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '8px', border: '1px solid rgba(239, 68, 68, 0.3)' }}>
                <strong>Error:</strong> {error}
              </div>
            )}

            {file && (
              <div className="file-preview">
                <div className="file-info">
                  <svg className="file-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <div>
                    <div className="file-name">{file.name}</div>
                    <div className="file-size">{formatFileSize(file.size)}</div>
                  </div>
                </div>
                <button 
                  className="btn" 
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
          <div className="loader-container">
            <div className="spinner"></div>
            <h3>Analyzing with Gemma3...</h3>
            <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem' }}>Extracting text and running neural classification</p>
          </div>
        )}

        {result && !loading && (
          <div className="glass-panel results-panel">
            <div className="results-header">
              <h2>Classification Results</h2>
              <div className="category-badge">
                {formatCategory(result.predicted_class)}
              </div>
            </div>
            
            <div className="results-body">
              <div className="confidence-section">
                <div className="confidence-label">
                  <span>Confidence Score</span>
                  <span>{Math.round(result.confidence * 100)}%</span>
                </div>
                <div className="confidence-bar-bg">
                  <div 
                    className="confidence-bar-fill" 
                    style={{ width: `${Math.round(result.confidence * 100)}%` }}
                  ></div>
                </div>
              </div>

              <div className="reason-section">
                <div className="reason-title">AI Reasoning</div>
                <div className="reason-text">{result.reason}</div>
              </div>

              <div className="meta-info">
                <div className="meta-item">
                  <svg style={{ width: '16px', color: 'var(--text-secondary)' }} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  Extraction Route: {result.route}
                </div>
                <div className="meta-item">
                  <svg style={{ width: '16px', color: 'var(--text-secondary)' }} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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
