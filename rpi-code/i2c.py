from smbus2 import SMBus
import time
import traceback
MEMORY_ADDR = 0x00
BYTE_LEN = 25
BUS = 1

# sensor type 1 for ph , 2 for turbidity, 3 for DO

I2Cbus = SMBus(BUS)

def convert_bytes_to_list(src):
    convert = []
    for byte in src:
        convert.append(byte)
    return convert


def read_arduino(slave_addr, sensor_type):
    try:
        byte = convert_bytes_to_list(bytes(str(sensor_type), "utf-8"))
        I2Cbus.write_i2c_block_data(slave_addr, MEMORY_ADDR, byte)
        response = I2Cbus.read_i2c_block_data(
            slave_addr, MEMORY_ADDR, BYTE_LEN)
        # I2Cbus.close()
        return "ok", int(bytearray(response).decode("utf-8", "ignore"))
    except Exception as e:
        I2Cbus.close()
        print("failed to retrieve data from arduino...")
        print(traceback.format_exc())
        return "error", e

if __name__ == "__main__":
    add= int(input("enter slave address: "))
    st= int(input("enter sensor type: "))
    print(read_arduino(add, st))

