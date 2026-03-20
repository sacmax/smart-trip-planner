from typing import TypedDict, Annotated
from smart_trip_planner.models.trip import TripRequest, FlightOption, HotelOption, ActivityOption, Itinerary, BudgetStatus
import operator

class TripState(TypedDict, total=False):
    user_input: str
    request: TripRequest
    flight_options: list[FlightOption]
    hotel_options: list[HotelOption]
    activity_options: list[ActivityOption]
    itinerary: Itinerary
    budget_status: BudgetStatus
    errors: Annotated[list[str], operator.add]
    session_id: str


