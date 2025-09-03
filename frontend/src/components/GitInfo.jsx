import { useEffect, useState } from 'react';
import { gitBranch } from '../lib/api';

export default function GitInfo(){
  const [data, setData] = useState(null);
  const [err, setErr] = useState('');
  const refresh = ()=> gitBranch().then(setData).catch(e=>setErr(String(e)));
  useEffect(()=>{ refresh(); },[]);
  return (
    <div className="card">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-xl font-semibold">Git</h2>
        <button className="btn" onClick={refresh}>Neu laden</button>
      </div>
      {err && <div className="text-red-600 text-sm">{err}</div>}
      <pre className="text-sm bg-gray-50 rounded p-3 overflow-auto">{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
