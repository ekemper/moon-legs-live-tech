import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// When running in Docker dev, set VITE_PROXY_TARGET (e.g. http://backend:8765)
const proxyTarget = process.env.VITE_PROXY_TARGET || 'http://127.0.0.1:8765'
const wsTarget = proxyTarget.replace(/^http/, 'ws')
const inDocker = !!process.env.VITE_PROXY_TARGET

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
    watch: {
      usePolling: inDocker,
      interval: inDocker ? 500 : undefined,
    },
    hmr: inDocker
      ? {
          host: 'localhost',
          port: 5173,
          clientPort: 5173,
        }
      : true,
    proxy: {
      '/ws': { target: wsTarget, ws: true },
      '/api': { target: proxyTarget },
      '/health': { target: proxyTarget },
    },
  },
})
