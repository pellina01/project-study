# edited for actual application
import time
import json
import logging
import traceback
from do import read_do
from i2c import read_arduino
from mqtt import mqtt
from wire1 import read_value
from sensor_serializer import sensor
from multiprocessing import Process

time.sleep(5)

with open('config.json', 'r') as file:
    data = json.loads(file.read())


with open("sample.txt", "w") as text_file:
    text_file.write("python starts")


raspi = {}
for key, value in data["raspi"].items():
    raspi.update({key: value})


if __name__ == "__main__":
    logging.basicConfig(filename=raspi["error_file"])

    sensor_list = []
    for sensor_listed in raspi["sensors"]:
        # sensor_list.append(sensor(raspi["mqtt_url"], sensor_listed).process)
        sensor(raspi["mqtt_url"], sensor_listed).Process()

    # processes = []
    # try:
    #     for sensor in sensor_list:
    #         sensor()
        #     process = Process(target=sensor.process)
        #     process.start()
        #     processes.append(process)
        # for process in processes:
        #     process.join()
        #     processes.remove(process)
    # except Exception as e:
    #     logging.error(traceback.format_exc())
    #     time.sleep(5)
