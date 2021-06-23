import traceback

x_raw1 = 171 #unit
y_ph1 = 4
x_raw2 = 228 #unit
y_ph2 = 6.86

m = (y_ph2 - y_ph1)/(x_raw2 - x_raw1)
b = y_ph2 - (x_raw2 * m)

def read_ph(read_arduino, slave_addr, sensor_type, *args):
    try:
        unit_list = []
        for i in range(0,10):
            unit_list.append(read_arduino(slave_addr, sensor_type)[1])
        unit_list.sort()
        unit_summation = 0
        for i in range(2,8):
            unit_summation += unit_list[i]
        unit_ave = unit_summation/6
        ph = round((m*unit_ave) + b, 2)
        if ph >= 14.0:
            ph = 14
        elif ph <= 0:
            ph = 0
        return "ok", ph 
    except:
        return "error", traceback.format_exc()


if __name__ == "__main__":
    from i2c import read_arduino
    print("ph raw: ", read_ph(read_arduino, 11, 1))