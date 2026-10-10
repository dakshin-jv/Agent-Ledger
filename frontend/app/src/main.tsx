import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './agent-board.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
