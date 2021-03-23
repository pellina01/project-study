A = 0.03209944751
D = 0.6544198895


def read_ph(self, read_arduino, slave_addr, sensor_type, *args):
    try:
        unit_list = []
        for i in range(0,10):
            unit_list.append(read_arduino(slave_addr, sensor_type)[1])
        unit_list.sort()
        unit_summation = 0
        for i in range(2,8):
            unit_summation += unit_list[i]
        unit_ave = unit_summation/6
        return "ok", (A*unit_ave) - D
    except Exception as e:
        return "error", e


if __name__ == "__main__":
    from i2c import read_arduino
    print("ph raw: ", read_ph(read_arduino, 11, 1))