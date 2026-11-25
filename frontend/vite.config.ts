import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Zelfde origin voor React en Django, zodat sessiecookie en CSRF zonder CORS werken
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    },
  },
})
