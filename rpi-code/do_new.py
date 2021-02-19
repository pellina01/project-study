from i2c import read_arduino
from wire1 import read_value as read_temp

cal1_v = 908 #mv
cal1_t = 33.125 # ℃
cal2_v = 761 #mv
cal2_t = 21 #℃

resolution = 1024 #level
reference = 5000 #mv
convert = 1000 #mV per V

do_table = [ 14.460, 14.220, 13.820, 13.440, 13.090, 12.740, 12.420, 12.110, 11.810, 11.530,
            11.260, 11.010, 10.770, 10.530, 10.300, 10.080, 9.860, 9.660, 9.460, 9.270, 
            9.080, 8.900, 8.730, 8.570, 8.410, 8.250, 8.110, 7.960, 7.820, 7.690,   
            7.560, 7.430, 7.300, 7.180, 7.070, 6.950, 6.840, 6.730, 6.630, 6.530, 6.410]

def read_do(self, slave_addr, sensor_type):
    try:
        adc_raw = read_arduino(slave_addr, sensor_type)
        print(adc_raw)
        adc_voltage  = round(adc_raw[1])*reference/resolution
        temp = read_temp()
        rounded_temp = round(temp[1])
        V_saturation = (temp[1] - cal2_t) *(cal1_v - cal2_v) / (cal1_t - cal2_t) + cal2_v
        return "ok", (adc_voltage * do_table[rounded_temp] / (V_saturation * convert))
    except Exception as e:
        return "error", e
