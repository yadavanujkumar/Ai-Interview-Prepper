import { defineConfig } from 'vite'

export default defineConfig({
  root: './static',
  build: {
    outDir: '../dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: './static/js/main.js',
        components: './static/js/components/index.js'
      },
      output: {
        entryFileNames: 'js/[name]-[hash].js',
        chunkFileNames: 'js/[name]-[hash].js',
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name.split('.')
          const extType = info[info.length - 1]
          if (/\.(css)$/.test(assetInfo.name)) {
            return `css/[name]-[hash].${extType}`
          }
          return `assets/[name]-[hash].${extType}`
        }
      }
    }
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@import "./static/css/variables.scss";`
      }
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:5000',
      '/upload': 'http://localhost:5000',
      '/interview': 'http://localhost:5000',
      '/study-resources': 'http://localhost:5000',
      '/chat': 'http://localhost:5000',
      '/analytics': 'http://localhost:5000',
      '/companies': 'http://localhost:5000',
      '/salary': 'http://localhost:5000'
    }
  }
})