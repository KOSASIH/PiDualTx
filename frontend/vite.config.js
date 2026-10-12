import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [
    vue(),
    {
      name: 'mock-rates-api',
      configureServer(server) {
        server.middlewares.use('/api/rates', (req, res) => {
          res.setHeader('Content-Type', 'application/json');
          res.end(JSON.stringify({
            internalRate: "314159.00",
            externalRate: "0.8111",
            timestamp: Math.floor(Date.now() / 1000)
          }));
        });
      }
    }
  ],
  server: {
    port: 3000,
    host: '0.0.0.0',
    allowedHosts: 'all'
  },
  define: {
    'process.env': {}
  },
  build: {
    outDir: 'dist'
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      'cross-fetch': path.resolve(__dirname, './src/shims/cross-fetch.js')
    }
  },
  optimizeDeps: {
    exclude: ['cross-fetch']
  }
})
