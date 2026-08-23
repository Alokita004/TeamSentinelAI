from langgraph.graph import END, START, StateGraph

from app.agents.nodes import AGENT_NODES, AGENT_ORDER
from app.agents.state import DisasterState


def build_disaster_graph():
    graph = StateGraph(DisasterState)
    for agent_name in AGENT_ORDER:
        graph.add_node(agent_name, AGENT_NODES[agent_name])
    graph.add_edge(START, AGENT_ORDER[0])
    for current, following in zip(AGENT_ORDER, AGENT_ORDER[1:]):
        graph.add_edge(current, following)
    graph.add_edge(AGENT_ORDER[-1], END)
    return graph.compile()


DISASTER_GRAPH = build_disaster_graph()
