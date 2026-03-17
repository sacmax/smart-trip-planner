from typing import TypedDict
from smart_trip_planner.models.trip import TripRequest, HotelOption

class HotelsState(TypedDict, total=False):
    request: TripRequest
    raw_hotels: list[HotelOption]
    hotel_options: list[HotelOption]
    errors: list[str]

class HotelsInput(TypedDict):
    request: TripRequest

class HotelsOutput(TypedDict, total=False):
    hotel_options: list[HotelOption]
    errors: list[str]
