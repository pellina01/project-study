class tz_correction:
	from datetime import datetime
	import pytz

	def __init__(self, timezone):
		self.timezone = self.pytz.timezone(timezone)

	def set_to_ph(self, time_in_z):
	    dt = self.datetime.strptime(time_in_z, '%Y-%m-%dT%H:%M:%S.%fZ')
	    print(dt)
	    return self.timezone.localize(dt)