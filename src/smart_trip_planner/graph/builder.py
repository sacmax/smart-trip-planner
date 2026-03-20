from langgraph.graph import StateGraph, START, END
from smart_trip_planner.graph.state import TripState
from smart_trip_planner.graph.nodes import request_parser_node, optimizer_node, budget_enforcer_node, fan_out_node, invalid_request_node
from smart_trip_planner.graph.edges import fan_out_searches, route_after_parse
from smart_trip_planner.subgraphs.flights.graph import build_flights_subgraph
from smart_trip_planner.subgraphs.hotels.graph import build_hotels_subgraph
from smart_trip_planner.subgraphs.activities.graph import build_activities_subgraph



def build_trip_graph(checkpointer=None):
    flights_subgraph = build_flights_subgraph()
    hotels_subgraph = build_hotels_subgraph()
    activities_subgraph = build_activities_subgraph()

    graph = StateGraph(TripState)

    # add nodes
    graph.add_node("parse_request", request_parser_node)
    graph.add_node("optimizer", optimizer_node)
    graph.add_node("budget_enforcer", budget_enforcer_node)
    graph.add_node("fan_out", fan_out_node)
    graph.add_node("invalid_request", invalid_request_node)

    graph.add_node("flights_subgraph",flights_subgraph)
    graph.add_node("hotels_subgraph", hotels_subgraph)
    graph.add_node("activities_subgraph", activities_subgraph)

    # add edges
    graph.add_edge(START, "parse_request")
    graph.add_conditional_edges("parse_request", route_after_parse, {"fan_out": "fan_out", "invalid_request": "invalid_request"})
    graph.add_conditional_edges("fan_out", fan_out_searches, ["flights_subgraph", "hotels_subgraph", "activities_subgraph"])

    graph.add_edge("flights_subgraph", "optimizer")
    graph.add_edge("hotels_subgraph", "optimizer")
    graph.add_edge("activities_subgraph", "optimizer")
    graph.add_edge("optimizer", "budget_enforcer")
    graph.add_edge("budget_enforcer", END)
    graph.add_edge("invalid_request", END)

    return graph.compile(checkpointer=checkpointer)