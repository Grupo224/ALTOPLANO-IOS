import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import frappeui from 'frappe-ui/vite'

export default defineConfig({
  plugins: [
    frappeui({
      frontendRoute: '/ios',
      frappeProxy: true,
      jinjaBootData: true,
      codeLanguages: false,
      buildConfig: {
        indexHtmlPath: '../altoplano_agents/www/ios.html',
        emptyOutDir: true,
      },
    }),
    vue(),
  ],
})
