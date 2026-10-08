# DRAIN X Python Gateway

## Purpose

Connect the Arduino serial stream to Supabase telemetry.

## Install

```bash
pip install -r requirements.txt
```

## Environment

Create a `.env` in the project root or gateway directory with:

```env
VITE_SUPABASE_URL=...
VITE_SUPABASE_ANON_KEY=...
DRAINX_DEVICE_ID=DRAINX-NODE-01
DRAINX_SERIAL_PORT=COM4
DRAINX_BAUD_RATE=9600
```

## Run

```bash
python gateway.py --port COM4 --baud 9600
```

## Serial protocol

Expected Arduino lines:

```text
Distance: 24.01 cm
>>> WATER HIGH - PUMP ON
>>> WATER LOW - PUMP OFF
```

## Important

The gateway assumes the `water_level` database field currently represents the measured distance in cm. If the database/UI later changes to true water depth, add a known mounting height and convert distance to depth consistently.
