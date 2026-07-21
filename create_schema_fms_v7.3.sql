-- Reference Tables
CREATE TABLE IF NOT EXISTS reference.vehicle_type_ref (
vehicle_type_id  SMALLSERIAL PRIMARY KEY,
vehicle_type_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS reference.maintenance_type_ref (
maintenance_type_id SERIAL PRIMARY KEY,
maintenance_type_name VARCHAR(50) UNIQUE NOT NULL
);

-- Vehicle component with serial number in a vehicle:
CREATE TABLE IF NOT EXISTS reference.component_type(
    component_id SERIAL PRIMARY KEY,
    component_name TEXT UNIQUE
);

INSERT INTO reference.component_type
    (component_name)
Values
    ('BATTERY'),
    ('TYRE'),
    ('FUEL_PUMP'),
    ('HYDRAULIC_PUMP'),
    ('CNG_KIT'),
    ('CNG_CYLINDER')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS reference.severity (
    severity_id SMALLSERIAL PRIMARY KEY,
    severity_name TEXT UNIQUE
);
insert into reference.severity
    (severity_name)
values
    ('MINOR'),
    ('MODERATE'),
    ('MAJOR'),
    ('CRITICAL'),
    ('BREAKDOWN')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS reference.fuel_type_ref(
    fuel_type_id SMALLSERIAL PRIMARY KEY,
    fuel_type_name TEXT UNIQUE
);

INSERT INTO reference.fuel_type_ref
(fuel_type_name)
values
    ('Diesel'),
    ('Petrol'),
    ('CNG'),
    ('LNG'),
    ('EV')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS reference.vehicle_status_ref(
    vehicle_status_id SMALLSERIAL PRIMARY KEY,
    vehicle_status_name TEXT UNIQUE
);
INSERT INTO reference.vehicle_status_ref
(vehicle_status_name)
values
    ('ACTIVE'),
    ('WORKSHOP'),
    ('BREAKDOWN'),
    ('SCRAPPED'),
    ('SOLD')
ON CONFLICT DO NOTHING;

CREATE TABLE  IF NOT EXISTS reference.stock_transaction_ref(
    reference_id SMALLSERIAL PRIMARY KEY,
    reference_type VARCHAR(30) UNIQUE
    );
INSERT INTO reference.stock_transaction_ref
(reference_type)
values
    ('ISSUE'),
    ('RECEIPT'),
    ('PURCHASE'),
    ('ADJUSTMENT'),
    ('RETURN')
ON CONFLICT DO NOTHING;


-- Master Tables
-- Vehicle Master
CREATE TABLE IF NOT EXISTS master.vehicle_master (
    vehicle_id BIGSERIAL PRIMARY KEY,
    vehicle_type_id INT REFERENCES reference.vehicle_type_ref(vehicle_type_id),
    purchase_date DATE,
    rc_number VARCHAR(50) UNIQUE NOT NULL,
    rc_expiry_date DATE,
    engine_no VARCHAR(100) UNIQUE,
    chassis_no VARCHAR(100) UNIQUE,
    gps_id VARCHAR(50) UNIQUE,
    fuel_type_id SMALLINT
        REFERENCES reference.fuel_type_ref(fuel_type_id),
    vehicle_status_id SMALLINT default 1
        references reference.vehicle_status_ref(vehicle_status_id),
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
        CHECK (
         status IN (
           'ACTIVE',
           'REPLACED',
           'REMOVED',
           'FAILED'
         )
        ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

-- Store Inventory
CREATE TABLE IF NOT EXISTS inventory.part_master (
    part_id BIGSERIAL PRIMARY KEY,
    part_code VARCHAR(100) UNIQUE,
    part_name VARCHAR(300),
    vehicle_type_id INT
        REFERENCES reference.vehicle_type_ref(vehicle_type_id),
    part_category VARCHAR(100),
    approval_required BOOLEAN,
    reorder_level INTEGER,
    max_stock INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vendor master like
-- Tyre Supplier
-- Battery Vendor
-- OEM Parts Vendor
-- Fuel Vendor
-- Workshop Contractor
CREATE TABLE IF NOT EXISTS master.vendor (
    vendor_id BIGSERIAL PRIMARY KEY,
    vendor_code VARCHAR(50) UNIQUE,
    vendor_name VARCHAR(200) NOT NULL,
    vendor_type VARCHAR(50),
    contact_person VARCHAR(200),
    mobile_number VARCHAR(20),
    email_address VARCHAR(200),
    gst_number VARCHAR(50),
    pan_number VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(20),
    active_flag BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Workshop master
CREATE TABLE IF NOT EXISTS master.workshop (
    workshop_id BIGSERIAL PRIMARY KEY,
    workshop_code VARCHAR(50) UNIQUE,
    workshop_name VARCHAR(200) NOT NULL,
    address TEXT,
    city VARCHAR(100),
    contact_person VARCHAR(200),
    contact_number VARCHAR(20),
    workshop_type VARCHAR(50),
    active_flag BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- WAREHOUSE Master
CREATE TABLE IF NOT EXISTS master.warehouse (
    warehouse_id BIGSERIAL PRIMARY KEY,
    warehouse_code VARCHAR(50) UNIQUE,
    warehouse_name VARCHAR(200) NOT NULL,
    warehouse_type VARCHAR(50),
    address TEXT,
    contact_person VARCHAR(200),
    contact_number VARCHAR(20),
    active_flag BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Toolkit Master
CREATE TABLE IF NOT EXISTS master.tool_kit (
    toolkit_id BIGSERIAL PRIMARY KEY,
    toolkit_code VARCHAR(50) UNIQUE,
    toolkit_name VARCHAR(200) NOT NULL,
    toolkit_description TEXT,
    assigned_to BIGINT
        REFERENCES master.employee_master(employee_id),
    issue_date DATE,
    return_date DATE,
    toolkit_status VARCHAR(20)
        CHECK (
            toolkit_status IN (
                'AVAILABLE',
                'ISSUED',
                'MAINTENANCE',
                'LOST'
            )
        ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Vehicle RC doc master
CREATE TABLE IF NOT EXISTS master.vehicle_rc_document (
    rc_doc_id BIGSERIAL PRIMARY KEY,
    vehicle_id BIGINT NOT NULL
        REFERENCES master.vehicle_master(vehicle_id),
    document_type VARCHAR(50),
    rc_number VARCHAR(50),
    issue_date DATE,
    expiry_date DATE,
    file_name VARCHAR(500),
    file_path VARCHAR(1000),
    uploaded_by BIGINT
        REFERENCES master.employee_master(employee_id),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    active_flag BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Driver Document Master
-- Supports:
-- DL
-- Aadhaar
-- PAN
-- Address Proof
CREATE TABLE IF NOT EXISTS master.driver_document (
    driver_doc_id BIGSERIAL PRIMARY KEY,
    driver_id BIGINT NOT NULL
        REFERENCES master.driver_master(driver_id),
    document_type VARCHAR(50)
        CHECK (
            document_type IN (
                'DL',
                'AADHAAR',
                'PAN',
                'ADDRESS_PROOF',
                'OTHER'
            )
        ),
    document_number VARCHAR(100),
    issue_date DATE,
    expiry_date DATE,
    file_name VARCHAR(500),
    file_path VARCHAR(1000),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    active_flag BOOLEAN DEFAULT TRUE,
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
    end_date TIMESTAMP,
    created_by BIGINT
        REFERENCES master.employee_master(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT
        REFERENCES master.employee_master(employee_id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(driver_id,start_date)
);

-- Helper Assignment table
CREATE TABLE IF NOT EXISTS operations.helper_vehicle_assignment (
    helper_assignment_id BIGSERIAL PRIMARY KEY,
    employee_id BIGINT
        REFERENCES master.employee_master(employee_id),
    vehicle_id BIGINT
        REFERENCES master.vehicle_master(vehicle_id),
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by BIGINT
        REFERENCES master.employee_master(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT
        REFERENCES master.employee_master(employee_id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
    vehicle_received_at TIMESTAMP,
    created_by BIGINT
        REFERENCES master.employee_master(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT
        REFERENCES master.employee_master(employee_id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Technical Inspection
CREATE TABLE IF NOT EXISTS maintenance.technician_inspection (
    inspection_id BIGSERIAL PRIMARY KEY,
    complaint_id BIGINT
       REFERENCES maintenance.vehicle_complaint(complaint_id),
    technician_id BIGINT NOT NULL
        REFERENCES master.employee_master(employee_id),
    inspection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observed_issue TEXT,
    operator_notes TEXT,
    status VARCHAR(30),
    created_by BIGINT
        REFERENCES master.employee_master(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT
        REFERENCES master.employee_master(employee_id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- GPS Raw Data (Time-Series)
CREATE TABLE IF NOT EXISTS timeseries.gps_raw_data (
    id BIGSERIAL PRIMARY KEY,
    vehicle_id BIGINT
        REFERENCES master.vehicle_master(vehicle_id),
    gps_timestamp TIMESTAMP NOT NULL,
    latitude NUMERIC(10,7),
    longitude NUMERIC(10,7),
    speed NUMERIC(8,2),
    heading NUMERIC,
    altitude NUMERIC,
    ignition_status NUMERIC,
    device_timestamp TIMESTAMP,
    server_timestamp TIMESTAMP
);

-- Maintenance Job Card
CREATE TABLE IF NOT EXISTS transact.maintenance_job_card (
    job_card_id SERIAL PRIMARY KEY,
    complaint_id BIGINT
        REFERENCES maintenance.vehicle_complaint(complaint_id),
    inspection_id BIGINT
        REFERENCES maintenance.technician_inspection(inspection_id),
    vehicle_id BIGINT REFERENCES master.vehicle_master(vehicle_id),
    maintenance_type_id INT REFERENCES reference.maintenance_type_ref(maintenance_type_id),
    severity_id SMALLINT
        REFERENCES reference.severity(severity_id),
    approval_required BOOLEAN DEFAULT FALSE,
    approved_by BIGINT,
    labour_charges NUMERIC(12,2),
    job_status VARCHAR(30),
    job_card_status VARCHAR(20),
    completion_date DATE,
    downtime_hours NUMERIC(6,2),
    description TEXT,
    created_by BIGINT
        REFERENCES master.employee_master(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT
        REFERENCES master.employee_master(employee_id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Maintenance Parts Usage
CREATE TABLE IF NOT EXISTS maintenance.job_card_part (
    id BIGSERIAL PRIMARY KEY,
    job_card_id BIGINT
        REFERENCES transact.maintenance_job_card(job_card_id),
    part_id BIGINT
        REFERENCES inventory.part_master(part_id),
    quantity NUMERIC(12,2),
    unit_price NUMERIC(12,2),
    total_price NUMERIC(12,2),
    created_by BIGINT
        REFERENCES master.employee_master(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT
        REFERENCES master.employee_master(employee_id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Requested Parts
CREATE TABLE IF NOT EXISTS inventory.part_request (
    request_id BIGSERIAL PRIMARY KEY,
    request_number VARCHAR(50) NOT NULL UNIQUE,
    vehicle_id BIGINT NOT NULL
        REFERENCES master.vehicle_master(vehicle_id),
    job_card_id BIGINT
        REFERENCES transact.maintenance_job_card(job_card_id),
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
    created_by BIGINT
        REFERENCES master.employee_master(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT
        REFERENCES master.employee_master(employee_id),
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
    created_by BIGINT
        REFERENCES master.employee_master(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT
        REFERENCES master.employee_master(employee_id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        REFERENCES transact.maintenance_job_card(job_card_id),
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
    created_by BIGINT
        REFERENCES master.employee_master(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT
        REFERENCES master.employee_master(employee_id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    created_by BIGINT
        REFERENCES master.employee_master(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT
        REFERENCES master.employee_master(employee_id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    created_by BIGINT
        REFERENCES master.employee_master(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT
        REFERENCES master.employee_master(employee_id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    remarks TEXT,
    created_by BIGINT
        REFERENCES master.employee_master(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT
        REFERENCES master.employee_master(employee_id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

-- Stock Ledger
CREATE TABLE IF NOT EXISTS inventory.stock_transaction(
    stock_txn_id BIGSERIAL PRIMARY KEY,
    part_id BIGINT
        REFERENCES inventory.part_master(part_id),
    job_card_id BIGINT
        REFERENCES transact.maintenance_job_card(job_card_id),
    txn_type VARCHAR(20),
    quantity NUMERIC(10,2),
    txn_datetime TIMESTAMP,
    reference_id SMALLINT
        REFERENCES reference.stock_transaction_ref(reference_id),
    opening_balance NUMERIC(10,2),
    closing_balance NUMERIC(10,2),
    unit_cost NUMERIC(10,2),
    warehouse_id BIGINT
        REFERENCES master.warehouse(warehouse_id)
);

-- Gate Pass Management
-- General Gate Pass
CREATE TABLE IF NOT EXISTS operations.gate_pass_regular (
    gate_pass_id BIGSERIAL PRIMARY KEY,
    employee_id BIGINT
        REFERENCES master.employee_master(employee_id),
    purpose TEXT,
    time_out TIMESTAMP,
    time_in TIMESTAMP,
    supervisor_id BIGINT
        REFERENCES master.employee_master(employee_id)
);

-- Technical Gate Pass
CREATE TABLE IF NOT EXISTS operations.gate_pass_technical (
    gate_pass_id BIGSERIAL PRIMARY KEY,
    employee_id BIGINT NOT NULL
        REFERENCES master.employee_master(employee_id),
    vehicle_id BIGINT
        REFERENCES master.vehicle_master(vehicle_id),
    area VARCHAR(200),
    issue_reported TEXT,
    tow_vehicle_number VARCHAR(50),
    tool_kit_details TEXT,
    time_out TIMESTAMP,
    time_in TIMESTAMP,
    supervisor_id BIGINT NOT NULL
        REFERENCES master.employee_master(employee_id)
);

-- Preventive Maintenance
CREATE TABLE IF NOT EXISTS maintenance.preventive_maintenance_checklist (
    checklist_id BIGSERIAL PRIMARY KEY,
    vehicle_id BIGINT
        REFERENCES master.vehicle_master(vehicle_id),
    technician_id BIGINT NOT NULL
        REFERENCES master.employee_master(employee_id),
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
    created_by BIGINT
        REFERENCES master.employee_master(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT
        REFERENCES master.employee_master(employee_id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    ('CNG_LEAK','CNG Leakage Check','DAILY')
ON CONFLICT DO NOTHING;

--Checklist for maintenance
CREATE TABLE  IF NOT EXISTS  maintenance.checklist_result (
    result_id BIGSERIAL PRIMARY KEY,
    checklist_id BIGINT
        REFERENCES maintenance.preventive_maintenance_checklist(checklist_id),
    checklist_item_id BIGINT
        REFERENCES maintenance.checklist_master(checklist_item_id),
    status VARCHAR(20),
    remarks TEXT
);


-- Inventory Table

-- CREATE TABLE IF NOT EXISTS transact.inventory (
--     spare_part_id SERIAL PRIMARY KEY,
--     vehicle_type_id INT REFERENCES reference.vehicle_type_ref(vehicle_type_id),
--     quantity INT NOT NULL,
--     part_type VARCHAR(50),
--     price NUMERIC,
--     created_by BIGINT
--         REFERENCES master.employee_master(employee_id),
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     modified_by BIGINT
--         REFERENCES master.employee_master(employee_id),
--     modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Spare Parts Mapping (Job Card)
-- CREATE TABLE IF NOT EXISTS transact.job_card_parts (
--     id SERIAL PRIMARY KEY,
--     job_card_id INT REFERENCES transact.maintenance_job_card(job_card_id),
--     spare_part_id INT 
--         REFERENCES inventory.part_master(part_id),
--     quantity INT NOT NULL,
--     created_by BIGINT
--         REFERENCES master.employee_master(employee_id),
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     modified_by BIGINT
--         REFERENCES master.employee_master(employee_id),
--     modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Fuel Rate Reference
CREATE TABLE IF NOT EXISTS reference.fuel_rate_reference (
    id SERIAL PRIMARY KEY,
    fuel_type_id SMALLINT NOT NULL
        REFERENCES reference.fuel_type_ref(fuel_type_id),
    price_per_unit NUMERIC(10,2) NOT NULL,
    effective_date DATE NOT NULL,
    created_by BIGINT
        REFERENCES master.employee_master(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT
        REFERENCES master.employee_master(employee_id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Fuel Transactions
CREATE TABLE IF NOT EXISTS transact.fuel_transactions (
    fuel_txn_id SERIAL PRIMARY KEY,
    vehicle_id BIGINT,
    fuel_date DATE NOT NULL,
    fuel_quantity NUMERIC(10,2) NOT NULL,
    fuel_price_per_unit NUMERIC(10,2),
    total_fuel_cost NUMERIC(12,2),
    odometer_reading NUMERIC(12,2),
    created_by BIGINT
        REFERENCES master.employee_master(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT
        REFERENCES master.employee_master(employee_id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fuel_vehicle
    FOREIGN KEY (vehicle_id)
    REFERENCES master.vehicle_master(vehicle_id)
);


-- Employee Salary
CREATE TABLE IF NOT EXISTS transact.employee_salary (
    salary_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    salary_month DATE NOT NULL,
    base_salary NUMERIC(12,2) NOT NULL,
    allowances NUMERIC(12,2) DEFAULT 0,
    deductions NUMERIC(12,2) DEFAULT 0,
    net_salary NUMERIC(12,2),
    payment_status VARCHAR(20) DEFAULT 'PENDING',
    created_by BIGINT
        REFERENCES master.employee_master(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT
        REFERENCES master.employee_master(employee_id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_salary_employee
    FOREIGN KEY (employee_id)
    REFERENCES master.employee_master(employee_id)
);


-- Attendance Tracking
CREATE TABLE IF NOT EXISTS transact.attendance_tracking (
    attendance_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    status VARCHAR(20) CHECK (status IN ('PRESENT', 'ABSENT', 'LEAVE')),
    shift_hours NUMERIC(5,2),
    created_by BIGINT
        REFERENCES master.employee_master(employee_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT
        REFERENCES master.employee_master(employee_id),
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_attendance_employee
    FOREIGN KEY (employee_id)
    REFERENCES master.employee_master(employee_id)
);


-- Add Spare Parts Consumption Table
-- CREATE TABLE IF NOT EXISTS transact.maintenance_parts_usage (
--     id SERIAL PRIMARY KEY,
--     job_card_id INT 
--         REFERENCES transact.maintenance_job_card(job_card_id),
--     spare_part_id INT 
--         REFERENCES inventory.part_master(part_id),
--     quantity INT NOT NULL,
--     total_cost NUMERIC(12,2),
--     created_by BIGINT
--         REFERENCES master.employee_master(employee_id),
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     modified_by BIGINT
--         REFERENCES master.employee_master(employee_id),
--     modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

--Explore future tables
CREATE TABLE IF NOT EXISTS master.location(location_id serial primary key);
-- not required as of now because working for one city onle
--    CREATE TABLE IF NOT EXISTS master.zone
--  CREATE TABLE IF NOT EXISTS master.area

-- VIEWS
-- Vehicle Service History View
CREATE OR REPLACE VIEW transact.vehicle_service_history AS
SELECT
    vm.rc_number,
    vm.engine_no,
    vm.chassis_no,
    vc.complaint_date,
    vc.issue_description,
    ti.observed_issue,
    mj.job_card_id,
    mt.maintenance_type_name,
    mj.labour_charges,
    mj.completion_date,
    mj.job_card_status
FROM maintenance.vehicle_complaint vc
JOIN master.vehicle_master vm
    ON vc.vehicle_id = vm.vehicle_id
LEFT JOIN maintenance.technician_inspection ti
    ON vc.complaint_id = ti.complaint_id
LEFT JOIN transact.maintenance_job_card mj
    ON vc.complaint_id = mj.complaint_id
LEFT JOIN reference.maintenance_type_ref mt
    ON mj.maintenance_type_id = mt.maintenance_type_id;

-- Driver Vehicle view History
CREATE OR REPLACE VIEW transact.driver_vehicle_history AS
SELECT
    d.driver_id,
    d.driver_name,
    d.mobile_number,
    v.rc_number,
    a.start_date,
    a.end_date
FROM operations.driver_vehicle_assignment a
JOIN master.driver_master d
    ON a.driver_id = d.driver_id
JOIN master.vehicle_master v
    ON a.vehicle_id = v.vehicle_id;

CREATE OR REPLACE FUNCTION audit.log_changes()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $function$
DECLARE
    v_record_id TEXT;
BEGIN
    IF TG_OP = 'DELETE' THEN
        v_record_id :=
            COALESCE(
                to_jsonb(OLD)->>'vehicle_id',
                to_jsonb(OLD)->>'employee_id',
                to_jsonb(OLD)->>'driver_id',
                to_jsonb(OLD)->>'complaint_id',
                to_jsonb(OLD)->>'inspection_id',
                to_jsonb(OLD)->>'job_card_id',
                to_jsonb(OLD)->>'checklist_id',
                to_jsonb(OLD)->>'part_id',
                to_jsonb(OLD)->>'id'
            );
    ELSE
        v_record_id :=
            COALESCE(
                to_jsonb(NEW)->>'vehicle_id',
                to_jsonb(NEW)->>'employee_id',
                to_jsonb(NEW)->>'driver_id',
                to_jsonb(NEW)->>'complaint_id',
                to_jsonb(NEW)->>'inspection_id',
                to_jsonb(NEW)->>'job_card_id',
                to_jsonb(NEW)->>'checklist_id',
                to_jsonb(NEW)->>'part_id',
                to_jsonb(NEW)->>'id'
            );
    END IF;
    INSERT INTO audit.audit_log
    (
        schema_name,
        table_name,
        record_id,
        operation,
        old_data,
        new_data,
        changed_by,
        changed_at
    )
    VALUES
    (
        TG_TABLE_SCHEMA,
        TG_TABLE_NAME,
        v_record_id,
        TG_OP,
        CASE
            WHEN TG_OP = 'INSERT'
            THEN NULL
            ELSE to_jsonb(OLD)
        END,
        CASE
            WHEN TG_OP = 'DELETE'
            THEN NULL
            ELSE to_jsonb(NEW)
        END,
        NULL,
        CURRENT_TIMESTAMP
    );
    RETURN COALESCE(NEW, OLD);
END;
$function$;

-- adding constriants for fk integrity
ALTER TABLE transact.maintenance_job_card
ALTER COLUMN inspection_id SET NOT NULL;

ALTER TABLE transact.maintenance_job_card
ALTER COLUMN complaint_id SET NOT NULL;

ALTER TABLE transact.maintenance_job_card
ALTER COLUMN vehicle_id SET NOT NULL;

ALTER TABLE maintenance.vehicle_complaint
ALTER COLUMN vehicle_id SET NOT NULL;

ALTER TABLE maintenance.vehicle_complaint
ALTER COLUMN driver_id SET NOT NULL;

ALTER TABLE maintenance.technician_inspection
ALTER COLUMN complaint_id SET NOT NULL;

ALTER TABLE transact.maintenance_job_card
ALTER COLUMN complaint_id SET NOT NULL;

ALTER TABLE transact.maintenance_job_card
ALTER COLUMN inspection_id SET NOT NULL;

ALTER TABLE transact.maintenance_job_card
ALTER COLUMN vehicle_id SET NOT NULL;

ALTER TABLE maintenance.job_card_part
ALTER COLUMN job_card_id SET NOT NULL;

ALTER TABLE maintenance.job_card_part
ALTER COLUMN part_id SET NOT NULL;

ALTER TABLE maintenance.preventive_maintenance_checklist
ALTER COLUMN vehicle_id SET NOT NULL;
-- adding column for enhaning job card 
ALTER TABLE transact.maintenance_job_card
ADD COLUMN driver_id INTEGER;

ALTER TABLE transact.maintenance_job_card
ADD COLUMN technician1_id INTEGER;

ALTER TABLE transact.maintenance_job_card
ADD COLUMN technician2_id INTEGER;

ALTER TABLE transact.maintenance_job_card
ADD COLUMN date_time_in TIMESTAMP;

ALTER TABLE transact.maintenance_job_card
ADD COLUMN date_time_out TIMESTAMP;

ALTER TABLE transact.maintenance_job_card
ADD COLUMN zone_area VARCHAR(200);

ALTER TABLE transact.maintenance_job_card
ADD COLUMN mileage_hours VARCHAR(100);

ALTER TABLE transact.maintenance_job_card
ADD COLUMN maintenance_type VARCHAR(50);

ALTER TABLE transact.maintenance_job_card
ADD COLUMN issue_reported TEXT;

ALTER TABLE transact.maintenance_job_card
ADD COLUMN problem_found_action_taken TEXT;

ALTER TABLE transact.maintenance_job_card
ADD COLUMN requisition_slip_number VARCHAR(100);
-- adding fk for job card new columns
ALTER TABLE transact.maintenance_job_card
ADD CONSTRAINT fk_jobcard_driver
FOREIGN KEY (driver_id)
REFERENCES master.driver_master(driver_id);

ALTER TABLE transact.maintenance_job_card
ADD CONSTRAINT fk_jobcard_technician1
FOREIGN KEY (technician1_id)
REFERENCES master.employee_master(employee_id);

ALTER TABLE transact.maintenance_job_card
ADD CONSTRAINT fk_jobcard_technician2
FOREIGN KEY (technician2_id)
REFERENCES master.employee_master(employee_id);

-- adding column for auditing
ALTER TABLE maintenance.technician_inspection
ADD COLUMN IF NOT EXISTS active_flag BOOL;
ALTER TABLE maintenance.job_card_part 
ADD COLUMN IF NOT EXISTS active_flag BOOL; SET DEFAULT TRUE;
ALTER TABLE transact.maintenance_job_card 
ADD COLUMN IF NOT EXISTS active_flag BOOL; SET DEFAULT TRUE;

-- for employee Master
ALTER TABLE master.employee_master
ADD COLUMN IF NOT EXISTS active_flag BOOL DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS created_by BIGINT,
ADD COLUMN IF NOT EXISTS modified_by BIGINT,
ADD COLUMN IF NOT EXISTS modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
-- Vehicle Master
ALTER TABLE master.vehicle_master
ADD COLUMN IF NOT EXISTS created_by BIGINT,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS modified_by BIGINT,
ADD COLUMN IF NOT EXISTS modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
-- Driver_master
ALTER TABLE master.driver_master
ADD COLUMN IF NOT EXISTS active_flag BOOL DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS created_by BIGINT,
ADD COLUMN IF NOT EXISTS modified_by BIGINT,
ADD COLUMN IF NOT EXISTS modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- COmplaints
ALTER TABLE maintenance.vehicle_complaint
ADD COLUMN IF NOT EXISTS active_flag BOOL DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS created_by BIGINT,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS modified_by BIGINT,
ADD COLUMN IF NOT EXISTS modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
-- for preventive_maintenance_checklist
ALTER TABLE maintenance.preventive_maintenance_checklist
ADD COLUMN IF NOT EXISTS active_flag BOOL DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS created_by BIGINT,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS modified_by BIGINT,
ADD COLUMN IF NOT EXISTS modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- for part_master
ALTER TABLE inventory.part_master
ADD COLUMN IF NOT EXISTS active_flag BOOL DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS created_by BIGINT,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS modified_by BIGINT,
ADD COLUMN IF NOT EXISTS modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
-- set active flag null and initilize with true for existing records
ALTER TABLE master.vendor ALTER COLUMN active_flag SET DEFAULT TRUE;
ALTER TABLE master.workshop ALTER COLUMN active_flag SET DEFAULT TRUE;
ALTER TABLE master.warehouse ALTER COLUMN active_flag SET DEFAULT TRUE;
ALTER TABLE master.vehicle_rc_document ALTER COLUMN active_flag SET DEFAULT TRUE;
ALTER TABLE maintenance.technician_inspection ALTER COLUMN active_flag SET DEFAULT TRUE;
ALTER TABLE master.driver_document ALTER COLUMN active_flag SET DEFAULT TRUE;
ALTER TABLE maintenance.vehicle_complaint ALTER COLUMN active_flag SET DEFAULT TRUE;
ALTER TABLE maintenance.checklist_master ALTER COLUMN active_flag SET DEFAULT TRUE;
ALTER TABLE master.vehicle_master ALTER COLUMN active_flag SET DEFAULT TRUE;
ALTER TABLE master.employee_master ALTER COLUMN active_flag SET DEFAULT TRUE;
ALTER TABLE master.driver_master ALTER COLUMN active_flag SET DEFAULT TRUE;
ALTER TABLE maintenance.preventive_maintenance_checklist ALTER COLUMN active_flag SET DEFAULT TRUE;
ALTER TABLE inventory.part_master ALTER COLUMN active_flag SET DEFAULT TRUE;
ALTER TABLE master.vendor ALTER COLUMN active_flag SET NOT NULL;
ALTER TABLE master.workshop ALTER COLUMN active_flag SET NOT NULL;
ALTER TABLE master.warehouse ALTER COLUMN active_flag SET NOT NULL;
ALTER TABLE master.vehicle_rc_document ALTER COLUMN active_flag SET NOT NULL;
ALTER TABLE maintenance.technician_inspection ALTER COLUMN active_flag SET NOT NULL;
ALTER TABLE master.driver_document ALTER COLUMN active_flag SET NOT NULL;
ALTER TABLE maintenance.vehicle_complaint ALTER COLUMN active_flag SET NOT NULL;
ALTER TABLE maintenance.checklist_master ALTER COLUMN active_flag SET NOT NULL;
ALTER TABLE master.vehicle_master ALTER COLUMN active_flag SET NOT NULL;
ALTER TABLE master.employee_master ALTER COLUMN active_flag SET NOT NULL;
ALTER TABLE master.driver_master ALTER COLUMN active_flag SET NOT NULL;
ALTER TABLE maintenance.preventive_maintenance_checklist ALTER COLUMN active_flag SET NOT NULL;
ALTER TABLE inventory.part_master ALTER COLUMN active_flag SET NOT NULL;
update transact.maintenance_job_card set active_flag=true where active_flag is null;
ALTER TABLE transact.maintenance_job_card ALTER COLUMN active_flag SET DEFAULT TRUE;
ALTER TABLE transact.maintenance_job_card ALTER COLUMN active_flag SET NOT NULL;
update maintenance.job_card_part set active_flag=true;
ALTER TABLE maintenance.job_card_part ALTER COLUMN active_flag SET DEFAULT TRUE;
ALTER TABLE maintenance.job_card_part ALTER COLUMN active_flag SET NOT NULL;


-- create audit table
CREATE TABLE IF NOT EXISTS audit.audit_log (
    audit_id BIGSERIAL PRIMARY KEY,

    schema_name VARCHAR(100),
    table_name VARCHAR(100),
    record_id TEXT,

    operation VARCHAR(20),

    old_data JSONB,
    new_data JSONB,

    changed_by BIGINT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Trigger to capture the changes
CREATE OR REPLACE FUNCTION audit.set_modified_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- trigger for vehicles
DROP TRIGGER IF EXISTS trg_vehicle_master_modified_at
ON master.vehicle_master;

CREATE TRIGGER trg_vehicle_master_modified_at
BEFORE UPDATE ON master.vehicle_master
FOR EACH ROW
EXECUTE FUNCTION audit.set_modified_at();

-- trigger for driver_master
DROP TRIGGER IF EXISTS trg_driver_master_modified_at
ON master.driver_master;

CREATE TRIGGER trg_driver_master_modified_at
BEFORE UPDATE ON master.driver_master
FOR EACH ROW
EXECUTE FUNCTION audit.set_modified_at();
-- trigger for employee_master
DROP TRIGGER IF EXISTS trg_employee_master_modified_at
ON master.employee_master;

CREATE TRIGGER trg_employee_master_modified_at
BEFORE UPDATE ON master.employee_master
FOR EACH ROW
EXECUTE FUNCTION audit.set_modified_at();
-- trigger for vehicle_complaint
DROP TRIGGER IF EXISTS trg_vehicle_complaint_modified_at
ON maintenance.vehicle_complaint;

CREATE TRIGGER trg_vehicle_complaint_modified_at
BEFORE UPDATE ON maintenance.vehicle_complaint
FOR EACH ROW
EXECUTE FUNCTION audit.set_modified_at();
-- trigger for technician_inspection
DROP TRIGGER IF EXISTS trg_technician_inspection_modified_at
ON maintenance.technician_inspection;

CREATE TRIGGER trg_technician_inspection_modified_at
BEFORE UPDATE ON maintenance.technician_inspection
FOR EACH ROW
EXECUTE FUNCTION audit.set_modified_at();
-- trigger for maintenance_job_card
DROP TRIGGER IF EXISTS trg_maintenance_job_card_modified_at
ON transact.maintenance_job_card;

CREATE TRIGGER trg_maintenance_job_card_modified_at
BEFORE UPDATE ON transact.maintenance_job_card
FOR EACH ROW
EXECUTE FUNCTION audit.set_modified_at();
-- trigger for job_card_part
DROP TRIGGER IF EXISTS trg_job_card_part_modified_at
ON maintenance.job_card_part;

CREATE TRIGGER trg_job_card_part_modified_at
BEFORE UPDATE ON maintenance.job_card_part
FOR EACH ROW
EXECUTE FUNCTION audit.set_modified_at();

-- trigger for preventive_maintenance_checklist
DROP TRIGGER IF EXISTS trg_preventive_maintenance_checklist_modified_at
ON maintenance.preventive_maintenance_checklist;

CREATE TRIGGER trg_preventive_maintenance_checklist_modified_at
BEFORE UPDATE ON maintenance.preventive_maintenance_checklist
FOR EACH ROW
EXECUTE FUNCTION audit.set_modified_at();

-- trigger for part_master
DROP TRIGGER IF EXISTS trg_part_master_modified_at
ON inventory.part_master;

CREATE TRIGGER trg_part_master_modified_at
BEFORE UPDATE ON inventory.part_master
FOR EACH ROW
EXECUTE FUNCTION audit.set_modified_at();

-- trigger for part_request
DROP TRIGGER IF EXISTS trg_part_request_modified_at
ON inventory.part_request;

CREATE TRIGGER trg_part_request_modified_at
BEFORE UPDATE ON inventory.part_request
FOR EACH ROW
EXECUTE FUNCTION audit.set_modified_at();

-- trigger for stock_transaction
DROP TRIGGER IF EXISTS trg_stock_transaction_modified_at
ON inventory.stock_transaction;

CREATE TRIGGER trg_stock_transaction_modified_at
BEFORE UPDATE ON inventory.stock_transaction
FOR EACH ROW
EXECUTE FUNCTION audit.set_modified_at();

-- trigger for approval_request
DROP TRIGGER IF EXISTS trg_approval_request_modified_at
ON inventory.approval_request;

CREATE TRIGGER trg_approval_request_modified_at
BEFORE UPDATE ON inventory.approval_request
FOR EACH ROW
EXECUTE FUNCTION audit.set_modified_at();

-- trigger for whatsapp_message_log
DROP TRIGGER IF EXISTS trg_whatsapp_message_log_modified_at
ON integration.whatsapp_message_log;

CREATE TRIGGER trg_whatsapp_message_log_modified_at
BEFORE UPDATE ON integration.whatsapp_message_log
FOR EACH ROW
EXECUTE FUNCTION audit.set_modified_at();
-- triger for updating audit log 
--vehicle
CREATE TRIGGER trg_vehicle_master_audit
AFTER INSERT OR UPDATE OR DELETE
ON master.vehicle_master
FOR EACH ROW
EXECUTE FUNCTION audit.log_changes();
-- employee
CREATE TRIGGER trg_employee_master_audit
AFTER INSERT OR UPDATE OR DELETE
ON master.employee_master
FOR EACH ROW
EXECUTE FUNCTION audit.log_changes();
-- driver
CREATE TRIGGER trg_driver_master_audit
AFTER INSERT OR UPDATE OR DELETE
ON master.driver_master
FOR EACH ROW
EXECUTE FUNCTION audit.log_changes();
-- part
CREATE TRIGGER trg_part_master_audit
AFTER INSERT OR UPDATE OR DELETE
ON inventory.part_master
FOR EACH ROW
EXECUTE FUNCTION audit.log_changes();
--vehicle_complaint
CREATE TRIGGER trg_vehicle_complaint
AFTER INSERT OR UPDATE OR DELETE
ON maintenance.vehicle_complaint
FOR EACH ROW
EXECUTE FUNCTION audit.log_changes();
--maintenance.technician_inspection
CREATE TRIGGER trg_technician_inspection
AFTER INSERT OR UPDATE OR DELETE
ON maintenance.technician_inspection
FOR EACH ROW
EXECUTE FUNCTION audit.log_changes();
--maintenance.preventive_maintenance_checklist
CREATE TRIGGER trg_preventive_maintenance_checklist
AFTER INSERT OR UPDATE OR DELETE
ON maintenance.preventive_maintenance_checklist
FOR EACH ROW
EXECUTE FUNCTION audit.log_changes();
--transact.maintenance_job_card
CREATE TRIGGER trg_maintenance_job_card
AFTER INSERT OR UPDATE OR DELETE
ON transact.maintenance_job_card
FOR EACH ROW
EXECUTE FUNCTION audit.log_changes();
--maintenance.job_card_part
CREATE TRIGGER trg_job_card_part
AFTER INSERT OR UPDATE OR DELETE
ON maintenance.job_card_part
FOR EACH ROW
EXECUTE FUNCTION audit.log_changes();
--inventory.part_master
CREATE TRIGGER trg_part_master
AFTER INSERT OR UPDATE OR DELETE
ON inventory.part_master
FOR EACH ROW
EXECUTE FUNCTION audit.log_changes();


--  CREATE TABLE IF NOT EXISTS master.fuel_station

-- Missing analytics tables
-- CREATE TABLE IF NOT EXISTS analytics.vehicle_health_score
-- CREATE TABLE IF NOT EXISTS analytics.daily_vehicle_cost
-- CREATE TABLE IF NOT EXISTS analytics.fuel_efficiency
-- CREATE TABLE IF NOT EXISTS analytics.breakdown_risk
-- CREATE TABLE IF NOT EXISTS analytics.maintenance_kpi

-- Indexes at one place

CREATE INDEX idx_job_card_part_job_card
ON maintenance.job_card_part(job_card_id);

CREATE INDEX idx_part_request_vehicle
ON inventory.part_request(vehicle_id);

CREATE INDEX idx_part_request_job_card
ON inventory.part_request(job_card_id);

CREATE INDEX idx_part_request_status
ON inventory.part_request(request_status);

CREATE INDEX idx_part_request_datetime
ON inventory.part_request(requested_datetime DESC);

CREATE INDEX idx_attendance_employee_date
ON transact.attendance_tracking (employee_id, attendance_date DESC);

CREATE INDEX idx_salary_employee_month
ON transact.employee_salary (employee_id, salary_month DESC);

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
ON reference.fuel_rate_reference (fuel_type_id, effective_date DESC);

CREATE INDEX idx_fuel_vehicle_date
ON transact.fuel_transactions (vehicle_id, fuel_date DESC);
