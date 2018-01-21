import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
from flask import Flask, render_template, request

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())

state = 0

settings = ['Off', 'Rainbow Blend', 'Rainbow Stripe', 'Rainbow Stripe Blend', 'Purple / Green', 'Random', 'Black / White', 'Black / White Blend', 'Cloud', 'Party', 'Red / White / Blue', 'Red / White / Blue Blend']

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
        'status': state,
        'settings': settings
    }
    return render_template('dashboard.html', **templateData)

@app.route('/changeMode/<option>')
def action(option):
    global state
    state = int(option)

    message = list(str(state))

    while len(message) < 3:
        message.append(0)

    radio.write(message)
    print("Sent the message: {}".format(message))


    templateData = {
        'status': state,
        'settings': settings
    }
    return render_template('dashboard.html', **templateData)

if __name__ == '__main__':
    try:
        setup()
        app.run(debug = True, host='0.0.0.0')
    finally:
        GPIO.cleanup()
