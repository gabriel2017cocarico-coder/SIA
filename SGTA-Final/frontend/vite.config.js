import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
    vue(),
  ],

  resolve: {
    alias: {
      '@': fileURLToPath(
        new URL('./src', import.meta.url)
      ),
    },
  },

  build: {
    // MediaPipe se carga dinámicamente desde CDN en runtime (import('@mediapipe/...'))
    // No necesita estar en el bundle - se marca como externo para el build
    rolldownOptions: {
      external: [
        '@mediapipe/face_mesh',
        '@mediapipe/camera_utils',
        '@mediapipe/drawing_utils',
      ],
    },
  },

  server: {
    // Permite el host publico del tunel (cloudflared/localtunnel);
    // sin esto Vite rechaza cualquier Host que no sea localhost.
    allowedHosts: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/media': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
