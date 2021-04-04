import traceback

def read_tb(read_arduino, slave_addr, sensor_type, *args):
    try:
        raw = read_arduino(slave_addr, sensor_type)[1]
        volt =  raw * 5 / 1024
        print("tb raw: ", raw)
        print("tb volt: ", volt)
        if volt < 2.5:
            ntu = 3000.0
        elif volt > 4.19:
            ntu = 10.0
        else:
            ntu = -1120.4 * pow(volt, 2) + (5742.3 * volt) - 4353.8
        return "ok", round(ntu,2)
    except:
        return "error", traceback.format_exc()


if __name__ == "__main__":
    from i2c import read_arduino
    tb = read_tb(read_arduino, 11, 2)
    print("turbidity NTU: ", tb)
