"""
scripts/003_init_city.py

Loads initial City data into the events"."city table.
Data sourced from the original backupFELA.py (cities / cities_tmp tables).

Each city requires a Country that already exists in the database.
Run AFTER 002_init_country.py.

Run via:
    python manage.py shell < scripts/003_init_city.py
"""
from FELA.models import Country, City

# ---------------------------------------------------------------------------
# Source data — (country_name, city_name, lat, lon)
# Coordinates from the original cities_tmp table in backupFELA.py.
# The 'Online' and '-' rows use (0.0, 0.0) as placeholder coordinates.
# ---------------------------------------------------------------------------
CITIES_DATA = [
    ('Morocco',          'Rabat',             34.0209000,  -6.8416000),
    ('Brazil',           'Florianópolis',     -27.5935000, -48.5585400),
    ('Malaysia',         'Sarawak',            1.5533000,  110.3592000),
    ('Belgium',          'Brujes',            51.2088900,    3.2241700),
    ('Ghana',            'Accra',              5.6148180,   -0.2058740),
    ('Mexico',           'Aguascalientes',    21.8853000, -102.2916000),
    ('Nepal',            'Dhulikhel',         27.6226000,   85.5423000),
    ('Chile',            'Santiago de Chile', -33.4489000,  -70.6693000),
    ('USA',              'Orlando',           28.5383000,   -81.3792000),
    ('USA',              'New York',          40.7127760,   -74.0059740),
    ('Poland',           'Warsaw',            52.2297000,    21.0122000),
    ('the Netherlands',  'Amsterdam',         52.3675730,    4.9041390),
    ('the Netherlands',  'Deventer',          52.2550000,    6.1639000),
    ('Singapore',        'Singapore',          1.3521000,  103.8198000),
    ('Australia',        'Canberra',          -35.2809000,  149.1300000),
    ('France',           'Paris',             46.6034000,    1.8883000),
    ('Spain',            'Madrid',            40.4637000,   -3.7492000),
    ('Kenya',            'Nairobi',           -1.2921000,   36.8219000),
    ('Online',           'Online',             0.0,          0.0),
    ('-',                '-',                  0.0,          0.0),
]

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
created_count = 0
skipped_count = 0
error_count   = 0

for country_name, city_name, lat, lon in CITIES_DATA:
    # Resolve parent country
    country = Country.objects.filter(country__iexact=country_name).first()
    if not country:
        print(f"  [!] ERROR — Country not found: '{country_name}' "
              f"(needed for city '{city_name}'). Run 002_init_country.py first.")
        error_count += 1
        continue

    city, created = City.objects.get_or_create(
        country=country,
        city=city_name,
        defaults={'lat': lat, 'lon': lon}
    )

    if created:
        created_count += 1
        print(f"  [+] Created : {city_name}, {country_name}  ({lat}, {lon})")
    else:
        skipped_count += 1
        print(f"  [=] Exists  : {city_name}, {country_name}")

print()
print(f"Done. Created: {created_count} | Skipped: {skipped_count} | "
      f"Errors: {error_count} | Total cities: {City.objects.count()}")
