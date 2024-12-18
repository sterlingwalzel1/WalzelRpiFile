import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
BUTTON_0_PIN = 16
LED_O_PIN = 18

flashlight_state = ['LIGHT_OFF', 'LIGHT_ON']
flashlight = enumerate(flashlight_state)
flashlight = 'LIGHT_OFF'

GPIO.setup(BUTTON_0_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(LED_O_PIN, GPIO.OUT)
current_state = None
prev_state = GPIO.LOW

try: 
    while(True):
        current_state = GPIO.input(BUTTON_0_PIN)
        if(current_state == GPIO.HIGH):
            if(prev_state == GPIO.LOW):
                flashlight = not flashlight
                GPIO.output(LED_O_PIN, flashlight)

        prev_state = current_state
        time.sleep(0.01)


except KeyboardInterrupt:
    print('Got Keyboard Interript. Cleaning up an dexiting')
    GPIO.output(LED_O_PIN, GPIO.LOW)
    GPIO.cleanup()
    sys.exit()


