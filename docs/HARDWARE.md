# DRAIN X Hardware

## Components

- Arduino UNO
- HC-SR04 ultrasonic sensor
- Relay module
- DC water pump
- External pump power supply
- Jumper wires

## Sensor interpretation

The ultrasonic sensor measures distance to the water surface.

Distance decreases as water rises.

## Pump

The Arduino drives a relay. The relay switches the pump's separate power circuit.

Never drive a high-current pump directly from an Arduino GPIO.
