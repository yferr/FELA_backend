#!/bin/sh
set -e

echo "=================================================="
echo "  FELA Backend — Database Initialization"
echo "=================================================="

echo ""
echo "==> Step 1: Creating database schema 'events'..."
python manage.py shell < scripts/001_create_schemas.py

echo ""
echo "==> Step 2: Resetting migration state (clean slate)..."
# Remove any stale migration records from a previous broken run.
# This forces Django to re-apply all migrations from scratch.
# Safe to run on an empty database — does nothing if the table does not exist.
python manage.py shell -c "
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute(\"DELETE FROM django_migrations;\")
    print('  Migration history cleared.')
except Exception as e:
    print(f'  django_migrations not found yet (first run) — OK: {e}')
"

echo ""
echo "==> Step 3: Generating migrations..."
python manage.py makemigrations

echo ""
echo "==> Step 4: Applying migrations..."
python manage.py migrate

echo ""
echo "==> Step 5: Creating superuser..."
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD} python manage.py createsuperuser \
    --noinput \
    --username ${DJANGO_SUPERUSER_USERNAME} \
    --email ${DJANGO_SUPERUSER_EMAIL} || true

echo ""
echo "==> Step 6: Loading countries..."
python manage.py shell < scripts/002_init_country.py

echo ""
echo "==> Step 7: Loading cities..."
python manage.py shell < scripts/003_init_city.py

echo ""
echo "==> Step 8: Loading agencies..."
python manage.py shell < scripts/004_init_agency.py

echo ""
echo "==> Step 9: Loading events..."
python manage.py shell < scripts/005_init_events.py

echo ""
echo "==> Step 10: Loading speakers..."
python manage.py shell < scripts/006_init_speakers.py

echo ""
echo "==> Step 11: Loading presentations..."
python manage.py shell < scripts/007_init_presentations.py

echo ""
echo "==> Step 12: Loading relations (EventAgency + PresentationSpeaker)..."
python manage.py shell < scripts/008_init_relations.py

echo ""
echo "==> Step 13: Backfill created_by for all legacy records..."
python manage.py shell < scripts/003_backfill_created_by.py

echo ""
echo "=================================================="
echo "  Initialization complete."
echo "=================================================="