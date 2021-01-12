class calibration_handler:
    def __init__(self, influxHost, username, password, database, topic, influxPort=8086):
        from influxdb import influxClient
        import logging
        import traceback
        import time
        self.time = time
        self.topic = topic
        self.influxClient = InfluxDBClient(
            influxHost, influxPort, username, password)
        self.influxClient.switch_database(database)

        self.logging = logging
        self.traceback = traceback
        self.logging.basicConfig(filename="error.log")

    def dbsend(self, recieved_list):
        self.influxClient.write_points(
            self.serialize(recieved_list),
            time_precision='ms', protocol='json')

    def serialize(self,recieved_messege):
        return[{
            "measurement": self.topic,
            "tags": {
                "data type": "string"
            },
            "fields":   {
                "messege": recieved_messege,
                "next calibration": int(self.time.time_ns() + 7776000000000000) # +3months in nanosecond
            }
        }]