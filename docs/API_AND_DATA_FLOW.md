# DRAIN X Data Flow

## Telemetry

Arduino produces a distance reading.

Gateway converts it into:

- water level/distance
- rise rate
- risk state
- pump state

The gateway posts these values to `telemetry_readings`.

## Example

```json
{
  "device_id": "DRAINX-NODE-01",
  "water_level": 12.4,
  "rise_rate": 3.2,
  "risk_state": "WARNING",
  "pump_state": false
}
```

## Citizen report

Citizen submits location, description, severity, GPS and optional images.

Text/metadata -> `citizen_reports`

Images -> private `report-images` bucket
