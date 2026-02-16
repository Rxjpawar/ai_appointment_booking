from langchain_core.tools import tool
from app.database.crud import create_appointment, get_appointments, delete_appointment
from datetime import datetime
import pytz

#DATABASE TOOLS
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


#current date and time tool
@tool
def get_current_date_time():
    """
    Returns current date and time of city in ISO-8601 format.
    this tool is used for current time and date of city
    """
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(tz)
    return now.strftime("%H:%M:%S")