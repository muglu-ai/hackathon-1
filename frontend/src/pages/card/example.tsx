import React from "react";
import "./GameCard.css";

const GameCard = () => {
  return (
    <div className="game-card">
      <div className="time">
        <span>6:10 AM ET</span>
      </div>
      <div className="teams">
        <div className="team">
          <img
            src="path/to/dodgers-logo.png"
            alt="Dodgers Logo"
            className="team-logo"
          />
          <span className="team-name">Dodgers</span>
          <span className="team-score">0 - 0</span>
        </div>
        <div className="team">
          <img
            src="path/to/cubs-logo.png"
            alt="Cubs Logo"
            className="team-logo"
          />
          <span className="team-name">Cubs</span>
          <span className="team-score">0 - 0</span>
        </div>
      </div>
      <div className="venue">
        <span>Tokyo Dome</span>
      </div>
      <div className="player-section">
        <div className="player">
          <span className="team-title">LA DODGERS</span>
          <div className="player-info">
            <div className="player-image-placeholder">TBD</div>
            <span className="player-name">-</span>
          </div>
        </div>
        <div className="player">
          <span className="team-title">CHI CUBS</span>
          <div className="player-info">
            <div className="player-image-placeholder">TBD</div>
            <span className="player-name">-</span>
          </div>
        </div>
      </div>
      <div className="preview">
        <button className="preview-button">Preview</button>
      </div>
    </div>
  );
};

export default GameCard;
