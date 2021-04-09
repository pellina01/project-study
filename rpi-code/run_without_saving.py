from tb import read_tb
from ph import read_ph
from do_new import read_do
from temp import read_temp
from i2c import read_arduino
import time

while True:
	print("----newline----")
	print("ph: ", read_ph(read_arduino, 11, 6))
	print("----separator----")
	print("tb: ", read_tb(read_arduino, 11, 2))
	print("----separator----")
	print("do: ", read_do(read_arduino, 11, 3))
	print("----separator----")
	print("temp: ", read_temp())
	print("----separator----")
	time.sleep(1)