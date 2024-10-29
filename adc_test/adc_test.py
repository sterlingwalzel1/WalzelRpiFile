import spidev
import sys
import time
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
to_send = [0b00000001, 0b10000000, 0b00000000]
 
try:
    while(True):
        to_send = [0b00000001, 0b10000000, 0b00000000]
        value = spi.xfer(to_send)
        print(value)
        time.sleep(0.3)
 
except KeyboardInterrupt:
    print('Got Keyboard Interript. Cleaning up an dexiting')
    sys.exit()