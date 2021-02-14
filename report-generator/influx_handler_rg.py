class dbase:
    from influxdb import InfluxDBClient

    def __init__(self, measurement, database, username, password, influxHost, influxPort=8086, tz_corrector):
        self.measurement = measurement
        self.tz_corrector = tz_corrector
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
            self.time.append(self.tz_corrector(point['time']))
            self.amplitude.append(point['value'])

        return self.time, self.amplitude
