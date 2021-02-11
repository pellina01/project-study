class chart:
    from matplotlib import pyplot as plt 
    from influxdb import InfluxDBClient

    def __init__(self, frm, to, topic, database, measurement, username, password, influxHost, influxPort=8086):
        self.influxClient = self.InfluxDBClient(
            influxHost, influxPort, username, password)
        self.influxClient.switch_database(database)
        self.influxClient.query(
            'SELECT "duration" FROM "pyexample"."autogen"."brushEvents" WHERE time > now() - 4d GROUP BY "user"')

    def plot(self, time, amplitude, name):
        self.plt.plot(time, amplitude) 
        self.plt.xlabel('time') 
        self.plt.ylabel('amplitude') 
        self.plt.title(name) 
        self.plt.savefig('report-generator/images/{}.png'.format(name))
