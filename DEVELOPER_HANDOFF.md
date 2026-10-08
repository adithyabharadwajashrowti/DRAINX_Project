# DRAIN X — Developer Handoff

## 1. Goal

Build and maintain a working hardware + software prototype for intelligent urban waterlogging monitoring and response.

The intended closed loop is:

SENSE -> ANALYZE -> DECIDE -> ACT -> VERIFY

## 2. End-to-end architecture

Ultrasonic Sensor
        |
        v
Arduino UNO
        |
     USB Serial
        |
        v
Python Gateway
        |
       HTTP
        |
        v
Supabase PostgreSQL
        |
    Realtime
        |
        v
React/Vite Dashboard

## 3. Hardware

Current prototype:

- Arduino UNO
- HC-SR04 ultrasonic sensor
- Relay module
- DC water pump
- External pump power

Arduino serial baud rate: 9600.

Current development computer has used COM4, but COM ports can change.

## 4. Arduino behavior

The Arduino measures the distance to the water surface.

Smaller distance means the water is closer to the sensor.

Reference states:

- SAFE: distance > 15 cm
- WARNING: 8-15 cm
- CRITICAL: <= 8 cm

At critical level the relay can activate the pump. Pump shutdown should use a recovery threshold/hysteresis so the relay does not chatter.

The Arduino emits machine-readable serial messages such as:

`Distance: 24.01 cm`

`>>> WATER HIGH - PUMP ON`

`>>> WATER LOW - PUMP OFF`

## 5. Gateway behavior

`gateway/gateway.py`:

1. Opens the Arduino serial port.
2. Parses `Distance: X cm`.
3. Tracks successive readings.
4. Calculates a rate-of-change/rise-rate metric.
5. Derives SAFE/WARNING/CRITICAL.
6. Parses pump state.
7. Sends telemetry to Supabase.
8. Reports errors without crashing the loop.

## 6. Supabase

Important tables:

- `profiles`
- `citizen_reports`
- `report_images`
- `telemetry_readings`
- `hardware_devices`
- `pump_events`
- `call_requests`
- `audit_events`
- `system_settings`

Telemetry fields:

- `device_id`
- `water_level`
- `rise_rate`
- `risk_state`
- `pump_state`
- `recorded_at`

Current device ID:

`DRAINX-NODE-01`

## 7. Citizen workflow

Citizen can:

1. Register/login.
2. Submit a waterlogging report.
3. Enter location and description.
4. Select severity.
5. Optionally send GPS coordinates.
6. Upload up to three images.
7. Submit the report.

Reports are stored in `citizen_reports`.

Images use the private `report-images` storage bucket.

## 8. Admin workflow

Admin dashboard should show:

- telemetry
- water level
- risk state
- pump state
- hardware status
- citizen reports
- report images
- audit activity

Realtime updates should be used where configured.

## 9. Hardware status

Do not assume a browser can directly prove Arduino connectivity.

The real chain is:

Arduino connected
 -> gateway receives serial data
 -> gateway sends telemetry
 -> Supabase receives telemetry
 -> dashboard sees recent telemetry

A stale dashboard can therefore mean the gateway or telemetry path is down even if the Arduino itself is powered.

## 10. Development priority

Priority 1: validate Arduino -> COM port.

Priority 2: validate gateway parsing.

Priority 3: validate gateway -> Supabase telemetry.

Priority 4: validate Realtime -> dashboard.

Priority 5: implement reliable heartbeat/last-seen.

Priority 6: multi-node support.

Priority 7: upstream/downstream node coordination.

Priority 8: production authentication and deployment.

## 11. Do not break working hardware

Test each layer independently.

Arduino/Serial Monitor
-> Python Gateway
-> Supabase
-> Dashboard

Do not debug every layer at once.

## 12. Production note

The prototype currently uses a simple telemetry ingestion path. For production, use authenticated/server-side ingestion or an Edge Function rather than allowing anonymous clients to write arbitrary telemetry.
