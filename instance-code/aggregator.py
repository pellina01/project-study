
class aggregator:
    import time
    import math
    import json
    import traceback
    import logging
    from influxdb import InfluxDBClient

    def __init__(self, topic, host, user, pw, db, db_aggregate):
        self.topic = topic
        self.db_aggregate = db_aggregate
        self.client = self.InfluxDBClient(host=host, port=8086,
                                          username=user, password=pw)
        self.client.switch_database(db)
        self.average = 0
        self.logging.basicConfig(filename="error.log")

    def aggregate(self):
        try:
            query_result = list(self.client.query(
                'SELECT * FROM {} WHERE time > now() - 1d'.format(self.topic)).get_points(measurement=self.topic))

            for lists in query_result:
                self.average += lists["value"]
            self.average /= len(query_result)

            json_body = self.__serializer()
            self.client.switch_database(self.db_aggregate)

            self.client.write_points(json_body)
        except Exception as e:
            print(self.traceback.format_exc())
            self.logging.error(self.traceback.format_exc())

    def __serializer(self):
        return [
            {
                "measurement": "{}_aggregated".format(self.topic),
                "tags": {
                    "user": self.topic,
                },
                "fields": {
                    "value": self.average
                }
            }]
