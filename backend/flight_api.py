# flight_api.py
from typing import List, Dict, Any
import requests
from datetime import datetime, timedelta

API_KEY = "kwuRgLP2BMdtx7BxUONmkQYZAgaDwDPQ"
SECRET_KEY = "aYPnJ5NZSxqOBGJT"

def get_auth_token() -> str:
    """Get authentication token using API credentials"""
    auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    response = requests.post(
        auth_url,
        data={"grant_type": "client_credentials"},
        auth=(API_KEY, SECRET_KEY)
    )
    return response.json()["access_token"]

async def search_flights(source: str, destination: str, travel_date: str) -> List[Dict[str, Any]]:
    """Search flights using actual API"""
    try:
        token = get_auth_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        api_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        params = {
            "origin": source.upper(),  # Expects IATA codes
            "destination": destination.upper(),
            "date": travel_date,
            "adults": 1
        }

        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        
        return process_api_response(response.json())
    
    except requests.exceptions.RequestException as e:
        print(f"API Error: {str(e)}")
        return []

def process_api_response(api_data: dict) -> List[Dict[str, Any]]:
    results = []
    for offer in api_data.get("data", []):
        itinerary = offer["itineraries"][0]["segments"][0]
        results.append({
            "id": offer["id"],
            "airline": itinerary["carrierCode"],
            "departure": itinerary["departure"]["at"],
            "arrival": itinerary["arrival"]["at"],
            "duration": itinerary["duration"],
            "price": offer["price"]["total"],
            "seats_available": offer.get("numberOfBookableSeats", "N/A")
        })
    return results


def format_flights_display(flights: List[Dict]) -> str:
    """Improved formatting with error handling"""
    if not flights:
        return "🚫 No flights found for your route. Try different cities or dates."
    
    display = [
        f"**Available Flights** ({len(flights)} options)\n",
        "--------------------------------------------------"
    ]
    
    for i, flight in enumerate(flights, 1):
        display.append(
            f"{i}. {flight['airline']} ({flight['id']})\n"
            f"   🕒 {flight['departure']} → {flight['arrival']} "
            f"({flight['duration']})\n"
            f"   💰 ₹{flight['price']} | 🪑 {flight['seats_available']} seats"
        )
    
    display.append("\n🔢 Reply with flight number to book")
    return "\n".join(display)

# Add this to flight_api.py
async def get_flight_details(flight_id: str) -> Dict[str, Any]:
    """Get detailed flight information from API"""
    try:
        token = get_auth_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        api_url = f"https://api.example-flight-provider.com/v1/flights/{flight_id}"
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        api_data = response.json()
        return {
            'id': api_data['flightNumber'],
            'airline': api_data['carrier']['name'],
            'departure': api_data['departure']['time'],
            'arrival': api_data['arrival']['time'],
            'duration': api_data['duration'],
            'price': api_data['price']['total'],
            'seats_available': api_data['availability']['seats'],
            'aircraft': api_data['aircraft']['model'],
            'baggage_allowance': api_data['baggage']['allowance']
        }
    
    except requests.exceptions.RequestException as e:
        print(f"API Error: {str(e)}")
        return {}
    except KeyError as e:
        print(f"Missing key in API response: {str(e)}")
        return {}

