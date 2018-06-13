import serial
import time
from ar_signal import ArSignal
from ar_signal import *


while True:
    time.sleep(3)
    print("Temp: " + str(get_temp()))
    print("Humid : " + str(get_humid()))


