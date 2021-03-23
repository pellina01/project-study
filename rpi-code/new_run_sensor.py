# this code is substitute for main.py . This code is for debugging purpose
import time
import json
import logging
import traceback
from new_serializer import sensor1
import logging
import traceback
from i2c import read_arduino



def main(raspi):
    logging.basicConfig(filename="error.log")

    sensor_list = []
    for sensor_listed in raspi["sensors"]:
                sensor_list.append(sensor1(raspi["mqtt_url"], sensor_listed, read_arduino))


    try:
        for sensors in sensor_list:
            sensors.Process()
    except:
        print(traceback.format_exc())
        logging.error(traceback.format_exc())



if __name__ == "__main__":
    with open('/home/pi/project-study/rpi-code/config.json', 'r') as file:
        data = json.loads(file.read())


    raspi = {}
    for key, value in data["raspi"].items():
        raspi.update({key: value})

    main(raspi)
       
