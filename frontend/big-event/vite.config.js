import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import path from 'node:path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    //vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server:{
    proxy:{
      '/api':{//获取路径中包含了/api的请求
           target:'http://localhost:8080',//后台服务所在的源
           changeOrigin:true,
      },
      '/static':{//静态文件（上传的图片）
           target:'http://localhost:8080',
           changeOrigin:true,
      }
    }
  }
})
