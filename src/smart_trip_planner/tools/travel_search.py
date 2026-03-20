from smart_trip_planner.models.trip import FlightOption, HotelOption, ActivityOption
from datetime import date, datetime
from smart_trip_planner.config import settings

def _mock_flights(origin, destination, departure):
    return [FlightOption(airline="A airways",departure_time="2026-03-28 15:30", arrival_time="2026-03-28 21:30",price=1000.0,stops=0,booking_url="a-airways.com"),FlightOption(airline="B airways",departure_time="2026-03-28 10:30", arrival_time="2026-03-28 22:30",price=700.0,stops=1,booking_url="b-airways.com"),FlightOption(airline="C airways",departure_time="2026-03-28 15:30", arrival_time="2026-03-29 05:30",price=500.0,stops=2,booking_url="c-airways.com")]

def _mock_hotels(destination, nights, travellers):
    return [HotelOption(name="A hotel",location="a street",price_per_night=150.0,rating=3.0,amenities=["swimming-pool","games-rooom"],booking_url="a-hotel.com"),HotelOption(name="B hotel",location="b street",price_per_night=250.0,rating=4.0,amenities=["swimming-pool","games-rooom","party-room"],booking_url="b-hotel.com"),HotelOption(name="C hotel",location="c street",price_per_night=90.0,rating=3.5,amenities=["games-rooom"],booking_url="c-hotel.com")]

def _mock_activities(destination, preferences):
    return [ActivityOption(name="Mount Climbing",category="outdoors",duration_hours=2.0,price=150.0,description="Mount Climbing"),ActivityOption(name="Horse Riding",category="outdoors",duration_hours=1.0,price=100.0,description="Horse Riding"), ActivityOption(name="Spa Treatment",category="indoors",duration_hours=3.0,price=300.0,description="Spa Treatment"),ActivityOption(name="Pickle ball",category="outdoors",duration_hours=1.0,price=50.0,description="Pickle ball"), ActivityOption(name="Painting Class",category="indoors",duration_hours=2.0,price=75.0,description="Painting Class"), ActivityOption(name="Pottery Class",category="indoors",duration_hours=2.0,price=150.0,description="Pottery Class"), ActivityOption(name="Bird Watching",category="outdoors",duration_hours=2.0,price=100.0,description="Bird Watching"), ActivityOption(name="Trekking",category="outdoors",duration_hours=4.0,price=200.0,description="Trekking"), ActivityOption(name="Grilling Class",category="outdoors",duration_hours=2.0,price=50.0,description="Grilling Class"), ActivityOption(name="Paintball",category="outdoors",duration_hours=1.0,price=100.0,description="Paintball")]


async def search_flights(origin: str, destination: str, departure: date, travelers: int) -> list[FlightOption]:
    if settings.TRAVEL_PROVIDER == "mock":
        return _mock_flights(origin, destination, departure)
    else:
        raise NotImplementedError(f"Function for {settings.TRAVEL_PROVIDER} not implemented")

async def search_hotels(destination: str, check_in: date, nights: int, travelers: int) -> list[HotelOption]:
    if settings.TRAVEL_PROVIDER == "mock":
        return _mock_hotels(destination, nights, travelers)
    else:
        raise NotImplementedError(f"Function for {settings.TRAVEL_PROVIDER} not implemented")


async def search_activities(destination: str, preferences: list[str] | None = None) -> list[ActivityOption]:
    if settings.TRAVEL_PROVIDER == "mock":
        return _mock_activities(destination, preferences)
    else:
        raise NotImplementedError(f"Function for {settings.TRAVEL_PROVIDER} not implemented")


