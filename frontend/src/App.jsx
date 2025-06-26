import { useEffect, useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import TeamBuilder from './components/TeamBuilder';
import Rankings from './components/Rankings';
import PointsHistory from './components/PointsHistory';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  const [user, setUser] = useState(null);
  const [team, setTeam] = useState(null);
  const [players, setPlayers] = useState([]);

  useEffect(() => {
    // Initialize Telegram WebApp
    if (window.Telegram?.WebApp) {
      const tg = window.Telegram.WebApp;
      tg.expand();
      
      const userData = {
        id: tg.initDataUnsafe.user?.id,
        name: `${tg.initDataUnsafe.user?.first_name || ''} ${tg.initDataUnsafe.user?.last_name || ''}`.trim(),
        photo: tg.initDataUnsafe.user?.photo_url
      };
      setUser(userData);
      
      if (userData.id) {
        fetchTeam(userData.id);
      }
    }

    // Load players
    fetch('/players')
      .then(res => res.json())
      .then(data => setPlayers(data))
      .catch(err => console.error('Error loading players:', err));
  }, []);

  const fetchTeam = (userId) => {
    fetch(`/teams/${userId}`)
      .then(res => res.json())
      .then(data => setTeam(data))
      .catch(() => setTeam(null));
  };

  const createTeam = (teamName) => {
    fetch('/teams/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: user.id, name: teamName })
    })
    .then(res => res.json())
    .then(data => setTeam(data));
  };

  if (!team) {
    return <TeamCreation user={user} onCreate={createTeam} />;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <ToastContainer position="bottom-right" />
      <header className="bg-blue-600 text-white p-4">
        <h1 className="text-2xl font-bold">Fantasy Futbol</h1>
        <p className="text-sm">Oxirgi yangilanish: {new Date().toLocaleString()}</p>
      </header>
      
      <main className="container mx-auto p-4">
        <Routes>
          <Route path="/" element={<TeamBuilder team={team} players={players} />} />
          <Route path="/rankings" element={<Rankings />} />
          <Route path="/history" element={<PointsHistory teamId={team.id} />} />
        </Routes>
      </main>
    </div>
  );
}

function TeamCreation({ user, onCreate }) {
  const [teamName, setTeamName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (teamName.trim()) {
      onCreate(teamName);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-xl font-semibold mb-4">Jamoangizni yarating</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2">Jamoa nomi</label>
            <input
              type="text"
              className="w-full p-2 border rounded"
              value={teamName}
              onChange={(e) => setTeamName(e.target.value)}
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
          >
            Jamoa yaratish
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
