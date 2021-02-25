class serializer:
    def __init__(self, topic, unit):
        self.topic = topic
        self.unit = unit
        self.state = {
        "connected":self.__connected,
        "disconnected":self.__disconnected,
        "ok":self.__ok,
        "error":self.__error,
        "note":self.__note
        }

    def serialize(self, recieved_list):
        return self.state.get(recieved_list["status"])(recieved_list)

    def __influx_serializer(self, measurement, tag, field):
        return [{
            "measurement": measurement,
            "tags": {
                "unit": tag
            },
            "fields":   {
                "value": field
            }
        }]

    def __ok(self, recieved_list):
        return self.__influx_serializer(self.topic, self.unit, float(recieved_list["value"]))

    def __error(self, recieved_list):
        return self.__influx_serializer("rpi", "error", str(self.topic+ " error: " + recieved_list["value"]))

    def __disconnected(self, recieved_list):
        return self.__influx_serializer("rpi", "disconnected", "RasPi has been disconnected")

    def __connected(self, recieved_list):
        return self.__influx_serializer("rpi", "connected", "RasPi is connected")

    def __note(self, recieved_list):
        return self.__influx_serializer(self.topic, "note", str(self.topic+ " note: " + recieved_list["value"]))

