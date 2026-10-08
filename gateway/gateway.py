import argparse
import os
import re
import time
from datetime import datetime, timezone

import requests
import serial
from dotenv import load_dotenv

load_dotenv()

DEFAULT_PORT = os.getenv("DRAINX_SERIAL_PORT", "COM4")
DEFAULT_BAUD = int(os.getenv("DRAINX_BAUD_RATE", "9600"))
DEVICE_ID = os.getenv("DRAINX_DEVICE_ID", "DRAINX-NODE-01")

SUPABASE_URL = os.getenv("VITE_SUPABASE_URL", "").rstrip("/")
SUPABASE_ANON_KEY = os.getenv("VITE_SUPABASE_ANON_KEY", "")

DISTANCE_RE = re.compile(r"Distance:\s*([-+]?\d+(?:\.\d+)?)\s*cm", re.I)


def classify(distance_cm: float, critical: float, warning: float) -> str:
    if distance_cm <= critical:
        return "CRITICAL"
    if distance_cm <= warning:
        return "WARNING"
    return "SAFE"


def send_telemetry(distance_cm, rise_rate, risk_state, pump_state):
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        print("[SUPABASE] Missing VITE_SUPABASE_URL or VITE_SUPABASE_ANON_KEY")
        return False

    url = f"{SUPABASE_URL}/rest/v1/telemetry_readings"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }
    payload = {
        "device_id": DEVICE_ID,
        "water_level": distance_cm,
        "rise_rate": rise_rate,
        "risk_state": risk_state,
        "pump_state": pump_state,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if 200 <= response.status_code < 300:
            print("[SUPABASE] Ingestion: SUCCESS")
            return True

        print(f"[SUPABASE] HTTP {response.status_code}: {response.text}")
        return False
    except requests.RequestException as exc:
        print(f"[SUPABASE] Network error: {exc}")
        return False


def main():
    parser = argparse.ArgumentParser(description="DRAIN X Arduino telemetry gateway")
    parser.add_argument("--port", default=DEFAULT_PORT)
    parser.add_argument("--baud", type=int, default=DEFAULT_BAUD)
    parser.add_argument("--critical", type=float, default=8.0)
    parser.add_argument("--warning", type=float, default=15.0)
    parser.add_argument("--interval", type=float, default=1.0)
    args = parser.parse_args()

    print("=== DRAIN X Gateway ===")
    print(f"Device : {DEVICE_ID}")
    print(f"Serial : {args.port} @ {args.baud}")
    print(f"Critical <= {args.critical} cm")
    print(f"Warning  <= {args.warning} cm")
    print("Listening...")

    try:
        ser = serial.Serial(args.port, args.baud, timeout=1)
    except serial.SerialException as exc:
        print(f"[SERIAL] Could not open {args.port}: {exc}")
        return

    previous_distance = None
    previous_time = None
    pump_state = False
    last_sent = 0.0

    try:
        while True:
            raw = ser.readline().decode("utf-8", errors="ignore").strip()
            if not raw:
                continue

            if "WATER HIGH - PUMP ON" in raw.upper():
                pump_state = True
                print("[PUMP] ON")
                continue

            if "WATER LOW - PUMP OFF" in raw.upper():
                pump_state = False
                print("[PUMP] OFF")
                continue

            match = DISTANCE_RE.search(raw)
            if not match:
                if "SENSOR ERROR" in raw.upper():
                    print("[SENSOR] SENSOR ERROR")
                continue

            distance = float(match.group(1))
            now = time.time()

            if previous_distance is not None and previous_time is not None:
                dt = now - previous_time
                # Distance decreases when water rises.
                # Convert to positive "water rise" rate by using -delta distance.
                rise_rate = ((previous_distance - distance) / dt) * 60.0 if dt > 0 else 0.0
            else:
                rise_rate = 0.0

            risk = classify(distance, args.critical, args.warning)

            print(
                f"[TELEMETRY] level={distance:.2f} cm | "
                f"rise_rate={rise_rate:+.2f} cm/min | "
                f"risk={risk} | pump={'ON' if pump_state else 'OFF'}"
            )

            if now - last_sent >= args.interval:
                send_telemetry(distance, rise_rate, risk, pump_state)
                last_sent = now

            previous_distance = distance
            previous_time = now

    except KeyboardInterrupt:
        print("\nStopping gateway.")
    finally:
        ser.close()


if __name__ == "__main__":
    main()
