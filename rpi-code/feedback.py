class feedback:
    from mqtt import mqtt
    import json
    import time
    import logging
    import traceback

    def __init__(self, mqtt_url, sensor_function, corrective_function, lower_limit, device_name):
        self.device = device_name
        self.lower_limit = lower_limit
        self.correction = corrective_function
        self.read_sensor_value = sensor_function

        self.logging.basicConfig(filename="error.log")
        self.feedback_is_on = False
        self.sent = False
        self.mq_client = self.mqtt(device_name, mqtt_url)
        self.prev_status = False
        print("successful establishing connection with mqtt")

    def check(self):
        try:
            if self.lower_limit < self.read_sensor_value()[1]:
                self.feedback_is_on = False
            else:
                self.feedback_is_on = True
        except:
            self.feedback_is_on = True
            self.logging.error(self.traceback.format_exc())
            print(self.traceback.format_exc())
            
        finally:
            if not self.sent or self.feedback_is_on != self.prev_status:
                self.sent = False
                self.prev_status = self.feedback_is_on
                if self.mq_client.send(self.__feedback_serializer()):
                    self.sent = True
                self.mq_client.disconnect()


        self.correction(not self.feedback_is_on) # aerator at relay normally closed 
        print("feedback status: " + str(self.feedback_is_on))
        print("sent: " + str(self.sent))

    def __feedback_serializer(self):
        return self.json.dumps({
            "status": "note",
            "value": "{} is {}".format(self.device, "on" if self.feedback_is_on else "off")
        })
    


def serialize(read, address, cmd_on, cmd_off):
    def switch(is_on):
        if is_on:
            return read(address, cmd_on)
        else:
            return read(address, cmd_off)
    return switch

def sensor_func(read, arduino_func, address, slave_address):
    def sens():
        return read(arduino_func, address, slave_address)
    return sens


if __name__ == "__main__":
    from do_new import read_do
    from i2c import read_arduino
    import json
    import time

    
    with open('/home/pi/project-study/rpi-code/config.json', 'r') as file:
        data = json.loads(file.read())

    raspi = {}
    for key, value in data["raspi"].items():
        raspi.update({key: value})

    switch = serialize(read_arduino, 11, 4, 5)
    sensor_function = sensor_func(read_do, read_arduino, 11, 3)
    aerator = feedback(raspi["mqtt_url"], sensor_function,
                       switch, raspi["lower_limit"], "aerator")
                       
    while True:
        try:
            time.sleep(raspi["aerator_delay_s"])
            aerator.check()
        except:
            time.sleep(raspi["aerator_delay_s"])
