#!/bin/sh
# fix_db_state.sh
#
# Run this script ONCE if initdb.sh fails with:
#   "relation core_customuser does not exist"
#   or
#   "No migrations to apply" followed by a missing table error
#
# It drops all FELA and Django tables and clears the migration history
# so that initdb.sh can start completely clean.
#
# Usage (inside the container):
#   chmod +x fix_db_state.sh
#   ./fix_db_state.sh
#   ./initdb.sh

set -e

echo "=================================================="
echo "  FELA — Fix broken database state"
echo "=================================================="

python manage.py shell -c "
from django.db import connection

print('Dropping FELA schema tables...')
with connection.cursor() as cursor:
    # Drop all tables in the events schema (CASCADE handles FK deps)
    cursor.execute(\"\"\"
        DO \$\$
        DECLARE
            r RECORD;
        BEGIN
            FOR r IN
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'events'
            LOOP
                EXECUTE 'DROP TABLE IF EXISTS events.' || quote_ident(r.tablename) || ' CASCADE';
                RAISE NOTICE 'Dropped: events.%', r.tablename;
            END LOOP;
        END \$\$;
    \"\"\")
    print('  events schema cleared.')

    # Drop Django system tables from public schema
    django_tables = [
        'django_migrations',
        'django_session',
        'django_admin_log',
        'django_content_type',
        'auth_permission',
        'auth_group',
        'auth_group_permissions',
        'auth_user',
        'auth_user_groups',
        'auth_user_user_permissions',
        'core_customuser',
        'core_customuser_groups',
        'core_customuser_user_permissions',
    ]
    for table in django_tables:
        try:
            cursor.execute(f'DROP TABLE IF EXISTS public.{table} CASCADE;')
            print(f'  Dropped: public.{table}')
        except Exception as e:
            print(f'  Could not drop {table}: {e}')

print('Database state reset complete.')
print('Now run: ./initdb.sh')
"

echo ""
echo "=================================================="
echo "  State reset done. Run ./initdb.sh to reinitialise."
echo "=================================================="