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
            if self.read_sensor_value > self.HL or self.read_sensor_value < self.LL:
                self.feedback_is_on = True
            else: 
                self.feedback_is_on = False

            if not self.sent or self.feedback_is_on != self.prev_status:
                self.sent = False
                self.prev_status = self.feedback_is_on
                self.correction(self.feedback_is_on)
                if self.mq_client.send(self.__feedback_serializer):
                    self.sent = True
                    delay_time = 600
                else:
                    delay_time = 60
            self.time.sleep(delay_time)

    def __feedback_serializer(self):
        return self.json.dumps({"status": "ok", "value": "{} is {}".format(self.device,self.feedback_is_on)})

            
                

