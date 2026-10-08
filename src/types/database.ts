export type Role='ADMIN'|'CITIZEN'; export type RiskState='SAFE'|'WARNING'|'CRITICAL';
export interface Profile{id:string;role:Role;full_name:string|null;phone:string|null;created_at:string}
export interface CitizenReport{id:string;citizen_id:string;location_text:string;description:string;severity:string;status:string;latitude:number|null;longitude:number|null;created_at:string;updated_at:string}
export interface ReportImage{id:string;report_id:string;storage_path:string;original_name:string;content_type:string;created_at:string}
export interface Telemetry{id:string;device_id:string;water_level:number;rise_rate:number;risk_state:RiskState;pump_state:boolean;recorded_at:string}
export interface HardwareDevice{id:string;device_id:string;device_name:string;is_active:boolean;last_seen_at:string|null;created_at:string}
export interface PumpEvent{id:string;device_id:string;mode:string;reason:string|null;created_at:string}
export interface AuditEvent{id:string;actor_id:string|null;event_type:string;metadata:Record<string,unknown>|null;message:string|null;created_at:string}
