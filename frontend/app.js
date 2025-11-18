// frontend/App.js

// Detect whether we're in Docker or local environment
const API_BASE =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "http://careplus-backend:8000";

// Universal fetch helper
async function api(path, options = {}) {
  const method = options.method || "GET";
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  const body = options.body ? JSON.stringify(options.body) : undefined;

  const res = await fetch(`${API_BASE}${path}`, { method, headers, body });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.json();
}

window.api = api;
