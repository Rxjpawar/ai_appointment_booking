from langchain_core.tools import tool
from app.database.crud import create_appointment, get_appointments, delete_appointment


@tool
def book_appointment(name: str, email: str, appointment_time: str, reason: str):
    """Book a new appointment."""
    return create_appointment(name, email, appointment_time, reason)


@tool
def list_appointments():
    """List all appointments."""
    return get_appointments()


@tool
def cancel_appointment(appointment_id: int):
    """Cancel an appointment using ID."""
    return delete_appointment(appointment_id)