
'use client';
import React, { useMemo, useState } from 'react';
type Message = { role: 'user' | 'assistant' | 'system'; content: string };
type ToolEvent = { name: string; input: any; output: any };
type Offer = { id: string; name: string; copy: string; cta: { label: string } };
type Reply = { text: string; media?: any };
type OrchestrateRes = { reply: Reply; offers: Offer[]; tool_events: ToolEvent[] };
const personas = [
  { id: 'teller-v1', label: 'Teller' },
  { id: 'exec-v1', label: 'Exec' },
  { id: 'kiosk-v1', label: 'Kiosk' },
  { id: 'budget-v1', label: 'Budget' },
];
export default function Chat() {
  const [persona, setPersona] = useState(personas[0].id);
  const [messages, setMessages] = useState<Message[]>([{ role: 'system', content: 'You are using the Agent Orchestration MVP' }]);
  const [input, setInput] = useState('Hey, what can you do for me today?');
  const [busy, setBusy] = useState(false);
  const [events, setEvents] = useState<ToolEvent[]>([]);
  const [offers, setOffers] = useState<Offer[]>([]);
  const userId = useMemo(() => 'u-' + Math.random().toString(36).slice(2, 8), []);
  async function send() {
    if (!input.trim()) return;
    setBusy(true);
    const next = [...messages, { role: 'user', content: input }];
    setMessages(next);
    try {
      const res = await fetch('/api/orchestrate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ persona, user_id: userId, messages: next }),
      });
      if (!res.ok) throw new Error('Bad response');
      const data: OrchestrateRes = await res.json();
      setMessages((m) => [...m, { role: 'assistant', content: data.reply.text }]);
      setEvents(data.tool_events || []);
      setOffers(data.offers || []);
      setInput('');
    } catch (err: any) {
      setMessages((m) => [...m, { role: 'assistant', content: 'Error: ' + err.message }]);
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="card">
      <div className="row" style={{ justifyContent: 'space-between' }}>
        <div className="row">
          <span className="badge">User: {userId}</span>
          <span className="badge">Persona:</span>
          <select value={persona} onChange={(e) => setPersona(e.target.value)}>
            {personas.map((p) => <option key={p.id} value={p.id}>{p.label}</option>)}
          </select>
        </div>
      </div>
      <div style={{ marginTop: 16 }}>
        {messages.map((m, i) => (
          <div key={i} className="row" style={{ alignItems: 'flex-start' }}>
            <div className="badge">{m.role}</div>
            <div>{m.content}</div>
          </div>
        ))}
      </div>
      <div className="row" style={{ marginTop: 12 }}>
        <input className="input" value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') send(); }} />
        <button className="btn" onClick={send} disabled={busy}>{busy ? 'Sending…' : 'Send'}</button>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginTop: 16 }}>
        <div className="card">
          <h3>Tool Events</h3>
          {events.length === 0 ? <p className="small">No tools called yet.</p> : events.map((ev, i) => (
            <pre key={i} className="tool">{JSON.stringify(ev, null, 2)}</pre>
          ))}
        </div>
        <div className="card">
          <h3>Offers</h3>
          {offers.length === 0 ? <p className="small">No offers yet.</p> : offers.map((o) => (
            <div key={o.id} className="offer">
              <div><strong>{o.name}</strong></div>
              <div className="small">{o.copy}</div>
              <div style={{ marginTop: 6 }}><button className="btn">{o.cta.label}</button></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
