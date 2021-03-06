class dbase:
    from influxdb import InfluxDBClient

    def __init__(self, tz_corrector, measurement, database, username, password, influxHost, influxPort=8086):
        self.measurement = measurement
        self.tz_corrector = tz_corrector
        self.influxClient = self.InfluxDBClient(
            influxHost, influxPort, username, password)
        self.influxClient.switch_database(database)

    def query(self, frm, to):
        self.data = self.influxClient.query(
            "SELECT * FROM {measurement} WHERE time >= '{frm}' AND time <= '{to}'".format(
                measurement=self.measurement, to=to, frm=frm))
        self.datapoints = self.data.get_points(measurement=self.measurement)

        self.time = []
        self.amplitude = []
        self.time_string = []

        for point in self.datapoints:
            self.time.append(self.tz_corrector.get_datetime(point['time']))
            self.amplitude.append(point['value'])
            self.time_string.append(
                self.tz_corrector.get_string(point['time']))

        return self.time, self.amplitude, self.tz_corrector.get_datetime(frm), self.tz_corrector.get_datetime(to)

    def date_value_string_list(self):
        if len(self.amplitude) > 0:
            return self.amplitude, self.time_string
        else:
            return ["no data"], ["no data"]
