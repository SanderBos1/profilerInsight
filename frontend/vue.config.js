const { defineConfig } = require('@vue/cli-service');
const fs = require('fs');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: process.env.VUE_APP_FRONTEND_HOST, 
    port: process.env.VUE_APP_FRONTEND_PORT, 
  },
});