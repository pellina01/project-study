#!/usr/bin/python3
import time
import json
from mqtt import mqtt
import schedule
from run_sensor import main


time.sleep(5)


schedule.every(1).minutes.do(main)


with open('home/pi/Desktop/project-study/rpi-code/config.json', 'r') as file:
    data = json.loads(file.read())

with open("sample2.txt", "w") as text_file:
    text_file.write("python starts")

raspi = {}
for key, value in data["raspi"].items():
    raspi.update({key: value})

rpi = mqtt("rpi", raspi["mqtt_url"])

while True:
    schedule.run_pending()
