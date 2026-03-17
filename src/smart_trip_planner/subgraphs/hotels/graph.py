from smart_trip_planner.tools.travel_search import search_hotels
from smart_trip_planner.subgraphs.hotels.state import HotelsState, HotelsInput, HotelsOutput
from langgraph.graph import StateGraph, START, END
from typing import Literal

async def search_hotels_node(state: HotelsState) -> dict:
    try:
        destination = state["request"].destination
        check_in = state["request"].departure
        nights = (state["request"].return_date - check_in).days
        travelers = state["request"].travelers
        hotels = await search_hotels(destination, check_in, nights, travelers)
        return {"raw_hotels": hotels, "errors": []}
    except Exception as e:
        return {"raw_hotels": [], "errors": [str(e)]}

def rank_hotels_node(state: HotelsState) -> dict:
    raw_hotels = state["raw_hotels"]
    #Sort by rating descending, then price ascending
    sorted_hotels = sorted(raw_hotels, key=lambda x: (-x.rating, x.price_per_night))
    return {"hotel_options": sorted_hotels}

def should_rank(state: HotelsState) -> Literal["rank_hotels", "END"]:
    if state["raw_hotels"]:
        return "rank_hotels"
    else:
        return "END"

def build_hotels_subgraph():
    graph = StateGraph(HotelsState, input=HotelsInput, output=HotelsOutput)
    graph.add_node("search_hotels", search_hotels_node)
    graph.add_node("rank_hotels", rank_hotels_node)

    graph.add_edge(START, "search_hotels")
    graph.add_conditional_edges("search_hotels", should_rank, {"rank_hotels":"rank_hotels", "END": END})
    return graph.compile()