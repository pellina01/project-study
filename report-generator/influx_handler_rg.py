class dbase:
    from influxdb import InfluxDBClient

    def __init__(self, measurement, database, username, password, influxHost, influxPort=8086):
        self.measurement = measurement

        self.influxClient = self.InfluxDBClient(
            influxHost, influxPort, username, password)
        self.influxClient.switch_database(database)

    def query(self, frm, to):
        self.data = self.influxClient.query(
            'SELECT * FROM {measurement} WHERE time > {time}'.format(
                measurement=self.measurement, time=(int(to)-int(frm))*1000000000))
        self.datapoints = self.data.get_points(measurement=self.measurement)

        self.time = []
        self.amplitude = []

        for point in self.datapoints:
            self.time.append(point['time'])
            self.amplitude.append(point['value'])

        return self.time, self.amplitude