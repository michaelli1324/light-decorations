# light-decorations

Light Decorations is a web application built using Flask which runs on top of the Raspberry Pi and Arduino and is used to control an RGB light strip used for decoration around the room.

## How it Works
The system works the Raspberry Pi as  both a server and central hub, which communicates with an Arduino module through an [NRF24L01 RFID transmitter](https://github.com/nRF24/RF24). The application provides a dashboard interface which can be used to control the various modes available. 

Currently, the lights can be set to the following modes:
- Rainbow Blend
- Rainbow Stripe
- Rainbow Stripe Blend
- Purple/Green
- Random
- Black/White
- Black/White Blend
- Cloud
- Party
- Red/White/Blue
- Red/White/Blue Blend

Additional color palettes can be created using the [FastLED library](http://fastled.io/)

