class feedback:
    from mqtt import mqtt
    import json
    import time

    def __init__(self, mqtt_url, sensor_function, corrective_function, higher_limit, lower_limit, device_name):
        self.device = device_name
        self.higher_limit = higher_limit
        self.lower_limit = lower_limit
        self.correction = corrective_function
        self.read_sensor_value = sensor_function

        self.feedback_is_on = False
        self.sent = False
        self.mq_client = self.mqtt(device_name, mqtt_url)
        self.prev_status = False

        print("successful establishing connection with mqtt")

    def check(self):
        print(self.read_sensor_value()[1])
        sensor_val = self.read_sensor_value()[1]
        if self.lower_limit > sensor_val or sensor_val > self.higher_limit:
            self.feedback_is_on = True
        else:
            self.feedback_is_on = False

        if not self.sent or self.feedback_is_on != self.prev_status:
            self.sent = False
            self.prev_status = self.feedback_is_on
            self.correction(self.feedback_is_on)
            if self.mq_client.send(self.__feedback_serializer()):
                self.sent = True
            # else:

        print("feedback status: " + str(self.feedback_is_on))
        print("sent: " + str(self.sent))
        return 300

    def __feedback_serializer(self):
        return self.json.dumps({
            "status": "ok",
            "value": "{} is {}".format(self.device, "on" if self.feedback_is_on else "off")
        })


def serialize(read, address, cmd_on, cmd_off):
    def switch(is_on):
        if is_on:
            read(address, cmd_on)
        else:
            read(address, cmd_off)
    return switch


if __name__ == "__main__":
    from do_new import read_do
    from i2c import read_arduino
    import json
    import logging
    import traceback
    import time

    logging.basicConfig(filename="error.log")
    
    with open('/home/pi/project-study/rpi-code/config.json', 'r') as file:
        data = json.loads(file.read())

    raspi = {}
    for key, value in data["raspi"].items():
        raspi.update({key: value})

    switch = serialize(read_arduino, 11, 4, 5)
    aerator = feedback(raspi["mqtt_url"], read_do,
                       switch, 8.25, 7.56, "aerator")
    while True:
        try:
            time.sleep(aerator.check())
        except Exception as e:
            logging.error(traceback.format_exc())
            print(e)
