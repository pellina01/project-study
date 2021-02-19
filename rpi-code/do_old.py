from wire1 import read_value
import math
import json

with open('/home/pi/Desktop/project-study/rpi-code/do_vs_temp.json', 'r') as file:
    data = json.loads(file.read())

temp = data["temp"]
d_o = data["do"]


def read_do(*args):
    
    try:
        status, value = read_value()
        if status == "error":
            return status, value
        if temp[0] > value or value > temp[46]:
            print(value)
            return "error", "Cannot interpolate. Limit reached"
        elif value in temp:
            index = temp.index(value)
            return "ok", d_o[index]
        else:
            max_index = temp.index(math.trunc(value))
            min_index = max_index + 1
            yout = d_o[min_index] + ((value - temp[min_index]) * (
                d_o[max_index] - d_o[min_index]) / (temp[max_index] - temp[min_index]))
            return "ok", round(yout, 2)
    except Exception as e:
        return "error", e


if __name__ == "__main__":
    print(read_do())
