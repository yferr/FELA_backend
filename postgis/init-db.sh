#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
until pg_isready; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

echo "PostgreSQL is ready. Restoring FELA seed data."

### RESTORE THE DATABASE
# fela_seed.dump is a pg_dump custom-format dump of the 'events' schema and
# the Django/auth tables in 'public' (see postgis/Dockerfile). It was
# produced with --no-owner, so objects are restored as ${POSTGRES_USER}
# (the role the base image already created from env vars) — no extra role
# needs to be created first. If you ever restore a dump that references a
# foreign owner, create that role first (see init-users.sql for the pattern)
# and drop --no-owner below.
#
# fela_seed.list filters out the dump's "public" schema entry, since a
# fresh cluster already has one (restoring it again is a harmless but fatal
# error under `set -e`).
pg_restore -v --no-owner --use-list=/usr/local/app/fela_seed.list \
    -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" /usr/local/app/fela_seed.dump

echo "FELA seed data restored."
