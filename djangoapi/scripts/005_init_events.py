"""
scripts/005_init_events.py

Loads initial Event data into the events"."event table.
Data sourced from the original backupFELA.py (events table).

Each event references:
  - A Country that must exist  (run 002_init_country.py first)
  - A City    that must exist  (run 003_init_city.py first)

Agency associations are handled separately in 008_init_relations.py.

Run via:
    python manage.py shell < scripts/005_init_events.py
"""
from FELA.models import Country, City, Event

# ---------------------------------------------------------------------------
# Source data
# Tuple: (date, year, event_type, country_name, city_name, event_title)
# ---------------------------------------------------------------------------
EVENTS_DATA = [
    (
        '3-5 november 2025', 2025, 'Conference',
        'Brazil', 'Florianópolis',
        'FIG Joint Land Administration Conference'
    ),
    (
        '17 july 2025', 2025, 'Webinar',
        'Online', 'Online',
        'Unlocking FELA a global dialogue on land administration '
    ),
    (
        '16-17 June 2025', 2025, 'Workshop',
        'France', 'Paris',
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)'
    ),
    (
        '30 April 2025, 20 May 2025', 2025, 'Lectures',
        'Online', 'Online',
        'Strengthening Academic Foundations in Land Governance: Online Lectures '
        'Hosted in Collaboration with Al-Quds and Duhok Universities'
    ),
    (
        '17 February 2025', 2025, 'pre-workshop',
        'Morocco', 'Rabat',
        'Technical pre-workshop 3rd Arab Land Conference '
        '"Fit-for-Purpose Land Administration in the Arab Region"'
    ),
    (
        '11-13 November 2024', 2024, 'Congress',
        'Brazil', 'Florianópolis',
        'Congress of Multifinalial Cadastre and Territorial Management '
        '– COBRAC 2024'
    ),
    (
        '24-26 September 2024', 2024, 'ANNUAL MEETING',
        'Malaysia', 'Sarawak',
        'FIG COMMISSION 5, 7 ANNUAL MEETING 2024 Framework for Effective Land '
        'Administration (WG7.1 FELA) + Fit for Purpose Land Administration '
        '(WG7.2 FFPLA)'
    ),
    (
        '17-19 June 2024', 2024, 'Conference',
        'Belgium', 'Brujes',
        'Permanent Committee on Cadastre in the European Union (PCC)'
    ),
    (
        '19-24 May 2024', 2024, 'Congress',
        'Ghana', 'Accra',
        'FIG Woorking Week 2024 - Land Policy Issues and Innovations'
    ),
    (
        '8-11 April 2024', 2024, 'Seminar',
        'Mexico', 'Aguascalientes',
        'Fifth meeting of the Expert Group on Land Administration and '
        'Management and the International Seminar on UN-GGIM'
    ),
    (
        '27-29 February 2024', 2024, 'Workshop',
        'Nepal', 'Dhulikhel',
        'Effective Land Administration in Nepal: Navigating Governance, Legal, '
        'and Financial Pathways within the Climate Change – Land Nexus'
    ),
    (
        '4-7 December 2023', 2023, 'Assembly',
        'Chile', 'Santiago de Chile',
        'XIV Simposio y IX Asamblea del CPCI'
    ),
    (
        '18-20 october 2023', 2023, 'Expert Group Meeting',
        'Chile', 'Santiago de Chile',
        'X session UN-GGIM : Americas '
    ),
    (
        '2-4 october 2023', 2023, 'Meeting',
        'the Netherlands', 'Deventer',
        'FIG Meeting Digital Transformation for Responsible Land Administration'
    ),
    (
        '28 may- 1 June 2023', 2023, 'Congress',
        'USA', 'Orlando',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers'
    ),
    (
        '11-15 September 2022', 2022, 'Congress',
        'Poland', 'Warsaw',
        'XXVII FIG Congress - Volunteering for the Future Geospatial Excellence '
        'for a better living'
    ),
    (
        '3-5 august  2022', 2022, 'Expert Group Meeting',
        'Online', 'Online',
        'Twelfth Session of the United Nations Committee of Experts on Global '
        'Geospatial Information Management (UN-GGIM)'
    ),
    (
        '11-12 May 2022', 2022, 'Seminar',
        'the Netherlands', 'Amsterdam',
        'Geospatial World Forum 2022, Symposium on Land Administration'
    ),
    (
        '17-18 May 2022', 2022, 'Expert Group Meeting',
        'Singapore', 'Singapore',
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management'
    ),
    (
        '12 August 2021', 2021, 'Expert Group Meeting',
        'Online', 'Online',
        'Expert Group on Land Administration and Management Side Event at the '
        'Eleventh Session of the Committee of Experts on Global Geospatial '
        'Information Management'
    ),
    (
        '26-27 August - 4 September  2020', 2020, 'Expert Group Meeting',
        'Online', 'Online',
        'Tenth Session of the United Nations Committee of Experts on Global '
        'Geospatial Information Management (UN-GGIM)'
    ),
    (
        'may-20', 2020, 'Document',
        'Online', 'Online',
        'Actual version FELA'
    ),
    (
        '3-5 November 2019', 2019, 'Meeting',
        'Australia', 'Canberra',
        'Eighth Plenary Meeting of UN-GGIM-AP (Asia-Pacific)'
    ),
    (
        '5 - 9 August 2019', 2019, 'Expert Group Meeting',
        'USA', 'New York',
        'Ninth Session of the United Nations Committee of Experts on Global '
        'Geospatial Information Management (UN-GGIM)'
    ),
    (
        '2-4 August 2017', 2017, 'Expert Group Meeting',
        'USA', 'New York',
        'Eighth Session of the United Nations Committee of Experts on Global '
        'Geospatial Information Management (UN-GGIM)'
    ),
]

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
created_count = 0
skipped_count = 0
error_count   = 0

for date, year, event_type, country_name, city_name, event_title in EVENTS_DATA:

    # Resolve country
    country = Country.objects.filter(country__iexact=country_name).first()
    if not country:
        print(f"  [!] ERROR — Country not found: '{country_name}' "
              f"(event: '{event_title[:60]}...')")
        error_count += 1
        continue

    # Resolve city (must match country + city name)
    city = City.objects.filter(
        country=country,
        city__iexact=city_name
    ).first()
    if not city:
        print(f"  [!] ERROR — City not found: '{city_name}' in '{country_name}' "
              f"(event: '{event_title[:50]}...')")
        error_count += 1
        continue

    event, created = Event.objects.get_or_create(
        event_title=event_title,
        defaults={
            'date':    date,
            'year':    year,
            'type':    event_type,
            'country': country,
            'city':    city.city,
        }
    )

    if created:
        created_count += 1
        print(f"  [+] Created : [{year}] {event_title[:70]}")
    else:
        skipped_count += 1
        print(f"  [=] Exists  : [{year}] {event_title[:70]}")

print()
print(f"Done. Created: {created_count} | Skipped: {skipped_count} | "
      f"Errors: {error_count} | Total events: {Event.objects.count()}")
