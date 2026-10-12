import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  build: { outDir: 'dist' },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      'uview-ui': path.resolve(__dirname, 'node_modules/uview-plus')
    }
  }
})
