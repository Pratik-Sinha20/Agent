# payment_gateway.py
import uuid
from typing import Dict, Any

class PaymentGatewayError(Exception):
    """Custom exception for payment gateway errors"""
    pass

async def initiate_payment(booking_id: str, amount: float) -> Dict[str, Any]:
    """
    Simulate payment initiation.
    Args:
        booking_id: The booking ID for which payment is being made.
        amount: The amount to be paid.
    Returns:
        A dictionary with payment initiation details.
    """
    try:
        payment_id = f"PAY-{uuid.uuid4().hex[:10].upper()}"
        # In a real-world scenario, you would redirect to a payment gateway here
        payment_url = f"https://mock-payment-gateway.com/pay/{payment_id}"
        return {
            "success": True,
            "payment_id": payment_id,
            "booking_id": booking_id,
            "amount": amount,
            "payment_url": payment_url,
            "message": "Payment initiated. Please proceed to the payment gateway."
        }
    except Exception as e:
        raise PaymentGatewayError(f"Failed to initiate payment: {str(e)}") from e

async def process_payment(payment_id: str, booking_id: str, amount: float) -> Dict[str, Any]:
    """
    Simulate payment processing.
    Args:
        payment_id: The payment transaction ID.
        booking_id: The booking ID.
        amount: The amount paid.
    Returns:
        A dictionary with payment confirmation details.
    """
    try:
        # Simulate payment processing logic
        transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        return {
            "success": True,
            "payment_id": payment_id,
            "booking_id": booking_id,
            "amount": amount,
            "transaction_id": transaction_id,
            "status": "completed",
            "message": "Payment successful!"
        }
    except Exception as e:
        raise PaymentGatewayError(f"Failed to process payment: {str(e)}") from e

# Example usage (for testing)
if __name__ == "__main__":
    import asyncio
    async def test():
        booking_id = "BOOK-EXAMPLE"
        amount = 5310.00
        init = await initiate_payment(booking_id, amount)
        print("Initiate Payment:", init)
        proc = await process_payment(init["payment_id"], booking_id, amount)
        print("Process Payment:", proc)
    asyncio.run(test())
