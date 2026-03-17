from smart_trip_planner.tools.travel_search import search_flights
from smart_trip_planner.subgraphs.flights.state import FlightsState, FlightsInput, FlightsOutput
from langgraph.graph import StateGraph, START, END
from typing import Literal

async def search_flights_node(state: FlightsState) -> dict:
    try:
        origin = state["request"].origin
        destination = state["request"].destination
        departure = state["request"].departure
        travelers = state["request"].travelers
        flights = await search_flights(origin, destination, departure, travelers)
        return {"raw_flights": flights, "errors":[]}
    except Exception as e:
        return {"raw_flights": [], "errors": [str(e)]}

def rank_flights_node(state: FlightsState) -> dict:
    raw_flights = state["raw_flights"]
    #Sort by  price ascending
    sorted_flights = sorted(raw_flights, key=lambda x: x.price)
    return {"flight_options": sorted_flights}

def should_rank(state: FlightsState) -> Literal["rank_flights", "END"]:
    if state["raw_flights"]:
        return "rank_flights"
    else:
        return "END"

def build_flights_subgraph():
    graph = StateGraph(FlightsState, input=FlightsInput, output=FlightsOutput)
    graph.add_node("search_flights", search_flights_node)
    graph.add_node("rank_flights", rank_flights_node)

    graph.add_edge(START, "search_flights")
    graph.add_conditional_edges("search_flights", should_rank, {"rank_flights": "rank_flights", "END": END})
    return graph.compile()


