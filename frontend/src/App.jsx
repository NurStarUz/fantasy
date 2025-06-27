import React, { useEffect, useState } from 'react'
import axios from 'axios'

const BACKEND_URL = 'https://fantasy-backend.onrender.com' // o‘zingizning URL

function App() {
  const [user, setUser] = useState(null)
  const [team, setTeam] = useState([])
  const [points, setPoints] = useState(null)

  useEffect(() => {
    if (window.Telegram.WebApp) {
      const tgUser = window.Telegram.WebApp.initDataUnsafe.user
      if (tgUser) {
        const newUser = {
          telegram_id: tgUser.id.toString(),
          full_name: tgUser.first_name + ' ' + (tgUser.last_name || ''),
          avatar: tgUser.photo_url,
        }
        axios.post(`${BACKEND_URL}/users`, newUser).then(res => {
          setUser(res.data)
          loadTeam(res.data.id)
        })
      }
    }
  }, [])

  const loadTeam = async (userId) => {
    try {
      const teamRes = await axios.get(`${BACKEND_URL}/points/team/${userId}`)
      setTeam(teamRes.data.details)
      setPoints(teamRes.data.total_points)
    } catch (err) {
      console.error('Team load error:', err)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-5">
      <h1 className="text-3xl font-bold mb-4">📊 Fantasy Ballar</h1>

      {user && (
        <div className="mb-4">
          <p><strong>👤 Ism:</strong> {user.full_name}</p>
          <p><strong>🆔 ID:</strong> {user.telegram_id}</p>
        </div>
      )}

      {points !== null && (
        <div className="bg-green-800 p-3 rounded mb-4">
          <h2 className="text-xl">Umumiy Ball: {points}</h2>
        </div>
      )}

      <div className="grid grid-cols-1 gap-2">
        {team.map(player => (
          <div key={player.player_id} className="bg-gray-800 p-3 rounded shadow">
            <p><strong>ID:</strong> {player.player_id}</p>
            <p>⚽ Gollar: {player.goals}, 🎯 Assist: {player.assists}</p>
            <p>🧤 Clean Sheet: {player.clean_sheet}</p>
            <p>🟨: {player.yellow_cards}, 🟥: {player.red_cards}</p>
            <p>🔢 Ballar: <strong>{player.points}</strong></p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App
