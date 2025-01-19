import {useEffect, useState} from 'react';
import '../../style/game.css'; // You can customize styles as needed
import '../../types/game.ts'

const API_BASE_URL = "http://34.72.213.107:8000/mlb/schedule/";

const fetchGames = async (season: number, gameType: string, page: number, pageSize: number) => {
    const response = await fetch(`${API_BASE_URL}?season=${season}&game_type=${gameType}&page=${page}&page_size=${pageSize}`);
    return await response.json();
};

const fetchTeamLogo = async (teamName: string) => {
  const response = await fetch(`https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t=${teamName}`);
  //from response use strLogo to fetch image
  const data = await response.json();
  return data.teams && data.teams.length > 0 ? data.teams[0].strLogo : null;
};



// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
const GameCard = ({game, onClick, key}) => {
    //console.log(game);
    const {gameDate, teams, venue, status, content} = game;
    const gameType = `${status}`;
    const gameTitleHome = `${teams.home.name}`;
    const gameTitleAway = `${teams.away.name}`;
    const homeScoreWin = `${teams.home.wins}`;
    const awayScoreWin = `${teams.away.wins}`;
    const homeScoreLoss = `${teams.home.losses}`;
    const awayScoreLoss = `${teams.away.losses}`;
    const contents = `${content.link}`;
    
    //console.log(contents);

    const gameTime = new Date(gameDate).toLocaleString();

    return (
        <div
            className="sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-4 game-card bg-white shadow-md rounded-lg p-4 cursor-pointer hover:shadow-lg transition-shadow"
            onClick={() => onClick(game)}
        >
            {/* Placeholder for image */}
            {/* <img src={getRandomImage(gameTitle)} alt={gameTitle} className="game-image" /> */}

            <div className="game-info text-center">
                <h5 className="text-gray-500 text-sm">{gameType}</h5>
                <h3 className="text-lg font-semibold mb-2">
                    {gameTitleHome} <br/> <span className="text-gray-400">vs</span> <br/> {gameTitleAway}
                </h3>
                <p className="text-sm text-gray-600">{gameTime}</p>
                <p className="text-sm text-gray-600 mb-4">{venue.name}</p>

                {/* Scores */}
                <div className="flex justify-between items-center mb-4">
                    <div className="text-left">
                        <p className="text-lg font-bold">{gameTitleHome}</p>
                        <p className="text-lg font-bold">{gameTitleAway}</p>
                    </div>
                    <div className="text-center">
                        <p className="text-sm text-gray-600">{ homeScoreWin  } - { homeScoreLoss  } </p>
                        <p className="text-sm text-gray-600">{ awayScoreWin } - {awayScoreLoss}</p>
                    </div>
                    <div className='hidden'>
                        <p className="text-sm text-gray-600">{contents} - {key}</p>
                    </div>
                </div>
            </div>
        </div>
    );
};


// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
const GameDetails = ({game, onClose}) => {
    const {gameDate, teams, venue, description, dayOrNight, seriesDescription, gameId} = game;
    const gameTime = new Date(gameDate).toLocaleString();
    const [homeLogo, setHomeLogo] = useState(null);
    const [awayLogo, setAwayLogo] = useState(null);


    useEffect(() => {
        const loadLogos = async () => {
            const homeLogoUrl = await fetchTeamLogo(teams.home.name);
            const awayLogoUrl = await fetchTeamLogo(teams.away.name);
            setHomeLogo(homeLogoUrl);
            setAwayLogo(awayLogoUrl);
            console.log(gameId);
        };
        loadLogos();
    }, [teams]);

    return (
        <div className="game-details-modal">
            <div className="game-details">
                <button onClick={onClose} className="close-button">&times;</button>
                <h2>{`${teams.home.name} vs <br/> ${teams.away.name}`}</h2>
                <div className="team-logos">
                    {homeLogo && <img src={homeLogo} alt={`${teams.home.name} Logo`} className="team-logo"
                                      style={{width: '40%', height: '30%', borderRadius: '50%'}}/>}
                    VS
                    {awayLogo && <img src={awayLogo} alt={`${teams.away.name} Logo`} className="team-logo"
                                style={{width: '40%', height: '30%', borderRadius: '50%'}}/>}
          </div>
          <p><strong>Date/Time:</strong> {gameTime}</p>
          <p><strong>Venue:</strong> {venue.name}</p>
          <p><strong>Description:</strong> {description}</p>
          <p><strong>Day/Night:</strong> {dayOrNight}</p>
          <p><strong>Series:</strong> {seriesDescription}</p>
      </div>
    </div>
    );
};

const App = () => {
    const [gamesData, setGamesData] = useState({games: [], totalGames: 0});
    const [selectedGame, setSelectedGame] = useState(null);
    const [page, setPage] = useState(1);
    const pageSize = 12;
    const season = 2024;
    const gameType = "R";

    useEffect(() => {
        const loadGames = async () => {
            const data = await fetchGames(season, gameType, page, pageSize);
            // console.log(data);
            setGamesData(data);
        };
        loadGames();
    }, [page]);

    const handleNextPage = () => {
        if (page < Math.ceil(gamesData.totalGames / pageSize)) {
            setPage(page + 1);
        }
    };

    const handlePreviousPage = () => {
        if (page > 1) {
            setPage(page - 1);
        }
    };

    return (
        <div className="app">
            <h1>Game Schedule</h1>
            <div className="game-list sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-4">
                {gamesData.games.map((game) => (

                    <GameCard key={game} game={game} onClick={setSelectedGame}/>
                ))}
            </div>
            <div className="pagination">
                <button onClick={handlePreviousPage} disabled={page === 1}>Previous</button>
                <span>Page {page}</span>
                <button onClick={handleNextPage} disabled={page >= Math.ceil(gamesData.totalGames / pageSize)}>Next
                </button>
            </div>
            {selectedGame && (
                <GameDetails game={selectedGame} onClose={() => setSelectedGame(null)}/>
            )}
        </div>
    );
};

export default App;