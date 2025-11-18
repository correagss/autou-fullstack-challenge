// src/components/Results.jsx
import React from 'react';

function Results({ result }) {
  if (!result) {
    return null;
  }

  // Lógica para definir a cor do "badge" com base na categoria
  const isProductive = result.category === 'Produtivo';
const badgeColor = isProductive
  ? 'bg-green-500 text-green-950'
  : 'bg-red-500 text-red-950';


  // Função para copiar o texto da resposta para a área de transferência
  const handleCopy = () => {
    navigator.clipboard.writeText(result.suggestedResponse);
    alert('Resposta copiada para a área de transferência!');
  };

  return (
    <div className="mt-8 bg-black bg-opacity-80 p-6 rounded-xl shadow-lg border border-gray-700 animate-fade-in">
      <h2 className="text-2xl font-bold text-orange-500 mb-4">
        Resultado da Análise
      </h2>

      {/* Seção da Categoria */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-300 mb-2">
          Categoria do E-mail:
        </h3>
        <p>
          <span className={`px-3 py-1 rounded-full font-bold text-sm ${badgeColor}`}>
            {result.category}
          </span>
        </p>
      </div>

      {/* Seção da Resposta Sugerida */}
      <div>
        <h3 className="text-lg font-semibold text-gray-300 mb-2">
          Resposta Sugerida:
        </h3>
        <div className="relative">
          <textarea
            readOnly
            rows="5"
            className="w-full p-3 bg-gray-900 border border-gray-600 text-gray-200 rounded-md"
            value={result.suggestedResponse}
          />
          <button
            onClick={handleCopy}
            className="absolute bottom-2 right-2 bg-orange-500 hover:bg-orange-600 
           text-black font-bold py-1 px-3 rounded-md text-xs transition"

          >
            Copiar
          </button>
        </div>
      </div>
    </div>
  );
}

export default Results;
