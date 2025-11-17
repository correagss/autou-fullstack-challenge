import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Qualquer chamada que comece com /api...
      '/api': {
        // ...será redirecionada para o seu backend na porta 8000.
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        // O '/api' é mantido, pois o backend espera por ele!
      },
    },
  },
})