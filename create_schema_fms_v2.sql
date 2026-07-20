-- Reference Tables
CREATE TABLE IF NOT EXISTS reference.vehicle_type_ref (
vehicle_type_id SERIAL PRIMARY KEY,
vehicle_type_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS reference.maintenance_type_ref (
maintenance_type_id SERIAL PRIMARY KEY,
maintenance_type_name VARCHAR(50) UNIQUE NOT NULL
);

-- Vehicle component with serial number in a vehicle:
CREATE TABLE IF NOT EXISTS reference.component_type(
    component_id SERIAL PRIMARY KEY,
    component_name TEXT
);

INSERT INTO reference.component_type
    (component_name)
Values
    ('BATTERY'),
    ('TYRE'),
    ('FUEL_PUMP'),
    ('HYDRAULIC_PUMP'),
    ('CNG_KIT'),
    ('CNG_CYLINDER');

-- severity classification
-- MINOR
-- MODERATE
-- MAJOR
-- CRITICAL
-- BREAKDOWN
CREATE TABLE IF NOT EXISTS reference.severity (
    severity_id SMALLSERIAL PRIMARY KEY,
    Description TEXT
);

insert into reference.severity
    (Description)
values
    ('MINOR'),
    ('MODERATE'),
    ('MAJOR'),
    ('CRITICAL'),
    ('BREAKDOWN');

CREATE TABLE IF NOT EXISTS reference.fuel_type_ref(
    fuel_type_id SMALLSERIAL PRIMARY KEY,
    description TEXT
);

INSERT INTO reference.fuel_type_ref
(description)
values
('Diesel'),
('Petrol'),
('CNG'),
('LNG'),
('EV');

CREATE TABLE IF NOT EXISTS reference.vehicle_status_ref(
    fuel_type_id SMALLSERIAL PRIMARY KEY,
    description TEXT
);
INSERT INTO reference.vehicle_status_ref
(description)
values
('ACTIVE'),
('WORKSHOP'),
('BREAKDOWN'),
('SCRAPPED'),
('SOLD');

-- Master Tables
-- Vehicle Master
CREATE TABLE IF NOT EXISTS master.vehicle_master (
    vehicle_id BIGSERIAL PRIMARY KEY,
    vehicle_type_id INT REFERENCES reference.vehicle_type_ref(vehicle_type_id),
    purchase_date DATE,
    rc_number VARCHAR(50),
    rc_expiry_date DATE,
    engine_no VARCHAR(100) UNIQUE,
    chassis_no VARCHAR(100) UNIQUE,
    gps_id VARCHAR(50) UNIQUE,
    fuel_type VARCHAR(20)
        reference reference.fuel_key_ref(description),
    vehicle_status VARCHAR(20)
        reference reference.vehicle_status_ref(description),
    fuel_capacity NUMERIC(4,2),
    active_flag BOOLEAN DEFAULT TRUE,
last_pm_date DATE,
last_workshop_date DATE,
last_job_card_id INT,
last_breakdown_id INT,
puc_last_date DATE,
fit_date DATE,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- components used with serial number in the vehicle
CREATE TABLE IF NOT EXISTS master.vehicle_component (
    component_id BIGSERIAL PRIMARY KEY,
    vehicle_id BIGINT
        REFERENCES master.vehicle_master(vehicle_id),
    component_type INT 
        REFERENCES reference.component_type(component_id),
    serial_number VARCHAR(200),
    installed_date DATE,
    removed_date DATE,
    status VARCHAR(20)
);

-- Employee Master
CREATE TABLE IF NOT EXISTS master.employee_master (
    employee_id SERIAL PRIMARY KEY,
    employee_type VARCHAR(30),
    full_name VARCHAR(100),
    phone_number VARCHAR(15) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Driver Master
CREATE TABLE IF NOT EXISTS master.driver_master (
    driver_id BIGSERIAL PRIMARY KEY,
    driver_name VARCHAR(200) NOT NULL,
    mobile_number VARCHAR(20) NOT NULL,
    dl_number VARCHAR(100) UNIQUE,
    dl_issue_city VARCHAR(100),
    dl_expiry_date DATE,
    permanent_address TEXT,
    current_address TEXT,
    zone VARCHAR(100),
    area VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Transaction Tables
--Driver Vehicle assignment history
CREATE TABLE IF NOT EXISTS operations.driver_vehicle_assignment (
    assignment_id BIGSERIAL PRIMARY KEY,
    driver_id BIGINT
      REFERENCES master.driver_master(driver_id),
    vehicle_id BIGINT
      REFERENCES master.vehicle_master(vehicle_id),
    start_date TIMESTAMP,
    end_date TIMESTAMP
);

-- Helper Assignment table
CREATE TABLE IF NOT EXISTS operations.helper_vehicle_assignment (
    helper_assignment_id BIGSERIAL PRIMARY KEY,
    employee_id BIGINT,
    vehicle_id BIGINT,
    start_date TIMESTAMP,
    end_date TIMESTAMP
);

-- Driver Complaint
CREATE TABLE IF NOT EXISTS maintenance.vehicle_complaint (
    complaint_id BIGSERIAL PRIMARY KEY,
    vehicle_id BIGINT
        REFERENCES master.vehicle_master(vehicle_id),
    driver_id BIGINT
        REFERENCES master.driver_master(driver_id),
    complaint_date TIMESTAMP,
    issue_description TEXT,
    driver_reason TEXT,
    vehicle_received_at TIMESTAMP
);

-- Technical Inspection
CREATE TABLE IF NOT EXISTS maintenance.technician_inspection (
    inspection_id BIGSERIAL PRIMARY KEY,
    complaint_id BIGINT
       REFERENCES maintenance.vehicle_complaint(complaint_id),
    technician_id BIGINT,
    inspection_time TIMESTAMP,
    observed_issue TEXT,
    operator_notes TEXT,
    status VARCHAR(30)
);

-- GPS Raw Data (Time-Series)
CREATE TABLE IF NOT EXISTS timeseries.gps_raw_data (
    id BIGSERIAL PRIMARY KEY,
    vehicle_id VARCHAR(20) REFERENCES master.vehicle_master(vehicle_id),
    gps_timestamp TIMESTAMP NOT NULL,
    latitude NUMERIC,
    longitude NUMERIC,
    speed NUMERIC,
    heading NUMERIC,
    altitude NUMERIC,
    ignition_status NUMERIC,
    device_timestamp TIMESTAMP,
    server_timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Maintenance Job Card
CREATE TABLE IF NOT EXISTS transaction.maintenance_job_card (
    job_card_id SERIAL PRIMARY KEY,
    complaint_id BIGINT,
    inspection_id BIGINT,
    vehicle_id VARCHAR(20) REFERENCES master.vehicle_master(vehicle_id),
    maintenance_type_id INT REFERENCES reference.maintenance_type_ref(maintenance_type_id),
    severity VARCHAR(20),
    approval_required BOOLEAN DEFAULT FALSE,
    approved_by BIGINT,
    labour_charges NUMERIC(12,2),
    job_status VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- Extend Maintenance Table (if not already done)
    job_card_status VARCHAR(20),
    completion_date DATE,
    downtime_hours NUMERIC(6,2),

    description TEXT
);

-- Maintenance Parts Usage
CREATE TABLE IF NOT EXISTS maintenance.job_card_part (
    id BIGSERIAL PRIMARY KEY,
    job_card_id BIGINT,
    part_id BIGINT,
    quantity NUMERIC(12,2),
    unit_price NUMERIC(12,2),
    total_price NUMERIC(12,2)
);

-- Requested Parts
CREATE TABLE IF NOT EXISTS inventory.part_request (
    request_id BIGSERIAL PRIMARY KEY,
    request_number VARCHAR(50) NOT NULL UNIQUE,
    vehicle_id BIGINT NOT NULL
        REFERENCES master.vehicle_master(vehicle_id),
    job_card_id BIGINT
        REFERENCES maintenance.job_card(job_card_id),
    technician_id BIGINT NOT NULL
        REFERENCES master.employee_master(employee_id),
    supervisor_id BIGINT
        REFERENCES master.employee_master(employee_id),
    driver_id BIGINT
        REFERENCES master.driver_master(driver_id),
    issue_description TEXT,
    request_type VARCHAR(20) NOT NULL
        CHECK (
            request_type IN (
                'REGULAR',
                'MAJOR',
                'EMERGENCY'
            )
        ),
    approval_required BOOLEAN NOT NULL DEFAULT FALSE,
    request_status VARCHAR(30) NOT NULL DEFAULT 'DRAFT'
        CHECK (
            request_status IN (
                'DRAFT',
                'SUBMITTED',
                'PENDING_APPROVAL',
                'APPROVED',
                'REJECTED',
                'ISSUED',
                'CANCELLED'
            )
        ),
    requested_datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    approved_datetime TIMESTAMP,
    approved_by BIGINT
        REFERENCES master.employee_master(employee_id),
    remarks TEXT,
    created_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inventory Part Request Items
CREATE TABLE IF NOT EXISTS inventory.part_request_item (
    request_item_id BIGSERIAL PRIMARY KEY,
    request_id BIGINT NOT NULL
        REFERENCES inventory.part_request(request_id)
        ON DELETE CASCADE,
    part_id BIGINT NOT NULL
        REFERENCES inventory.part_master(part_id),
    requested_quantity NUMERIC(10,2) NOT NULL
        CHECK (requested_quantity > 0),
    approved_quantity NUMERIC(10,2),
    issued_quantity NUMERIC(10,2),
    unit_price NUMERIC(12,2),
    estimated_cost NUMERIC(14,2),
    requires_approval BOOLEAN DEFAULT FALSE,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inventory Part Issue
CREATE TABLE IF NOT EXISTS inventory.part_issue (
    issue_id BIGSERIAL PRIMARY KEY,
    issue_number VARCHAR(50) NOT NULL UNIQUE,
    request_id BIGINT NOT NULL
        REFERENCES inventory.part_request(request_id),
    vehicle_id BIGINT NOT NULL
        REFERENCES master.vehicle_master(vehicle_id),
    job_card_id BIGINT
        REFERENCES maintenance.job_card(job_card_id),
    issued_by BIGINT NOT NULL
        REFERENCES master.employee_master(employee_id),
    receiver_id BIGINT NOT NULL
        REFERENCES master.employee_master(employee_id),
    issue_datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    issue_status VARCHAR(30) NOT NULL DEFAULT 'ISSUED'
        CHECK (
            issue_status IN (
                'ISSUED',
                'PARTIALLY_ISSUED',
                'RECEIVED',
                'RETURNED',
                'CANCELLED'
            )
        ),
    store_remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by BIGINT
);


-- Issue Line Items
CREATE TABLE IF NOT EXISTS inventory.part_issue_item (
    issue_item_id BIGSERIAL PRIMARY KEY,
    issue_id BIGINT NOT NULL
        REFERENCES inventory.part_issue(issue_id)
        ON DELETE CASCADE,
    request_item_id BIGINT
        REFERENCES inventory.part_request_item(request_item_id),
    part_id BIGINT NOT NULL
        REFERENCES inventory.part_master(part_id),
    issued_quantity NUMERIC(10,2) NOT NULL,
    unit_price NUMERIC(12,2),
    total_price NUMERIC(14,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Inventory Part Receipt
CREATE TABLE IF NOT EXISTS inventory.part_receipt (
    receipt_id BIGSERIAL PRIMARY KEY,
    receipt_number VARCHAR(50) UNIQUE NOT NULL,
    issue_id BIGINT NOT NULL
        REFERENCES inventory.part_issue(issue_id),
    received_by BIGINT NOT NULL
        REFERENCES master.employee_master(employee_id),
    receiver_name VARCHAR(200),
    received_datetime TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    receipt_status VARCHAR(30)
        DEFAULT 'RECEIVED'
        CHECK (
            receipt_status IN (
                'RECEIVED',
                'PARTIALLY_RECEIVED',
                'REJECTED',
                'MISSING_ITEMS'
            )
        ),
    remarks TEXT,
    acknowledged_by BIGINT
        REFERENCES master.employee_master(employee_id),
    acknowledged_datetime TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Receipt Items
CREATE TABLE IF NOT EXISTS inventory.part_receipt_item (
    receipt_item_id BIGSERIAL PRIMARY KEY,
    receipt_id BIGINT NOT NULL
        REFERENCES inventory.part_receipt(receipt_id)
        ON DELETE CASCADE,
    issue_item_id BIGINT
        REFERENCES inventory.part_issue_item(issue_item_id),
    part_id BIGINT
        REFERENCES inventory.part_master(part_id),
    expected_qty NUMERIC(10,2),
    received_qty NUMERIC(10,2),
    shortage_qty NUMERIC(10,2),
    remarks TEXT
);


-- Approval work flow
-- for inventory utilization 

CREATE TABLE IF NOT EXISTS inventory.approval_request (
    approval_id BIGSERIAL PRIMARY KEY,
    request_id BIGINT NOT NULL
        REFERENCES inventory.part_request(request_id),
    approver_id BIGINT NOT NULL
        REFERENCES master.employee_master(employee_id),
    approval_type VARCHAR(30)
        CHECK (
            approval_type IN (
                'PART_REQUEST',
                'MAINTENANCE',
                'PURCHASE'
            )
        ),
    approval_status VARCHAR(20)
        DEFAULT 'PENDING'
        CHECK (
            approval_status IN (
                'PENDING',
                'APPROVED',
                'REJECTED'
            )
        ),
    comments TEXT,
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP
);

-- WhatsApp Integration in approval workflow
-- WhatsApp Message Audit Log
-- Required for approval workflow and audit compliance.
-- WhatsApp Message Log
-- Stores actual message sent.
CREATE TABLE IF NOT EXISTS integration.whatsapp_message_log (
    message_id BIGSERIAL PRIMARY KEY,
    approval_id BIGINT
        REFERENCES inventory.approval_request(approval_id),
    recipient_mobile VARCHAR(20) NOT NULL,
    message_type VARCHAR(50),
    message_body TEXT,
    provider_message_id VARCHAR(200),
    send_status VARCHAR(30)
        DEFAULT 'QUEUED'
        CHECK (
            send_status IN (
                'QUEUED',
                'SENT',
                'DELIVERED',
                'READ',
                'FAILED'
            )
        ),
    sent_at TIMESTAMP,
    delivered_at TIMESTAMP,
    read_at TIMESTAMP,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Approval Response Audit
-- Stores what manager actually selected.
CREATE TABLE IF NOT EXISTS inventory.approval_response_audit (
    response_id BIGSERIAL PRIMARY KEY,
    approval_id BIGINT NOT NULL
        REFERENCES inventory.approval_request(approval_id),
    action_taken VARCHAR(20)
        CHECK (
            action_taken IN (
                'APPROVED',
                'REJECTED'
            )
        ),
    response_source VARCHAR(20)
        DEFAULT 'WHATSAPP'
        CHECK (
            response_source IN (
                'WHATSAPP',
                'WEB',
                'MOBILE_APP'
            )
        ),
    responded_by BIGINT
        REFERENCES master.employee_master(employee_id),
    response_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    remarks TEXT
);
-- Store Inventory
CREATE TABLE IF NOT EXISTS inventory.part_master (
    part_id BIGSERIAL PRIMARY KEY,
    part_code VARCHAR(100),
    part_name VARCHAR(300),
    vehicle_type_id INT,
    part_category VARCHAR(100),
    approval_required BOOLEAN,
    reorder_level INTEGER,
    max_stock INTEGER
);

-- Stock Ledger
CREATE TABLE IF NOT EXISTS inventory.stock_transaction (
    stock_txn_id BIGSERIAL PRIMARY KEY,
    part_id BIGINT,
    txn_type VARCHAR(20),
    quantity NUMERIC(10,2),
    txn_datetime TIMESTAMP,
    reference_id BIGINT,
    opening_balance NUMERIC(10,2),
    closing_balance NUMERIC(10,2),
    unit_cost NUMERIC(10,2),
    warehouse_id NUMERIC(3)
);

-- Gate Pass Management
-- General Gate Pass
CREATE TABLE IF NOT EXISTS operations.gate_pass_regular (
    gate_pass_id BIGSERIAL PRIMARY KEY,
    employee_id BIGINT,
    purpose TEXT,
    time_out TIMESTAMP,
    time_in TIMESTAMP,
    supervisor_id BIGINT
);

-- Technical Gate Pass
CREATE TABLE IF NOT EXISTS operations.gate_pass_technical (
    gate_pass_id BIGSERIAL PRIMARY KEY,
    employee_id BIGINT,
    vehicle_id BIGINT,
    area VARCHAR(200),
    issue_reported TEXT,
    tow_vehicle_number VARCHAR(50),
    tool_kit_details TEXT,
    time_out TIMESTAMP,
    time_in TIMESTAMP,
    supervisor_id BIGINT
);

-- Preventive Maintenance
CREATE TABLE IF NOT EXISTS maintenance.preventive_maintenance_checklist (
    checklist_id BIGSERIAL PRIMARY KEY,
    vehicle_id BIGINT,
    technician_id BIGINT,
    inspection_datetime TIMESTAMP,
    observation TEXT,
    issue_found BOOLEAN,
    issue_description TEXT,
    maintenance_action TEXT,
    final_status VARCHAR(30)
);


-- Daily checklist
-- Preventive Maintenance Checklist Master
-- Instead of hardcoding columns such as "Vehicle Washing", "Brake Oil", etc., use configurable checklist items.

CREATE TABLE IF NOT EXISTS maintenance.checklist_master (
    checklist_item_id BIGSERIAL PRIMARY KEY,
    checklist_code VARCHAR(50) UNIQUE NOT NULL,
    checklist_name VARCHAR(200) NOT NULL,
    checklist_category VARCHAR(100),
    frequency_type VARCHAR(30)
        CHECK (
            frequency_type IN (
                'DAILY',
                'WEEKLY',
                'MONTHLY',
                'QUARTERLY',
                'YEARLY'
            )
        ),
    vehicle_type_id INT
        REFERENCES reference.vehicle_type_ref(vehicle_type_id),
    mandatory_flag BOOLEAN DEFAULT TRUE,
    requires_photo BOOLEAN DEFAULT FALSE,
    requires_reading BOOLEAN DEFAULT FALSE,
    active_flag BOOLEAN DEFAULT TRUE,
    display_order INTEGER,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by BIGINT,
    modified_at TIMESTAMP,
    modified_by BIGINT
);

INSERT INTO maintenance.checklist_master
(checklist_code, checklist_name, frequency_type)
VALUES
('WASHING','Vehicle Washing','DAILY'),
('TYRE','Tyre Inspection','DAILY'),
('BATTERY','Battery Check','DAILY'),
('BRAKE','Brake Oil Check','DAILY'),
('ENGINE_OIL','Engine Oil Level','DAILY'),
('LIGHTS','Lights Inspection','DAILY'),
('HYDRAULIC','Hydraulic System Check','DAILY'),
('CNG_LEAK','CNG Leakage Check','DAILY');


-- Inventory Table

CREATE TABLE IF NOT EXISTS transaction.inventory (
spare_part_id SERIAL PRIMARY KEY,
vehicle_type_id INT REFERENCES reference.vehicle_type_ref(vehicle_type_id),
quantity INT NOT NULL,
part_type VARCHAR(50),
price NUMERIC,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Spare Parts Mapping (Job Card)
CREATE TABLE IF NOT EXISTS transaction.job_card_parts (
id SERIAL PRIMARY KEY,
job_card_id INT REFERENCES transaction.maintenance_job_card(job_card_id),
spare_part_id INT REFERENCES transaction.inventory(spare_part_id),
quantity INT NOT NULL
);

-- Fuel Rate Reference
CREATE TABLE IF NOT EXISTS reference.fuel_rate_reference (
    id SERIAL PRIMARY KEY,
    fuel_type VARCHAR(20) NOT NULL,
    price_per_unit NUMERIC(10,2) NOT NULL,
    effective_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Fuel Transactions
CREATE TABLE IF NOT EXISTS transaction.fuel_transactions (
    fuel_txn_id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(20) NOT NULL,
    fuel_date DATE NOT NULL,
    fuel_quantity NUMERIC(10,2) NOT NULL,
    fuel_price_per_unit NUMERIC(10,2),
    total_fuel_cost NUMERIC(12,2),
    odometer_reading NUMERIC(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fuel_vehicle
    FOREIGN KEY (vehicle_id)
    REFERENCES master.vehicle_master(vehicle_id)
);


-- Employee Salary
CREATE TABLE IF NOT EXISTS transaction.employee_salary (
    salary_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    salary_month DATE NOT NULL,
    base_salary NUMERIC(12,2) NOT NULL,
    allowances NUMERIC(12,2) DEFAULT 0,
    deductions NUMERIC(12,2) DEFAULT 0,
    net_salary NUMERIC(12,2),
    payment_status VARCHAR(20) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_salary_employee
    FOREIGN KEY (employee_id)
    REFERENCES master.employee_master(employee_id)
);


-- Attendance Tracking
CREATE TABLE IF NOT EXISTS transaction.attendance_tracking (
    attendance_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    status VARCHAR(20) CHECK (status IN ('PRESENT', 'ABSENT', 'LEAVE')),
    shift_hours NUMERIC(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_attendance_employee
    FOREIGN KEY (employee_id)
    REFERENCES master.employee_master(employee_id)
);


-- Add Spare Parts Consumption Table
CREATE TABLE IF NOT EXISTS transaction.maintenance_parts_usage (
    id SERIAL PRIMARY KEY,
    job_card_id INT REFERENCES transaction.maintenance_job_card(job_card_id),
    spare_part_id INT REFERENCES transaction.inventory(spare_part_id),
    quantity INT NOT NULL,
    total_cost NUMERIC(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Explore future tables
CREATE TABLE IF NOT EXISTS master.location();
-- not required as of now because working for one city onle
--    CREATE TABLE IF NOT EXISTS master.zone
--  CREATE TABLE IF NOT EXISTS master.area
CREATE TABLE IF NOT EXISTS master.vendor();
CREATE TABLE IF NOT EXISTS master.workshop();
CREATE TABLE IF NOT EXISTS master.warehouse();
CREATE TABLE IF NOT EXISTS master.tool_kit();
--  CREATE TABLE IF NOT EXISTS master.fuel_station

-- Missing analytics tables
-- CREATE TABLE IF NOT EXISTS analytics.vehicle_health_score
-- CREATE TABLE IF NOT EXISTS analytics.daily_vehicle_cost
-- CREATE TABLE IF NOT EXISTS analytics.fuel_efficiency
-- CREATE TABLE IF NOT EXISTS analytics.breakdown_risk
-- CREATE TABLE IF NOT EXISTS analytics.maintenance_kpi

-- Indexes at one place

CREATE INDEX idx_parts_job_card
ON transaction.maintenance_parts_usage(job_card_id);

CREATE INDEX idx_part_request_vehicle
ON inventory.part_request(vehicle_id);

CREATE INDEX idx_part_request_job_card
ON inventory.part_request(job_card_id);

CREATE INDEX idx_part_request_status
ON inventory.part_request(request_status);

CREATE INDEX idx_part_request_datetime
ON inventory.part_request(requested_datetime DESC);

CREATE INDEX idx_attendance_employee_date
ON transaction.attendance_tracking (employee_id, attendance_date DESC);

CREATE INDEX idx_salary_employee_month
ON transaction.employee_salary (employee_id, salary_month DESC);

CREATE INDEX idx_gps_vehicle_time
ON timeseries.gps_raw_data(vehicle_id, gps_timestamp DESC);

CREATE INDEX idx_part_issue_vehicle
ON inventory.part_issue(vehicle_id);

CREATE INDEX idx_part_issue_request
ON inventory.part_issue(request_id);

CREATE INDEX idx_part_issue_receiver
ON inventory.part_issue(receiver_id);

CREATE INDEX idx_checklist_active
ON maintenance.checklist_master(active_flag);

CREATE INDEX idx_checklist_frequency
ON maintenance.checklist_master(frequency_type);

CREATE INDEX idx_checklist_vehicle_type
ON maintenance.checklist_master(vehicle_type_id);

CREATE INDEX idx_fuel_rate_type_date
ON reference.fuel_rate_reference (fuel_type, effective_date DESC);

CREATE INDEX idx_fuel_vehicle_date
ON transaction.fuel_transactions (vehicle_id, fuel_date DESC);
