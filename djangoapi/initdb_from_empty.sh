#!/bin/sh
set -e

echo "=================================================="
echo "  FELA Backend — Bootstrap from an empty database"
echo "=================================================="
echo ""
echo "Use this only when no FELA seed dump is available (e.g. the postgis"
echo "container could not restore postgis/fela_seed.dump). It rebuilds the"
echo "schema from Django migrations and reloads the historical seed data"
echo "as a fixture — the data that scripts/002_init_country.py through"
echo "scripts/008_init_relations.py originally produced. Those scripts are"
echo "kept in scripts/ for historical reference; this fixture is the"
echo "regenerated, loaddata-ready equivalent (see scripts/README.md)."

echo ""
echo "==> Step 1: Creating database schema 'events'..."
python manage.py shell < scripts/001_create_schemas.py

echo ""
echo "==> Step 2: Applying Django migrations..."
python manage.py migrate

echo ""
echo "==> Step 3: Creating superuser..."
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD} python manage.py createsuperuser \
    --noinput \
    --username ${DJANGO_SUPERUSER_USERNAME} \
    --email ${DJANGO_SUPERUSER_EMAIL} || true

echo ""
echo "==> Step 4: Loading historical seed data fixture..."
python manage.py loaddata FELA/fixtures/historical_seed_data.json

echo ""
echo "==> Step 5: Backfill created_by for all legacy records..."
python manage.py shell < scripts/003_backfill_created_by.py

echo ""
echo "=================================================="
echo "  Bootstrap complete."
echo "=================================================="
