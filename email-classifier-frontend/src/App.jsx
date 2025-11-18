// src/App.jsx
import React, { useState } from 'react';
import EmailForm from './components/EmailForm';
import Results from './components/Results';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState('');

  const handleAnalyze = async ({ text, file }) => {
    setIsLoading(true);
    setAnalysisResult(null);
    setError('');

    const formData = new FormData();

    if (file) {
      formData.append('file', file);
    } else if (text) {
      formData.append('text', text);
    } else {
      setError("Nenhum conteúdo para analisar.");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch('https://autou-fullstack-challenge.onrender.com/api/analyze', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Ocorreu um erro na análise.');
      }

      setAnalysisResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center font-sans text-gray-200 p-4">
      <div className="w-full max-w-2xl mx-auto">

        {/* TÍTULO EM LARANJA */}
        <header className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-orange-500 mb-2">
            Analisador de E-mails 📧
          </h1>
          <p className="text-gray-300">
            Cole o texto de um email ou faça o upload de um arquivo para classificar seu conteúdo.
          </p>
        </header>

        <main>
          <EmailForm onAnalyze={handleAnalyze} isLoading={isLoading} />

          {error && (
            <p className="text-red-500 text-center mt-4 font-semibold">
              {error}
            </p>
          )}

          <Results result={analysisResult} />
        </main>
      </div>
    </div>
  );
}

export default App;
