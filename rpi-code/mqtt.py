
class mqtt:

    def __init__(self, topic, host, qos=0, retain=False, port=1883, keepalive=60):
        import paho.mqtt.client as mqtt
        import json

        import logging
        import traceback

        self.json = json
        self.topic = topic
        self.client = mqtt.Client()

        self.client.will_set(
            topic, self.json.dumps({"status": "disconnected"}), qos, retain)

        # run code until connect
        print(host)
        self.connected = False
        self.printed = False
        while self.connected is False:
            try:
                self.client.connect(host, port, keepalive)
                self.connected = True
            except:
                if self.printed is False:
                    print(
                        "unable to establish connection with topic:'%s', retrying...." % topic)
                    self.printed = True

        if self.topic == "rpi":
            self.client.on_connect = self.on_connect

        self.client.loop_start()
        print("done topic:'%s' connection setup." % topic)

        self.logging = logging
        self.traceback = traceback
        self.logging.basicConfig(filename="error.log")

    def send(self, payload, retain=False):
        try:
            self.client.publish(self.topic, payload, retain)
        except Exception as e:
            print("error occured: %s" % e)
            self.logging.error(self.traceback.format_exc())

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()

    def on_connect(self, client, userdata, flags, rc):
        self.client.publish(
            self.topic, self.json.dumps({"status": "connected"}))
