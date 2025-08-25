import React, { useEffect, useState } from 'react'
import { listItems, updateQuantity } from '../api'

export default function InventoryTable({ onUpdated }) {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [updatingId, setUpdatingId] = useState(null)
  const [newQty, setNewQty] = useState({})
  const load = async () => {
    setLoading(true)
    try {
      const data = await listItems()
      setItems(data)
    } finally {
      setLoading(false)
    }
  }
  useEffect(()=>{ load() }, [])

  const submitUpdate = async (id) => {
    const q = parseInt(newQty[id] ?? '', 10)
    if (Number.isNaN(q) || q < 0) return alert('Enter a valid non-negative number')
    setUpdatingId(id)
    try {
      await updateQuantity(id, q)
      await load()
      onUpdated?.()
    } catch (err) {
      alert('Update failed (are you logged in?)')
    } finally {
      setUpdatingId(null)
    }
  }

  if (loading) return <div>Loading...</div>
  return (
    <table>
      <thead>
        <tr><th>ID</th><th>SKU</th><th>EAN13</th><th>Quantity</th><th>Update</th></tr>
      </thead>
      <tbody>
        {items.map(it => (
          <tr key={it.id}>
            <td>{it.id}</td>
            <td>{it.sku}</td>
            <td>{it.ean13}</td>
            <td>{it.quantity}</td>
            <td>
              <div className="row">
                <input type="number" min="0" placeholder="new qty" value={newQty[it.id] ?? ''} onChange={e=>setNewQty({...newQty, [it.id]: e.target.value})} />
                <button onClick={()=>submitUpdate(it.id)} disabled={updatingId===it.id}>{updatingId===it.id?'Saving...':'Save'}</button>
              </div>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
