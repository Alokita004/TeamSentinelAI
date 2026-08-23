"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import {
  Activity, AlertTriangle, ArrowUpRight, Bell, Bot, ChevronDown, CircleHelp,
  Gauge, LayoutDashboard, Map, Menu, MessageSquare, Navigation, Network, Radio, Route,
  RefreshCw, Settings, ShieldCheck, Siren, Users, Waves, X,
} from "lucide-react";

const agents = [
  { name: "Alert Agent", detail: "Signal triage", state: "queued" },
  { name: "Risk Agent", detail: "Hazard assessment", state: "queued" },
  { name: "Impact Agent", detail: "Zone analysis", state: "queued" },
  { name: "Graph Agent", detail: "Relationship context", state: "queued" },
  { name: "Route Agent", detail: "Evacuation paths", state: "queued" },
  { name: "Resource Agent", detail: "Capacity matching", state: "queued" },
  { name: "Decision Agent", detail: "Priority recommendation", state: "queued" },
  { name: "Notification Agent", detail: "Response communications", state: "queued" },
];

const buildAllCompleteProgress = () => Object.fromEntries(agents.map((agent) => [agent.name.replace(" ", ""), "complete"]));

const timeline = [
  { time: "14:32:08", title: "Flood signal received", copy: "River gauge cluster 04 crossed alert threshold.", tone: "red" },
  { time: "14:31:42", title: "Risk assessment updated", copy: "Northbank exposure moved to severe.", tone: "amber" },
  { time: "14:30:15", title: "Incident workspace opened", copy: "Urban Flood 042 is now under review.", tone: "blue" },
];

function IconButton({ label, children, onClick }: { label: string; children: React.ReactNode; onClick?: () => void }) {
  return <button className="icon-button" aria-label={label} title={label} onClick={onClick}>{children}</button>;
}

function StatusDot({ tone = "green" }: { tone?: "green" | "amber" | "red" | "blue" }) {
  return <span className={`status-dot ${tone}`} aria-hidden="true" />;
}

export default function Home() {
  const [mobileNav, setMobileNav] = useState(false);
  const [demoActive, setDemoActive] = useState(false);
  const [demoBusy, setDemoBusy] = useState(false);
  const [backendStatus, setBackendStatus] = useState<"idle" | "connected" | "offline">("idle");
  const [liveAgent, setLiveAgent] = useState("Waiting for execution");
  const [agentProgress, setAgentProgress] = useState<Record<string, string>>({});
  const [mapExpanded, setMapExpanded] = useState(false);
  const [assistantQuestion, setAssistantQuestion] = useState("");
  const [assistantAnswer, setAssistantAnswer] = useState("Ask about risk, shelters, evacuation routes, or resources.");
  const [assistantBusy, setAssistantBusy] = useState(false);

  const runDemoAction = async (action: "simulate" | "reset") => {
    setDemoBusy(true);
    try {
      await api.demo(action);
      if (action === "simulate") {
        const queuedState = Object.fromEntries(agents.map((agent) => [agent.name.replace(" ", ""), "queued"]));
        setAgentProgress(queuedState);
        setLiveAgent("Waiting for execution");

        await api.streamFloodEvents((agentName) => {
          if (agentName === "execution_complete") {
            setLiveAgent("All agents complete");
            setAgentProgress(buildAllCompleteProgress());
            return;
          }
          const currentIndex = agents.findIndex((agent) => agent.name.replace(" ", "") === agentName);
          const nextAgent = agents[currentIndex + 1]?.name.replace(" ", "");
          setLiveAgent(nextAgent ? agents[currentIndex + 1].name : "All agents complete");
          setAgentProgress((current) => ({
            ...current,
            [agentName]: "complete",
            ...(nextAgent ? { [nextAgent]: "active" } : {}),
          }));
        });
        await api.planOperations();
      } else {
        setAgentProgress({});
        setLiveAgent("Waiting for execution");
      }
      setDemoActive(action === "simulate");
      setBackendStatus("connected");
    } catch {
      setBackendStatus("offline");
    } finally {
      setDemoBusy(false);
    }
  };

  const askAssistant = async () => {
    const trimmedQuestion = assistantQuestion.trim();
    if (!trimmedQuestion) return;
    setAssistantQuestion("");
    setAssistantBusy(true);
    try {
      const response = await api.askAssistant(trimmedQuestion);
      setAssistantAnswer(response.answer);
      setBackendStatus("connected");
    } catch {
      setAssistantAnswer("The assistant API is unavailable. Start the backend and try again.");
      setBackendStatus("offline");
    } finally {
      setAssistantBusy(false);
    }
  };

  return (
    <main className="app-shell">
      <aside className={`sidebar ${mobileNav ? "open" : ""}`}>
        <div className="brand-lockup">
          <div className="brand-mark"><ShieldCheck size={22} strokeWidth={2.5} /></div>
          <div><strong>SENTINEL<span>AI</span></strong><small>COMMAND CENTER</small></div>
          <IconButton label="Close navigation" onClick={() => setMobileNav(false)}><X size={18} /></IconButton>
        </div>
        <div className="workspace-switcher"><span className="eyebrow">WORKSPACE</span><button className="workspace-button"><span className="workspace-avatar">G</span><span>GOVERNMENT OPS</span><ChevronDown size={15} /></button></div>
        <nav className="primary-nav" aria-label="Primary navigation">
          <span className="eyebrow">OPERATIONS</span>
          <a className="nav-link active" href="#dashboard"><LayoutDashboard size={18} />Dashboard</a>
          <a className="nav-link" href="#map"><Map size={18} />Live Map<span className="nav-badge">4</span></a>
          <a className="nav-link" href="#incidents"><Siren size={18} />Incidents</a>
          <a className="nav-link" href="#resources"><Users size={18} />Resources</a>
          <a className="nav-link" href="#alerts"><Bell size={18} />Alerts</a>
          <span className="eyebrow nav-section-label">INTELLIGENCE</span>
          <a className="nav-link" href="#agents"><Bot size={18} />Agent Pipeline</a>
          <a className="nav-link" href="#assistant"><MessageSquare size={18} />AI Assistant</a>
          <a className="nav-link" href="#audit"><Activity size={18} />Audit Log</a>
        </nav>
        <div className="sidebar-footer"><div className="system-status"><StatusDot /><span>All systems nominal</span><span className="system-pulse" /></div><a className="nav-link" href="#settings"><Settings size={18} />Settings</a><div className="user-profile"><div className="user-avatar">AR</div><div><strong>Alex Rivera</strong><small>Emergency Director</small></div><ChevronDown size={15} /></div></div>
      </aside>

      <section className="main-stage">
        <header className="topbar"><button className="mobile-menu" aria-label="Open navigation" onClick={() => setMobileNav(true)}><Menu size={21} /></button><div className="breadcrumb"><span>OPERATIONS</span><span>/</span><strong>OVERVIEW</strong></div><div className="topbar-actions"><div className="live-indicator"><StatusDot tone={backendStatus === "offline" ? "red" : "green"} />{backendStatus === "offline" ? "API OFFLINE" : "LIVE DATA"}</div><IconButton label="Help"><CircleHelp size={19} /></IconButton><IconButton label="Notifications"><Bell size={19} /><span className="notification-dot" /></IconButton><div className="topbar-time">20 AUG 2026 <b>14:32:08 UTC</b></div></div></header>
        <div className="content" id="dashboard">
          <div className="page-heading"><div><p className="kicker"><span className="kicker-line" />THURSDAY, 20 AUGUST 2026</p><h1>Good afternoon, Alex.</h1><p className="heading-copy">Here&apos;s the current situation across your response network.</p></div><div className="heading-actions"><button className="button secondary" onClick={() => runDemoAction("reset")} disabled={demoBusy}><RefreshCw size={16} />Reset demo</button><button className={`button ${demoActive ? "danger" : "primary"}`} onClick={() => runDemoAction("simulate")} disabled={demoBusy}><Waves size={17} />{demoBusy ? "Connecting to API" : demoActive ? "Flood simulation active" : "Simulate flood emergency"}</button></div></div>
          <div className="alert-strip"><div className="alert-icon"><AlertTriangle size={19} /></div><div><strong>ACTIVE INCIDENT · URBAN FLOOD 042</strong><span>Northbank district · Severity: <b>HIGH</b> · Started 14:30 UTC</span></div><button className="alert-link">View incident <ArrowUpRight size={15} /></button></div>
          <div className="kpi-grid"><KpiCard label="ACTIVE INCIDENTS" value="01" meta="+1 since last hour" icon={<Siren size={18} />} tone="red" trend="up" /><KpiCard label="PEOPLE AT RISK" value="12,480" meta="Northbank · 4 zones" icon={<Users size={18} />} tone="amber" trend="up" /><KpiCard label="SHELTER CAPACITY" value="68%" meta="2,140 spaces available" icon={<ShieldCheck size={18} />} tone="green" progress={68} /><KpiCard label="RESPONSE READINESS" value="94%" meta="All teams operational" icon={<Gauge size={18} />} tone="blue" progress={94} /></div>
          <div className="dashboard-grid">
            <section className="panel map-panel" id="map"><PanelHeader eyebrow="SITUATIONAL AWARENESS" title="Live incident map" action="Expand map" icon={<Map size={17} />} onAction={() => setMapExpanded(true)} /><MapCanvas /><div className="map-footer"><div><span className="footer-label">LAST UPDATED</span><strong>14:32:08 UTC</strong></div><div><span className="footer-label">DATA SOURCES</span><strong><Radio size={13} /> 12 connected</strong></div><button className="text-button" onClick={() => setMapExpanded(true)}>Open full map <ArrowUpRight size={14} /></button></div></section>
            <section className="panel pipeline-panel" id="agents"><PanelHeader eyebrow="ORCHESTRATION" title="Agent pipeline" action="View execution" icon={<Bot size={17} />} /><div className="pipeline-list">{agents.map((agent, index) => { const status = agentProgress[agent.name.replace(" ", "")] ?? agentProgress[agent.name] ?? (Object.keys(agentProgress).length ? "queued" : agent.state); return <div className={`pipeline-row ${status}`} key={agent.name}><div className="pipeline-index">0{index + 1}</div><div className="pipeline-connector" /><div className="agent-icon"><Bot size={15} /></div><div className="agent-copy"><strong>{agent.name}</strong><span>{agent.detail}</span></div><div className="agent-state">{status === "complete" ? <><StatusDot /><span>Complete</span></> : status === "active" ? <><span className="spinner" /><span>Running</span></> : <><span className="queued-dot" /><span>Queued</span></>}</div></div>; })}</div><div className="pipeline-footer"><span><span className="spinner" /> {liveAgent}</span><span>Live SSE</span></div></section>
          </div>
          <div className="lower-grid"><section className="panel recommendation-panel"><PanelHeader eyebrow="DECISION SUPPORT" title="Top recommendation" action="All recommendations" icon={<ShieldCheck size={17} />} /><div className="recommendation-content"><div className="recommendation-priority"><span>PRIORITY 01</span><strong>Initiate Northbank evacuation</strong><p>Move residents in zones Z-04 and Z-05 toward Shelter S-02 before water levels peak.</p></div><div className="recommendation-meta"><div><span>CONFIDENCE</span><strong>96.4%</strong></div><div><span>IMPACT</span><strong>~4,200 people</strong></div><div><span>TRIGGERED BY</span><strong>Risk + Route agents</strong></div></div><button className="button primary full">Review recommendation <ArrowUpRight size={16} /></button></div></section><section className="panel timeline-panel" id="incidents"><PanelHeader eyebrow="AUDIT TRAIL" title="Incident timeline" action="Open audit log" icon={<Activity size={17} />} /><div className="timeline-list">{timeline.map((event) => <div className="timeline-item" key={event.time}><div className={`timeline-marker ${event.tone}`}><Activity size={12} /></div><div className="timeline-copy"><div><strong>{event.title}</strong><time>{event.time}</time></div><p>{event.copy}</p></div></div>)}</div><button className="timeline-more">View all activity <ArrowUpRight size={14} /></button></section></div>
          <section className="panel graph-panel"><PanelHeader eyebrow="RELATIONSHIP INTELLIGENCE" title="Knowledge graph context" action="Open graph" icon={<Network size={17} />} /><div className="graph-canvas"><div className="graph-edge edge-a" /><div className="graph-edge edge-b" /><div className="graph-edge edge-c" /><div className="graph-node incident-node"><Siren size={15} /><span>Incident<br /><b>FLOOD 042</b></span></div><div className="graph-node zone-node"><Map size={14} /><span>Zone<br /><b>NORTHBANK</b></span></div><div className="graph-node shelter-node"><ShieldCheck size={14} /><span>Shelter<br /><b>S-02</b></span></div><div className="graph-node resource-node"><Users size={14} /><span>Rescue team<br /><b>RT-1</b></span></div></div><div className="graph-footer"><span><StatusDot tone="amber" /> Demo projection pending</span><span>4 entities · 3 relationships</span></div></section>
          <section className="panel operations-panel"><PanelHeader eyebrow="EVACUATION + RESOURCES" title="Response plan" action="Review plan" icon={<Route size={17} />} /><div className="operations-content"><div className="operation-row"><span className="operation-icon safe"><Route size={15} /></span><div><strong>Northbank → Shelter S-02</strong><small>Safe route · 1.8 km · 12 min</small></div><b className="operation-value">94% safe</b></div><div className="operation-row"><span className="operation-icon green"><Users size={15} /></span><div><strong>Rescue teams allocated</strong><small>2 teams · 3 ambulances</small></div><b className="operation-value">READY</b></div><div className="operation-row"><span className="operation-icon amber"><AlertTriangle size={15} /></span><div><strong>Shelter capacity shortfall</strong><small>Current plan requires review</small></div><b className="operation-value warning">9,130</b></div></div></section>
          <section className="panel assistant-panel" id="assistant"><PanelHeader eyebrow="ASSISTED RESPONSE" title="AI emergency assistant" action="Tool trace" icon={<MessageSquare size={17} />} /><div className="assistant-content"><div className="assistant-answer"><Bot size={17} /><p>{assistantAnswer}</p></div><div className="assistant-input"><input value={assistantQuestion} onChange={(event) => setAssistantQuestion(event.target.value)} onKeyDown={(event) => { if (event.key === "Enter") void askAssistant(); }} placeholder="Ask an operational question..." aria-label="Ask the emergency assistant" /><button className="button primary" onClick={() => void askAssistant()} disabled={assistantBusy}>{assistantBusy ? "Checking..." : "Ask assistant"}<ArrowUpRight size={15} /></button></div></div></section>
        </div>
      </section>
      {mapExpanded && <div className="map-modal" role="dialog" aria-modal="true" aria-label="Expanded incident map"><div className="map-modal-header"><div><span className="eyebrow">SITUATIONAL AWARENESS</span><h2>Live incident map</h2></div><IconButton label="Close full map" onClick={() => setMapExpanded(false)}><X size={19} /></IconButton></div><MapCanvas expanded /></div>}
    </main>
  );
}

function KpiCard({ label, value, meta, icon, tone, trend, progress }: { label: string; value: string; meta: string; icon: React.ReactNode; tone: string; trend?: string; progress?: number }) { return <article className="kpi-card"><div className="kpi-top"><span>{label}</span><span className={`kpi-icon ${tone}`}>{icon}</span></div><div className="kpi-value">{value}{trend && <span className={`trend ${trend}`}><ArrowUpRight size={14} /></span>}</div><div className="kpi-meta">{progress ? <div className="progress-track"><span style={{ width: `${progress}%` }} /></div> : <span className={`meta-dot ${tone}`} />}<span>{meta}</span></div></article>; }
function PanelHeader({ eyebrow, title, action, icon, onAction }: { eyebrow: string; title: string; action: string; icon: React.ReactNode; onAction?: () => void }) { return <div className="panel-header"><div><span className="eyebrow">{eyebrow}</span><h2>{title}</h2></div><button className="panel-action" onClick={onAction}>{icon}{action}<ArrowUpRight size={13} /></button></div>; }
function MapCanvas({ expanded = false }: { expanded?: boolean }) { return <div className={`map-canvas ${expanded ? "expanded" : ""}`}><div className="map-label north">NORTHBANK</div><div className="map-label east">EAST QUAY</div><div className="map-label south">SOUTH DISTRICT</div><div className="map-river" /><div className="map-road road-one" /><div className="map-road road-two" /><div className="map-road road-three" /><div className="map-road road-four" /><div className="map-zone zone-one" /><div className="map-zone zone-two" /><div className="map-zone zone-three" /><MapPin x="39%" y="34%" type="alert" label="Z-04" /><MapPin x="58%" y="48%" type="shelter" label="S-02" /><MapPin x="68%" y="67%" type="team" label="RT-1" /><div className="map-scale"><span>0</span><i /><span>1 km</span></div><div className="map-legend"><span><i className="legend-dot red" />High risk</span><span><i className="legend-dot yellow" />Moderate</span><span><i className="legend-dot cyan" />Shelter</span></div><div className="map-controls"><IconButton label="Zoom in">+</IconButton><IconButton label="Zoom out">−</IconButton><IconButton label="Center map"><Navigation size={15} /></IconButton></div></div>; }
function MapPin({ x, y, type, label }: { x: string; y: string; type: string; label: string }) { return <div className={`map-pin ${type}`} style={{ left: x, top: y }}><span>{type === "alert" ? <AlertTriangle size={13} /> : type === "shelter" ? <ShieldCheck size={13} /> : <Users size={13} />}</span><b>{label}</b></div>; }
