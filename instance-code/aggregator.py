
class aggregator:
    from influxdb import InfluxDBClient
    import time
    import math
    import json

    def __init__(self, topic, host, user, pw, db):
        self.topic = topic
        self.client = self.InfluxDBClient(host=host, port=8086,
                                          username=user, password=pw)
        self.client.switch_database(db)

    def aggregate(self):
        try:
            query_result = list(self.client.query(
                'SELECT * FROM {} WHERE time > now() - 1d'.format(self.topic)).get_points(measurement=self.topic))

            self.aggregated_data = 0
            n = 0
            for lists in query_result:
                self.aggregated_data += lists["value"]
                n += 1
            self.aggregated_data /= n

            json_body = __serializer()

            self.client.write_points(json_body)
        except Exception as e:
            print(e)

    def __serializer(self):
        return [
            {
                "measurement": "{}_aggregated".format(self.topic),
                "tags": {
                    "user": self.topic,
                },
                "time": self.math.trunc(time.time())-86400,
                "fields": {
                    "value": aggregated_data
                }
            }]
