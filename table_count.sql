DO \$\$
DECLARE
    sql text;
BEGIN
    SELECT string_agg(
        format(
            'SELECT %L as tablename, COUNT(*) as count FROM %I.%I',
            schemaname || '.' || tablename,
            schemaname,
            tablename
        ),
        ' UNION ALL '
    )
    INTO sql
    FROM pg_tables
    WHERE schemaname IN
        ('master','reference','transaction','timeseries');
    EXECUTE '%i',sql;
    
    RAISE NOTICE '%', sql;
END \$\$;

