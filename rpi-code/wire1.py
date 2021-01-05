from w1thermsensor import W1ThermSensor
import time


def read_value(*args):
    try:
        sensor = W1ThermSensor()
        temperature_in_celsius = sensor.get_temperature()
        del sensor
        return "ok", temperature_in_celsius
    except Exception as e:
        return "error", e


if __name__ == "__main__":
    print(read_value())
