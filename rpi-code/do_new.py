from i2c import read_arduino
from wire1 import read_value as read_temp

cal1_v = 908 #mv
cal1_t = 33.125 # ℃
cal2_v = 761 #mv
cal2_t = 21 #℃

resolution = 1024 #level
reference = 5000 #mv
convert = 1000 #mV per V

do_table = [ 14460, 14220, 13820, 13440, 13090, 12740, 12420, 12110, 11810, 11530,
            11260, 11010, 10770, 10530, 10300, 10080, 9860, 9660, 9460, 9270, 
            9080, 8900, 8730, 8570, 8410, 8250, 8110, 7960, 7820, 7690,   
            7560, 7430, 7300, 7180, 7070, 6950, 6840, 6730, 6630, 6530, 6410]

def read_do(slave_addr, sensor_type):
    try:
        adc_raw = round(read_arduino(slave_addr, sensor_type)[1])
        print(adc_raw)
        adc_voltage  = adc_raw*reference/resolution
        temp = read_temp()
        rounded_temp = round(temp[1])
        V_saturation = (temp[1] - cal2_t) *(cal1_v - cal2_v) / (cal1_t - cal2_t) + cal2_v
        print("do not converted: " , str(adc_voltage * do_table[rounded_temp] / V_saturation))
        return "ok", (adc_voltage * do_table[rounded_temp] / (V_saturation * convert))
    except Exception as e:
        return "error", e
