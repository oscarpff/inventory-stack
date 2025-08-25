import React, { useEffect, useState } from 'react'
import InventoryTable from './components/InventoryTable.jsx'
import MovementLog from './components/MovementLog.jsx'
import Login from './components/Login.jsx'

export default function App() {
  const [logged, setLogged] = useState(!!localStorage.getItem('token'));
  const [refreshKey, setRefreshKey] = useState(0);
  const onUpdated = () => setRefreshKey(k => k+1);
  return (
    <>
      <header>
        <div className="row">
          <div className="grow"><strong>Inventory Dashboard</strong></div>
          <div>
            {logged ? (
              <button className="secondary" onClick={() => { localStorage.removeItem('token'); setLogged(false); }}>Logout</button>
            ) : null}
          </div>
        </div>
      </header>
      <main className="stack">
        {!logged ? (
          <div className="card"><Login onLogged={() => setLogged(true)} /></div>
        ) : null}
        <div className="split">
          <div className="card">
            <h3>Stock List</h3>
            <p className="muted">SKU, EAN13 and current quantity. Update quantities inline.</p>
            <InventoryTable onUpdated={onUpdated} />
          </div>
          <div className="card">
            <h3>Movement History</h3>
            <p className="muted">Most recent movements (entries/exits).</p>
            <MovementLog refreshKey={refreshKey} />
          </div>
        </div>
      </main>
    </>
  )
}
