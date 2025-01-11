import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default ({ mode }) => {

  return defineConfig({
    plugins: [react()],
    define: {},
    server: {
      watch: {
        usePolling: true, // To work HMR with VSCode Remote Container on WSL2 Docker Devcontainer
        interval: 500,
      },
    },
  })
}
