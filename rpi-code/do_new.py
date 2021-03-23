from temp import read_temp
import traceback

cal2_v = 268.5547  # mv
cal2_t = 26.5  # ℃
cal1_v = 307.6172  # mv
cal1_t = 36.12  # ℃

resolution = 1024  # level
reference = 5000  # mv

do_table = [14.460, 14.220, 13.820, 13.440, 13.090, 12.740, 12.420, 12.110, 11.810, 11.530,
            11.260, 11.010, 10.770, 10.530, 10.300, 10.080, 9.860, 9.660, 9.460, 9.270,
            9.080, 8.900, 8.730, 8.570, 8.410, 8.250, 8.110, 7.960, 7.820, 7.690,
            7.560, 7.430, 7.300, 7.180, 7.070, 6.950, 6.840, 6.730, 6.630, 6.530, 6.410]  # 0C to 41C only

# do_table = [14460, 14220, 13820, 13440, 13090, 12740, 12420, 12110, 11810, 11530,
#     11260, 11010, 10770, 10530, 10300, 10080, 9860, 9660, 9460, 9270,
#     9080, 8900, 8730, 8570, 8410, 8250, 8110, 7960, 7820, 7690,
#     7560, 7430, 7300, 7180, 7070, 6950, 6840, 6730, 6630, 6530, 6410]


def read_do(read_arduino, slave_addr, sensor_type, *args):
    try:
        adc_raw = read_arduino(slave_addr, sensor_type)[1]
        adc_voltage = round(adc_raw)*reference/resolution
        print("mv: ", adc_voltage)
        temp = read_temp()
        rounded_temp = round(temp[1])
        V_saturation = (temp[1] - cal2_t) * (cal1_v -
                                             cal2_v) / (cal1_t - cal2_t) + cal2_v
        print("do" , round(adc_voltage * do_table[rounded_temp] / V_saturation, 2))
        return "ok", round(adc_voltage * do_table[rounded_temp] / V_saturation, 2)
    except Exception as e:
        print(traceback.format_exc())
        return "error", e

if __name__ == "__main__":
    from i2c import read_arduino
    print("dissolved oxygen: ", read_do(read_arduino, 11, 2))
    print("temp: ", read_temp())
