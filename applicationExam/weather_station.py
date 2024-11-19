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
        to_send = [0b00000001, 0b10000000, 0b00000000]
        value = spi.xfer(to_send)
        adc_value = (value[1] * 256) + value[2]
        print(adc_value)
        pwm_value = (min_val + adc_value) / ((max_val-min_val)/100)
        time.sleep(1)
  
except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    led.set_duty_cycle(0)
    sys.exit()
