import RPi.GPIO as GPIO
import time
import sys
import os

sys.path.insert(0, '../utilities')
import utilities

pwm = utilities.HW_PWM(25000)
pwm.set_duty_cycle(100.0)

file = open("rpm_value_file.txt", "a") 
TACH_PIN = 16
count = 0
prev = time.time_ns()


def callback(TACH_PIN):
    cur = time.time_ns()
    global period += cur - prev
    global count += 1

     if count % 10 == 0:
        period /= 10
        freq = period^-1
        rpm = freq * 60 / 2
        file.write(string(rpm) + "\n")   
        

    global prev = cur

GPIO.add_event_detect(TACH_PIN, GPIO.RISING, callback = callback)

try:
    while True:
        pwm_value = float(input("Enter desired PWM Duty Cycle (0.0 to 100.0): "))
        pwm_value = 100 - pwm_value
        pwm.set_duty_cycle(pwm_value)
        if pwm_value < 0.0:
            print('ERROR: Duty cycle below 0.0')
        if pwm_value > 100.0:
            print('ERROR: Duty cycle below 100.0')
        time.sleep(.1)


except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    pwm.set_duty_cycle(100.0)
    file.close()
    sys.exit()




