# DRAIN X Arduino Node

## Pins

| Component | Arduino |
|---|---|
| HC-SR04 TRIG | D9 |
| HC-SR04 ECHO | D10 |
| Relay IN | D7 |

The exact relay logic depends on the relay module. The firmware defaults to active-LOW.

## Serial

9600 baud.

Example:

```text
Distance: 24.01 cm
Distance: 15.00 cm
Distance: 8.00 cm
>>> WATER HIGH - PUMP ON
Distance: 16.00 cm
>>> WATER LOW - PUMP OFF
```

## Safety

Use an external supply appropriate for the pump. The Arduino should only control the relay input.
