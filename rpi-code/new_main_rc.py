#!/usr/bin/python3
import time
import json
from mqtt import mqtt
from sensor_serializer import sensor
import math
import schedule
import logging
import traceback
from i2c import read_arduino

with open('/home/pi/project-study/rpi-code/config.json', 'r') as file:
    data = json.loads(file.read())


raspi = {}
for key, value in data["raspi"].items():
    raspi.update({key: value})

sensor_list = []
for sensor_listed in raspi["sensors"]:
            sensor_list.append(sensor(raspi["mqtt_url"], sensor_listed, read_arduino))

def main():
    logging.basicConfig(filename="error.log")
    try:
        for sensors in sensor_list:
            sensors.Process()
    except:
        print(traceback.format_exc())
        logging.error(traceback.format_exc())


schedules = []

if raspi["mode"] == "dev":
# this code is for scheduling with interval in a day

    def sched(mins):
        hour = math.trunc(mins/60)
        minute = mins - (60*hour)
        formatted_hour = "0{}".format(hour) if hour < 10 else hour
        formatted_minute = "0{}".format(minute) if minute < 10 else minute
        return "{}:{}".format(formatted_hour, formatted_minute)


    period = math.trunc(1440/raspi["schedule_per_day"])
    for i in range(0, raspi["schedule_per_day"]):
        schedules.append(schedule.every().day.at(sched(period*i)).do(main))
        print("done scheduling time at: ", sched(period*i))

elif raspi["mode"] == "prod":
# this code is for schedule with specified time
    schedules = []
    for t in raspi["schedules"]:
        schedules.append(schedule.every().day.at(t).do(main))
        print("done scheduling time at: ", t)

rpi = mqtt("rpi", raspi["mqtt_url"])

while True:
    schedule.run_pending()
    time.sleep(1)
