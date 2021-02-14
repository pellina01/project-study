class dbase:
    from influxdb import InfluxDBClient
    from datetime import datetime
    import pytz

    @staticmethod
    def tz_correction(time_in_z):
        timezone = pytz.timezone("Asia/Manila")
        utc = datetime.strptime(time_in_z, '%Y-%m-%dT%H:%M:%S.%fZ')
        datetime_manila = utc.astimezone(timezone)
        return datetime_manila

    def __init__(self, measurement, database, username, password, influxHost, influxPort=8086):
        self.measurement = measurement

        self.influxClient = self.InfluxDBClient(
            influxHost, influxPort, username, password)
        self.influxClient.switch_database(database)

    def query(self, frm, to):
        self.data = self.influxClient.query(
            "SELECT * FROM {measurement} WHERE time >= '{frm}' AND time <= '{to}'".format(
                measurement=self.measurement,to=to,frm=frm))
        print("SELECT * FROM {measurement} WHERE time >= '{frm}' AND time <= '{to}'".format(
                measurement=self.measurement,to=to,frm=frm))
        self.datapoints = self.data.get_points(measurement=self.measurement)

        self.time = []
        self.amplitude = []

        for point in self.datapoints:
            self.time.append(dbase.tz_correction(point['time']))
            self.amplitude.append(point['value'])

        return self.time, self.amplitude
