import { useState } from 'react';
import './index.css';
import Header from './components/Header';
import Dropzone from './components/Dropzone';
import FilePreview from './components/FilePreview';
import ClassificationResult from './components/ClassificationResult';
import { classifyDocument } from './services/api';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileSelection = (selectedFile) => {
    const validTypes = ['application/pdf', 'image/jpeg', 'image/png'];
    if (!validTypes.includes(selectedFile.type)) {
      setError("Please upload a PDF, JPEG, or PNG file.");
      return;
    }
    
    setFile(selectedFile);
    setResult(null);
    setError(null);
  };

  const handleClassify = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await classifyDocument(file);
      setResult(data);
    } catch (err) {
      console.error(err);
      setError("Failed to classify document. " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-[1000px] mx-auto p-8 w-full">
      <Header />

      <main>
        <div className="bg-slate-800/70 backdrop-blur-xl border border-white/10 rounded-2xl shadow-md">
          <div className="p-8">
            <Dropzone onFileSelect={handleFileSelection} error={error} />

            {file && (
              <FilePreview 
                file={file} 
                loading={loading} 
                onClassify={handleClassify} 
              />
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
          <ClassificationResult result={result} />
        )}
      </main>
    </div>
  );
}

export default App;
