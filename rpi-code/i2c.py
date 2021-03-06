# import smbus2 as smbus


from smbus2 import SMBus
# sensor type 1 for ph , 2 for turbidity
MEMORY_ADDR = 0x00
BYTE_LEN = 25
BUS = 1


def convert_bytes_to_list(src):
    convert = []
    for byte in src:
        convert.append(byte)
    return convert


# def read_arduino(slave_addr, sensor_type):
#     try:
#         SMBus(BUS).write_i2c_block_data(
#             slave_addr, MEMORY_ADDR, convert_bytes_to_list(bytes(str(sensor_type), "utf-8")))
#         return "ok", float(bytearray(SMBus(BUS).read_i2c_block_data(
#             slave_addr, MEMORY_ADDR, BYTE_LEN)).decode("utf-8", "ignore"))
#     except Exception as e:
#         print("failed to retrieve data from arduino...")
#         print(e)
#         return "error", e

def read_arduino(slave_addr, sensor_type):
    try:
        I2Cbus = SMBus(BUS)
        byte = convert_bytes_to_list(bytes(str(sensor_type), "utf-8"))
        I2Cbus.write_i2c_block_data(slave_addr, MEMORY_ADDR, byte)
        response = I2Cbus.read_i2c_block_data(
            slave_addr, MEMORY_ADDR, BYTE_LEN)
        I2Cbus.close()
        return "ok", float(bytearray(response).decode("utf-8", "ignore"))
    except Exception as e:
        print("failed to retrieve data from arduino...")
        print(e)
        return "error", e


if __name__ == "__main__":
    print(read_arduino(11, 1))
    print(read_arduino(11, 2))
