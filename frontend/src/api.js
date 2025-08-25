const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

function authHeaders() {
  const token = localStorage.getItem('token');
  return token ? { 'Authorization': `Bearer ${token}` } : {};
}

export async function login(username, password) {
  const form = new URLSearchParams();
  form.append('username', username);
  form.append('password', password);
  const r = await fetch(`${API_BASE}/auth/token`, { method: 'POST', body: form });
  if (!r.ok) throw new Error('Invalid credentials');
  const data = await r.json();
  localStorage.setItem('token', data.access_token);
  return data;
}

export async function listItems() {
  const r = await fetch(`${API_BASE}/items`);
  if (!r.ok) throw new Error('Failed to load items');
  return await r.json();
}

export async function updateQuantity(itemId, quantity, reason='manual update') {
  const r = await fetch(`${API_BASE}/items/${itemId}/quantity`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify({ quantity, reason })
  });
  if (!r.ok) throw new Error('Failed to update quantity');
  return await r.json();
}

export async function listMovements(limit=50) {
  const r = await fetch(`${API_BASE}/movements?limit=${limit}`);
  if (!r.ok) throw new Error('Failed to load movements');
  return await r.json();
}
