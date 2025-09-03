import { useEffect, useState } from 'react';
import { getHealth } from '../lib/api';

export default function HealthCard() {
  const [data, setData] = useState(null);
  const [err, setErr] = useState('');
  useEffect(() => { getHealth().then(setData).catch(e => setErr(String(e))); }, []);

  return (
    <div className="card">
      <h2 className="text-xl font-semibold mb-2">Health</h2>
      {err && <div className="text-red-600 text-sm">{err}</div>}
      <pre className="text-sm bg-gray-50 rounded p-3 overflow-auto">{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
