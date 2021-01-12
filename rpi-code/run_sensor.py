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
import logging
import traceback

time.sleep(5)

with open('/home/pi/Desktop/project-study/rpi-code/config.json', 'r') as file:
    data = json.loads(file.read())


raspi = {}
for key, value in data["raspi"].items():
    raspi.update({key: value})

def main():
    logging.basicConfig(filename="error.log")

    try:
        for sensor_listed in raspi["sensors"]:
            sensor(raspi["mqtt_url"], sensor_listed).Process()
    except:
        print(traceback.format_exc())
        logging.error(traceback.format_exc())



if __name__ == "__main__":
    main()
        # sensor_list.append(sensor(raspi["mqtt_url"], sensor_listed).process)

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
