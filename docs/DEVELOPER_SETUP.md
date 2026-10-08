# DRAIN X Developer Setup

## Requirements

- Node.js
- npm
- Python 3
- Git
- Arduino IDE

## Frontend

From repository root:

```bash
npm install
npm run dev
```

Create `.env` from `.env.example`.

## Gateway

```bash
cd gateway
pip install -r requirements.txt
python gateway.py --port COM4 --baud 9600
```

## Arduino

Open `arduino/drainx_node.ino` in Arduino IDE.

Select Arduino UNO and the correct COM port.

Upload.

Open Serial Monitor at 9600 baud.

## Debug order

1. Arduino hardware
2. Serial Monitor
3. Python gateway
4. Supabase telemetry
5. Dashboard

Do not debug all five layers simultaneously.
