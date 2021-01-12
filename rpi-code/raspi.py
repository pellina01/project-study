#!/usr/bin/python3
import time
import json
from mqtt import mqtt
import math
import schedule
from run_sensor import main

with open('/home/pi/Desktop/project-study/rpi-code/config.json', 'r') as file:
    data = json.loads(file.read())


raspi = {}
for key, value in data["raspi"].items():
    raspi.update({key: value})

def sched(mins):
    hour = mins/60
    minute = mins - (60*math.trunc(hour))
    return "{}:{}".format(math.trunc(hour),minute)

schedules = []
period = 1440/raspi["schedule_per_day"]
for i in range(1, raspi["schedule_per_day"] + 1):
    schedules.append(schedule.every(sched(math.trunc(period)*i)).minutes.do(main))

rpi = mqtt("rpi", raspi["mqtt_url"])

#schedule.every(1).minutes.do(main)
while True:
    schedule.run_pending(raspi)
