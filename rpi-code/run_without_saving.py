from tb import read_tb
from ph import read_ph
from do_new import read_do
from temp import read_temp
from i2c import read_arduino
import time

while True:
	print("ph: ", read_ph(read_arduino, 11, 6))
	print("tb: ", read_tb(read_arduino, 11, 2))
	print("do: ", read_do(read_arduino, 11, 3))
	print("temp: ", read_temp())
	time.sleep(1)