import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
BUTTON_0_PIN = 16
LED_O_PIN = 18


GPIO.setup(BUTTON_0_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(LED_O_PIN, GPIO.OUT)

def callback(BUTTON_0_PIN):
    GPIO.output(LED_O_PIN, GPIO.HIGH)
    print('In rising_edge_callback')
    while(GPIO.input(BUTTON_0_PIN) == GPIO.HIGH):
        time.sleep(0.10)
        print('abc')
        continue
    GPIO.output(LED_O_PIN, GPIO.LOW)
    print('Leaving Callback')

GPIO.add_event_detect(BUTTON_0_PIN, GPIO.RISING, callback = callback)
cnt = 0

try:
    while(True):
        time.sleep(1)
        print(cnt)
        cnt += 1

except KeyboardInterrupt:
    print('Got Keyboard Interript. Cleaning up an dexiting')
    GPIO.output(LED_O_PIN, GPIO.LOW)
    GPIO.cleanup()
    sys.exit()


