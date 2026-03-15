from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class TripRequest(BaseModel):
    origin: str
    destination: str
    departure: date
    return_date: date
    budget_usd: float
    travelers: int
    preferences: list[str] = Field(default_factory=list)

class FlightOption(BaseModel):
    airline: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    stops: int
    booking_url: str

class HotelOption(BaseModel):
    name: str
    location: str 
    price_per_night: float
    rating: float = Field(ge=0, le=5)
    amenities: list[str] = Field(default_factory=list)
    booking_url: str

class ActivityOption(BaseModel):
    name: str
    category: str
    duration_hours: float
    price: float
    description: str

class DayPlan(BaseModel):
    day: int
    date: date
    activities: list[ActivityOption] = Field(default_factory=list)
    hotel: Optional[HotelOption] = None
    notes: str = ""

class Itinerary(BaseModel):
    request: TripRequest
    days: list[DayPlan]
    selected_flight: Optional[FlightOption] = None
    total_cost: float
    summary: str

class BudgetStatus(BaseModel):
    budget_usd: float
    allocated: float
    remaining: float
    over_budget: bool
    breakdown: dict[str, float]
