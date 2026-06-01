"""
scripts/002_init_country.py

Loads initial Country data into the new 'events'."country" table.
Data sourced from the original backupFELA.py (countries_tmp table).

Run via:
    python manage.py shell < scripts/002_init_country.py
"""
from FELA.models import Country

countries_data = [
    {'country': 'Morocco',                    'lat': 34.0209000, 'lon': -6.8416000},
    {'country': 'Malaysia',                   'lat': 1.5533000,  'lon': 110.3592000},
    {'country': 'Belgium',                    'lat': 51.2088900, 'lon': 3.2241700},
    {'country': 'Ghana',                      'lat': 5.6148180,  'lon': -0.2058740},
    {'country': 'Mexico',                     'lat': 21.8853000, 'lon': -102.2916000},
    {'country': 'Nepal',                      'lat': 27.6226000, 'lon': 85.5423000},
    {'country': 'Chile',                      'lat': -33.4489000,'lon': -70.6693000},
    {'country': 'USA',                        'lat': 39.8283000, 'lon': -98.5795000},
    {'country': 'Poland',                     'lat': 52.2297000, 'lon': 21.0122000},
    {'country': 'the Netherlands',            'lat': 52.3675730, 'lon': 4.9041390},
    {'country': 'Singapore',                  'lat': 1.3521000,  'lon': 103.8198000},
    {'country': 'Australia',                  'lat': -25.2744000,'lon': 133.7751000},
    {'country': 'France',                     'lat': 46.6034000, 'lon': 1.8883000},
    {'country': 'Spain',                      'lat': 40.4637000, 'lon': -3.7492000},
    {'country': 'Argentina',                  'lat': -34.0000000,'lon': -64.0000000},
    {'country': 'Germany',                    'lat': 51.1657000, 'lon': 10.4515000},
    {'country': 'Nigeria',                    'lat': 9.0820000,  'lon': 8.6753000},
    {'country': 'Sweden',                     'lat': 60.1282000, 'lon': 18.6435000},
    {'country': 'Finland',                    'lat': 64.0000000, 'lon': 26.0000000},
    {'country': 'Democratic Republic of Congo','lat': -4.0383000, 'lon': 21.7587000},
    {'country': 'Kenya',                      'lat': -1.2921000, 'lon': 36.8219000},
    {'country': 'Barbados',                   'lat': 13.1939000, 'lon': -59.5432000},
    {'country': 'Republica Dominicana',       'lat': 18.7357000, 'lon': -70.1627000},
    {'country': 'Trinidad And Tobago',        'lat': 10.6918000, 'lon': -61.2225000},
    {'country': 'Chad',                       'lat': 15.4542000, 'lon': 18.7322000},
    {'country': 'Rwanda',                     'lat': -1.9403000, 'lon': 29.8739000},
    {'country': 'Egypt',                      'lat': 26.8206000, 'lon': 30.8025000},
    {'country': 'Armenia',                    'lat': 40.0691000, 'lon': 45.0382000},
    {'country': 'Indonesia',                  'lat': -0.7893000, 'lon': 113.9213000},
    {'country': 'Fiji',                       'lat': -17.7134000,'lon': 178.0650000},
    {'country': 'Sri Lanka',                  'lat': 7.8731000,  'lon': 80.7718000},
    {'country': 'Kingdom of Saudi Arabia',    'lat': 23.8859000, 'lon': 45.0792000},
    {'country': 'China',                      'lat': 35.8617000, 'lon': 103.0000000},
    {'country': 'United Kingdom',             'lat': 55.3781000, 'lon': -3.4360000},
    {'country': 'Slovenia',                   'lat': 46.1512000, 'lon': 14.9955000},
    {'country': 'Latvia',                     'lat': 56.8796000, 'lon': 24.6032000},
    {'country': 'Sierra Leone',               'lat': 8.4606000,  'lon': -11.7799000},
    {'country': 'Brazil',                     'lat': -14.2350000,'lon': -51.9253000},
    {'country': 'Online',                     'lat': 0.0,        'lon': 0.0},
    {'country': '-',                          'lat': 0.0,        'lon': 0.0},
]

created_count = 0
skipped_count = 0

for data in countries_data:
    obj, created = Country.objects.get_or_create(
        country=data['country'],
        defaults={'lat': data['lat'], 'lon': data['lon']}
    )
    if created:
        created_count += 1
        print(f"  [+] Created: {obj.country}")
    else:
        skipped_count += 1
        print(f"  [=] Already exists: {obj.country}")

print(f"\nDone. Created: {created_count} | Skipped: {skipped_count} | Total: {Country.objects.count()}")
