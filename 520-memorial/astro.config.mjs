import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  server: {
    host: true,
    port: 5174,
    strictPort: true,
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
