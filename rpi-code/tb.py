

def read_tb(read_arduino, slave_addr, sensor_type, *args):
    try:
        volt = read_arduino(slave_addr, sensor_type)[1] * 5 / 1024
        if volt < 2.5:
            ntu = 3000.0
        elif volt > 4.19:
            ntu = 10.0
        else:
            ntu = -1120.4 * pow(volt, 2) + (5742.3 * volt) - 4353.8
        return "ok", ntu
    except Exception as e:
        return "error", e


if __name__ == "__main__":
    from i2c import read_arduino
    print("turbidity raw: ", read_tb(read_arduino, 11, 3))
