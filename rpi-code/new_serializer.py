class sensor:
    import logging
    import traceback
    import json
    from mqtt import mqtt


    def function_serializer(self, func, read_arduino, slave_addr, sensor_type):
        def f():
            return func(read_arduino, slave_addr,sensor_type)
        return f

    def __formatter(self, topic, status, value):
        print({"topic": topic, "status": status, "value": str(value)})
        return self.json.dumps({"status": status, "value": str(value)})

    def __serialize(self, mqtt_send, mqtt_disconnect, topic):
        def send(validity, value):
            mqtt_send(self.__formatter(topic, validity, value))

        def disconnect():
            mqtt_disconnect()
        return(send, disconnect)

    def __init__(self, url, sensor_parameters, read_arduino):
        
        from temp import read_temp
        from do_new import read_do
        from tb import read_tb 
        from ph import read_ph
        
        switch = {
            "read_ph": read_ph,
            "read_do": read_do,
            "read_tb": read_tb,
            "read_temp": read_temp
        }

        self.logging.basicConfig(filename="error.log")
        self.sensor_type = sensor_parameters[3]
        self.slave_addr = sensor_parameters[2]
        self.function = switch.get(sensor_parameters[1])
        self.topic = sensor_parameters[0]
        self.mq = self.mqtt(self.topic, url)

        self.send, self.disconnect = self.__serialize(
            self.mq.send,
            self.mq.disconnect,
            self.topic,
        )

        self.sensor_func = self.function_serializer(
            self.function, read_arduino, self.slave_addr, self.sensor_type)
        
    def Process(self):
        try:
            validity, value = self.sensor_func()
            self.send(validity, value)
            self.disconnect()
        except Exception as e:
            self.logging.error(self.traceback.format_exc())
            print(e)
