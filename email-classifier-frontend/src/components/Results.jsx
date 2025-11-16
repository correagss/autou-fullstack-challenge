// src/components/Results.jsx
import React from 'react';

function Results({ result }) {
  if (!result) {
    return null;
  }

  // Lógica para definir a cor do "badge" com base na categoria
  const isProductive = result.category === 'Produtivo';
  const badgeColor = isProductive ? 'bg-green-500 text-green-950' : 'bg-gray-500 text-gray-950';

  // Função para copiar o texto da resposta para a área de transferência
  const handleCopy = () => {
    navigator.clipboard.writeText(result.suggestedResponse);
    alert('Resposta copiada para a área de transferência!');
  };

  return (
    // 'animate-fade-in' é uma animação que vamos criar no CSS
    <div className="mt-8 bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700 animate-fade-in">
      <h2 className="text-2xl font-bold text-cyan-400 mb-4">Resultado da Análise</h2>

      {/* Seção da Categoria */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-300 mb-2">Categoria do E-mail:</h3>
        <p>
          <span className={`px-3 py-1 rounded-full font-bold text-sm ${badgeColor}`}>
            {result.category}
          </span>
        </p>
      </div>

      {/* Seção da Resposta Sugerida */}
      <div>
        <h3 className="text-lg font-semibold text-gray-300 mb-2">Resposta Sugerida:</h3>
        <div className="relative">
          <textarea
            readOnly // O usuário não pode editar a resposta
            rows="5"
            className="w-full p-3 bg-gray-900 border border-gray-600 rounded-md"
            value={result.suggestedResponse}
          />
          <button
            onClick={handleCopy}
            className="absolute top-2 right-2 bg-gray-700 hover:bg-gray-600 text-gray-300 font-bold py-1 px-3 rounded-md text-xs transition"
          >
            Copiar
          </button>
        </div>
      </div>
    </div>
  );
}

export default Results;