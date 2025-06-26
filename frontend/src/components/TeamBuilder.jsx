import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PlayerCard from './PlayerCard';
import { toast } from 'react-toastify';

export default function TeamBuilder({ team, players }) {
  const [selectedPlayers, setSelectedPlayers] = useState([]);
  const [remainingBudget, setRemainingBudget] = useState(team.budget);
  const navigate = useNavigate();

  const addPlayer = (player) => {
    if (remainingBudget >= player.price && selectedPlayers.length < 15) {
      setSelectedPlayers([...selectedPlayers, player]);
      setRemainingBudget(remainingBudget - player.price);
      toast.success(`${player.name} jamoangizga qo'shildi`);
    }
  };

  const removePlayer = (player) => {
    setSelectedPlayers(selectedPlayers.filter(p => p.id !== player.id));
    setRemainingBudget(remainingBudget + player.price);
    toast.info(`${player.name} jamoangizdan olib tashlandi`);
  };

  return (
    <div className="mb-8">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">{team.name}</h2>
        <button 
          onClick={() => navigate('/history')}
          className="bg-green-600 text-white px-3 py-1 rounded text-sm"
        >
          Ballar tarixi
        </button>
      </div>
      
      <div className="bg-white rounded-lg shadow p-4 mb-4">
        <div className="flex justify-between mb-2">
          <span>Qolgan byudjet:</span>
          <span className="font-bold">${remainingBudget.toFixed(1)}M</span>
        </div>
        
        <div className="grid grid-cols-3 gap-2 mb-4">
          {selectedPlayers.length > 0 ? (
            selectedPlayers.map(player => (
              <PlayerCard 
                key={player.id} 
                player={player} 
                onRemove={removePlayer}
              />
            ))
          ) : (
            <p className="col-span-3 text-gray-500 text-center py-4">
              Hozircha futbolchilar yo'q
            </p>
          )}
        </div>
      </div>
      
      <h3 className="text-lg font-medium mb-2">Futbolchilar ro'yxati</h3>
      <div className="grid grid-cols-2 gap-3">
        {players.map(player => (
          <PlayerCard 
            key={player.id} 
            player={player} 
            onSelect={addPlayer}
            disabled={remainingBudget < player.price || selectedPlayers.some(p => p.id === player.id)}
          />
        ))}
      </div>
    </div>
  );
}
