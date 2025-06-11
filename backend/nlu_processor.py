# nlu_processor.py
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any

class Intent:
    BOOK_FLIGHT = "book_flight"
    SELECT_FLIGHT = "select_flight"
    PROVIDE_INFO = "provide_info"
    CONFIRM_BOOKING = "confirm_booking"
    PAYMENT = "payment"

def extract_cities(text: str) -> Dict[str, str]:
    """Extract source and destination cities from text"""
    # Common city patterns
    city_patterns = {
        'delhi': ['delhi', 'new delhi', 'del'],
        'mumbai': ['mumbai', 'bombay', 'bom'],
        'bangalore': ['bangalore', 'bengaluru', 'blr'],
        'chennai': ['chennai', 'madras', 'maa'],
        'kolkata': ['kolkata', 'calcutta', 'ccu'],
        'hyderabad': ['hyderabad', 'hyd'],
        'pune': ['pune', 'pnq'],
        'ahmedabad': ['ahmedabad', 'amd']
    }
    
    text_lower = text.lower()
    found_cities = []
    
    for city, variants in city_patterns.items():
        for variant in variants:
            if variant in text_lower:
                found_cities.append(city)
                break
    
    # Extract from/to pattern
    from_to_pattern = r'from\s+(\w+)\s+to\s+(\w+)'
    match = re.search(from_to_pattern, text_lower, re.IGNORECASE)
    
    if match:
        return {
            'source': match.group(1).title(),
            'destination': match.group(2).title()
        }
    elif len(found_cities) >= 2:
        return {
            'source': found_cities[0].title(),
            'destination': found_cities[1].title()
        }
    
    return {}

def extract_date(text: str) -> str:
    """Extract travel date from text"""
    today = datetime.now()
    
    # Tomorrow, today patterns
    if 'tomorrow' in text.lower():
        return (today + timedelta(days=1)).strftime('%Y-%m-%d')
    elif 'today' in text.lower():
        return today.strftime('%Y-%m-%d')
    
    # Date patterns (DD/MM/YYYY, DD-MM-YYYY, etc.)
    date_patterns = [
        r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',
        r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})'
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            try:
                if len(match.group(1)) == 4:  # YYYY-MM-DD format
                    return f"{match.group(1)}-{match.group(2).zfill(2)}-{match.group(3).zfill(2)}"
                else:  # DD/MM/YYYY format
                    return f"{match.group(3)}-{match.group(2).zfill(2)}-{match.group(1).zfill(2)}"
            except:
                pass
    
    # Default to tomorrow if no date found
    return (today + timedelta(days=1)).strftime('%Y-%m-%d')

def classify_intent(text: str, conversation_state: str) -> str:
    """Classify user intent based on text and conversation state"""
    text_lower = text.lower()
    
    # Initial booking intent
    booking_keywords = ['book', 'flight', 'ticket', 'travel']
    if any(keyword in text_lower for keyword in booking_keywords) and 'from' in text_lower and 'to' in text_lower:
        return Intent.BOOK_FLIGHT
    
    # Flight selection
    if conversation_state == 'showing_flights':
        if any(char.isdigit() for char in text) or 'select' in text_lower or 'choose' in text_lower:
            return Intent.SELECT_FLIGHT
    
    # Information providing
    if conversation_state in ['collecting_passenger_info', 'collecting_contact_info']:
        return Intent.PROVIDE_INFO
    
    # Payment confirmation
    if conversation_state == 'payment_confirmation':
        return Intent.PAYMENT
    
    return Intent.PROVIDE_INFO

def process_user_input(text: str, conversation_state: str = None) -> Dict[str, Any]:
    """Main NLU processing function"""
    intent = classify_intent(text, conversation_state)
    entities = {}
    
    if intent == Intent.BOOK_FLIGHT:
        entities.update(extract_cities(text))
        entities['travel_date'] = extract_date(text)
    
    return {
        'intent': intent,
        'entities': entities,
        'original_text': text
    }
