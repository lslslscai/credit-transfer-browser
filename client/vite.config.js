import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from "fs"
import path from "path"
import commonjsExternals from 'vite-plugin-commonjs-externals';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server:{
    open: true,
    https: true,
    host:"127.0.0.1",
    port: 443
  }
})
