# DRAIN X 🌊

## Intelligent Urban Waterlogging Monitoring & Response System

DRAIN X is a full-stack hardware + software prototype for real-time urban waterlogging detection, risk assessment, automated pump response, citizen reporting and an Emergency Operations Centre dashboard.

### Core loop

**SENSE → ANALYZE → DECIDE → ACT → VERIFY**

### Architecture

```text
Ultrasonic Sensor
      ↓
 Arduino UNO
      ↓ USB Serial
 Python Gateway
      ↓ HTTP
   Supabase
      ↓ Realtime
 React / Vite Dashboard
```

## Repository

```text
drainx/
├── src/                         # React + TypeScript frontend
├── gateway/                     # Python serial → Supabase gateway
├── arduino/                     # Arduino UNO firmware
├── supabase/                    # Database/policy documentation
├── docs/                        # Architecture and setup docs
├── DEVELOPER_HANDOFF.md
├── README.md
├── .env.example
└── .gitignore
```

## Frontend features

- Supabase authentication
- Citizen portal
- Citizen waterlogging reports
- Severity selection
- Photo uploads to private Supabase Storage
- Admin/EOC dashboard
- Live telemetry display
- Risk state display
- Pump state display
- Hardware node display
- Realtime subscriptions
- Report status management

## Hardware

- Arduino UNO
- HC-SR04 ultrasonic sensor
- Relay module
- DC water pump
- Appropriate external pump power supply

## Gateway

The Python gateway reads Arduino serial output, calculates a rate-of-rise metric, classifies risk and posts telemetry to Supabase.

Default serial configuration:

```text
COM4
9600 baud
DRAINX-NODE-01
```

## Current prototype thresholds

These are distance-from-sensor thresholds and must be calibrated for the physical installation:

```text
SAFE       > 15 cm
WARNING    > 8 cm and <= 15 cm
CRITICAL   <= 8 cm
```

## Frontend setup

```bash
npm install
```

Create `.env` from `.env.example` and put in your Supabase URL and anon/public key.

Then:

```bash
npm run dev
```

Build:

```bash
npm run build
```

## Gateway setup

```bash
cd gateway
pip install -r requirements.txt
python gateway.py --port COM4 --baud 9600
```

## Arduino setup

Open `arduino/drainx_node.ino` in Arduino IDE, select Arduino UNO and the correct COM port, upload it, then open Serial Monitor at 9600 baud.

## Supabase

The application uses:

- Auth
- PostgreSQL
- Storage
- Realtime
- Row Level Security

See `supabase/` for the actual prototype schema reference and security notes.

## Security

**Never commit `.env`, passwords, service-role keys or other private credentials.**

The browser uses the Supabase anon/public key. For production, telemetry ingestion should be moved behind authenticated/server-side infrastructure or a Supabase Edge Function.

## Debugging order

Always test in this order:

1. Arduino hardware
2. Arduino Serial Monitor
3. Python gateway
4. Supabase telemetry table
5. React dashboard

This prevents debugging all layers at once.

## Developer handoff

Start with `DEVELOPER_HANDOFF.md`, then read:

- `docs/ARCHITECTURE.md`
- `docs/HARDWARE.md`
- `docs/API_AND_DATA_FLOW.md`
- `docs/DEVELOPER_SETUP.md`
