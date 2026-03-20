import click
import asyncio
from rich.console import Console
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from smart_trip_planner.graph.builder import build_trip_graph
from smart_trip_planner.config import settings
import uuid

async def run_graph(user_input):
    async with AsyncSqliteSaver.from_conn_string(settings.DB_PATH) as checkpointer:
        session_id = str(uuid.uuid4())
        graph = build_trip_graph(checkpointer=checkpointer)
        async for chunk in  graph.astream(
            {"user_input": user_input, "session_id": session_id},
            config={"configurable": {"thread_id": session_id}}
        ):
            if "parse_request" in chunk:
                print("🔍 Request parsed...")
            elif "flights_subgraph" in chunk:
                print("✈️  Flights found")
            elif "hotels_subgraph" in chunk:
                print("🏨  Hotels found")
            elif "activities_subgraph" in chunk:
                print("🎯  Activities found")
            elif "optimizer" in chunk:
                print("📋  Itinerary built")
            elif "budget_enforcer" in chunk:
                print("💰  Budget checked")
        final_state = await graph.aget_state(config={"configurable": {"thread_id": session_id}})
        itinerary = final_state.values.get("itinerary")
        budget_status = final_state.values.get("budget_status")
        errors = final_state.values.get("errors", [])

        console = Console()
        if errors:
            console.print(f"[red]Errors: {errors}[/red]")
        else:
            console.print(itinerary)
            console.print(budget_status)

@click.command()
@click.argument("user_query")
def main(user_query):
    asyncio.run(run_graph(user_query))