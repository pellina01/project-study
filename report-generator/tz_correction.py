class tz_correction:
	from datetime import datetime
	import pytz

	def __init__(self, timezone):
		self.timezone = self.pytz.timezone(timezone)

	def set_to_ph(self, time_in_z):
		utc = self.datetime.strptime(time_in_z, '%Y-%m-%dT%H:%M:%S.%fZ')
		datetime_manila = utc.astimezone(self.timezone)
		return datetime_manila.strftime('%Y-%m-%d %I:%M %p')

	def get_datetime_obj(self, frm, to):
	    new_frm = self.datetime.strptime(frm, '%Y-%m-%dT%H:%M:%S.%fZ')
	    new_frm = new_frm.astimezone(self.timezone)
	    new_to = self.datetime.strptime(frm, '%Y-%m-%dT%H:%M:%S.%fZ')
	    new_to = new_to.astimezone(self.timezone)
	    return new_frm.strftime('%Y-%m-%d %I:%M %p'), new_to.strftime('%Y-%m-%d %I:%M %p')