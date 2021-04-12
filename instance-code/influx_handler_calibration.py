class calibration_handler:
    def __init__(self, influxHost, username, password, database, topic, influxPort=8086):
        from influxdb import InfluxDBClient
        import logging
        import traceback
        import time
        from datetime import datetime
        switch = {
        "do_calibrate" : 2629746,
        "ph_calibrate" : 2629746,
        "do_cap_replace" : 15778476
        } #7889231
        self.datetime = datetime
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
                "message": recieved_messege,
                "next calibration date": self.datetime.fromtimestamp(self.time.time() + self.switch[self.topic]).strftime('%Y-%m-%d %H:%M:%S') # +3months
            }
        }]