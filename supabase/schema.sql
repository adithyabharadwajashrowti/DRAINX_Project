-- DRAIN X database reference
--
-- This file documents the ACTUAL application tables used by the prototype.
-- It is intentionally not a blind migration script.
-- Inspect the live Supabase project before applying any CREATE/ALTER statements.

-- profiles
-- id, role, full_name, phone, created_at

-- citizen_reports
-- id, citizen_id, location_text, description, severity, status,
-- latitude, longitude, created_at, updated_at

-- report_images
-- id, report_id, storage_path, original_name, content_type, created_at

-- telemetry_readings
-- id, device_id, water_level, rise_rate, risk_state, pump_state, recorded_at

-- hardware_devices
-- id, device_id, device_name, is_active, last_seen_at, created_at

-- pump_events
-- id, device_id, mode, reason, created_at

-- call_requests
-- id, citizen_id, status, created_at, updated_at

-- audit_events
-- id, actor_id, event_type, metadata, message, created_at

-- system_settings
-- id, updated_at
