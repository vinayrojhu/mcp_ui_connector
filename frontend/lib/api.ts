export type Plan = { objective: string; application_id: string; environment: 'browser'|'desktop'; actions: string[]; expected_result: string; risk_level: string; approval_may_be_required: boolean };
export type Step = { type: string; target?: Record<string,string>; value?: string; risk: string; approval_required: boolean };
export type Connector = { schema_version: '1.0'; name: string; application_id: string; environment: 'browser'|'desktop'; inputs: string[]; preconditions: string[]; steps: Step[]; expected_result: string };
const api = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';
export async function propose(request: string) {
  const response = await fetch(`${api}/api/connectors/propose`, { method: 'POST', headers: {'content-type':'application/json'}, body: JSON.stringify({request}) });
  if (!response.ok) throw new Error((await response.json()).detail ?? 'Request failed');
  return response.json() as Promise<{plan:Plan; connector:Connector}>;
}
export async function execute(connector: Connector) {
  const response = await fetch(`${api}/api/executions`, { method:'POST', headers:{'content-type':'application/json'}, body:JSON.stringify(connector) });
  if (!response.ok) throw new Error((await response.json()).detail ?? 'Execution failed');
  return response.json();
}
export async function decideApproval(id: string, approved: boolean) {
  const response = await fetch(`${api}/api/approvals/${id}`, { method:'POST', headers:{'content-type':'application/json'}, body:JSON.stringify({approved}) });
  if (!response.ok) throw new Error((await response.json()).detail ?? 'Approval failed');
  return response.json();
}
