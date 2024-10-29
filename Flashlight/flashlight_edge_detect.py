import RPi.GPIO as GPIO
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


try:
    while(True):
        GPIO.wait_for_edge(BUTTON_0_PIN, GPIO.RISING, bouncetime = 10)
        flashlight = not flashlight
        GPIO.output(LED_O_PIN, flashlight)


except KeyboardInterrupt:
    print('Got Keyboard Interript. Cleaning up an dexiting')
    GPIO.output(LED_O_PIN, GPIO.LOW)
    GPIO.cleanup()
    sys.exit()
