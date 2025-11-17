// src/App.jsx
import React, { useState } from 'react';
import EmailForm from './components/EmailForm';
import Results from './components/Results';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState('');

  // --- A NOVA E PODEROSA FUNÇÃO handleAnalyze ---
  const handleAnalyze = async ({ text, file }) => {
    setIsLoading(true);
    setAnalysisResult(null);
    setError('');

    // FormData é a ferramenta perfeita para enviar tanto texto quanto arquivos
    const formData = new FormData();

    if (file) {
      // Se tiver um arquivo, anexa-o ao formulário
      formData.append('file', file);
    } else if (text) {
      // Se tiver texto, anexa-o ao formulário
      formData.append('text', text);
    } else {
      // Se não tiver nenhum dos dois (embora o EmailForm já valide isso)
      setError("Nenhum conteúdo para analisar.");
      setIsLoading(false);
      return;
    }

    try {
      // Faz a chamada real para o nosso backend
      // A URL está configurada para funcionar tanto localmente quanto no deploy
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData, // Envia os dados como FormData
      });

      const data = await response.json();

      if (!response.ok) {
        // Se a API retornar um erro (ex: 400), usa a mensagem de erro dela
        throw new Error(data.detail || 'Ocorreu um erro na análise.');
      }
      
      // Guarda o resultado de sucesso na memória (estado)
      setAnalysisResult(data);

    } catch (err) {
      // Se a chamada falhar (ex: rede, erro de JSON), mostra o erro
      setError(err.message);
    } finally {
      // Aconteça o que acontecer, desliga o spinner de carregamento
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-gray-900 min-h-screen flex items-center justify-center font-sans text-gray-200 p-4">
      <div className="w-full max-w-2xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-cyan-400 mb-2">
            Analisador de E-mails com IA ⚡
          </h1>
          <p className="text-gray-400">
            Cole o texto de um email ou faça o upload de um arquivo para classificar seu conteúdo.
          </p>
        </header>

        <main>
          <EmailForm onAnalyze={handleAnalyze} isLoading={isLoading} />
          
          {error && <p className="text-red-500 text-center mt-4 font-semibold">{error}</p>}
          
          <Results result={analysisResult} />
        </main>
      </div>
    </div>
  );
}

export default App;