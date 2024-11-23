import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from "node:path";

export default defineConfig({
  root: path.join(__dirname, "./assets_source/"),
  base: "/assets/",
  build: {
    outDir: path.join(__dirname, "./assets_compiled/"),
    manifest: "manifest.json",
    assetsDir: "bundled",
    rollupOptions: {
        input: [
          "assets_source/main.tsx",
        ],
    },
    emptyOutDir: true,
    copyPublicDir: false,
  },
  server: {
    origin: 'http://127.0.0.1:5173',
  },
  plugins: [react()],
});