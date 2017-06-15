import network
from mqtt import MQTTClient 
import machine 
import ubinascii
import time 
from machine import Pin
from machine import ADC

# Many ESP8266 boards have active-low "flash" button on GPIO0.
button = Pin(0, Pin.IN)

SERVER = "host_mqtt_broker"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"led"

def sub_cb(topic, msg):
    print((topic, msg))

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('SSID', 'PasswordWiFi')
        while not sta_if.isconnected():
            machine.idle() 
    print('network config:', sta_if.ifconfig())

do_connect()

def main(server=SERVER):
    client = MQTTClient(CLIENT_ID, server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(b"messages")
    adc = ADC(0)          # create ADC object on ADC pin
    while True:
        tstadc = adc.read()
        client.publish(b'messages', tstadc);
        time.sleep_ms(200)

    c.disconnect()


main()


 