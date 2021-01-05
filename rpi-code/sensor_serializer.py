class sensor:
    from i2c import read_arduino
    from wire1 import read_value
    from do import read_do
    import logging
    import traceback
    import json

    def __formatter(self, topic, status, value):
        print({"topic": topic, "status": status, "value": str(value)})
        return self.json.dumps({"status": status, "value": str(value)})

    def __serialize(self, mqtt_send, mqtt_disconnect,topic, value, validity):
        def get_send():
            def send():
                mqtt_send(format(topic, validity, value))
            def disconnect():
                mqtt_disconnect()
        return(get_send)

    def __init__(self, url, sensor_parameters):
        from mqtt import mqtt

        self.logging.basicConfig(filename="error.log")

        sensor_type = sensor_parameters[3]
        slave_addr = sensor_parameters[2]
        sensor_function = sensor_parameters[1]
        topic = sensor_parameters[0]
        switch = {
            "read_arduino": read_arduino,
            "read_value": read_value,
            "read_do": read_do
        }
        sensor = mqtt(topic, url)
        validity, return_value = switch.get(sensor_function)(slave_addr, sensor_type)
        self.process = self.__serialize(
            sensor.send,
            sensor.disconnect,
            topic,
            return_value,
            validity
        )

    def process(self):
        try:
            self.process.send()
            self.process.disconnect()
        except Exception as e:
            self.logging.error(self.traceback.format_exc())
            print(e)
