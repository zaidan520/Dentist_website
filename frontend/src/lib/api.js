// src/lib/api.js
const API_BASE = import.meta.env.PUBLIC_API_URL || 'http://localhost:8000/api';

export async function getClientBySlug(slug) {
  const res = await fetch(`${API_BASE}/clients/${slug}`);
  if (!res.ok) {
    if (res.status === 404) return null;
    throw new Error(`Failed to fetch client: ${res.status}`);
  }
  return res.json();
}