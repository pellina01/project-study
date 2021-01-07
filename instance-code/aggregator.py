
class aggregator:
    import time
    import math
    import json

    def __init__(self, topic, host, user, pw, db, db_aggregate):
        from influxdb import InfluxDBClient
        self.topic = topic
        self.db_aggregate = db_aggregate
        self.client = InfluxDBClient(host=host, port=8086,
                                     username=user, password=pw)
        self.client.switch_database(db)

    def aggregate(self):
        try:
            query_result = list(self.client.query(
                'SELECT * FROM {} WHERE time > now() - 10d'.format(self.topic)).get_points(measurement=self.topic))
            # query_result = self.client.query(
            #     'SELECT * FROM {} WHERE time > now() - 10d'.format(self.topic))

            # data_points = list(query_result.get_points(measurement=self.topic))
            self.aggregated_data = 0
            n = 0
            for lists in data_points:
                self.aggregated_data += lists["value"]
                n += 1
            self.aggregated_data /= n

            json_body = __serializer()
            self.client.switch_database(self.db_aggregate)

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
