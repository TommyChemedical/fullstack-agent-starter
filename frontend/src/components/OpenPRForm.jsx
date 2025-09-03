import { useState } from 'react';
import { openPR } from '../lib/api';

export default function OpenPRForm(){
  const [title, setTitle] = useState('feat: change by agent');
  const [body, setBody] = useState('Automated PR');
  const [base, setBase] = useState('main');
  const [out, setOut] = useState(null);
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);

  const submit = async (e)=>{
    e.preventDefault(); setBusy(true); setErr(''); setOut(null);
    try{
      const res = await openPR({ title, body, base });
      setOut(res);
    }catch(e){ setErr(String(e)); }
    finally{ setBusy(false); }
  };

  return (
    <form onSubmit={submit} className="card space-y-3">
      <h2 className="text-xl font-semibold">PR öffnen</h2>
      <div>
        <label className="label">Title</label>
        <input className="input mt-1" value={title} onChange={e=>setTitle(e.target.value)} />
      </div>
      <div>
        <label className="label">Body</label>
        <input className="input mt-1" value={body} onChange={e=>setBody(e.target.value)} />
      </div>
      <div>
        <label className="label">Base (z.B. main)</label>
        <input className="input mt-1" value={base} onChange={e=>setBase(e.target.value)} />
      </div>
      <button className="btn" disabled={busy}>{busy? 'Sende…':'Senden'}</button>
      {err && <div className="text-red-600 text-sm">{err}</div>}
      {out && <div className="text-sm">PR #{out.number}: <a className="text-blue-600 underline" href={out.url} target="_blank" rel="noreferrer">{out.url}</a></div>}
    </form>
  );
}
