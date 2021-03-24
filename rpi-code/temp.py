from w1thermsensor import W1ThermSensor
import traceback

def read_temp(*args):
    try:
        sensor = W1ThermSensor()
        temperature_in_celsius = sensor.get_temperature()
        del sensor
        return "ok", round(temperature_in_celsius,2)
    except:
        return "error", traceback.format_exc()


if __name__ == "__main__":
    print("temp (Celsius): ",read_temp())
