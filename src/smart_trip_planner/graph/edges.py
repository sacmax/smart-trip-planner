from langgraph.types import Send
from smart_trip_planner.graph.state import TripState

def fan_out_searches(state: TripState) -> list[Send]:
    request = state["request"]
    return [
        Send("flights_subgraph", {"request": request}),
        Send("hotels_subgraph", {"request": request}),
        Send("activities_subgraph", {"request": request})
    ]

def route_after_parse(state: TripState) -> str:
    request = state.get("request")
    if not request or not request.origin:
        return "invalid_request"
    else:
        return "fan_out"