import time
import json
import logging
import traceback
from sensor_serializer import sensor
import logging
import traceback

def main(raspi):
    logging.basicConfig(filename="error.log")

    try:
        for sensor_listed in raspi["sensors"]:
            sensor(raspi["mqtt_url"], sensor_listed).Process()
    except:
        print(traceback.format_exc())
        logging.error(traceback.format_exc())



if __name__ == "__main__":
    with open('/home/pi/Desktop/project-study/rpi-code/config.json', 'r') as file:
        data = json.loads(file.read())


    raspi = {}
    for key, value in data["raspi"].items():
        raspi.update({key: value})

    main(raspi)
       
