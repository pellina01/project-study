
class mqtt:

    def __init__(self, topic, host, qos=0, retain=False, port=1883, keepalive=60):
        import paho.mqtt.client as mqtt
        import json

        import logging
        import traceback

        self.json = json
        self.topic = topic
        self.client = mqtt.Client()
        self.host = host
        self.port = port
        self.keepalive = keepalive

        # only rpi topic(the status of the main device) will have will_set and on_connect method set
        if topic == "rpi":
            self.client.on_connect = self.on_connect
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

            self.client.loop_start()
        print("done topic:'%s' connection setup." % topic)

        self.logging = logging
        self.traceback = traceback
        self.logging.basicConfig(filename="error.log")

    def send(self, payload, retain=False):
        try:
            self.client.connect(self.host, self.port, self.keepalive)
            self.client.publish(self.topic, payload, retain)
            return True
        except Exception as e:
            print("error occured: %s" % e)
            self.logging.error(self.traceback.format_exc())
            return False

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()

    def on_connect(self, client, userdata, flags, rc):
        print("here at on_connect")
        if self.topic == "rpi":
            self.client.publish(
                self.topic, self.json.dumps({"status": "connected"}))

    def on_grid(self, status): #status is true if grid is on, false if not
        if self.topic == "rpi":
            if status:
                msg = {"status": "note", "value": "using on-grid power"}
            else:
                msg = {"status": "note", "value":  "using battery power"}
            self.client.publish(
                self.topic, self.json.dumps(msg))
