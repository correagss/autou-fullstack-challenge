// src/App.jsx
import React, { useState } from 'react';
import EmailForm from './components/EmailForm';
import Results from './components/Results'; // 1. Importa a vitrine

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null); // 2. Novo potinho de memória para o resultado
  const [error, setError] = useState(''); // Potinho para erros

  const handleAnalyze = async ({ text, file }) => {
    setIsLoading(true);
    setAnalysisResult(null); // Limpa resultados antigos
    setError(''); // Limpa erros antigos

    // Simulação de chamada de API (vamos substituir isso depois)
    try {
      console.log("Analisando:", { text, file });
      // Simula uma espera de 2 segundos
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Simula um resultado de sucesso
      const mockResult = {
        category: 'Produtivo',
        suggestedResponse: 'Olá! Recebemos sua solicitação e nossa equipe já está trabalhando nela. Entraremos em contato em breve com uma atualização. Atenciosamente, Equipe de Suporte.'
      };
      
      setAnalysisResult(mockResult); // 3. Guarda o resultado no potinho de memória

    } catch (err) {
      setError('Ocorreu um erro ao analisar o email. Tente novamente.');
    } finally {
      setIsLoading(false); // 4. Desliga a luz vermelha (aconteça o que acontecer)
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
          
          {/* Mostra o erro, se houver */}
          {error && <p className="text-red-500 text-center mt-4">{error}</p>}
          
          {/* 5. Coloca a vitrine aqui, passando o resultado */}
          <Results result={analysisResult} />
        </main>
      </div>
    </div>
  );
}

export default App;