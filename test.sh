# #!/bin/bash
# 
# DB=fms
# USER=postgres
# LOG=abc.log
# 
# SQL_FILE=/tmp/table_count.sql
# 
# psql -U "$USER" -d "$DB" -At -c "
# SELECT
#     'SELECT ''' ||
#     schemaname || '.' || tablename ||
#     ''' AS tablename, COUNT(*) AS count FROM ' ||
#     quote_ident(schemaname) || '.' || quote_ident(tablename)
# FROM pg_tables
# WHERE schemaname IN ('master','reference','transaction','timeseries')
# ORDER BY schemaname, tablename;
# " |
# awk '
# NR==1 {printf "%s", $0}
# NR>1 {printf "\nUNION ALL\n%s", $0}
# END {print ";"}
# ' > "$SQL_FILE"
# 
# psql -U "$USER" -d "$DB" -f "$SQL_FILE" \
#     2>&1 | tee -a "$LOG"
# 
# rm -f "$SQL_FILE"

#!/bin/bash
 DB=fms
 USER=postgres
 
 QUERY=$(psql -U "$USER" -d "$DB" -At -c "
 SELECT string_agg(
     'SELECT ''' ||
     schemaname || '.' || tablename ||
     ''' AS tablename, COUNT(*) AS count FROM ' ||
     quote_ident(schemaname) || '.' || quote_ident(tablename),
     ' UNION ALL '
 )
 FROM pg_tables
 WHERE schemaname IN ('master','reference','transaction','timeseries');
 ")
 
 psql -U "$USER" -d "$DB" -c "$QUERY"


# LOG_FILE="a_setup_fms_db.log"
# SQL_COUNT=$(mktemp /tmp/pg_count_XXXXXX.sql)
# cat > "$SQL_COUNT" << SQLEOF
# -- ==========================================================
# -- PostgreSQL Setup: appuser + pharma db database
# -- Run as postgres superuser
# -- ==========================================================
# DO \$\$
# DECLARE
#     sql text;
# BEGIN
#     SELECT string_agg(
#         format(
#             'SELECT %L as tablename, COUNT(*) as count FROM %I.%I',
#             schemaname || '.' || tablename,
#             schemaname,
#             tablename
#         ),
#         ' UNION ALL '
#     )
#     INTO sql
#     FROM pg_tables
#     WHERE schemaname IN
#         ('master','reference','transaction','timeseries');
#   
# END \$\$;
# SQLEOF
# 
# # Execute setup SQL as postgres
# if [ "$OS" = "Linux" ]; then
#     sudo -u postgres psql -f "$SQL_COUNT" -v ON_ERROR_STOP=1 \
#         2>&1 | tee -a "$LOG_FILE"
# else
#     psql -U postgres -f "$SQL_COUNT" -v ON_ERROR_STOP=1 \
#         2>&1 | tee -a "$LOG_FILE"
# fi
