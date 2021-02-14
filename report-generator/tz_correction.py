class tz_correction:
	from datetime import datetime
	import pytz

	def __init__(self):
		self.timezone = self.pytz.timezone("Asia/Manila")

	def set_to_ph(self, time_in_z):
	    utc = self.datetime.strptime(time_in_z, '%Y-%m-%dT%H:%M:%S.%fZ')
	    datetime_manila = utc.astimezone(self.timezone)
	    return datetime_manila
