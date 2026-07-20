#!/usr/bin/env bash
# =============================================================================
# setup_postgresql.sh — Day 01 Sprint 01
# PostgreSQL 17 install + fleet_user + fms db DB + hardening
# Usage: bash db_setup.sh
# =============================================================================

set -euo pipefail
LOG_FILE="setup_fms_db.log"

log()  { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"; }
fail() { log "ERROR: $*"; exit 1; }
hr()   { log "------------------------------------------------------"; }

log "======================================================"
log "  PostgreSQL 17 Setup + Hardening Script"
log "======================================================"

# -------------------------------------------------------
# 0. Configuration — CHANGE THESE BEFORE RUNNING
# -------------------------------------------------------
DB_HOST="127.0.0.1"
DB_PORT="5432"
DB_NAME="fms"
APP_USER="fleet_user"
APP_PASS="FleetUser@2024!"   # ⚠️  Change this in production
DB=$DB_NAME
PGUSER="postgres"
log "Target DB:   $DB_NAME"
log "App User:    $APP_USER"

# -------------------------------------------------------
# 2. Create user/role pharma + pharma DB via SQL
# -------------------------------------------------------
hr
log "Creating user $APP_USER and $DB_NAME database..."

# Write the SQL setup to a temp file
SQL_SETUP=$(mktemp /tmp/pg_setup_XXXXXX.sql)
cat > "$SQL_SETUP" << SQLEOF
-- ==========================================================
-- PostgreSQL Setup: appuser + pharma db database
-- Run as postgres superuser
-- ==========================================================

-- 1. Drop and recreate appuser (idempotent)
DO \$\$
DECLARE
    users TEXT[] := ARRAY['fleet_user', 'workshop_user', 'driver_user', 'management_user'];
    passwords TEXT[] := ARRAY['FleetUser@2024!', 'WorkshopUser@2024!', 'DriverUser@2024!', 'ManagementUser@2024!'];
    i INTEGER;
BEGIN
    FOR i IN 1..array_length(users, 1)
    LOOP
        IF EXISTS (SELECT FROM pg_roles WHERE rolname = users[i]) THEN
            RAISE NOTICE 'Role % already exists, updating password...', users[i];
            EXECUTE format('ALTER ROLE %I WITH PASSWORD %L', users[i], passwords[i]);
        ELSE
            EXECUTE format('CREATE USER %I WITH LOGIN PASSWORD %L', users[i], passwords[i]);
            RAISE NOTICE 'Role % created.', users[i];
        END IF;
    END LOOP;
END
\$\$;

-- grant
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA master TO fleet_user;
-- GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA transaction TO workshop_user;
-- GRANT SELECT ON ALL TABLES IN SCHEMA timeseries TO management_user;
-- GRANT ALL PRIVILEGES ON DATABASE fms TO fleet_user;
-- 
-- ALTER ROLE fleet_user SET client_encoding TO 'utf8';
-- ALTER ROLE fleet_user SET default_transaction_isolation TO 'read committed';

-- 2. Harden users timeouts

DO \$\$
DECLARE
    users TEXT[] := ARRAY['fleet_user', 'workshop_user', 'driver_user', 'management_user'];
    i INTEGER;
BEGIN
    FOR i IN 1..array_length(users, 1)
    LOOP
        IF EXISTS (SELECT FROM pg_roles WHERE rolname = users[i]) THEN
            RAISE NOTICE 'Role % already exists, updating timeout details...', users[i];
            EXECUTE format('ALTER ROLE %I SET idle_in_transaction_session_timeout = "30s"', users[i]);
            EXECUTE format('ALTER ROLE %I SET statement_timeout = "60000"', users[i]);
            EXECUTE format('ALTER ROLE %I SET lock_timeout = "10s"', users[i]);
            EXECUTE format('ALTER ROLE %I SET search_path = public', users[i]);
        ELSE
            RAISE NOTICE 'User % not available...' , users[i];
        END IF;
    END LOOP;
END
\$\$;


-- 3. Drop and recreate fms db DB (WARNING: drops if exists)
-- Comment out DROP if you want to keep existing data
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = '${DB_NAME}' AND pid <> pg_backend_pid();

DROP DATABASE IF EXISTS ${DB_NAME};

CREATE DATABASE ${DB_NAME}
    WITH OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0
    CONNECTION LIMIT = 50;

COMMENT ON DATABASE ${DB_NAME} IS
    'Fleet Management database — for ${DB_NAME} environment';

-- 4. Grant appuser CONNECT to pharma db
GRANT CONNECT ON DATABASE ${DB_NAME} TO ${APP_USER};

\echo 'Database ${DB_NAME} created and CONNECT granted to ${APP_USER}'
SQLEOF

# Execute setup SQL as postgres
if [ "$OS" = "Linux" ]; then
    sudo -u postgres psql -f "$SQL_SETUP" -v ON_ERROR_STOP=1 \
        2>&1 | tee -a "$LOG_FILE"
else
    psql -U postgres -f "$SQL_SETUP" -v ON_ERROR_STOP=1 \
        2>&1 | tee -a "$LOG_FILE"
fi

#rm -f "$SQL_SETUP"
log "$APP_USER and $DB_NAME database created"


# -------------------------------------------------------
# 3. Schema-level permissions (must run AFTER connecting to pharma db)
# -------------------------------------------------------
hr
log "Setting schema-level permissions for $APP_USER on $DB_NAME..."

SQL_PERMS=$(mktemp /tmp/pg_perms_XXXXXX.sql)
log "Granting schema permissions to $APP_USER on $DB_NAME..."
log "SQL permissions script: $SQL_PERMS"
log "This will grant USAGE on schema and SELECT/INSERT/UPDATE/DELETE on all tables, plus future object permissions."

cat > "$SQL_PERMS" << SQLEOF
-- Connect to pharma db and grant schema permissions
\c ${DB_NAME}

-- Create pharma schema if not exists
-- Create schems
CREATE SCHEMA IF NOT EXISTS master AUTHORIZATION ${APP_USER};
CREATE SCHEMA IF NOT EXISTS reference AUTHORIZATION ${APP_USER};
CREATE SCHEMA IF NOT EXISTS transact AUTHORIZATION ${APP_USER};
CREATE SCHEMA IF NOT EXISTS timeseries AUTHORIZATION ${APP_USER};
CREATE SCHEMA IF NOT EXISTS maintenance AUTHORIZATION ${APP_USER};
CREATE SCHEMA IF NOT EXISTS inventory AUTHORIZATION ${APP_USER};
CREATE SCHEMA IF NOT EXISTS operations AUTHORIZATION ${APP_USER};
CREATE SCHEMA IF NOT EXISTS integration AUTHORIZATION ${APP_USER};
CREATE SCHEMA IF NOT EXISTS analytics AUTHORIZATION ${APP_USER};
CREATE SCHEMA IF NOT EXISTS audit AUTHORIZATION ${APP_USER};


-- Grant schema usage
GRANT USAGE ON SCHEMA master,reference,transact,timeseries,maintenance,inventory,operations,integration,analytics,audit  TO ${APP_USER};
-- grant
GRANT ALL PRIVILEGES ON DATABASE fms TO fleet_user;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA master TO fleet_user;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA transact TO workshop_user;
GRANT SELECT ON ALL TABLES IN SCHEMA timeseries TO management_user;

ALTER ROLE fleet_user SET client_encoding TO 'utf8';
ALTER ROLE fleet_user SET default_transaction_isolation TO 'read committed';

-- Current objects
GRANT SELECT, INSERT, UPDATE, DELETE
    ON ALL TABLES IN SCHEMA master,reference,transact,timeseries,maintenance,inventory,operations,integration,analytics,audit  TO ${APP_USER};
GRANT USAGE, SELECT
    ON ALL SEQUENCES IN SCHEMA master,reference,transact,timeseries,maintenance,inventory,operations,integration,analytics,audit  TO ${APP_USER};
GRANT EXECUTE
    ON ALL FUNCTIONS IN SCHEMA master,reference,transact,timeseries,maintenance,inventory,operations,integration,analytics,audit  TO ${APP_USER};

-- Future objects (ALTER DEFAULT PRIVILEGES for postgres role)
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA master,reference,transact,timeseries,maintenance,inventory,operations,integration,analytics,audit 
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO ${APP_USER};
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA master,reference,transact,timeseries,maintenance,inventory,operations,integration,analytics,audit 
    GRANT USAGE, SELECT ON SEQUENCES TO ${APP_USER};
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA master,reference,transact,timeseries,maintenance,inventory,operations,integration,analytics,audit 
    GRANT EXECUTE ON FUNCTIONS TO ${APP_USER};
ALTER DEFAULT PRIVILEGES IN SCHEMA master,reference,transact,timeseries,maintenance,inventory,operations,integration,analytics,audit 
    GRANT ALL ON TABLES TO ${APP_USER};
ALTER DEFAULT PRIVILEGES IN SCHEMA master,reference,transact,timeseries,maintenance,inventory,operations,integration,analytics,audit 
    GRANT ALL ON SEQUENCES TO ${APP_USER};



-- Explicitly REVOKE dangerous privileges
-- REVOKE CREATE ON SCHEMA public FROM ${APP_USER};
REVOKE ALL ON DATABASE ${DB_NAME} FROM PUBLIC;
GRANT CONNECT ON DATABASE ${DB_NAME} TO ${APP_USER};

\echo 'Schema permissions set for ${APP_USER} on ${DB_NAME}'
SQLEOF

if [ "$OS" = "Linux" ]; then
    sudo -u postgres psql -f "$SQL_PERMS" -v ON_ERROR_STOP=1 \
        2>&1 | tee -a "$LOG_FILE"
else
    psql -U postgres -f "$SQL_PERMS" -v ON_ERROR_STOP=1 \
        2>&1 | tee -a "$LOG_FILE"
fi

#rm -f "$SQL_PERMS"
# -------------------------------------------------------
# Create required tables
# -------------------------------------------------------
log "Creating required tables and views in database ${DB_NAME} ---START---"
psql -U "postgres" -d ${DB_NAME} -f "create_schema_fms_v7.3.sql" -v ON_ERROR_STOP=1 2>&1 | tee -a "$LOG_FILE"
log "Creating required tables and views in database ${DB_NAME} ---DONE---"

log "Schema permissions granted"



# -------------------------------------------------------
# 8. Verify appuser can query the database
# -------------------------------------------------------
hr
log "Verifying $APP_USER access..."

PGPASSWORD="$APP_PASS" psql \
    -h 127.0.0.1 \
    -U "$APP_USER" \
    -d "$DB_NAME" \
    -c "SELECT COUNT(*) AS Employee FROM master.employee_master;" \
    2>&1 | tee -a "$LOG_FILE" || \
    log "WARNING: $APP_USER verification query failed — check pg_hba.conf"

# -------------------------------------------------------
# 9. Print table inventory
# -------------------------------------------------------
hr
log "Table inventory in $DB_NAME:"

#if [ "$OS" = "Linux" ]; then
     psql -U postgres -d $DB_NAME \
        -c "SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(quote_ident(schemaname)||'.'||quote_ident(tablename)::text)) AS size FROM pg_tables WHERE schemaname in ('master','reference','transact','timeseries','maintenance','inventory','operations','integration','analytics','audit') ORDER BY tablename;" \
        2>&1 | tee -a "$LOG_FILE"
#fi
log "Record count of each table"

# QUERY=$(psql -U postgres -d $DB_NAME -At -c "
#  SELECT string_agg(
#      'SELECT ''' ||
#      schemaname || '.' || tablename ||
#      ''' AS tablename, COUNT(*) AS count FROM ' ||
#      quote_ident(schemaname) || '.' || quote_ident(tablename),
#      ' UNION ALL '
#  ) FROM pg_tables WHERE schemaname IN ('master','reference','transact','timeseries','maintenance','inventory','operations','integration','analytics','audit')")

QUERY=$(psql -U postgres -d "$DB_NAME" -At -c "
SELECT string_agg(
    format(
        'SELECT %L AS tablename, COUNT(*) AS count FROM %I.%I',
        schemaname || '.' || tablename,
        schemaname,
        tablename
    ),
    ' UNION ALL '
)
FROM pg_tables
WHERE schemaname IN (
    'master',
    'reference',
    'transact',
    'timeseries',
    'maintenance',
    'inventory',
    'operations',
    'integration',
    'analytics',
    'audit'
);
")

 psql -U "postgres" -d "$DB_NAME" -c "$QUERY"
 
#     psql -U postgres -d $DB_NAME \
#     -c "SELECT 'SELECT '''||schemaname||'.'|| tablename|| ''' as tablename ,COUNT(*) as count FROM '||schemaname||'.'|| tablename||' ;' FROM pg_tables WHERE schemaname in ('master','reference','transact','timeseries','pharma')  group by schemaname,tablename ORDER BY tablename;
#" \
#     2>&1 | tee -a "$LOG_FILE" |tee -a "table_count.sql"
#     psql -U "postgres" -d ${DB_NAME} -f "table_count.sql" -v ON_ERROR_STOP=1 2>&1 | tee -a "$LOG_FILE"


# -------------------------------------------------------
# 10. Create .env file template
# -------------------------------------------------------
hr
ENV_FILE="/c/gitrepo/Vehicle_Management_System/.env"
if [ ! -f "$ENV_FILE" ]; then
    log "Creating .env file..."
    cat > "$ENV_FILE" << ENVEOF
# ============================================================
# Database Configuration — python-de-journey
# ⚠️  NEVER commit this file to git
# ============================================================
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=${DB_NAME}
DB_USER=${APP_USER}
DB_PASSWORD=${APP_PASS}

# Connection Pool Settings
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=2
DB_POOL_RECYCLE=1800
DB_POOL_PRE_PING=true

# App Settings
APP_ENV=development
LOG_LEVEL=INFO
ENVEOF
    log ".env file created at $ENV_FILE"
else
    log ".env already exists — skipping"
fi

# -------------------------------------------------------
# 11. Summary
# -------------------------------------------------------
log "======================================================"
log "  PostgreSQL Setup Complete"
log "======================================================"
log "Database:   $DB_NAME"
log "App User:   $APP_USER"
log "Host:       127.0.0.1:5432"
log "Auth:       scram-sha-256 (pg_hba.conf)"
log "Log:        $LOG_FILE"
log ""
log "Connection string:"
log "  postgresql://${APP_USER}:***@127.0.0.1:5432/${DB_NAME}"
log ""
log "Test with:"
log "  PGPASSWORD='${APP_PASS}' psql -h 127.0.0.1 -U ${APP_USER} -d ${DB_NAME}"
log "======================================================"
