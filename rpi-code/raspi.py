#!/usr/bin/python3
import time
import json
from mqtt import mqtt
import schedule
import run_sensor


time.sleep(5)


schedule.every(1).minutes.do(run_sensor.main())


with open('config.json', 'r') as file:
    data = json.loads(file.read())

with open("sample2.txt", "w") as text_file:
    text_file.write("python starts")

raspi = {}
for key, value in data["raspi"].items():
    raspi.update({key: value})

rpi = mqtt("rpi", raspi["mqtt_url"])

while True:
    time.sleep(100)
