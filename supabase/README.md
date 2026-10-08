# DRAIN X Supabase

## Services

- Supabase Auth
- PostgreSQL
- Storage
- Realtime
- Row Level Security

## Main tables

`profiles`
`citizen_reports`
`report_images`
`telemetry_readings`
`hardware_devices`
`pump_events`
`call_requests`
`audit_events`
`system_settings`

## Storage

Private bucket:

`report-images`

Expected path:

`{citizen-user-id}/{report-id}/{filename}`

## Telemetry

Gateway writes to:

`telemetry_readings`

## Security

Never commit service-role keys, passwords or private credentials.
