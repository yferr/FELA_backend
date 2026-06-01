"""
scripts/004_init_agency.py

Loads initial Agency data into the events"."agency table.
Data sourced from the original backupFELA.py (agencies table).

Run AFTER 003_init_city.py (no hard dependency, but keep order consistent).

Run via:
    python manage.py shell < scripts/004_init_agency.py
"""
from FELA.models import Agency

# ---------------------------------------------------------------------------
# Source data — (name, long_name)
# Sourced from the original agencies table in backupFELA.py.
# long_name is None where the original had no value.
# ---------------------------------------------------------------------------
AGENCIES_DATA = [
    (
        'FIG',
        'Fédération Internationale des Géomètres'
    ),
    (
        'Un-GGIM (EG-LAM)',
        'United Nations Global Geospatial Information Management '
        '(Group of Experts on Land Administration and Management)'
    ),
    (
        'EuroSDR',
        'European Spatial Data Research'
    ),
    (
        'IGN France',
        "Institut National de l'Information Géographique et Forestière"
    ),
    (
        'UN-GGIM Europe',
        'Europe Regional Committee of the United Nations Committee on '
        'Global Geospatial Information Management'
    ),
    (
        'EuroGeographics',
        None
    ),
    (
        'ARA-LG',
        'Arab Academic Network for Land Governance'
    ),
    (
        'Arab Land Initiative',
        None
    ),
    (
        'SLAS',
        'School for Land Administration Studies'
    ),
    (
        'Kadaster',
        "The Netherlands' Cadastre, Land Registry and Mapping Agency"
    ),
    (
        'ITC Faculty University of Twente',
        'Faculty of Geo-information Sciences and Earth Observation '
        'at the University of Twente'
    ),
    (
        'School of Geomatic Sciences and Land Survey Engineering at '
        'Institut Agronomique et Vétérinaire Hassan II',
        None
    ),
    (
        'UFSC',
        'Universidade Federal de Santa Catarina'
    ),
    (
        'PCC',
        'Permanent Committee on Cadastre in the European Union'
    ),
    (
        'CLRKEN EuroGeographics',
        'EuroGeographics Cadastre and Land Registry Knowledge Exchange Network'
    ),
    (
        'UN-GGIM',
        'United Nations Global Geospatial Information Management'
    ),
    (
        'CPCI',
        'Comité Permanente del Catastro en Iberoamérica'
    ),
    (
        'GLTN',
        'Global Land Tool Network'
    ),
    (
        'Land Management Training Center of Government of Nepal',
        None
    ),
    (
        'UN-Habitat',
        'United Nations Human Settlements Programme'
    ),
    (
        'Kadaster International',
        None
    ),
    (
        'UN-GGIM Américas',
        'United Nations Regional Committee on Global Geospatial Information '
        'Management for the Americas'
    ),
    (
        'Geospatial World',
        None
    ),
]

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
created_count = 0
skipped_count = 0

for name, long_name in AGENCIES_DATA:
    agency, created = Agency.objects.get_or_create(
        name=name,
        defaults={'long_name': long_name}
    )
    if created:
        created_count += 1
        print(f"  [+] Created : {name}")
    else:
        skipped_count += 1
        print(f"  [=] Exists  : {name}")

print()
print(f"Done. Created: {created_count} | Skipped: {skipped_count} | "
      f"Total agencies: {Agency.objects.count()}")
