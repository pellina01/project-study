
class aggregator:
    import time
    import math
    import json
    import traceback
    import logging
    from influxdb import InfluxDBClient

    def __init__(self, topic, host, user, pw, db, db_aggregate, unit):
        self.db = db
        self.unit = unit
        self.topic = topic
        self.db_aggregate = db_aggregate
        self.client = self.InfluxDBClient(host=host, port=8086,
                                          username=user, password=pw)
        self.logging.basicConfig(filename="error.log")

    def aggregate(self):
        try:
            self.client.switch_database(self.db)
            self.average = 0
            query_result = list(self.client.query(
                'SELECT * FROM {} WHERE time > now() - 1d'.format(self.topic)).get_points(measurement=self.topic))

            print(len(query_result))

            for lists in query_result:
                self.average += lists["value"]
            self.average /= len(query_result)

            json_body = self.__serializer()
            self.client.switch_database(self.db_aggregate)

            self.client.write_points(json_body)
        except:
            print(self.traceback.format_exc())
            self.logging.error(self.traceback.format_exc())

    def __serializer(self):
        return [
            {
                "measurement": "{}_aggregated".format(self.topic),
                "tags": {
                    "unit": self.unit,
                },
                "fields": {
                    "value": float(round(self.average, 2))
                }
            }]
