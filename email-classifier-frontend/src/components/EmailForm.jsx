// src/components/EmailForm.jsx
import React, { useState } from 'react';

// A "ponte" para enviar os dados para o App.jsx
function EmailForm({ onAnalyze, isLoading }) {
  const [emailText, setEmailText] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      // Se um arquivo for selecionado, apaga o texto do textarea
      setEmailText(''); 
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // O formulário só pode ser enviado se tiver texto OU um arquivo
    if (!emailText && !selectedFile) {
      alert('Por favor, insira o texto do email ou selecione um arquivo.');
      return;
    }
    onAnalyze({ text: emailText, file: selectedFile });
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700">
      <div className="mb-4">
        <label htmlFor="emailText" className="block text-sm font-medium text-gray-300 mb-2">
          Cole o texto do e-mail aqui
        </label>
        <textarea
          id="emailText"
          rows="8"
          className="w-full p-3 bg-gray-900 border border-gray-600 rounded-md focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition"
          placeholder="Prezados, gostaria de saber o status do meu caso..."
          value={emailText}
          onChange={(e) => {
            setEmailText(e.target.value);
            // Se o usuário digitar, deseleciona o arquivo
            setSelectedFile(null);
          }}
          disabled={isLoading}
        />
      </div>

      <div className="text-center my-4 text-gray-500">OU</div>

      <div className="mb-6">
        <label htmlFor="fileUpload" className="block text-sm font-medium text-gray-300 mb-2">
          Faça o upload de um arquivo (.txt ou .pdf)
        </label>
        <input
          id="fileUpload"
          type="file"
          accept=".txt,.pdf"
          className="w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-cyan-500 file:text-cyan-950 hover:file:bg-cyan-600 cursor-pointer"
          onChange={handleFileChange}
          disabled={isLoading}
        />
        {selectedFile && <p className="text-xs text-gray-400 mt-2">Arquivo selecionado: {selectedFile.name}</p>}
      </div>

      <button
        type="submit"
        className="w-full bg-cyan-500 text-white font-bold py-3 px-4 rounded-md hover:bg-cyan-600 disabled:bg-gray-600 disabled:cursor-not-allowed flex items-center justify-center transition"
        disabled={isLoading}
      >
        {isLoading ? (
          <>
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Analisando...
          </>
        ) : (
          'Analisar E-mail'
        )}
      </button>
    </form>
  );
}

export default EmailForm;