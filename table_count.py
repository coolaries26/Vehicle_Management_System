import psycopg2
db_list=('dvdrental','fms','dev_pharma','prd_pharma')
for i in db_list:
    I = str.upper(i)
    conn = psycopg2.connect(
        host="localhost",
        database=i,
        user="postgres",
        password="passw0rd"
    )

    cur = conn.cursor()

#    cur.execute("""
#    SELECT schemaname, tablename
#    FROM pg_tables
#    WHERE schemaname IN
#        ('public','pharma','master','reference','transaction','timeseries')
#    ORDER BY schemaname, tablename
#    """)
    
    cur.execute("""
    SELECT schemaname, tablename
    FROM pg_tables
    WHERE schemaname NOT IN (
        'pg_catalog',
        'information_schema'
    )
    AND schemaname NOT LIKE 'pg_toast%'
    ORDER BY schemaname, tablename
    """)

    tables = cur.fetchall()

    print('-' * 80)
    print(f'------                  For database  ** {I} **                    ------')
    print(f'{"Schema":20} {"Table":40} {"Count":15}')
    print('-' * 80)

    for schema, table in tables:
        sql = f'SELECT COUNT(*) FROM "{schema}"."{table}"'
        cur.execute(sql)

        count = cur.fetchone()[0]

        print(f'{schema}.{table:40} {count}')

    cur.close()
    conn.close()
