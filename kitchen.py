import random
import time
from paho.mqtt import client as mqtt_client
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

led1 = 23
pirPin = 24
lightPin = 25
firePin = 27
buzzerled = 26

GPIO.setup(led1, GPIO.OUT)
GPIO.setup(pirPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(lightPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(firePin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buzzerled, GPIO.OUT)

print("Sensor Alarm (CTRL+C to exit)")
time.sleep(.2)
print("Ready")

broker = 'test.mosquitto.org'
mqttport = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, mqttport)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        warningmsg = "on buzzer"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            try:
                GPIO.add_event_detect(firePin, GPIO.BOTH, bouncetime=300)

                while 1:
                    #if motion is detected, no light, lights on
                    if GPIO.input(pirPin) == 1:
                        print("Motion Detected!")

                        #if light is detected
                        if GPIO.input(lightPin) == 1:
                            print("Room Lightning Detected!")
                            print("LED Off")
                            GPIO.output(led1, GPIO.LOW)
                        else:
                            print("No Room Lightning Detected!")
                            print("LED On")
                            GPIO.output(led1, GPIO.HIGH)

                    #if no motion, check light, if lights on, off light
                    else:
                        print("No Motion Detected!")
            
                        #if fire is detected
                        if GPIO.event_detected(firePin):
                            time.sleep(5)
                            print("Flame Detected!")
                            print("Buzzer LED On")
                            GPIO.output(buzzerled, GPIO.HIGH)
                            result1 = client.publish(topic, warningmsg)
                            if result1[0] == 0:
                                print(f"Send `{warningmsg}` to topic `{topic}`")

                            #if light is detected
                            if GPIO.input(lightPin) == 1:
                                time.sleep(5)
                                print("Room Lightning Detected!")
                                print("Buzzer LED On")
                                GPIO.output(buzzerled, GPIO.HIGH)
                                result1 = client.publish(topic, warningmsg)
                                if result1[0] == 0:
                                    print(f"Send `{warningmsg}` to topic `{topic}`")

                        #no fire is detected
                        else:
                            print("No Flame Detected!")

                            #if light is detected
                            if GPIO.input(lightPin) == 1:
                                time.sleep(10)
                                print("Room Lightning Detected!")
                                print("Buzzer LED On")
                                GPIO.output(buzzerled, GPIO.HIGH)
                                result1 = client.publish(topic, warningmsg)
                                if result1[0] == 0:
                                    print(f"Send `{warningmsg}` to topic `{topic}`")
                            else:
                                print("No Room Lightning Detected!")
                                GPIO.output(buzzerled, GPIO.LOW)
                                GPIO.output(led1, GPIO.LOW)
            
                    time.sleep(2)

            except KeyboardInterrupt:
                print("Quit")
                GPIO.cleanup()
            
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()