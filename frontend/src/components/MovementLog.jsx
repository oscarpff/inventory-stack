import React, { useEffect, useState } from 'react'
import { listMovements } from '../api'

export default function MovementLog({ refreshKey }) {
  const [moves, setMoves] = useState([])
  const [loading, setLoading] = useState(true)
  const load = async () => {
    setLoading(true)
    try {
      const data = await listMovements(50)
      setMoves(data)
    } finally {
      setLoading(false)
    }
  }
  useEffect(()=>{ load() }, [])
  useEffect(()=>{ load() }, [refreshKey])

  if (loading) return <div>Loading...</div>
  return (
    <table>
      <thead>
        <tr><th>ID</th><th>Item</th><th>Delta</th><th>Reason</th><th>When</th></tr>
      </thead>
      <tbody>
        {moves.map(m => (
          <tr key={m.id}>
            <td>{m.id}</td>
            <td>{m.item_id}</td>
            <td>{m.delta}</td>
            <td>{m.reason ?? '-'}</td>
            <td>{new Date(m.created_at).toLocaleString()}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
