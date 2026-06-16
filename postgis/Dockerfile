FROM postgis/postgis:16-3.4

WORKDIR /usr/local/app

# The FELA seed: a pg_dump (custom format) of the 'events' schema plus the
# Django/auth tables in 'public'. Generated from scripts/001-008 (see
# djangoapi/scripts/README.md) or, ideally, from the live accumulated
# database so manually-added data is preserved across re-deployments.
#
# fela_seed.list is a pg_restore TOC list with the "public" schema's own
# CREATE SCHEMA/COMMENT entries commented out (every fresh cluster already
# has a 'public' schema, so restoring it too just errors with "schema
# public already exists" and would abort init-db.sh). Regenerate both with:
#   pg_dump -Fc -n events -n public --exclude-table-data=public.spatial_ref_sys \
#     --no-owner --no-privileges -f fela_seed.dump
#   pg_restore --list fela_seed.dump > fela_seed.list
#   # then comment out (prefix ';') the "SCHEMA public" and its COMMENT lines
COPY ./fela_seed.dump ./fela_seed.list ./

# Copy the init-db.sh script into the container.
# Everything in /docker-entrypoint-initdb.d is executed by the base image's
# entrypoint, but ONLY the first time the container starts with an empty
# PGDATA directory. If the volume already has data, this is skipped entirely.
COPY ./init-db.sh /docker-entrypoint-initdb.d/init-db.sh

# Grant execution permissions for the init-db.sh script
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh
