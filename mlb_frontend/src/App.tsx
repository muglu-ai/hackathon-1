
import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from "./pages/home/home.tsx";
import Game from "./pages/game/games.tsx";


function App() {

  return (
      <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/game" element={<Game />} />
      </Routes>
    </Router>
  )
}

export default App
