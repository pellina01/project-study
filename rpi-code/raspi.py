#!/bin/bash
import time
import json
from mqtt import mqtt


time.sleep(5)

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
