import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
from flask import Flask, render_template, request

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())

lightsOn = False

def setup():
    radio.begin(0, 17)

    radio.setPayloadSize(32)
    radio.setChannel(0x76)
    radio.setDataRate(NRF24.BR_1MBPS)
    radio.setPALevel(NRF24.PA_MIN)

    radio.setAutoAck(True)
    radio.enableDynamicPayloads()
    radio.enableAckPayload()

    radio.openWritingPipe(pipes[0])
    radio.openReadingPipe(1, pipes[1])
    radio.printDetails()

@app.route('/')
def index():
    templateData = {
        'status': lightsOn
    }
    return render_template('dashboard.html', **templateData)

@app.route('/<status>')
def action(status):
    global lightsOn
    if status != 'ON' and status != 'OFF':
        templateData = {
            'status': lightsOn
        }
        return render_template('dashboard.html', **templateData)

    message = ""

    if status == 'ON':
        lightsOn = True
        message = list("TURNON")
    if status == 'OFF':
        lightsOn = False
        message = list("TURNOFF")

    while len(message) < 32:
        message.append(0)

    radio.write(message)
    print("Sent the message: {}".format(message))


    templateData = {
        'status': lightsOn
    }
    return render_template('dashboard.html', **templateData)


if __name__ == '__main__':
    try:
        setup()
        app.run(debug = True, host='0.0.0.0')
    finally:
        GPIO.cleanup()
