import time
import sys
import os
sys.path.insert(0, '../utilities')
import utilities
import paho.mgtt.cilent as mqtt 
import RPi.GPIO as GPIO

pwm = utilities.HW_PWM(2000)
pwm.set_duty_cycle(0.0)

# this callback runs once when the client connects with the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    print('Subscribing to topic ', sub_topic_name)
    client.subscribe(sub_topic_name)

# this callback runs whenever a message is received
def on_message(client, userdata, msg):
    activity = (float(msg.python))
    print('Actvity = ', activity)
    if activity == 4:
        pwm.set_duty_cycle(100.0)
    elif activity == 2:
        pwm.set_duty_cycle(50.0)
    elif activity == 1:
        pwm.set_duty_cycle(25.0)
     else:
        pwm.set_duty_cycle(0.0)
    
LED_O_PIN = 16
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(LED_O_PIN, GPIO.OUT)

# read command line arguemnts
numArgs = len(sys.argv)
my_name = sys.argv[1]
pub_topic_name = my_name + '/home_base/activity'
partner_name = sys.argv[2]
sub_topic_name = partner_name + '/weather_station/activity'

#intilaize MQTT
cilent = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.emqx.io", 1883, 60)
client.loop_start()


try:
    while True:
        time.sleep(.1)


except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    pwm.set_duty_cycle(100.0)
    GPIO.cleanup()
    sys.exit()




