module.exports = {
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://stock-api:5050',
        ws: false,
        changeOrigin: true,
        // pathRewrite: {'^/api': '/api'},
      }
    }
  }
}
