# booking_api.py
import json
import uuid
import os
from datetime import datetime
from typing import Dict, Any
from ticket_generator import generate_ticket

class BookingError(Exception):
    """Custom exception for booking-related errors"""
    pass

def _ensure_directory_exists(directory: str) -> None:
    """Create directory if it doesn't exist"""
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as e:
        raise BookingError(f"Failed to create directory {directory}: {str(e)}") from e

async def create_booking(
    flight_details: Dict[str, Any],
    passenger_info: Dict[str, Any],
    payment_status: str = "pending"
) -> Dict[str, Any]:
    """
    Create a flight booking with complete details
    Args:
        flight_details: Dictionary containing flight information
        passenger_info: Dictionary containing passenger details
        payment_status: Initial payment status (default: "pending")
    Returns:
        Dictionary with booking details and status
    """
    try:
        # Generate unique booking ID
        booking_id = f"BOOK-{uuid.uuid4().hex[:8].upper()}"
        booking_date = datetime.now().isoformat()

        # Calculate total amount with taxes
        base_price = flight_details.get('price', 0)
        taxes = base_price * 0.18  # 18% GST
        total_amount = round(base_price + taxes, 2)

        # Create booking payload
        booking_data = {
            "metadata": {
                "booking_id": booking_id,
                "booking_date": booking_date,
                "status": "confirmed",
                "payment_status": payment_status,
                "source_system": "chatbot_ai"
            },
            "flight_details": {
                **flight_details,
                "travel_date": flight_details.get('travel_date', datetime.now().date().isoformat()),
                "base_price": base_price,
                "taxes": taxes,
                "total_amount": total_amount
            },
            "passenger_details": {
                **passenger_info,
                "passenger_id": f"PAX-{uuid.uuid4().hex[:6].upper()}"
            }
        }

        # Ensure bookings directory exists
        _ensure_directory_exists("bookings")

        # Save booking to JSON file
        booking_path = f"bookings/{booking_id}.json"
        with open(booking_path, 'w') as f:
            json.dump(booking_data, f, indent=2)

        # Generate ticket (PDF/text file)
        ticket_path = generate_ticket(booking_data)

        return {
            "success": True,
            "booking_id": booking_id,
            "booking_data": booking_data,
            "ticket_path": ticket_path,
            "payment_amount": total_amount,
            "next_step": "payment_initiation"
        }

    except json.JSONDecodeError as e:
        raise BookingError(f"JSON encoding error: {str(e)}") from e
    except OSError as e:
        raise BookingError(f"File operation error: {str(e)}") from e
    except Exception as e:
        raise BookingError(f"Unexpected error creating booking: {str(e)}") from e

def get_booking(booking_id: str) -> Dict[str, Any]:
    """
    Retrieve booking details by ID
    Args:
        booking_id: Unique booking identifier
    Returns:
        Dictionary with complete booking details
    """
    try:
        booking_path = f"bookings/{booking_id}.json"
        with open(booking_path, 'r') as f:
            booking_data = json.load(f)
        
        return {
            "success": True,
            "exists": True,
            "booking_id": booking_id,
            "data": booking_data
        }
    except FileNotFoundError:
        return {
            "success": False,
            "exists": False,
            "error": "Booking not found"
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Invalid booking data: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error retrieving booking: {str(e)}"
        }

def update_booking_status(booking_id: str, new_status: str) -> Dict[str, Any]:
    """
    Update booking status (e.g., after payment)
    Args:
        booking_id: Unique booking identifier
        new_status: New status to set
    Returns:
        Dictionary with update result
    """
    try:
        booking = get_booking(booking_id)
        if not booking['success'] or not booking['exists']:
            return booking
        
        booking_data = booking['data']
        booking_data['metadata']['status'] = new_status
        
        with open(f"bookings/{booking_id}.json", 'w') as f:
            json.dump(booking_data, f, indent=2)
        
        return {
            "success": True,
            "booking_id": booking_id,
            "new_status": new_status
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error updating booking: {str(e)}"
        }

# Example usage
if __name__ == "__main__":
    # Test booking creation
    test_flight = {
        "id": "IN-101",
        "airline": "IndiGo",
        "source": "Delhi",
        "destination": "Mumbai",
        "departure": "08:00",
        "arrival": "10:30",
        "price": 4500.00,
        "travel_date": "2023-12-25"
    }
    
    test_passenger = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+911234567890",
        "age": 30
    }
    
    booking = create_booking(test_flight, test_passenger)
    print("Booking created:", booking)
