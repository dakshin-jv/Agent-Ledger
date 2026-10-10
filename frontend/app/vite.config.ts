import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    include: [
      '@bryntum/grid',
      '@bryntum/grid-react',
      '@bryntum/scheduler',
      '@bryntum/scheduler-react',
      '@bryntum/taskboard',
      '@bryntum/taskboard-react',
      '@bryntum/gantt',
      '@bryntum/gantt-react',
    ],
  },
})
