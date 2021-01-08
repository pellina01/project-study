#!/usr/bin/env python
import time
import json
from mqtt import mqtt


time.sleep(5)

with open('config.json', 'r') as file:
    data = json.loads(file.read())

raspi = {}
for key, value in data["raspi"].items():
    raspi.update({key: value})

rpi = mqtt("rpi", raspi["mqtt_url"])

while True:
    time.sleep(100)
