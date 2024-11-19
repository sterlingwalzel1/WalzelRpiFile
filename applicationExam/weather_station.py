import RPi.GPIO as GPIO
import time
import sys
import os
import spidev

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
BUTTON_0_PIN = 16
GPIO.setup(BUTTON_0_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

sys.path.insert(0, '../utilities')
import utilities
led = utilities.HW_PWM(2000)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
#to_send = [0b00000001, 0b10000000, 0b00000000] #channel 0
to_send = [0b00000001, 0b00100000, 0b00000000] #difference between channel 2 and 3

try:
    pwm_value = 0.0
    factor = 1
    while True:
        #getting temp value
        to_send = [0b00000001, 0b00100000, 0b00000000]
        value = spi.xfer(to_send)
        temp = (value[1] * 256) + value[2]
        temp = (temp /1024) * 3.3 #convert numerical value to voltage
        temp = (temp - 0.5) / 0.01 #convert voltage to temp c
        temp = (1.8 * temp) + 32 #convert to c to f

        #getting photo sensor value
        to_send = [0b00000001, 0b10000000, 0b00000000]
        value = spi.xfer(to_send)
        adc_value = (value[1] * 256) + value[2]
        photo_volt = 3.3 - ((adc_value /1024) * 3.3) #convert numerical value to voltage

        #figure out what activity
        if temp < 35.0:
            activity = 'STAY_HOME'
        elif temp > 35.0 and temp < 50.0:
            activity = 'BONFIRE'
        elif temp > 50.0 and temp < 65.0:
            if photo_volt > 2.0:
                activity = 'SURFS_UP'
            else:
                activity = 'TOO_DARK_TO_SURF'
        else:
            if photo_volt > 2.0:
                activity = 'BAG_RAYS'
            else:
                activity = 'TOO_DARK_TO_BAG_RAYS'

        #SWITCH CASE TO FIGURE OUT WHAT ACTIVITY
        if activity == "STAY_HOME":
            print('Stay home, dude!')
        elif activity == 'BONFIRE':
            print('Bonfire, dude!')
        elif activity == 'SURFS_UP':
            print('Surf\'s up, dude!')
        elif activity == 'TOO_DARK_TO_SURF':
            print('Too dark to surf, dude!')
        elif activity == 'BAG_RAYS':
            print('Bag some rays, dude!')
        elif activity == 'TOO_DARK_TO_BAG_RAYS':
            print('Too dark to bag Rays, dude!')

        print(temp, photo_volt)
        time.sleep(1)
  
  
except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    led.set_duty_cycle(0)
    sys.exit()
