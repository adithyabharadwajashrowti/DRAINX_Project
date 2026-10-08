/*
  DRAIN X - Arduino UNO Node

  Hardware reference:
  HC-SR04:
    TRIG -> D9
    ECHO -> D10

  Relay:
    IN -> D7

  IMPORTANT:
  - Keep the pump on its appropriate external power supply.
  - Do NOT power a high-current pump directly from an Arduino GPIO.
  - Some relay modules are active LOW. Set RELAY_ACTIVE_LOW below accordingly.
*/

const int TRIG_PIN = 9;
const int ECHO_PIN = 10;
const int RELAY_PIN = 7;

const bool RELAY_ACTIVE_LOW = true;

// Distance thresholds from the ultrasonic sensor.
// Smaller distance = water is higher.
const float CRITICAL_DISTANCE_CM = 8.0;
const float RECOVERY_DISTANCE_CM = 15.0;

const unsigned long SAMPLE_INTERVAL_MS = 1000;

bool pumpOn = false;
unsigned long lastSample = 0;

void setPump(bool on) {
  pumpOn = on;

  if (RELAY_ACTIVE_LOW) {
    digitalWrite(RELAY_PIN, on ? LOW : HIGH);
  } else {
    digitalWrite(RELAY_PIN, on ? HIGH : LOW);
  }

  if (on) {
    Serial.println(">>> WATER HIGH - PUMP ON");
  } else {
    Serial.println(">>> WATER LOW - PUMP OFF");
  }
}

float readDistanceCm() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  unsigned long duration = pulseIn(ECHO_PIN, HIGH, 30000UL);

  if (duration == 0) {
    return -1.0;
  }

  return duration * 0.0343 / 2.0;
}

void setup() {
  Serial.begin(9600);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);

  // Start with pump OFF.
  if (RELAY_ACTIVE_LOW) {
    digitalWrite(RELAY_PIN, HIGH);
  } else {
    digitalWrite(RELAY_PIN, LOW);
  }

  Serial.println("DRAIN X NODE STARTED");
  Serial.println("Device: DRAINX-NODE-01");
}

void loop() {
  if (millis() - lastSample < SAMPLE_INTERVAL_MS) {
    return;
  }

  lastSample = millis();

  float distance = readDistanceCm();

  if (distance < 0) {
    Serial.println("SENSOR ERROR");
    return;
  }

  Serial.print("Distance: ");
  Serial.print(distance, 2);
  Serial.println(" cm");

  // Hysteresis:
  // Turn ON at critical level.
  // Turn OFF only after recovery above the safe threshold.
  if (!pumpOn && distance <= CRITICAL_DISTANCE_CM) {
    setPump(true);
  }

  if (pumpOn && distance >= RECOVERY_DISTANCE_CM) {
    setPump(false);
  }
}
