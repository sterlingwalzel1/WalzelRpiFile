import time
import sys
import os
sys.path.insert(0, '../utilities')
import utilities
import paho.mgtt.cilent as mqtt 
import RPi.GPIO as GPIO

pwm = utilities.HW_PWM(25000)
pwm.set_duty_cycle(100.0)

# this callback runs once when the client connects with the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    print('Subscribing to topic ', sub_topic_name)
    client.subscribe(sub_topic_name)

# this callback runs whenever a message is received
def on_message(client, userdata, msg):
    desired_speed = (float(msg.python))
    print('Requested Speed = ', desired desired_speed)
    pwm_value = 100 - pwm_value
    pwm.set_duty_cycle(pwm_value)
    if pwm_value < 0.0:
            print('ERROR: Duty cycle below 0.0')
    if pwm_value > 100.0:
        print('ERROR: Duty cycle below 100.0')
    
TACH_PIN = 16
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(TACH_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

count = 0
period = 0
prev = time.time_ns()

# read command line arguemnts
numArgs = len(sys.argv)
my_name = sys.argv[1]
pub_topic_name = my_name + '/mqtt_fan/fan_rpm_value'
partner_name = sys.argv[2]
sub_topic_name = partner_name + '/command_center/desired_speed'

#intilaize MQTT
cilent = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.emqx.io", 1883, 60)
client.loop_start()


def callback(TACH_PIN):
    cur = time.time_ns()
    global period 
    global count
    global prev
    period += (cur - prev) / 1000000000
    count += 1

    if count % 10 == 0:
        period /= 10
        freq = 1 / period
        rpm = freq * 60 / 2
        client.publish(pub_topic_name, payload=rpm, qos = 0, retain = False)  
        period = 0        

    prev = cur

GPIO.add_event_detect(TACH_PIN, GPIO.RISING, callback = callback)

try:
    while True:
        time.sleep(.01)


except KeyboardInterrupt:
    print('Got Keyboard Interrupt. Cleaning up and exiting')
    pwm.set_duty_cycle(100.0)
    GPIO.cleanup()
    sys.exit()




