module.exports = {
  publicPath: process.env.NODE_ENV === 'production' ? '/' : '/',
  outputDir: 'dist',
  assetsDir: 'assets',
  productionSourceMap: false,

  devServer: {
    port: 8080,
    open: true,
    proxy: {
      '^/api': {
        target: process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000',
        changeOrigin: true,
        pathRewrite: { '^/api': '' },
        secure: false,
      },
    },
    hot: true,
  },

  configureWebpack: {
    resolve: {
      alias: {
        '@': require('path').resolve(__dirname, 'src'),
      },
    },
  },

  css: {
    loaderOptions: {
      scss: {
        additionalData: `@import "@/styles/variables.scss";`,
      },
    },
  },

  lintOnSave: true,
};
