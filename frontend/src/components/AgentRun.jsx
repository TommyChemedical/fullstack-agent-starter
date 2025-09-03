import { useState } from 'react';
import { execCommand } from '../lib/api';

export default function AgentRun(){
  const [cmd, setCmd] = useState('python -c "print(40+2)"');
  const [timeout, setTimeout] = useState('');
  const [out, setOut] = useState(null);
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);

  const run = async (e)=>{
    e.preventDefault(); setBusy(true); setErr(''); setOut(null);
    try{
      const t = timeout === '' ? undefined : Number(timeout);
      const res = await execCommand(cmd, t);
      setOut(res);
    }catch(e){ setErr(String(e)); }
    finally{ setBusy(false); }
  };

  return (
    <form onSubmit={run} className="card space-y-3">
      <h2 className="text-xl font-semibold">Kommando ausführen</h2>
      <div>
        <label className="label">Befehl</label>
        <input className="input mt-1" value={cmd} onChange={e=>setCmd(e.target.value)} />
      </div>
      <div>
        <label className="label">Timeout (Sek., leer = Default)</label>
        <input className="input mt-1" value={timeout} onChange={e=>setTimeout(e.target.value)} />
      </div>
      <button className="btn" disabled={busy}>{busy? 'Ausführen…':'Ausführen'}</button>
      {err && <div className="text-red-600 text-sm">{err}</div>}
      {out && <pre className="text-sm bg-gray-50 rounded p-3 overflow-auto">{JSON.stringify(out, null, 2)}</pre>}
    </form>
  );
}
