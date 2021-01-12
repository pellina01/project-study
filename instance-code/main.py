#!/usr/bin/python3
from mqtt_handler import listen
import time
import json
import logging
import traceback
from aggregator import aggregator
import schedule

with open('/home/ubuntu/project-study/instance-code/config.json', 'r') as file:
    data = json.loads(file.read())

cloud = {}
for key, value in data["cloud"].items():
    cloud.update({key: value})


logging.basicConfig(filename=cloud["error_file"])

sensors = []
for topic in cloud["topics"]:
    sensors.append(listen(topic, cloud["url"], cloud["influxHost"],
                          cloud["database"], cloud["username"], cloud["password"]))
calibrate = []
for items in cloud["calibration"]:
    calibrate.append(listen(cloud["calibration"], cloud["url"], cloud["influxHost"],
        cloud["database"], cloud["username"], cloud["password"], type="calibration"))

switch =   { "ph": "pH",
            "tb": "NTU",
            "temp": "Celsius",
            "do": "mg/L"
            }
       
data_to_aggregate = []
for topic in cloud["topics_aggregated"]:
    data_to_aggregate.append(aggregator(topic, cloud["influxHost"], cloud["username"],
            cloud["password"], cloud["database"], cloud["database_aggregated"], switch.get(topic, "no unit")))



def aggregating():
    for data in data_to_aggregate:
        data.aggregate()

schedule.every(1440/cloud["per_day"]).minutes.do(aggregating)



listening = True
while True:
    try:
        schedule.run_pending()
        if listening is True:
            print("listening..")
            listening = False
    except Exception as e:
        print("error occured: %s" % traceback.format_exc())
        print("error message: %s" % e)
        logging.error(traceback.format_exc())
        listening = True
