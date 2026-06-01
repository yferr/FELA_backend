"""
scripts/001_create_schemas.py

Creates the 'events' PostgreSQL schema if it does not already exist.

Run via:
    python manage.py shell < scripts/001_create_schemas.py
"""
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("CREATE SCHEMA IF NOT EXISTS events;")
    print("Schema 'events' created (or already exists).")
