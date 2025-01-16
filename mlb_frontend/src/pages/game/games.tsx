/*
To-Do
- Consume the API to get the games
- Crate search functionality
- Create a page that will display the game information
- Filter the games by date, year
- live matches section should on be displayed when there are live matches
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';


const Game = () => {
    const [games, setGames] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [filteredGames, setFilteredGames] = useState([]);
    const [liveMatches, setLiveMatches] = useState([]);
    useEffect(() => {
        // Fetch games from API with query parameters
        axios.get('/mlb/schedule/', {
            params: {
                season: 2025,
                game_type: 'R'
            }
        })
        .then(response => {
            setGames(response.data);
            setFilteredGames(response.data);
            setLiveMatches(response.data.filter((game: { isLive: any; }) => game.isLive));
        })
        .catch(error => console.error('Error fetching games:', error));
    }, []);

    useEffect(() => {
        // Filter games based on search term
        setFilteredGames(games.filter(game =>
            game.name.toLowerCase().includes(searchTerm.toLowerCase())
        ));
    }, [searchTerm, games]);



    const handleSearch = (event: { target: { value: React.SetStateAction<string>; }; }) => {
        setSearchTerm(event.target.value);
    };

    return (
        <div>
            <h1>Game Page</h1>
            <input
                type="text"
                placeholder="Search games..."
                value={searchTerm}
                onChange={handleSearch}
            />
            <div>
                {filteredGames.map(game => (
                    <div key={game.id}>
                        <h2>{game.name}</h2>
                        <p>{game.date}</p>
                    </div>
                ))}
            </div>
            {liveMatches.length > 0 && (
                <div>
                    <h2>Live Matches</h2>
                    {liveMatches.map(game => (
                        <div key={game.id}>
                            <h2>{game.name}</h2>
                            <p>{game.date}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Game;
/*
const Game = () =>


    <h1>Game Page</h1>;
export default Game;


*/