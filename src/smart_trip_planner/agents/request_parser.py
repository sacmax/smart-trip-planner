from smart_trip_planner.config import settings
from smart_trip_planner.models.trip import TripRequest
import litellm

SYSTEM_PROMPT = """
You are a helpful and detail-oriented AI travel assistant.
You help users plan trips by searching for flights, hotels, and activities.
Your job is to collect all required trip details from the user's request into a structured format.
Extract the following fields:
  - origin: city the traveler is departing from
  - destination: city the traveler wants to visit
  - departure: departure date in YYYY-MM-DD format
  - return_date: return date in YYYY-MM-DD format
  - travelers: number of people traveling
  - budget_usd: total budget in USD, default 5000 if not mentioned
  - preferences: list of activity preferences, empty list if not mentioned
"""

class RequestParserAgent:
    def __init__(self, llm_client=None):
        self._llm_client = llm_client

    async def run(self, state: dict) -> dict:
        user_input = state["user_input"] 
        try:
            if self._llm_client is not None:
                return self._llm_client.requestparse(state)
            else:
                response = await litellm.acompletion(
                    model=settings.LLM_MODEL,
                    messages=[{"role": "system", "content":SYSTEM_PROMPT},{"role": "user", "content":user_input}],
                    response_format=TripRequest
                )
                trip_request = response.choices[0].message.content
                if isinstance(trip_request, str):
                    parsed_trip_request = TripRequest.model_validate_json(trip_request)
                else:
                    parsed_trip_request = trip_request
                return {"request": parsed_trip_request}
        except Exception as e:
            return {"errors": [f"Failed to parse trip request: {str(e)}"]}
