'use client';
import { useState } from 'react';
import { Connector, decideApproval, execute, Plan, propose } from '../lib/api';

export default function Home() {
  const [request, setRequest] = useState('');
  const [plan, setPlan] = useState<Plan|null>(null);
  const [connector, setConnector] = useState<Connector|null>(null);
  const [status, setStatus] = useState('Ready for a task');
  const [error, setError] = useState('');
  const [pendingApproval, setPendingApproval] = useState('');
  async function create() { setError(''); setStatus('Planning and checking connector policy…'); try { const result = await propose(request); setPlan(result.plan); setConnector(result.connector); setStatus('Connector proposal is ready for review'); } catch(e) { setError(String(e)); setStatus('Could not create a proposal'); } }
  async function run() { if (!connector) return; setStatus('Executing locally…'); try { const result = await execute(connector); if (result.status === 'pending_approval') { setPendingApproval(result.id); setStatus('Waiting for one-time approval'); } else setStatus(`Completed: ${result.result.summary}`); } catch(e) { setError(String(e)); setStatus('Execution failed'); } }
  async function approve(approved: boolean) { try { const result = await decideApproval(pendingApproval, approved); setPendingApproval(''); setStatus(result.status === 'completed' ? 'Approval granted; execution completed' : 'Execution rejected'); } catch(e) { setError(String(e)); } }
  return <main className="min-h-screen grid lg:grid-cols-[220px_1fr_280px]">
    <nav className="bg-slate-950 text-white p-6 space-y-5"><h1 className="font-bold text-xl">Adaptive UI</h1>{['New Task','Chat Sessions','Connectors','Executions','Approvals','Applications','Settings'].map(x=><div key={x} className="text-slate-300">{x}</div>)}</nav>
    <section className="p-6 lg:p-10 max-w-4xl w-full mx-auto"><p className="text-sm text-indigo-700 font-semibold">WORKFLOW CONSOLE</p><h2 className="text-3xl font-bold mt-2">What should I do?</h2><p className="text-slate-600 mt-2">The planner proposes a workflow. Review it before local execution.</p>
      <div className="mt-8 bg-white rounded-xl border p-5"><label className="font-semibold" htmlFor="task">Describe a task</label><textarea id="task" value={request} onChange={e=>setRequest(e.target.value)} className="mt-3 w-full border rounded-lg p-3 min-h-28" placeholder="Search the fund portal for Fund ABC…"/><button onClick={create} disabled={request.trim().length<3} className="mt-3 px-4 py-2 rounded-lg bg-indigo-700 text-white disabled:opacity-40">Create plan</button></div>
      <p role="status" className="mt-5 text-slate-600">{status}</p>{error&&<p role="alert" className="mt-3 text-red-700">{error}</p>}
      {plan&&<article className="mt-5 bg-white rounded-xl border p-5"><h3 className="text-xl font-bold">Task plan</h3><p className="mt-3"><b>Objective:</b> {plan.objective}</p><p><b>Application:</b> {plan.application_id} ({plan.environment})</p><p><b>Expected result:</b> {plan.expected_result}</p><p><b>Risk:</b> {plan.risk_level} {plan.approval_may_be_required?'· may require approval':''}</p><ul className="list-disc ml-6 mt-2">{plan.actions.map((a,i)=><li key={i}>{a}</li>)}</ul></article>}
      {connector&&<article className="mt-5 bg-white rounded-xl border p-5"><h3 className="text-xl font-bold">Proposed connector</h3><p className="mt-2">{connector.name} · {connector.environment}</p><ol className="list-decimal ml-6 my-3">{connector.steps.map((s,i)=><li key={i}>{s.type} {s.target?.name??s.target?.role??''} <span className="text-slate-500">({s.risk} risk)</span></li>)}</ol><p className="text-sm text-amber-800">MVP executor is simulated. Device control requires a connected local worker.</p><button onClick={run} className="mt-3 px-4 py-2 rounded-lg bg-emerald-700 text-white">Run connector</button></article>}
      {pendingApproval&&<article className="mt-5 rounded-xl border border-amber-300 bg-amber-50 p-5" aria-label="Approval required"><h3 className="text-xl font-bold">Approval required</h3><p className="mt-2">Review the high-risk step above. Approval applies to this execution only.</p><button onClick={()=>approve(true)} className="mt-3 px-4 py-2 rounded-lg bg-amber-800 text-white">Approve once</button><button onClick={()=>approve(false)} className="mt-3 ml-2 px-4 py-2 rounded-lg border">Reject</button></article>}
    </section>
    <aside className="bg-white border-l p-6"><h2 className="font-bold">Execution status</h2><div className="mt-4 text-sm text-slate-600">Application<br/><b className="text-slate-900">{plan?.application_id??'Not selected'}</b></div><div className="mt-4 text-sm text-slate-600">Worker status<br/><b className="text-slate-900">Mock executor</b></div><div className="mt-4 text-sm text-slate-600">Timeline<br/><b className="text-slate-900">{status}</b></div></aside>
  </main>;
}
