from smart_trip_planner.models.trip import BudgetStatus

class BudgetEnforcerAgent:

    async def run(self, state: dict) -> dict:
        itinerary = state["itinerary"]
        total_nights = (itinerary.request.return_date - itinerary.request.departure).days
        flight_cost = itinerary.selected_flight.price
        hotel_cost = itinerary.days[0].hotel.price_per_night * total_nights
        activities_cost =  itinerary.total_cost - flight_cost - hotel_cost
        original_budget = itinerary.request.budget_usd
        breakdown = {"flights": flight_cost, "hotels": hotel_cost, "activities": activities_cost }
        allocated = itinerary.total_cost
        remaining = original_budget - allocated
        over_budget = remaining < 0

        return {"budget_status": BudgetStatus(budget_usd=original_budget, allocated=allocated, remaining=remaining, over_budget=over_budget, breakdown=breakdown)} 