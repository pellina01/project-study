import json
from aggregator import aggregator

with open('config.json', 'r') as file:
    data = json.loads(file.read())

cloud = {}
for key, value in data["cloud"].items():
    cloud.update({key: value})

for topic in cloud["topics_aggregated"]:
    aggregator(topic, cloud["influxHost"], cloud["username"],
               cloud["password"], cloud["database"], cloud["database_aggregated"]).aggregate()
