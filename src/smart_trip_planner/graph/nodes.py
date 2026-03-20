from smart_trip_planner.agents.request_parser import RequestParserAgent
from smart_trip_planner.agents.optimizer import OptimizerAgent
from smart_trip_planner.agents.budget_enforcer import BudgetEnforcerAgent
from smart_trip_planner.graph.state import TripState

request_parser = RequestParserAgent()
optimizer = OptimizerAgent()
budget_enforcer = BudgetEnforcerAgent()

async def request_parser_node(state: TripState) -> dict:
    return await request_parser.run(state)

async def optimizer_node(state: TripState) -> dict:
    return await optimizer.run(state)

async def budget_enforcer_node(state: TripState) -> dict:
    return await budget_enforcer.run(state)

async def fan_out_node(state: TripState) -> dict:
    return {}

async def invalid_request_node(state: TripState) -> dict:
    return {"errors": ["Origin city not found. Please specify where you are traveling from."]}
