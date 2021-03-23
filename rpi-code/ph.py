A = 0.042101
D = 1.346884


def read_ph(read_arduino, slave_addr, sensor_type, *args):
    try:
        unit_list = []
        for i in range(0,10):
            unit_list.append(read_arduino(slave_addr, sensor_type)[1])
        unit_summation = sum(unit_list)
        unit_ave = unit_summation/10
        return "ok", round((A*unit_ave) - D, 2)
    except Exception as e:
        return "error", e


if __name__ == "__main__":
    from i2c import read_arduino
    print("ph raw: ", read_ph(read_arduino, 11, 1))