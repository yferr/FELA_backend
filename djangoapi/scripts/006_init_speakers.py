"""
scripts/006_init_speakers.py

Loads initial Speaker data into the events"."speaker table.
Data sourced from the original backupFELA.py (speakers table).

Each speaker references:
  - A Country that must exist  (run 002_init_country.py first)
  - An Agency that must exist  (run 004_init_agency.py first)
    → agency_name = None means the speaker has no agency (null FK allowed)

IMPORTANT: In the new model, Speaker.agency is a ForeignKey to Agency
(null=True, blank=True), replacing the old free-text agency_s field.
Speakers whose original agency_s value does not match an existing Agency
name are created with agency = None. You can update them later via the admin.

Run via:
    python manage.py shell < scripts/006_init_speakers.py
"""
from FELA.models import Country, Agency, Speaker

# ---------------------------------------------------------------------------
# Source data — (name, country_name, agency_name_or_None)
# Sourced from the original speakers table in backupFELA.py.
# agency_name matches the 'name' field in the new Agency model.
# ---------------------------------------------------------------------------
SPEAKERS_DATA = [
    # id=1
    ('Amalia Velasco',
     'Spain',
     'FIG'),                                    # original: Direccion General del Catastro España — no exact match, map to None
    # id=2
    ('Mario Piumetto',
     'Argentina',
     None),
    # id=3
    ('Markus Koper',
     'Germany',
     None),
    # id=4
    ('Kean Huat Soon',
     'Singapore',
     None),
    # id=5
    ('Victor Khoo',
     'Singapore',
     None),
    # id=6
    ('Israel Taiwo',
     'Nigeria',
     None),
    # id=7
    ('Magdalena Andersson',
     'Sweden',
     None),
    # id=8
    ('Joep Crompvoets',
     'Belgium',
     None),
    # id=9
    ('Rohan Bennett',
     'Australia',
     'FIG'),
    # id=10
    ('Eva-Maria Unger',
     'the Netherlands',
     'Kadaster'),
    # id=11
    ('Kirsikka Riekkinen',
     'Finland',
     None),
    # id=12
    ('Oluwafemi Adekola',
     'Finland',
     None),
    # id=13
    ('Opeyemi Michael Ajayi',
     'Finland',
     None),
    # id=14
    ('Mamadou Mballo',
     'Democratic Republic of Congo',
     'GLTN'),
    # id=15
    ('Hellen Ndungu',
     'Kenya',
     'GLTN'),
    # id=16
    ('John Gitau',
     'Kenya',
     'GLTN'),
    # id=17
    ('Leandre Murrell-Forde',
     'Barbados',
     None),
    # id=18
    ('Claudio Martínez Topete',
     'Mexico',
     None),
    # id=19
    ('Raffaella Anilio Olguín',
     'Chile',
     'UN-GGIM Américas'),
    # id=20
    ('Ridomil Alejandro Rojas Ferreyra',
     'Republica Dominicana',
     None),
    # id=21
    ('Markku Markkula',
     'Finland',
     None),
    # id=22
    ('Ganesh Prasad Bhatta',
     'Nepal',
     None),
    # id=23
    ('Raja Ram Chhatkuli',
     'Nepal',
     None),
    # id=24
    ('Janak Raj Joshi',
     'Nepal',
     None),
    # id=25
    ('Mikael Lilje',
     'Sweden',
     None),
    # id=26
    ('Jean-Philippe Lestang',
     'France',
     'IGN France'),
    # id=27
    ('Charisse Griffith-Charles',
     'Trinidad And Tobago',
     None),
    # id=28
    ('Katie Pickett',
     'USA',
     None),
    # id=29
    ('Kees de Zeeuw',
     'the Netherlands',
     'Kadaster International'),
    # id=30
    ('Brandon Tourtelotte',
     'USA',
     None),
    # id=31
    ('Mahamat Abdoulaye Malloum',
     'Chad',
     None),
    # id=32
    ('Claudia Stöcker',
     'Germany',
     None),
    # id=33
    ('Christelle van den Berg',
     'the Netherlands',
     'Kadaster'),
    # id=34
    ('Kaspar Kundert',
     'Rwanda',
     None),
    # id=35
    ('Dina Naguib',
     'Egypt',
     None),
    # id=36
    ('Jobo Samba',
     'Sierra Leone',
     None),
    # id=37
    ('Divyani Kohli',
     'the Netherlands',
     None),
    # id=38
    ('Mila Koeva',
     'the Netherlands',
     None),
    # id=39
    ('Vincent Verheij',
     'the Netherlands',
     None),
    # id=40
    ('Haico Van der Vegt',
     'the Netherlands',
     None),
    # id=41
    ('Suren Tovmasyan',
     'Armenia',
     None),
    # id=42
    ('Indra Hutabarat',
     'Indonesia',
     None),
    # id=43
    ('Aram Gugarats',
     'Armenia',
     None),
    # id=44
    ('Aulia Latif',
     'Indonesia',
     None),
    # id=45
    ('Chalemyan Trdat',
     'Armenia',
     None),
    # id=46
    ('Committee of Experts on Global Geospatial Information Management',
     '-',
     'UN-GGIM'),
    # id=47
    ('Brent Jones',
     'USA',
     None),
    # id=48
    ('Ching Tuan Yee',
     'Singapore',
     None),
    # id=49
    ('Meizyanne Hicks',
     'Fiji',
     None),
    # id=50
    ('Chris Body',
     'Australia',
     None),
    # id=51
    ('Christiaan Lemmen',
     'the Netherlands',
     None),
    # id=52
    ('Abdullah Kara',
     '-',
     None),
    # id=53
    ('Peter van Oosterom',
     'the Netherlands',
     None),
    # id=54
    ('Mohamed Rafeek',
     'Sri Lanka',
     None),
    # id=55
    ('Paula Dijkstra',
     'the Netherlands',
     'Kadaster International'),
    # id=56
    ('Ingrid van de Berghe',
     'Belgium',
     None),
    # id=57
    ('Mario Cruz',
     'Mexico',
     None),
    # id=58
    ('Cristian Araneda Hernandez',
     'Chile',
     None),
    # id=59
    ('Ali Alawaji',
     'Kingdom of Saudi Arabia',
     None),
    # id=60
    ('Liao Rong',
     'China',
     None),
    # id=61
    ('Liu Yong',
     'China',
     None),
    # id=62
    ('Zhong Taiyang',
     'China',
     None),
    # id=63
    ('Trevor Benn',
     '-',
     'UN-GGIM'),
    # id=64
    ('Teo Chee Hai',
     '-',
     'UN-GGIM'),
    # id=65
    ('Expert Group',
     '-',
     None),
    # id=66
    ('Anka Lisec',
     'Slovenia',
     None),
    # id=67
    ('Frédéric Cantat',
     'France',
     'IGN France'),
    # id=68
    ('Regina Orvananos',
     'Mexico',
     None),
    # id=69
    ('Elisabeth Leblanc',
     'France',
     'IGN France'),
    # id=70
    ('Vents Priedoliņš',
     'Latvia',
     None),
    # id=71
    ('Aurélia Decherf',
     'France',
     'IGN France'),
    # id=72
    ('Kholoud Saad Salama',
     'Egypt',
     None),
    # id=73
    ('Bénédicte Bucher',
     'France',
     'IGN France'),
    # id=74
    ('Romain Vialle',
     'France',
     'IGN France'),
    # id=75
    ('Nick Land',
     'United Kingdom',
     None),
]

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
created_count  = 0
skipped_count  = 0
error_count    = 0
no_agency      = 0

for name, country_name, agency_name in SPEAKERS_DATA:

    # Resolve country
    country = Country.objects.filter(country__iexact=country_name).first()
    if not country:
        print(f"  [!] ERROR — Country not found: '{country_name}' "
              f"(speaker: '{name}')")
        error_count += 1
        continue

    # Resolve agency (optional)
    agency = None
    if agency_name:
        agency = Agency.objects.filter(name__iexact=agency_name).first()
        if not agency:
            print(f"  [~] WARNING — Agency not found: '{agency_name}' "
                  f"(speaker: '{name}') — created with agency=None")
            no_agency += 1

    speaker, created = Speaker.objects.get_or_create(
        name=name,
        country=country,
        defaults={'agency': agency}
    )

    if created:
        created_count += 1
        agency_label = agency.name if agency else '—'
        print(f"  [+] Created : {name} | {country_name} | {agency_label}")
    else:
        skipped_count += 1
        print(f"  [=] Exists  : {name} | {country_name}")

print()
print(f"Done. Created: {created_count} | Skipped: {skipped_count} | "
      f"Errors: {error_count} | Agency not found (set to None): {no_agency} | "
      f"Total speakers: {Speaker.objects.count()}")
