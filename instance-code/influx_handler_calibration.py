class calibration_handler:
    def __init__(self, influxHost, username, password, database, topic, influxPort=8086):
        from influxdb import InfluxDBClient
        import logging
        import traceback


        self.influxClient = InfluxDBClient(
            influxHost, influxPort, username, password)
        self.influxClient.switch_database(database)

        self.logging = logging
        self.traceback = traceback
        self.logging.basicConfig(filename="error.log")

    def dbsend(self, recieved_list):
        self.influxClient.write_points(
            self.serializer.serialize(recieved_list),
            time_precision='ms', protocol='json')