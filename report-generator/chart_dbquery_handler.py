class chart:
    from matplotlib import pyplot as plt 
    from influxdb import InfluxDBClient

    def __init__(self, frm, to, topic, database, measurement, username, password, influxHost, influxPort=8086):
        self.influxClient = self.InfluxDBClient(
            influxHost, influxPort, username, password)
        self.influxClient.switch_database(database)
        self. data = self.influxClient.query(
            'SELECT {topic} FROM {measurement} WHERE time > {time}'.format(
                topic=topic, measurement=measurement,time=to-frm))

    def generate_plot(self):
        pass

    def __plot(self, time, amplitude, name):
        self.plt.plot(time, amplitude) 
        self.plt.xlabel('time') 
        self.plt.ylabel('amplitude') 
        self.plt.title(name) 
        self.plt.savefig('report-generator/images/{}.png'.format(name))
