import React, { useState } from 'react'
import { login } from '../api'

export default function Login({ onLogged }) {
  const [username, setUsername] = useState('admin')
  const [password, setPassword] = useState('admin123')
  const [error, setError] = useState(null)
  const submit = async (e) => {
    e.preventDefault()
    setError(null)
    try {
      await login(username, password)
      onLogged?.()
    } catch (err) {
      setError('Invalid credentials')
    }
  }
  return (
    <form onSubmit={submit} className="stack">
      <div className="row">
        <input placeholder="username" value={username} onChange={e=>setUsername(e.target.value)} />
        <input type="password" placeholder="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button type="submit">Login</button>
      </div>
      {error && <div className="muted">{error}</div>}
      <div className="muted">Demo credentials seeded: <code>admin / admin123</code></div>
    </form>
  )
}
