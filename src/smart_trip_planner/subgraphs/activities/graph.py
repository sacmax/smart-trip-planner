from smart_trip_planner.subgraphs.activities.state import ActivitiesState, ActivitiesInput, ActivitiesOutput
from smart_trip_planner.tools.travel_search import search_activities
from langgraph.graph import StateGraph, START, END
from typing import Literal



async def search_activities_node(state: ActivitiesState) -> dict:
    try:
        destination = state["request"].destination
        preferences = state["request"].preferences
        activities = await search_activities(destination, preferences)
        return {"raw_activities": activities, "errors": []}
    except Exception as e:
        return {"raw_activities": [], "errors": [str(e)]}

def rank_activities_node(state: ActivitiesState) -> dict:
    raw_activities  = state["raw_activities"]
    preferences = state["request"].preferences
    sorted_activities = sorted(raw_activities, key=lambda x: (x.category not in preferences, x.price))
    return {"activity_options": sorted_activities} 

def should_rank(state: ActivitiesState) -> Literal["rank_activities", "END"]:
    if state["raw_activities"]:
        return "rank_activities"
    else:
        return "END"
    
def build_activities_subgraph():
    graph = StateGraph(ActivitiesState, input=ActivitiesInput, output=ActivitiesOutput)
    graph.add_node("search_activities", search_activities_node)
    graph.add_node("rank_activities", rank_activities_node)

    graph.add_edge(START, "search_activities")
    graph.add_conditional_edges("search_activities", should_rank, {"rank_activities": "rank_activities", "END": END})
    return graph.compile()