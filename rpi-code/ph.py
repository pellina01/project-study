A = (259/7250)
D = (-7519/7250)


def read_ph(read_arduino, slave_addr, sensor_type, *args):
    try:
        unit_list = []
        for i in range(0,10):
            unit_list.append(read_arduino(slave_addr, 6)[1])
        unit_list.sort()
        unit_summation = 0
        for i in range(2,8):
            unit_summation += unit_list[i]
        unit_ave = unit_summation/6
        return "ok", round((A*unit_ave) + D, 2)
    except Exception as e:
        return "error", e


if __name__ == "__main__":
    from i2c import read_arduino
    print("ph raw: ", read_ph(read_arduino, 11, 6))