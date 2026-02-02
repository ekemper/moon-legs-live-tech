import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// When running in Docker dev, set VITE_PROXY_TARGET (e.g. http://backend:8765)
const proxyTarget = process.env.VITE_PROXY_TARGET || 'http://127.0.0.1:8765'
const wsTarget = proxyTarget.replace(/^http/, 'ws')
const inDocker = !!process.env.VITE_PROXY_TARGET

/** Swallow ECONNRESET/EPIPE on socket so proxy never logs "ws proxy socket error". */
function swallowSocketErrors(socket: NodeJS.EventEmitter) {
  if (!socket || typeof socket.emit !== 'function') return
  const origEmit = socket.emit.bind(socket)
  socket.emit = function (event: string, ...args: unknown[]) {
    if (
      event === 'error' &&
      args[0] &&
      typeof args[0] === 'object' &&
      'code' in args[0] &&
      ((args[0] as NodeJS.ErrnoException).code === 'ECONNRESET' ||
        (args[0] as NodeJS.ErrnoException).code === 'EPIPE')
    ) {
      return true
    }
    return origEmit(event, ...args)
  }
}

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
      '/ws': {
        target: wsTarget,
        ws: true,
        configure: (proxy) => {
          // Patch client socket so ECONNRESET/EPIPE never reach proxy (Vite logs from socket error)
          proxy.on('proxyReqWs', (proxyReq: unknown, req: { socket?: NodeJS.EventEmitter }, socket: NodeJS.EventEmitter) => {
            swallowSocketErrors(socket)
          })
          // Patch target (backend) socket when proxy opens connection
          proxy.on('open', (proxySocket: NodeJS.EventEmitter) => {
            swallowSocketErrors(proxySocket)
          })
          proxy.on('error', (err: NodeJS.ErrnoException) => {
            if (err.code === 'ECONNRESET' || err.code === 'EPIPE') return
            console.error('[vite] ws proxy error:', err.message)
          })
        },
      },
      '/api': { target: proxyTarget },
      '/health': { target: proxyTarget },
    },
  },
})
