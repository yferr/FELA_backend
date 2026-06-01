"""
scripts/003_backfill_created_by.py

Assigns the first superuser as created_by to all existing records
that have created_by = NULL (legacy data loaded before ownership tracking).

Run via:
    python manage.py shell < scripts/003_backfill_created_by.py
"""
from django.contrib.auth import get_user_model
from FELA.models import (
    Country, City, Agency, Event, Presentation,
    Speaker, PresentationSpeaker, EventAgency
)

User = get_user_model()

superuser = User.objects.filter(is_superuser=True).order_by('id').first()

if not superuser:
    print("ERROR: No superuser found. Create one first:")
    print("  python manage.py createsuperuser")
    raise SystemExit(1)

print(f"Using superuser: '{superuser.username}' (id={superuser.id})")
print("")

MODELS = [
    Country,
    City,
    Agency,
    Event,
    Presentation,
    Speaker,
    PresentationSpeaker,
    EventAgency,
]

total_updated = 0

for Model in MODELS:
    qs = Model.objects.filter(created_by__isnull=True)
    count = qs.count()
    if count > 0:
        updated = qs.update(created_by=superuser)
        total_updated += updated
        print(f"  [+] {Model.__name__}: {updated} record(s) updated")
    else:
        print(f"  [=] {Model.__name__}: nothing to update")

print(f"\nBackfill complete. Total records updated: {total_updated}")