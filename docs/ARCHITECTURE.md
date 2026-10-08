# DRAIN X Architecture

## Hardware path

Ultrasonic sensor
-> Arduino UNO
-> USB serial
-> Python gateway
-> Supabase
-> Realtime
-> React dashboard

## Citizen path

Citizen
-> React
-> Supabase Auth
-> citizen_reports
-> report-images
-> Admin EOC

## Control loop

SENSE
-> ANALYZE
-> DECIDE
-> ACT
-> VERIFY
