from pydantic import BaseModel, EmailStr
from typing import Optional

class PassengerDetails(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str]
    age: int

class BookingRequest(BaseModel):
    flight_id: str
    passenger_details: PassengerDetails
