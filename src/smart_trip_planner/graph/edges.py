from langgraph.types import Send
from smart_trip_planner.graph.state import TripState

def fan_out_searches(state: TripState) -> list[Send]:
    request = state["request"]
    return [
        Send("flights_subgraph", {"request": request}),
        Send("hotels_subgraph", {"request": request}),
        Send("activities_subgraph", {"request": request})
    ]
