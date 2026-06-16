#!/bin/sh
# postgis/regenerate_seed.sh
#
# Regenerates postgis/fela_seed.dump + fela_seed.list from whatever data is
# currently in the running 'postgis' container's database.
#
# Run this whenever you've added or edited data directly in Postgres
# (psql, pgAdmin, Django admin, etc.) and want that data to become the seed
# that gets restored automatically into fresh deployments — i.e. whenever
# you want to "make a new backup" of the FELA dataset.
#
# Usage (from the repo root, with the stack already running):
#   ./postgis/regenerate_seed.sh                       # dev stack (docker-compose.yml)
#   ./postgis/regenerate_seed.sh docker-compose.prod.yml
#
# After it finishes, review the diff and commit postgis/fela_seed.dump and
# postgis/fela_seed.list if it looks right.
set -e

COMPOSE_FILE="${1:-docker-compose.yml}"
CONTAINER_TMP_DUMP="/tmp/fela_seed.dump"

CID=$(docker compose -f "$COMPOSE_FILE" ps -q postgis)
if [ -z "$CID" ]; then
    echo "ERROR: no running 'postgis' service found for $COMPOSE_FILE. Is the stack up?" >&2
    exit 1
fi

echo "==> Dumping 'events' schema + Django/auth tables from container $CID..."
docker exec "$CID" sh -c "
    pg_dump -Fc -U \"\$POSTGRES_USER\" -d \"\$POSTGRES_DB\" \
        -n events -n public \
        --exclude-table-data=public.spatial_ref_sys \
        --no-owner --no-privileges \
        -f ${CONTAINER_TMP_DUMP}
"

echo "==> Building filtered TOC list (drops the 'public' schema's own CREATE SCHEMA — it always pre-exists on a fresh cluster)..."
docker exec "$CID" pg_restore --list "$CONTAINER_TMP_DUMP" \
    | sed -E \
        -e 's/^([0-9]+; [0-9]+ [0-9]+ SCHEMA - public .*)$/;\1/' \
        -e 's/^([0-9]+; [0-9]+ [0-9]+ COMMENT - SCHEMA public .*)$/;\1/' \
    > postgis/fela_seed.list

docker cp "${CID}:${CONTAINER_TMP_DUMP}" postgis/fela_seed.dump
docker exec "$CID" rm -f "$CONTAINER_TMP_DUMP"

echo ""
echo "==> Done. postgis/fela_seed.dump and postgis/fela_seed.list updated."
echo "    Row counts in the new dump:"
docker exec "$CID" sh -c '
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -t -c "
        select '"'"'event'"'"', count(*) from events.event
        union all select '"'"'speaker'"'"', count(*) from events.speaker
        union all select '"'"'country'"'"', count(*) from events.country
        union all select '"'"'agency'"'"', count(*) from events.agency
        union all select '"'"'city'"'"', count(*) from events.city
        union all select '"'"'presentation'"'"', count(*) from events.presentation
    "
'
