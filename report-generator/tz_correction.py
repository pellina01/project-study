class tz_correction:
    from datetime import datetime, timezone
    import pytz

    def __init__(self, timezone):
        self.tzone = self.pytz.timezone(timezone)

    def get_string(self, time_in_z):
        try:
            unaware = self.datetime.strptime(time_in_z, '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            unaware = self.datetime.strptime(time_in_z, '%Y-%m-%dT%H:%M:%SZ')
        utc_aware = unaware.replace(tzinfo=self.pytz.utc)
        tz_aware = utc_aware.astimezone(self.tzone)

        return tz_aware.strftime('%Y-%m-%d %I:%M %p')

    def get_datetime(self, time_in_z):
        try:
            unaware = self.datetime.strptime(time_in_z, '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            unaware = self.datetime.strptime(time_in_z, '%Y-%m-%dT%H:%M:%SZ')
        utc_aware = unaware.replace(tzinfo=self.pytz.utc)
        return utc_aware.astimezone(self.tzone)

