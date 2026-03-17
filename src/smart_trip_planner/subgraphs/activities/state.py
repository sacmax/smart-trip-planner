from typing import TypedDict
from smart_trip_planner.models.trip import TripRequest, ActivityOption


class ActivitiesState(TypedDict, total=False):
    request: TripRequest
    raw_activities: list[ActivityOption]
    activity_options: list[ActivityOption]
    errors: list[str]

class ActivitiesInput(TypedDict):
    request: TripRequest

class ActivitiesOutput(TypedDict, total=False):
    activity_options: list[ActivityOption]
    errors: list[str]
