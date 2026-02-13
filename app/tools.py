from langchain_core.tools import tool
from datetime import datetime
import pytz
@tool
def get_current_time():
    """
    Returns current date and time of city in ISO-8601 format.
    this tool is used for current time and date of city
    """
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(tz)
    return now.strftime("%H:%M:%S")

