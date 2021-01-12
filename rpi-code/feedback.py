class feedback:
    from mqtt import mqtt
    import json
    import time

    def __init__(self, mqtt_url, sensor_function, corrective_function, higher_limit, lower_limit, device_name):
        self.device = device_name
        self.HL = higher_limit
        self.LL = lower_limit
        self.correction = corrective_function
        self.read_sensor_value = sensor_function

        self.feedback_is_on = False
        self.sent = False
        self.mq_client = self.mqtt("rpi", mqtt_url)
        self.prev_status = False

    def start(self):
        while True:
            print(self.read_sensor_value()[1])
            if (self.read_sensor_value()[1] > self.HL) or (self.read_sensor_value()[1] < self.LL):
                self.feedback_is_on = True
            else: 
                self.feedback_is_on = False

            if not self.sent or self.feedback_is_on != self.prev_status:
                self.sent = False
                self.prev_status = self.feedback_is_on
                self.correction(self.feedback_is_on)
                if self.mq_client.send(self.__feedback_serializer()):
                    self.sent = True
                    delay_time = 10
                else:
                    delay_time = 5

            print(self.feedback_is_on)
            self.time.sleep(delay_time)

    def __feedback_serializer(self):
        if self.feedback_is_on:
            return self.json.dumps({"status": "on", "value": "{} is {}".format(self.device,"on")})
        else:
            return self.json.dumps({"status": "off", "value": "{} is {}".format(self.device,"off")})

if __name__ == "__main__":
    from do import read_do
    from aerator import aerate
    import json
    with open('/home/pi/Desktop/project-study/rpi-code/config.json', 'r') as file:
        data = json.loads(file.read())

    raspi = {}
    for key, value in data["raspi"].items():
        raspi.update({key: value})

    aerator = feedback(raspi["mqtt_url"], read_do, aerate,8.25, 7.56, "aerator")
    aerator.start()


