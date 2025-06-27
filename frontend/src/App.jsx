import React, { useEffect, useState } from 'react'
import axios from 'axios'

const BACKEND_URL = 'https://fantasy-backend-eruk.onrender.com'

function App() {
  const [user, setUser] = useState(null)
  const [team, setTeam] = useState([])
  const [points, setPoints] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (window.Telegram?.WebApp?.initDataUnsafe?.user) {
      const tgUser = window.Telegram.WebApp.initDataUnsafe.user
      const newUser = {
        telegram_id: tgUser.id.toString(),
        full_name: tgUser.first_name + ' ' + (tgUser.last_name || ''),
        avatar: tgUser.photo_url,
      }
      axios.post(`${BACKEND_URL}/users`, newUser)
        .then(res => {
          setUser(res.data)
          loadTeam(res.data.id)
        })
        .catch(() => setError("❌ Foydalanuvchini saqlab bo‘lmadi."))
    } else {
      setError("🔒 Iltimos, botni Telegram ichida oching.")
    }
  }, [])

  const loadTeam = async (userId) => {
    try {
      const teamRes = await axios.get(`${BACKEND_URL}/points/team/${userId}`)
      setTeam(teamRes.data.details)
      setPoints(teamRes.data.total_points)
    } catch {
      setError("❌ Jamoani yuklashda xatolik bo‘ldi.")
    }
  }

  if (error) {
    return <div className="bg-gray-900 text-white p-5 min-h-screen text-center text-lg">{error}</div>
  }

  if (!user) {
    return <div className="bg-gray-900 text-white p-5 min-h-screen text-center text-lg">⏳ Yuklanmoqda...</div>
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-5">
      <h1 className="text-3xl font-bold mb-4">📊 Fantasy Ballar</h1>

      <div className="mb-4">
        <p><strong>👤 Ism:</strong> {user.full_name}</p>
        <p><strong>🆔 ID:</strong> {user.telegram_id}</p>
      </div>

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
