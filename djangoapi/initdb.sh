#!/bin/sh
set -e

echo "=================================================="
echo "  FELA Backend — Database Initialization"
echo "=================================================="
echo ""
echo "This assumes the 'postgis' container already restored the FELA seed"
echo "dump on first start (see postgis/init-db.sh). This script only brings"
echo "the Django side of the schema up to date and ensures an admin user"
echo "exists."
echo ""
echo "If you are bootstrapping from a truly empty database (no seed dump"
echo "available), use ./initdb_from_empty.sh instead."

echo ""
echo "==> Step 1: Applying Django migrations..."
python manage.py migrate

echo ""
echo "==> Step 2: Creating superuser (skipped if one already exists)..."
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD} python manage.py createsuperuser \
    --noinput \
    --username ${DJANGO_SUPERUSER_USERNAME} \
    --email ${DJANGO_SUPERUSER_EMAIL} || true

echo ""
echo "=================================================="
echo "  Initialization complete."
echo "=================================================="
