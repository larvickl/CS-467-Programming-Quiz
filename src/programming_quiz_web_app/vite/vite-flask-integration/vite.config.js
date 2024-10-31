import path from "node:path";

import { defineConfig } from "vite";

export default defineConfig({
  root: path.join(__dirname, "./src/"),
  base: "/assets/",
  build: {
    outDir: path.join(__dirname, "./assets_compiled/"),
    manifest: "manifest.json",
    assetsDir: "bundled",
    rollupOptions: {
        input: [
          "src/example.jsx",
        ],
    },
    emptyOutDir: true,
    copyPublicDir: false,
  },
});
