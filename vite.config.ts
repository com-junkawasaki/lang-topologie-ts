import { defineConfig } from "vite";

export default defineConfig({
  plugins: [],
  server: {
    port: 25324,
    open: true,
  },
  build: {
    target: "esnext",
    minify: false,
  },
});

