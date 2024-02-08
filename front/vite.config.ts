import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default ({ mode }) => {
  const port = process.env.API_PORT || 5000;

  return defineConfig({
    plugins: [react()], 
    define: {
      'API_PORT': JSON.stringify(port),
    },
  })
}
