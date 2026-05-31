import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/auth': 'http://localhost:8000',
      '/personajes': 'http://localhost:8000',
      '/npcs': 'http://localhost:8000',
      '/sesiones': 'http://localhost:8000',
      '/tablas': 'http://localhost:8000',
      '/partidas': 'http://localhost:8000',
    }
  }
})
