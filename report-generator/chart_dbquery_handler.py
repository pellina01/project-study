class chart:
    from matplotlib import pyplot as plt 
    from influxdb import InfluxDBClient

    def __init__(self, database, measurement, username, password, influxHost, influxPort=8086):
        self.measurement = measurement

        self.influxClient = self.InfluxDBClient(
            influxHost, influxPort, username, password)
        self.influxClient.switch_database(database)

    def query_db(self, frm, to):
        self.data = self.influxClient.query(
            'SELECT * FROM {measurement} WHERE time > {time}'.format(
                measurement=self.measurement,time=to-frm))
        self.datapoints = self.data.get_points(measurement=self.measurement)

        self.time = []
        self.amplitude = []

        for point in self.datapoints:
            self.time.append(point['time'])
            self.amplitude.append(['value'])

    def generate_plot(self):

        self.plt.plot(self.time, self.amplitude) 
        self.plt.gca.set_xlim([min(self.time),max(self.time)])
        self.plt.gca.set_ylim([min(self.amplitude),max(self.amplitude)])
        self.plt.xlabel('time') 
        self.plt.ylabel('{} value'.format(self.measurement)) 
        self.plt.title(self.measurement) 
        self.plt.savefig('report-generator/images/{}.png'.format(self.measurement))

    def get_plot_directory(self):
        return 'report-generator/images/{}.png'.format(self.measurement)
