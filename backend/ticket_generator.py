# ticket_generator.py
import os
import uuid
from datetime import datetime
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class TicketGenerationError(Exception):
    """Custom exception for ticket generation errors"""
    pass

def _ensure_ticket_directory() -> str:
    """Create tickets directory if it doesn't exist"""
    try:
        os.makedirs("tickets", exist_ok=True)
        return "tickets"
    except OSError as e:
        raise TicketGenerationError(f"Directory creation failed: {str(e)}") from e

def _generate_text_ticket(booking_data: Dict[str, Any]) -> str:
    """Generate plain text ticket"""
    try:
        ticket_id = f"TXT-{uuid.uuid4().hex[:6].upper()}"
        filename = f"ticket_{booking_data['metadata']['booking_id']}.txt"
        filepath = os.path.join(_ensure_ticket_directory(), filename)
        
        content = f"""
        {'='*50}
        {'FLIGHT TICKET'.center(50)}
        {'='*50}

        Booking ID: {booking_data['metadata']['booking_id']}
        Issue Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        Passenger Information:
        Name: {booking_data['passenger_details']['full_name']}
        Email: {booking_data['passenger_details']['email']}
        Phone: {booking_data['passenger_details']['phone']}
        Age: {booking_data['passenger_details']['age']}

        Flight Details:
        Airline: {booking_data['flight_details']['airline']}
        Flight No: {booking_data['flight_details']['id']}
        Route: {booking_data['flight_details']['source']} → {booking_data['flight_details']['destination']}
        Date: {booking_data['flight_details']['travel_date']}
        Departure: {booking_data['flight_details']['departure']}
        Arrival: {booking_data['flight_details']['arrival']}

        Fare Breakdown:
        Base Fare: ₹{booking_data['flight_details']['base_price']:.2f}
        Taxes: ₹{booking_data['flight_details']['taxes']:.2f}
        Total: ₹{booking_data['flight_details']['total_amount']:.2f}

        Status: {booking_data['metadata']['status'].upper()}
        {'='*50}
        """

        with open(filepath, 'w') as f:
            f.write(content)
        
        return filepath
    except Exception as e:
        raise TicketGenerationError(f"Text ticket generation failed: {str(e)}") from e

def _generate_pdf_ticket(booking_data: Dict[str, Any]) -> str:
    """Generate PDF ticket using ReportLab"""
    try:
        filename = f"ticket_{booking_data['metadata']['booking_id']}.pdf"
        filepath = os.path.join(_ensure_ticket_directory(), filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Add title
        title_style = ParagraphStyle(
            name='Title',
            fontName='Helvetica-Bold',
            fontSize=18,
            alignment=1,
            parent=styles['Heading1']
        )
        elements.append(Paragraph("FLIGHT TICKET", title_style))
        elements.append(Spacer(1, 0.3*inch))

        # Add booking info
        elements.append(Paragraph(f"Booking ID: {booking_data['metadata']['booking_id']}", styles['Normal']))
        elements.append(Paragraph(f"Issue Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))

        # Passenger section
        elements.append(Paragraph("<b>Passenger Information:</b>", styles['Normal']))
        elements.append(Paragraph(f"Name: {booking_data['passenger_details']['full_name']}", styles['Normal']))
        elements.append(Paragraph(f"Email: {booking_data['passenger_details']['email']}", styles['Normal']))
        elements.append(Paragraph(f"Phone: {booking_data['passenger_details']['phone']}", styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))

        # Flight section
        elements.append(Paragraph("<b>Flight Details:</b>", styles['Normal']))
        elements.append(Paragraph(f"Airline: {booking_data['flight_details']['airline']}", styles['Normal']))
        elements.append(Paragraph(f"Flight No: {booking_data['flight_details']['id']}", styles['Normal']))
        elements.append(Paragraph(f"Route: {booking_data['flight_details']['source']} → {booking_data['flight_details']['destination']}", styles['Normal']))
        elements.append(Paragraph(f"Date: {booking_data['flight_details']['travel_date']}", styles['Normal']))
        elements.append(Paragraph(f"Departure: {booking_data['flight_details']['departure']}", styles['Normal']))
        elements.append(Paragraph(f"Arrival: {booking_data['flight_details']['arrival']}", styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))

        # Fare section
        elements.append(Paragraph("<b>Fare Breakdown:</b>", styles['Normal']))
        elements.append(Paragraph(f"Base Fare: ₹{booking_data['flight_details']['base_price']:.2f}", styles['Normal']))
        elements.append(Paragraph(f"Taxes: ₹{booking_data['flight_details']['taxes']:.2f}", styles['Normal']))
        elements.append(Paragraph(f"Total: ₹{booking_data['flight_details']['total_amount']:.2f}", styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))

        # Status
        elements.append(Paragraph(f"<b>Status:</b> {booking_data['metadata']['status'].upper()}", styles['Normal']))

        doc.build(elements)
        return filepath
    except Exception as e:
        raise TicketGenerationError(f"PDF ticket generation failed: {str(e)}") from e

def generate_ticket(booking_data: Dict[str, Any], format: str = 'pdf') -> str:
    """
    Generate flight ticket in specified format
    Args:
        booking_data: Complete booking information
        format: Output format ('pdf' or 'text')
    Returns:
        Path to generated ticket file
    """
    try:
        if format.lower() == 'pdf':
            return _generate_pdf_ticket(booking_data)
        elif format.lower() == 'text':
            return _generate_text_ticket(booking_data)
        else:
            raise TicketGenerationError(f"Unsupported format: {format}")
    except Exception as e:
        raise TicketGenerationError(f"Ticket generation failed: {str(e)}") from e

# Example usage
if __name__ == "__main__":
    sample_booking = {
        "metadata": {
            "booking_id": "BOOK-ABC123",
            "booking_date": "2023-12-25T12:00:00",
            "status": "confirmed",
            "payment_status": "completed"
        },
        "flight_details": {
            "id": "IN-101",
            "airline": "IndiGo",
            "source": "Delhi",
            "destination": "Mumbai",
            "departure": "08:00",
            "arrival": "10:30",
            "price": 4500.00,
            "travel_date": "2023-12-25",
            "base_price": 4500.00,
            "taxes": 810.00,
            "total_amount": 5310.00
        },
        "passenger_details": {
            "full_name": "John Doe",
            "email": "john@example.com",
            "phone": "+911234567890",
            "age": 30,
            "passenger_id": "PAX-123ABC"
        }
    }

    try:
        # Generate PDF ticket
        pdf_path = generate_ticket(sample_booking)
        print(f"PDF ticket generated: {pdf_path}")

        # Generate text ticket
        text_path = generate_ticket(sample_booking, 'text')
        print(f"Text ticket generated: {text_path}")
    except TicketGenerationError as e:
        print(f"Error generating ticket: {e}")
