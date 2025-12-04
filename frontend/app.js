const API_BASE = "http://localhost:8000";

async function api(path, options = {}) {
  const res = await fetch(API_BASE + path, {
    method: options.method || "GET",
    headers: { "Content-Type": "application/json" },
    body: options.body ? JSON.stringify(options.body) : null
  });

  if (!res.ok) {
    console.error("API ERROR:", res.status, await res.text());
    alert("Backend error: " + res.status);
    return [];
  }

  return res.json();
}
