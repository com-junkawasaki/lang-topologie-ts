import { defineConfig } from "vite";
import typegpu from "unplugin-typegpu/vite";

export default defineConfig({
  plugins: [
    typegpu({
      // TypeGPU plugin configuration
    }),
  ],
  server: {
    port: 3000,
    open: true,
  },
  build: {
    target: "esnext",
    minify: false,
  },
});

