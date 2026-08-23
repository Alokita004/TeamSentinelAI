export type HealthResponse = {
  status: "ok";
  service: string;
  environment: string;
};

export type LoginResponse = {
  access_token: string;
  token_type: "bearer";
  expires_in: number;
};

export type DemoSnapshot = {
  mode: "demo";
  incident: { id: string; status: string; severity: string } | null;
  zones: Array<{ id: string; name: string; risk_level: string; population: number }>;
  shelters: Array<{ id: string; name: string; capacity: number; available: number }>;
  resources: Array<{ id: string; name: string; quantity: number; unit: string }>;
};

export type DemoActionResponse = { action: "simulated" | "reset"; snapshot: DemoSnapshot };

export type ApiError = {
  code: string;
  message: string;
  request_id: string;
};

const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!response.ok) {
    const error = (await response.json()) as { detail?: ApiError };
    throw error.detail ?? { code: "REQUEST_FAILED", message: "API request failed", request_id: "unknown" };
  }
  return response.json() as Promise<T>;
}

export const api = {
  health: () => request<HealthResponse>("/health"),
  login: (email: string, password: string) => request<LoginResponse>("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) }),
  demo: async (action: "simulate" | "reset") => {
    const session = await request<LoginResponse>("/auth/login", { method: "POST", body: JSON.stringify({ email: "admin@sentinelai.example", password: "change-me" }) });
    return request<DemoActionResponse>(action === "simulate" ? "/demo/flood/simulate" : "/demo/reset", { method: "POST", headers: { Authorization: `Bearer ${session.access_token}` } });
  },
  executeFlood: async () => {
    const session = await request<LoginResponse>("/auth/login", { method: "POST", body: JSON.stringify({ email: "admin@sentinelai.example", password: "change-me" }) });
    return request<{ id: string; status: string; events: Array<{ agent_name: string }> }>("/executions/flood", { method: "POST", headers: { Authorization: `Bearer ${session.access_token}` } });
  },
  planOperations: async () => {
    const session = await request<LoginResponse>("/auth/login", { method: "POST", body: JSON.stringify({ email: "admin@sentinelai.example", password: "change-me" }) });
    return request<{ routes: Array<{ id: string; status: string }>; allocations: Array<{ resource_id: string; quantity: number }>; decision: { status: string; capacity_shortfall: number } }>("/operations/incident-flood-042/plan", { method: "POST", headers: { Authorization: `Bearer ${session.access_token}` }, body: JSON.stringify({ blocked_route_ids: [] }) });
  },
  streamFloodEvents: async (onAgent: (agentName: string) => void) => {
    const session = await request<LoginResponse>("/auth/login", { method: "POST", body: JSON.stringify({ email: "admin@sentinelai.example", password: "change-me" }) });
    const response = await fetch(`${apiBaseUrl}/events/flood`, { headers: { Authorization: `Bearer ${session.access_token}`, Accept: "text/event-stream" } });
    if (!response.ok || !response.body) throw new Error("SSE stream unavailable");
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    while (true) {
      const { value, done } = await reader.read();
      buffer += decoder.decode(value ?? new Uint8Array(), { stream: !done });
      const messages = buffer.split("\n\n");
      buffer = messages.pop() ?? "";
      for (const message of messages) {
        const dataLine = message.split("\n").find((line) => line.startsWith("data: "));
        if (!dataLine) continue;
        if (message.includes("event: agent_event")) {
          onAgent(JSON.parse(dataLine.slice(6)).agent_name);
        }
        if (message.includes("event: execution_complete")) {
          onAgent("execution_complete");
        }
      }
      if (done) break;
    }
  },
  askAssistant: async (question: string) => {
    const session = await request<LoginResponse>("/auth/login", { method: "POST", body: JSON.stringify({ email: "admin@sentinelai.example", password: "change-me" }) });
    return request<{ answer: string; intent: string; sources: string[] }>("/assistant/ask", { method: "POST", headers: { Authorization: `Bearer ${session.access_token}` }, body: JSON.stringify({ question }) });
  },
};