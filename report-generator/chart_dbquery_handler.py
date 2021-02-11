class chart:
    from matplotlib import pyplot as plt 
    from influxdb import InfluxDBClient

    def __init__(self, measurement, database, username, password, influxHost, influxPort=8086):
        self.measurement = measurement
        self.has_data = False

        self.influxClient = self.InfluxDBClient(
            influxHost, influxPort, username, password)
        self.influxClient.switch_database(database)

    def query_db(self, frm, to):
        try:
            self.data = self.influxClient.query(
                'SELECT * FROM {measurement} WHERE time > {time}'.format(
                    measurement=self.measurement,time=to-frm))
            self.datapoints = self.data.get_points(measurement=self.measurement)

            self.time = []
            self.amplitude = []

            for point in self.datapoints:
                self.time.append(point['time'])
                self.amplitude.append(['value'])
            self.has_data = True
        except:
            self.has_data = False

    def generate_plot(self):

        if self.has_data:
            self.plt.plot(self.time, self.amplitude) 
            self.plt.gca.set_xlim([min(self.time),max(self.time)])
            self.plt.gca.set_ylim([min(self.amplitude),max(self.amplitude)])
            self.plt.xlabel('time') 
            self.plt.ylabel('{} value'.format(self.measurement)) 
            self.plt.title(self.measurement) 
            self.plt.savefig('report-generator/images/{}.png'.format(self.measurement))
            self.image_link = 'report-generator/images/{}.png'.format(self.measurement)

        else:
            self.image_link = 'report-generator/images/no_data.png'


    def get_plot_directory(self):
        del self.time 
        del self.amplitude 
        return self.image_link
