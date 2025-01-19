
import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from "./pages/home/home.tsx";
import Game from "./pages/game/games.tsx";
import BaseballScoreboard from "./pages/card";
import GameCard from "./pages/card/example.tsx";
import Test from "./pages/test/test.tsx";


function App() {

  return (
      <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/game" element={<Game />} />
        <Route path="/baseball-scoreboard" element={<BaseballScoreboard />} />
          <Route path="/example-card" element={<GameCard />} />
          //add test route
          <Route path="/test" element={<Test />} />

      </Routes>
    </Router>
  )
}

export default App
