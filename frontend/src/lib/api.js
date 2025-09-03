const BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export async function getHealth() {
  const r = await fetch(`${BASE}/health`);
  if (!r.ok) throw new Error('health failed');
  return r.json();
}

export async function execCommand(cmd, timeout) {
  const r = await fetch(`${BASE}/api/agent/execute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ cmd, timeout }),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function gitBranch() {
  const r = await fetch(`${BASE}/api/agent/git/branch`);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function openPR({ title, body, base='main' }) {
  const r = await fetch(`${BASE}/api/agent/pr/open`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, body, base }),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function getTelemetry() {
  const r = await fetch(`${BASE}/api/telemetry/summary`);
  if (!r.ok) throw new Error('telemetry failed');
  return r.json();
}