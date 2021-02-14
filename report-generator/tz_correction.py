
from datetime import datetime
import pytz

def tz_correction(time_in_z):
    timezone = pytz.timezone("Asia/Manila")
    utc = datetime.strptime(time_in_z, '%Y-%m-%dT%H:%M:%S.%fZ')
    datetime_manila = utc.astimezone(timezone)
    return datetime_manila
