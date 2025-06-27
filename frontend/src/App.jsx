import React, { useEffect, useState } from 'react'
import axios from 'axios'

const BACKEND_URL = 'https://fantasy-backend.onrender.com' // o‘zingizdagi to‘g‘ri URL

function App() {
  const [user, setUser] = useState(null)
  const [team, setTeam] = useState([])
  const [points, setPoints] = useState(null)

  const [manualData, setManualData] = useState({
    telegram_id: '',
    full_name: '',
    avatar: ''
  })

  useEffect(() => {
    // Agar Telegram orqali kirgan bo‘lsa
    if (window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.initDataUnsafe?.user) {
      const tgUser = window.Telegram.WebApp.initDataUnsafe.user
      const newUser = {
        telegram_id: tgUser.id.toString(),
        full_name: tgUser.first_name + ' ' + (tgUser.last_name || ''),
        avatar: tgUser.photo_url,
      }
      registerUser(newUser)
    }
  }, [])

  const registerUser = async (userObj) => {
    try {
      const res = await axios.post(`${BACKEND_URL}/users`, userObj)
      setUser(res.data)
      loadTeam(res.data.id)
    } catch (err) {
      console.error("User registration failed:", err)
    }
  }

  const handleManualSubmit = (e) => {
    e.preventDefault()
    if (manualData.telegram_id) {
      registerUser(manualData)
    }
  }

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

      {/* Agar foydalanuvchi yo‘q bo‘lsa va Telegram emas bo‘lsa */}
      {!user && (
        <form onSubmit={handleManualSubmit} className="mb-4 space-y-2">
          <input type="text" className="w-full p-2 rounded text-black" placeholder="Telegram ID" value={manualData.telegram_id} onChange={e => setManualData({ ...manualData, telegram_id: e.target.value })} required />
          <input type="text" className="w-full p-2 rounded text-black" placeholder="Ism Familiya" value={manualData.full_name} onChange={e => setManualData({ ...manualData, full_name: e.target.value })} />
          <input type="text" className="w-full p-2 rounded text-black" placeholder="Avatar URL" value={manualData.avatar} onChange={e => setManualData({ ...manualData, avatar: e.target.value })} />
          <button type="submit" className="bg-green-600 px-4 py-2 rounded">Kirish</button>
        </form>
      )}

      {user && (
        <>
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
        </>
      )}
    </div>
  )
}

export default App
