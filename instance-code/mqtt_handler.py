class listen:

    def __message_callback_add(self, client, userdata, msg):
        try:
            self.influxHandler.dbsend(self.jsonParser(msg.payload.decode("utf-8")))
        except Exception as e:
            print(e)

    def __message_callback_add_calibration(self, client, userdata, msg):
        try:
            self.calibrate_influxHandler.dbsend(str(msg.payload.decode("utf-8")))
            print(str(msg.payload.decode("utf-8")))
        except Exception as e:
            print(e)
 

    def __init__(self, topic, mqtturl, influxHost, database, username, password, influxPort=8086, mqttport=1883, keepalive=60, type="sensor"):
        import paho.mqtt.client as mqtt
        import json

        import logging
        import traceback
        self.logging = logging
        self.traceback = traceback
        self.logging.basicConfig(filename="error.log")
        # for logging

        self.jsonParser = json.loads


        mqttClient = mqtt.Client()

        connected = False
        printed = False
        while connected is False:
            try:
                mqttClient.connect(mqtturl, mqttport, keepalive)
                connected = True
            except:
                if not printed:
                    print(
                        "failed to establish connection with topic: %s, retryng.." % topic)
                    printed = True

        mqttClient.loop_start()

        mqttClient.subscribe(topic)

        if type == "calibration":
            from influx_handler_calibration import calibration_handler
            self.calibrate_influxHandler = calibration_handler(
                influxHost, username, password, database, topic)
            mqttClient.message_callback_add(
                topic, self.__message_callback_add_calibration)


        else:
            from influx_handler import handler
            self.influxHandler = handler(
                influxHost, username, password, database, topic)
            mqttClient.message_callback_add(
                topic, self.__message_callback_add)
            

        print("Connected and subscribed to topic: %s" % topic)
