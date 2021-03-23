from w1thermsensor import W1ThermSensor


def read_temp(*args):
    try:
        sensor = W1ThermSensor()
        temperature_in_celsius = sensor.get_temperature()
        del sensor
        return "ok", temperature_in_celsius
    except Exception as e:
        return "error", e


if __name__ == "__main__":
    print("temp (Celsius): ",read_temp())
