from datetime import timedelta
from smart_trip_planner.models.trip import DayPlan, Itinerary

class OptimizerAgent:
    async def run(self, state: dict) -> dict:
        if not state["flight_options"]:
            return {"errors": ["No flights found, cannot build itinerary"]}
        if not state["hotel_options"]:
            return {"errors": ["No hotels found, cannot build itinerary"]}
        if not state["activity_options"]:
            return {"errors": ["No activity found, cannot build itinerary"]}
        best_flight = state["flight_options"][0]
        best_hotel = state["hotel_options"][0]
        total_nights = (state["request"].return_date - state["request"].departure).days
        activities_per_day = 2
        total_activities_to_take = activities_per_day * total_nights
        selected_activities = state["activity_options"][:total_activities_to_take]

        days = []
        for day_num in range(total_nights):
            day_date = state["request"].departure + timedelta(days=day_num)
            day_activities = selected_activities[day_num * activities_per_day: (day_num + 1) * activities_per_day]
            day_plan = DayPlan(
                day=day_num + 1,
                date=day_date,
                activities=day_activities,
                hotel=best_hotel
            )
            days.append(day_plan)
        
        total_cost = best_flight.price + best_hotel.price_per_night * total_nights + sum(act.price for act in selected_activities)
        return {"itinerary": Itinerary(request=state["request"], days=days, selected_flight=best_flight,total_cost=total_cost, summary=f"{total_nights}-night trip to {state['request'].destination} for {state['request'].travelers} traveler(s). Total cost: ${total_cost:.2f}")}

