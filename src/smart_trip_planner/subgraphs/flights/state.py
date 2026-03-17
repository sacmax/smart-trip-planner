from typing import TypedDict
from smart_trip_planner.models.trip import TripRequest, FlightOption

class FlightsState(TypedDict, total=False):
    request: TripRequest
    raw_flights: list[FlightOption]
    flight_options: list[FlightOption]
    errors: list[str]

class FlightsInput(TypedDict):
    request: TripRequest

class FlightsOutput(TypedDict, total=False):
    flight_options: list[FlightOption]
    errors: list[str]
