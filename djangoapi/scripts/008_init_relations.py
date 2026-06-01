"""
scripts/008_init_relations.py

Loads all many-to-many relations:
  1. EventAgency        — which agency(ies) organised each event
  2. PresentationSpeaker — which speaker(s) gave each presentation

Data sourced from the original backupFELA.py
(events_agencies and presentation_speakers tables).

Relations are resolved by natural keys (event_title, agency name,
presentation title, speaker name + country) instead of raw integer IDs,
so the load order of previous scripts does not affect this one as long as
all entities already exist.

Run AFTER:
  002_init_country.py
  003_init_city.py
  004_init_agency.py
  005_init_events.py
  006_init_speakers.py
  007_init_presentations.py

Run via:
    python manage.py shell < scripts/008_init_relations.py
"""
from FELA.models import (
    Event, Agency, EventAgency,
    Presentation, Speaker, Country, PresentationSpeaker
)

# ===========================================================================
# PART 1 — EventAgency relations
# ===========================================================================
# Each tuple: (event_title, agency_name)
# Derived from events_agencies table in backupFELA.py, replacing integer IDs
# with the natural keys used in the new model.
# ===========================================================================

EVENT_AGENCY_DATA = [
    # Event 1 — FIG Joint Land Administration Conference
    ('FIG Joint Land Administration Conference',
     'FIG'),

    # Event 2 — Unlocking FELA
    ('Unlocking FELA a global dialogue on land administration ',
     'Un-GGIM (EG-LAM)'),

    # Event 3 — International Workshop on challenges (FELA)
    ('International Workshop on challenges in relation to the UN Framework '
     'for Effective Land Administration (FELA)',
     'EuroSDR'),
    ('International Workshop on challenges in relation to the UN Framework '
     'for Effective Land Administration (FELA)',
     'IGN France'),
    ('International Workshop on challenges in relation to the UN Framework '
     'for Effective Land Administration (FELA)',
     'UN-GGIM Europe'),
    ('International Workshop on challenges in relation to the UN Framework '
     'for Effective Land Administration (FELA)',
     'EuroGeographics'),

    # Event 4 — Strengthening Academic Foundations
    ('Strengthening Academic Foundations in Land Governance: Online Lectures '
     'Hosted in Collaboration with Al-Quds and Duhok Universities',
     'ARA-LG'),
    ('Strengthening Academic Foundations in Land Governance: Online Lectures '
     'Hosted in Collaboration with Al-Quds and Duhok Universities',
     'Arab Land Initiative'),

    # Event 5 — Technical pre-workshop 3rd Arab Land Conference
    ('Technical pre-workshop 3rd Arab Land Conference '
     '"Fit-for-Purpose Land Administration in the Arab Region"',
     'SLAS'),
    ('Technical pre-workshop 3rd Arab Land Conference '
     '"Fit-for-Purpose Land Administration in the Arab Region"',
     'Kadaster'),
    ('Technical pre-workshop 3rd Arab Land Conference '
     '"Fit-for-Purpose Land Administration in the Arab Region"',
     'ITC Faculty University of Twente'),
    ('Technical pre-workshop 3rd Arab Land Conference '
     '"Fit-for-Purpose Land Administration in the Arab Region"',
     'School of Geomatic Sciences and Land Survey Engineering at '
     'Institut Agronomique et Vétérinaire Hassan II'),

    # Event 6 — COBRAC 2024
    ('Congress of Multifinalial Cadastre and Territorial Management '
     '– COBRAC 2024',
     'UFSC'),

    # Event 7 — FIG COMMISSION 5, 7 ANNUAL MEETING 2024
    ('FIG COMMISSION 5, 7 ANNUAL MEETING 2024 Framework for Effective Land '
     'Administration (WG7.1 FELA) + Fit for Purpose Land Administration '
     '(WG7.2 FFPLA)',
     'FIG'),

    # Event 8 — PCC
    ('Permanent Committee on Cadastre in the European Union (PCC)',
     'PCC'),
    ('Permanent Committee on Cadastre in the European Union (PCC)',
     'CLRKEN EuroGeographics'),

    # Event 9 — FIG Working Week 2024
    ('FIG Woorking Week 2024 - Land Policy Issues and Innovations',
     'FIG'),

    # Event 10 — Fifth EG-LAM meeting
    ('Fifth meeting of the Expert Group on Land Administration and '
     'Management and the International Seminar on UN-GGIM',
     'UN-GGIM'),
    ('Fifth meeting of the Expert Group on Land Administration and '
     'Management and the International Seminar on UN-GGIM',
     'CPCI'),

    # Event 11 — Nepal Workshop
    ('Effective Land Administration in Nepal: Navigating Governance, Legal, '
     'and Financial Pathways within the Climate Change – Land Nexus',
     'GLTN'),
    ('Effective Land Administration in Nepal: Navigating Governance, Legal, '
     'and Financial Pathways within the Climate Change – Land Nexus',
     'Land Management Training Center of Government of Nepal'),
    ('Effective Land Administration in Nepal: Navigating Governance, Legal, '
     'and Financial Pathways within the Climate Change – Land Nexus',
     'UN-Habitat'),
    ('Effective Land Administration in Nepal: Navigating Governance, Legal, '
     'and Financial Pathways within the Climate Change – Land Nexus',
     'Kadaster International'),

    # Event 12 — CPCI
    ('XIV Simposio y IX Asamblea del CPCI',
     'CPCI'),

    # Event 13 — UN-GGIM Americas X
    ('X session UN-GGIM : Americas ',
     'UN-GGIM Américas'),

    # Event 14 — FIG Meeting Digital Transformation
    ('FIG Meeting Digital Transformation for Responsible Land Administration',
     'FIG'),

    # Event 15 — FIG Working Week 2023
    ('FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
     'FIG'),

    # Event 16 — XXVII FIG Congress 2022
    ('XXVII FIG Congress - Volunteering for the Future Geospatial Excellence '
     'for a better living',
     'FIG'),

    # Event 17 — UN-GGIM Twelfth Session
    ('Twelfth Session of the United Nations Committee of Experts on Global '
     'Geospatial Information Management (UN-GGIM)',
     'UN-GGIM'),

    # Event 18 — Geospatial World Forum 2022
    ('Geospatial World Forum 2022, Symposium on Land Administration',
     'Geospatial World'),

    # Event 19 — Fourth EG-LAM meeting
    ('Fourth expert meeting of the Expert Group on Land Administration and '
     'Management and International Seminar on United Nations Global '
     'Geospatial Information Management',
     'UN-GGIM'),

    # Event 20 — EG-LAM Side Event (Eleventh Session)
    ('Expert Group on Land Administration and Management Side Event at the '
     'Eleventh Session of the Committee of Experts on Global Geospatial '
     'Information Management',
     'UN-GGIM'),

    # Event 21 — Tenth Session UN-GGIM
    ('Tenth Session of the United Nations Committee of Experts on Global '
     'Geospatial Information Management (UN-GGIM)',
     'UN-GGIM'),

    # Event 22 — Actual version FELA
    ('Actual version FELA',
     'UN-GGIM'),

    # Event 23 — Eighth Plenary UN-GGIM-AP
    ('Eighth Plenary Meeting of UN-GGIM-AP (Asia-Pacific)',
     'UN-GGIM'),

    # Event 24 — Ninth Session UN-GGIM
    ('Ninth Session of the United Nations Committee of Experts on Global '
     'Geospatial Information Management (UN-GGIM)',
     'UN-GGIM'),

    # Event 25 — Eighth Session UN-GGIM
    ('Eighth Session of the United Nations Committee of Experts on Global '
     'Geospatial Information Management (UN-GGIM)',
     'UN-GGIM'),
]


# ===========================================================================
# PART 2 — PresentationSpeaker relations
# ===========================================================================
# Each tuple: (presentation_title, event_title, speaker_name, speaker_country)
#
# presentation_title + event_title together uniquely identify the presentation.
# speaker_name + speaker_country uniquely identify the speaker.
#
# Source: presentation_speakers table in backupFELA.py, with integer IDs
# replaced by natural keys cross-referenced against presentations and speakers
# data loaded in previous scripts.
# ===========================================================================

PRESENTATION_SPEAKER_DATA = [
    # ── Presentation 1 (event 1) ───────────────────────────────────────────
    (
        'Claves del éxito del catastro español y sus retos para el Furturo '
        'con relación con el FELA',
        'FIG Joint Land Administration Conference',
        'Amalia Velasco', 'Spain'
    ),

    # ── Presentation 2 (event 2) ───────────────────────────────────────────
    (
        'FELA implementation experiences: Key achievement of FELA Principles '
        'in Sierra Leone',
        'Unlocking FELA a global dialogue on land administration ',
        'Jobo Samba', 'Sierra Leone'
    ),

    # ── Presentation 3 (event 2) ───────────────────────────────────────────
    (
        'FELA implementation experiences: El estado de la administracion de '
        'tierras en Mexico, una perspectiva registral y catastral desde el FELA ',
        'Unlocking FELA a global dialogue on land administration ',
        'Mario Cruz', 'Mexico'
    ),

    # ── Presentation 4 (event 2) ───────────────────────────────────────────
    (
        'FELA implementation experiences: Towards Effective Land Administration: '
        'Lessons For and From Nigeria',
        'Unlocking FELA a global dialogue on land administration ',
        'Israel Taiwo', 'Nigeria'
    ),

    # ── Presentation 5 (event 2) ───────────────────────────────────────────
    (
        'FELA implementation experiences: de SIT a SAT Orientaciones para '
        'integrar FELa en la provincia de Córdoba, Argentina ',
        'Unlocking FELA a global dialogue on land administration ',
        'Mario Piumetto', 'Argentina'
    ),

    # ── Presentation 6 (event 2) ───────────────────────────────────────────
    (
        'Tools for land administration: FELA implementation: French urban '
        'planning geoportal',
        'Unlocking FELA a global dialogue on land administration ',
        'Elisabeth Leblanc', 'France'
    ),

    # ── Presentation 7 (event 2) ───────────────────────────────────────────
    (
        'Tools for land administration: UN tools to implement FELA',
        'Unlocking FELA a global dialogue on land administration ',
        'Regina Orvananos', 'Mexico'
    ),

    # ── Presentation 8 (event 2) — two speakers ───────────────────────────
    (
        'FELA and effective land Administration ',
        'Unlocking FELA a global dialogue on land administration ',
        'Eva-Maria Unger', 'the Netherlands'
    ),
    (
        'FELA and effective land Administration ',
        'Unlocking FELA a global dialogue on land administration ',
        'Paula Dijkstra', 'the Netherlands'
    ),

    # ── Presentation 9 (event 3) ───────────────────────────────────────────
    (
        'UN-GGIM Expert Group on Land administration and Management',
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Raffaella Anilio Olguín', 'Chile'
    ),

    # ── Presentation 10 (event 3) ─────────────────────────────────────────
    (
        'Introduction to UN-GGIM Framework for Effective Land Administration '
        '(FELA)',
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Eva-Maria Unger', 'the Netherlands'
    ),

    # ── Presentation 11 (event 3) — two speakers ──────────────────────────
    (
        'Results of FELA surveys',
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Anka Lisec', 'Slovenia'
    ),
    (
        'Results of FELA surveys',
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Frédéric Cantat', 'France'
    ),

    # ── Presentation 12 (event 3) ─────────────────────────────────────────
    (
        'Effective land administration in the Netherlands',
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Christelle van den Berg', 'the Netherlands'
    ),

    # ── Presentation 13 (event 3) ─────────────────────────────────────────
    (
        'FELA implementation: French urban planning geoportal',
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Elisabeth Leblanc', 'France'
    ),

    # ── Presentation 14 (event 3) ─────────────────────────────────────────
    (
        'FELA implementation: feedback from Latvia',
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Vents Priedoliņš', 'Latvia'
    ),

    # ── Presentation 15 (event 3) — two speakers ──────────────────────────
    (
        'Making land information systems the cornerstone of FELA implementation '
        'in Africa',
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Aurélia Decherf', 'France'
    ),
    (
        'Making land information systems the cornerstone of FELA implementation '
        'in Africa',
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Jean-Philippe Lestang', 'France'
    ),

    # ── Presentation 16 (event 3) — two speakers ──────────────────────────
    (
        'Improving the usage of land administration data for education and '
        'capacity building',
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Bénédicte Bucher', 'France'
    ),
    (
        'Improving the usage of land administration data for education and '
        'capacity building',
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Romain Vialle', 'France'
    ),

    # ── Presentation 17 (event 3) — two speakers ──────────────────────────
    (
        'The use of GIS in FELA implementations',
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Kees de Zeeuw', 'the Netherlands'
    ),
    (
        'The use of GIS in FELA implementations',
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Nick Land', 'United Kingdom'
    ),

    # ── Presentation 18 (event 4) ─────────────────────────────────────────
    (
        'international frameworks and models',
        'Strengthening Academic Foundations in Land Governance: Online Lectures '
        'Hosted in Collaboration with Al-Quds and Duhok Universities',
        'Kholoud Saad Salama', 'Egypt'
    ),

    # ── Presentation 19 (event 5) ─────────────────────────────────────────
    (
        '-',
        'Technical pre-workshop 3rd Arab Land Conference '
        '"Fit-for-Purpose Land Administration in the Arab Region"',
        'Expert Group', '-'
    ),

    # ── Presentation 20 (event 6) — two speakers ──────────────────────────
    (
        'International and national frameworks that link the Multifinality '
        'Territorial Cadastre with the Sustainable Development Goals',
        'Congress of Multifinalial Cadastre and Territorial Management '
        '– COBRAC 2024',
        'Amalia Velasco', 'Spain'
    ),
    (
        'International and national frameworks that link the Multifinality '
        'Territorial Cadastre with the Sustainable Development Goals',
        'Congress of Multifinalial Cadastre and Territorial Management '
        '– COBRAC 2024',
        'Mario Piumetto', 'Argentina'
    ),

    # ── Presentation 21 (event 6 — COBRAC) ───────────────────────────────
    (
        'Where things are at with the FELA Working group ',
        'Congress of Multifinalial Cadastre and Territorial Management '
        '– COBRAC 2024',
        'Markus Koper', 'Germany'
    ),

    # ── Presentation 22 (event 7 — FIG Commission 2024) ──────────────────
    (
        'Fit-for-Purpose Land Administration Solutions from Trimble',
        'FIG COMMISSION 5, 7 ANNUAL MEETING 2024 Framework for Effective Land '
        'Administration (WG7.1 FELA) + Fit for Purpose Land Administration '
        '(WG7.2 FFPLA)',
        'Amalia Velasco', 'Spain'
    ),

    # ── Presentation 23 (event 7) — two speakers ──────────────────────────
    (
        'A prliminary UN-GGIM Work to integrate Land and Sea',
        'FIG COMMISSION 5, 7 ANNUAL MEETING 2024 Framework for Effective Land '
        'Administration (WG7.1 FELA) + Fit for Purpose Land Administration '
        '(WG7.2 FFPLA)',
        'Kean Huat Soon', 'Singapore'
    ),
    (
        'A prliminary UN-GGIM Work to integrate Land and Sea',
        'FIG COMMISSION 5, 7 ANNUAL MEETING 2024 Framework for Effective Land '
        'Administration (WG7.1 FELA) + Fit for Purpose Land Administration '
        '(WG7.2 FFPLA)',
        'Victor Khoo', 'Singapore'
    ),

    # ── Presentation 24 (event 7) ─────────────────────────────────────────
    (
        'From no Cadastre to 3D Cadastre: The evolving role of Spatially '
        'Enabled Framework',
        'FIG COMMISSION 5, 7 ANNUAL MEETING 2024 Framework for Effective Land '
        'Administration (WG7.1 FELA) + Fit for Purpose Land Administration '
        '(WG7.2 FFPLA)',
        'Israel Taiwo', 'Nigeria'
    ),

    # ── Presentation 25 (event 8 — PCC) — two speakers ────────────────────
    (
        'Framework for Effective Land Administration (FELA)',
        'Permanent Committee on Cadastre in the European Union (PCC)',
        'Amalia Velasco', 'Spain'
    ),
    (
        'Framework for Effective Land Administration (FELA)',
        'Permanent Committee on Cadastre in the European Union (PCC)',
        'Magdalena Andersson', 'Sweden'
    ),

    # ── Presentation 26 (event 9 — FIG WW 2024) — many speakers ──────────
    (
        'Framework for Effective Land Administration (FELA): Research Synthesis',
        'FIG Woorking Week 2024 - Land Policy Issues and Innovations',
        'Eva-Maria Unger', 'the Netherlands'
    ),
    (
        'Framework for Effective Land Administration (FELA): Research Synthesis',
        'FIG Woorking Week 2024 - Land Policy Issues and Innovations',
        'Amalia Velasco', 'Spain'
    ),
    (
        'Framework for Effective Land Administration (FELA): Research Synthesis',
        'FIG Woorking Week 2024 - Land Policy Issues and Innovations',
        'Joep Crompvoets', 'Belgium'
    ),
    (
        'Framework for Effective Land Administration (FELA): Research Synthesis',
        'FIG Woorking Week 2024 - Land Policy Issues and Innovations',
        'Rohan Bennett', 'Australia'
    ),

    # ── Presentation 27 (event 9) — three speakers ────────────────────────
    (
        'Exploring Technology Integration Through FELA in Nigeria',
        'FIG Woorking Week 2024 - Land Policy Issues and Innovations',
        'Kirsikka Riekkinen', 'Finland'
    ),
    (
        'Exploring Technology Integration Through FELA in Nigeria',
        'FIG Woorking Week 2024 - Land Policy Issues and Innovations',
        'Oluwafemi Adekola', 'Finland'
    ),
    (
        'Exploring Technology Integration Through FELA in Nigeria',
        'FIG Woorking Week 2024 - Land Policy Issues and Innovations',
        'Opeyemi Michael Ajayi', 'Finland'
    ),

    # ── Presentation 28 (event 9) — three speakers ────────────────────────
    (
        'Land Reforms and Implementation of the Framework for Effective Land '
        'Administration (FELA): a Case Study for Customary Land Registry '
        'Implementation in the Democratic Republic of Congo',
        'FIG Woorking Week 2024 - Land Policy Issues and Innovations',
        'Mamadou Mballo', 'Democratic Republic of Congo'
    ),
    (
        'Land Reforms and Implementation of the Framework for Effective Land '
        'Administration (FELA): a Case Study for Customary Land Registry '
        'Implementation in the Democratic Republic of Congo',
        'FIG Woorking Week 2024 - Land Policy Issues and Innovations',
        'Hellen Ndungu', 'Kenya'
    ),
    (
        'Land Reforms and Implementation of the Framework for Effective Land '
        'Administration (FELA): a Case Study for Customary Land Registry '
        'Implementation in the Democratic Republic of Congo',
        'FIG Woorking Week 2024 - Land Policy Issues and Innovations',
        'John Gitau', 'Kenya'
    ),

    # ── Presentation 29 (event 10 — Fifth EG-LAM) ────────────────────────
    (
        'Implementing the framework for effective land administration in Barbados',
        'Fifth meeting of the Expert Group on Land Administration and '
        'Management and the International Seminar on UN-GGIM',
        'Leandre Murrell-Forde', 'Barbados'
    ),

    # ── Presentation 30 (event 10) ────────────────────────────────────────
    (
        "Mexico's experiences in the implementation of FELA",
        'Fifth meeting of the Expert Group on Land Administration and '
        'Management and the International Seminar on UN-GGIM',
        'Claudio Martínez Topete', 'Mexico'
    ),

    # ── Presentation 31 (event 10) ────────────────────────────────────────
    (
        'How the implementation of the Framework for Effective Land '
        'Administration can assist cadastral institutions in Iberoamerica',
        'Fifth meeting of the Expert Group on Land Administration and '
        'Management and the International Seminar on UN-GGIM',
        'Amalia Velasco', 'Spain'
    ),

    # ── Presentation 32 (event 10) ────────────────────────────────────────
    (
        'Management of geospatial data and cadastral data in Chile, a pending '
        'challenge',
        'Fifth meeting of the Expert Group on Land Administration and '
        'Management and the International Seminar on UN-GGIM',
        'Raffaella Anilio Olguín', 'Chile'
    ),

    # ── Presentation 33 (event 10) ────────────────────────────────────────
    (
        'Key Elements of the Framework for Effective Land Management',
        'Fifth meeting of the Expert Group on Land Administration and '
        'Management and the International Seminar on UN-GGIM',
        'Ridomil Alejandro Rojas Ferreyra', 'Republica Dominicana'
    ),

    # ── Presentation 34 (event 10) ────────────────────────────────────────
    (
        'We know the earth-we secure the future',
        'Fifth meeting of the Expert Group on Land Administration and '
        'Management and the International Seminar on UN-GGIM',
        'Markku Markkula', 'Finland'
    ),

    # ── Presentation 35 (event 11 — Nepal) — many speakers ───────────────
    (
        '-',
        'Effective Land Administration in Nepal: Navigating Governance, Legal, '
        'and Financial Pathways within the Climate Change – Land Nexus',
        'Janak Raj Joshi', 'Nepal'
    ),
    (
        '-',
        'Effective Land Administration in Nepal: Navigating Governance, Legal, '
        'and Financial Pathways within the Climate Change – Land Nexus',
        'Ganesh Prasad Bhatta', 'Nepal'
    ),
    (
        '-',
        'Effective Land Administration in Nepal: Navigating Governance, Legal, '
        'and Financial Pathways within the Climate Change – Land Nexus',
        'Raja Ram Chhatkuli', 'Nepal'
    ),
    (
        '-',
        'Effective Land Administration in Nepal: Navigating Governance, Legal, '
        'and Financial Pathways within the Climate Change – Land Nexus',
        'Eva-Maria Unger', 'the Netherlands'
    ),
    (
        '-',
        'Effective Land Administration in Nepal: Navigating Governance, Legal, '
        'and Financial Pathways within the Climate Change – Land Nexus',
        'John Gitau', 'Kenya'
    ),

    # ── Presentation 36 (event 12 — CPCI) ────────────────────────────────
    (
        'Presentación de los trabajos realizados en 2023 por la Presidencia CPCI',
        'XIV Simposio y IX Asamblea del CPCI',
        'Amalia Velasco', 'Spain'
    ),

    # ── Presentation 37 (event 13 — UN-GGIM Americas X) ──────────────────
    (
        'Implementing the Framework for Effective Land Administration (FELA): '
        'New Workplan and Developments',
        'X session UN-GGIM : Americas ',
        'Raffaella Anilio Olguín', 'Chile'
    ),

    # ── Presentation 38 (event 14 — FIG Digital Transformation) ──────────
    (
        'Framework for efective land administration (WG7.1) Work plan 2023-2026',
        'FIG Meeting Digital Transformation for Responsible Land Administration',
        'Amalia Velasco', 'Spain'
    ),

    # ── Presentation 39 (event 15 — FIG WW 2023) — two speakers ──────────
    (
        'Implementing the Framework for Effective Land Administration (FELA): '
        'New Workplan and Developments',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Kean Huat Soon', 'Singapore'
    ),
    (
        'Implementing the Framework for Effective Land Administration (FELA): '
        'New Workplan and Developments',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Victor Khoo', 'Singapore'
    ),

    # ── Presentation 40 (event 15) ────────────────────────────────────────
    (
        'The UN-GGIM Integrated Geospatial Information Framework and the status '
        'of the High-Level Group of the IGIF',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Mikael Lilje', 'Sweden'
    ),

    # ── Presentation 41 (event 15) ────────────────────────────────────────
    (
        'Improved Land Management, a Key Factor for a Stable and Protective '
        'Social Economic Development',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Jean-Philippe Lestang', 'France'
    ),

    # ── Presentation 42 (event 15) ────────────────────────────────────────
    (
        'Land Registration for Conquering New SDG Frontiers',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Charisse Griffith-Charles', 'Trinidad And Tobago'
    ),

    # ── Presentation 43 (event 15) — three speakers ───────────────────────
    (
        'FELA-based Geospatial Knowledge Infrastructure',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Brandon Tourtelotte', 'USA'
    ),
    (
        'FELA-based Geospatial Knowledge Infrastructure',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Katie Pickett', 'USA'
    ),
    (
        'FELA-based Geospatial Knowledge Infrastructure',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Kees de Zeeuw', 'the Netherlands'
    ),

    # ── Presentation 44 (event 15) — many speakers ────────────────────────
    (
        'Fit-For-Purpose Land Administration and the Framework for Effective '
        'Land Administration in Chad',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Eva-Maria Unger', 'the Netherlands'
    ),
    (
        'Fit-For-Purpose Land Administration and the Framework for Effective '
        'Land Administration in Chad',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Rohan Bennett', 'Australia'
    ),
    (
        'Fit-For-Purpose Land Administration and the Framework for Effective '
        'Land Administration in Chad',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Mahamat Abdoulaye Malloum', 'Chad'
    ),
    (
        'Fit-For-Purpose Land Administration and the Framework for Effective '
        'Land Administration in Chad',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Claudia Stöcker', 'Germany'
    ),
    (
        'Fit-For-Purpose Land Administration and the Framework for Effective '
        'Land Administration in Chad',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Kaspar Kundert', 'Rwanda'
    ),
    (
        'Fit-For-Purpose Land Administration and the Framework for Effective '
        'Land Administration in Chad',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Dina Naguib', 'Egypt'
    ),
    (
        'Fit-For-Purpose Land Administration and the Framework for Effective '
        'Land Administration in Chad',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Markus Koper', 'Germany'
    ),
    (
        'Fit-For-Purpose Land Administration and the Framework for Effective '
        'Land Administration in Chad',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Divyani Kohli', 'the Netherlands'
    ),
    (
        'Fit-For-Purpose Land Administration and the Framework for Effective '
        'Land Administration in Chad',
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Mila Koeva', 'the Netherlands'
    ),

    # ── Presentation 45 (event 16 — XXVII FIG Congress) ──────────────────
    (
        'GIS in Land Administration Can Help You Implement the FELA and Support '
        "the SDG's",
        'XXVII FIG Congress - Volunteering for the Future Geospatial Excellence '
        'for a better living',
        'Brandon Tourtelotte', 'USA'
    ),

    # ── Presentation 46 (event 16) — many speakers ────────────────────────
    (
        'Digital Transformation of Land Administration: Stages, Status, and '
        'Solutions',
        'XXVII FIG Congress - Volunteering for the Future Geospatial Excellence '
        'for a better living',
        'Rohan Bennett', 'Australia'
    ),
    (
        'Digital Transformation of Land Administration: Stages, Status, and '
        'Solutions',
        'XXVII FIG Congress - Volunteering for the Future Geospatial Excellence '
        'for a better living',
        'Eva-Maria Unger', 'the Netherlands'
    ),
    (
        'Digital Transformation of Land Administration: Stages, Status, and '
        'Solutions',
        'XXVII FIG Congress - Volunteering for the Future Geospatial Excellence '
        'for a better living',
        'Vincent Verheij', 'the Netherlands'
    ),
    (
        'Digital Transformation of Land Administration: Stages, Status, and '
        'Solutions',
        'XXVII FIG Congress - Volunteering for the Future Geospatial Excellence '
        'for a better living',
        'Haico Van der Vegt', 'the Netherlands'
    ),
    (
        'Digital Transformation of Land Administration: Stages, Status, and '
        'Solutions',
        'XXVII FIG Congress - Volunteering for the Future Geospatial Excellence '
        'for a better living',
        'Suren Tovmasyan', 'Armenia'
    ),
    (
        'Digital Transformation of Land Administration: Stages, Status, and '
        'Solutions',
        'XXVII FIG Congress - Volunteering for the Future Geospatial Excellence '
        'for a better living',
        'Indra Hutabarat', 'Indonesia'
    ),
    (
        'Digital Transformation of Land Administration: Stages, Status, and '
        'Solutions',
        'XXVII FIG Congress - Volunteering for the Future Geospatial Excellence '
        'for a better living',
        'Aram Gugarats', 'Armenia'
    ),
    (
        'Digital Transformation of Land Administration: Stages, Status, and '
        'Solutions',
        'XXVII FIG Congress - Volunteering for the Future Geospatial Excellence '
        'for a better living',
        'Aulia Latif', 'Indonesia'
    ),
    (
        'Digital Transformation of Land Administration: Stages, Status, and '
        'Solutions',
        'XXVII FIG Congress - Volunteering for the Future Geospatial Excellence '
        'for a better living',
        'Chalemyan Trdat', 'Armenia'
    ),

    # ── Presentation 47 (event 17 — Twelfth Session UN-GGIM) ─────────────
    (
        'Application of geospatial information related to land administration '
        'and management ',
        'Twelfth Session of the United Nations Committee of Experts on Global '
        'Geospatial Information Management (UN-GGIM)',
        'Committee of Experts on Global Geospatial Information Management', '-'
    ),

    # ── Presentation 48 (event 18 — Geospatial World Forum 2022) ─────────
    (
        'Modern Land Administration, Innovation and Investment for Sustainable '
        'Development',
        'Geospatial World Forum 2022, Symposium on Land Administration',
        'Brent Jones', 'USA'
    ),

    # ── Presentation 49 (event 19 — Fourth EG-LAM) ───────────────────────
    (
        'Framework for Effective Land Administration (FELA)',
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management',
        'Kees de Zeeuw', 'the Netherlands'
    ),

    # ── Presentation 50 (event 19) ────────────────────────────────────────
    (
        'Effective Land Administration - Digitally-Enabled Urban Planning in '
        'Singapore',
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management',
        'Ching Tuan Yee', 'Singapore'
    ),

    # ── Presentation 51 (event 19) ────────────────────────────────────────
    (
        "Enhancing Land Administration in Fiji through the IGIF and It's "
        'Country Action Plan',
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management',
        'Meizyanne Hicks', 'Fiji'
    ),

    # ── Presentation 52 (event 19) — four speakers ────────────────────────
    (
        'Progress Report on the Revision of the Land Administration Domain '
        'Model (LADM)',
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management',
        'Chris Body', 'Australia'
    ),
    (
        'Progress Report on the Revision of the Land Administration Domain '
        'Model (LADM)',
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management',
        'Christiaan Lemmen', 'the Netherlands'
    ),
    (
        'Progress Report on the Revision of the Land Administration Domain '
        'Model (LADM)',
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management',
        'Abdullah Kara', '-'
    ),
    (
        'Progress Report on the Revision of the Land Administration Domain '
        'Model (LADM)',
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management',
        'Peter van Oosterom', 'the Netherlands'
    ),

    # ── Presentation 53 (event 19) ────────────────────────────────────────
    (
        'Road Map to Implement the Framework for Effective Land Administration '
        'System in Sri Lanka',
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management',
        'Mohamed Rafeek', 'Sri Lanka'
    ),

    # ── Presentation 54 (event 19) ────────────────────────────────────────
    (
        'Leveraging FELA, Sharing Experiences from the Netherlands and Abroad',
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management',
        'Paula Dijkstra', 'the Netherlands'
    ),

    # ── Presentation 55 (event 19) ────────────────────────────────────────
    (
        'Implementing the Framework for Effective Land Administration (FELA)',
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management',
        'Eva-Maria Unger', 'the Netherlands'
    ),

    # ── Presentation 56 (event 20 — EG-LAM Side Event) — many speakers ───
    (
        'Framework for Effective Land Administration: -Implementation of the '
        'FELA, -FELA: Spanish, Arabic, Chinese, -Mexico\'s experience in the '
        'implementation of FELA',
        'Expert Group on Land Administration and Management Side Event at the '
        'Eleventh Session of the Committee of Experts on Global Geospatial '
        'Information Management',
        'Kees de Zeeuw', 'the Netherlands'
    ),
    (
        'Framework for Effective Land Administration: -Implementation of the '
        'FELA, -FELA: Spanish, Arabic, Chinese, -Mexico\'s experience in the '
        'implementation of FELA',
        'Expert Group on Land Administration and Management Side Event at the '
        'Eleventh Session of the Committee of Experts on Global Geospatial '
        'Information Management',
        'Ingrid van de Berghe', 'Belgium'
    ),
    (
        'Framework for Effective Land Administration: -Implementation of the '
        'FELA, -FELA: Spanish, Arabic, Chinese, -Mexico\'s experience in the '
        'implementation of FELA',
        'Expert Group on Land Administration and Management Side Event at the '
        'Eleventh Session of the Committee of Experts on Global Geospatial '
        'Information Management',
        'Eva-Maria Unger', 'the Netherlands'
    ),
    (
        'Framework for Effective Land Administration: -Implementation of the '
        'FELA, -FELA: Spanish, Arabic, Chinese, -Mexico\'s experience in the '
        'implementation of FELA',
        'Expert Group on Land Administration and Management Side Event at the '
        'Eleventh Session of the Committee of Experts on Global Geospatial '
        'Information Management',
        'Rohan Bennett', 'Australia'
    ),
    (
        'Framework for Effective Land Administration: -Implementation of the '
        'FELA, -FELA: Spanish, Arabic, Chinese, -Mexico\'s experience in the '
        'implementation of FELA',
        'Expert Group on Land Administration and Management Side Event at the '
        'Eleventh Session of the Committee of Experts on Global Geospatial '
        'Information Management',
        'Claudio Martínez Topete', 'Mexico'
    ),
    (
        'Framework for Effective Land Administration: -Implementation of the '
        'FELA, -FELA: Spanish, Arabic, Chinese, -Mexico\'s experience in the '
        'implementation of FELA',
        'Expert Group on Land Administration and Management Side Event at the '
        'Eleventh Session of the Committee of Experts on Global Geospatial '
        'Information Management',
        'Cristian Araneda Hernandez', 'Chile'
    ),
    (
        'Framework for Effective Land Administration: -Implementation of the '
        'FELA, -FELA: Spanish, Arabic, Chinese, -Mexico\'s experience in the '
        'implementation of FELA',
        'Expert Group on Land Administration and Management Side Event at the '
        'Eleventh Session of the Committee of Experts on Global Geospatial '
        'Information Management',
        'Ali Alawaji', 'Kingdom of Saudi Arabia'
    ),
    (
        'Framework for Effective Land Administration: -Implementation of the '
        'FELA, -FELA: Spanish, Arabic, Chinese, -Mexico\'s experience in the '
        'implementation of FELA',
        'Expert Group on Land Administration and Management Side Event at the '
        'Eleventh Session of the Committee of Experts on Global Geospatial '
        'Information Management',
        'Liao Rong', 'China'
    ),
    (
        'Framework for Effective Land Administration: -Implementation of the '
        'FELA, -FELA: Spanish, Arabic, Chinese, -Mexico\'s experience in the '
        'implementation of FELA',
        'Expert Group on Land Administration and Management Side Event at the '
        'Eleventh Session of the Committee of Experts on Global Geospatial '
        'Information Management',
        'Liu Yong', 'China'
    ),
    (
        'Framework for Effective Land Administration: -Implementation of the '
        'FELA, -FELA: Spanish, Arabic, Chinese, -Mexico\'s experience in the '
        'implementation of FELA',
        'Expert Group on Land Administration and Management Side Event at the '
        'Eleventh Session of the Committee of Experts on Global Geospatial '
        'Information Management',
        'Zhong Taiyang', 'China'
    ),

    # ── Presentation 57 (event 21 — Tenth Session UN-GGIM) ───────────────
    (
        'Application of geospatial information related to land administration '
        'and management ',
        'Tenth Session of the United Nations Committee of Experts on Global '
        'Geospatial Information Management (UN-GGIM)',
        'Committee of Experts on Global Geospatial Information Management', '-'
    ),

    # ── Presentation 58 (event 22 — Actual version FELA) ─────────────────
    (
        '-',
        'Actual version FELA',
        'Committee of Experts on Global Geospatial Information Management', '-'
    ),

    # ── Presentation 59 (event 23 — Eighth Plenary UN-GGIM-AP) ──── many ─
    (
        'Report from UN-GGIM Expert Group on Land Administration and Management '
        '(within Session 6: Working Group 2 on Cadastre and Land Management)',
        'Eighth Plenary Meeting of UN-GGIM-AP (Asia-Pacific)',
        'Kees de Zeeuw', 'the Netherlands'
    ),
    (
        'Report from UN-GGIM Expert Group on Land Administration and Management '
        '(within Session 6: Working Group 2 on Cadastre and Land Management)',
        'Eighth Plenary Meeting of UN-GGIM-AP (Asia-Pacific)',
        'Trevor Benn', '-'
    ),
    (
        'Report from UN-GGIM Expert Group on Land Administration and Management '
        '(within Session 6: Working Group 2 on Cadastre and Land Management)',
        'Eighth Plenary Meeting of UN-GGIM-AP (Asia-Pacific)',
        'Teo Chee Hai', '-'
    ),
    (
        'Report from UN-GGIM Expert Group on Land Administration and Management '
        '(within Session 6: Working Group 2 on Cadastre and Land Management)',
        'Eighth Plenary Meeting of UN-GGIM-AP (Asia-Pacific)',
        'Rohan Bennett', 'Australia'
    ),
    (
        'Report from UN-GGIM Expert Group on Land Administration and Management '
        '(within Session 6: Working Group 2 on Cadastre and Land Management)',
        'Eighth Plenary Meeting of UN-GGIM-AP (Asia-Pacific)',
        'Eva-Maria Unger', 'the Netherlands'
    ),

    # ── Presentation 60 (event 24 — Ninth Session UN-GGIM) ───────────────
    (
        'Application of geospatial information related to land administration '
        'and management ',
        'Ninth Session of the United Nations Committee of Experts on Global '
        'Geospatial Information Management (UN-GGIM)',
        'Committee of Experts on Global Geospatial Information Management', '-'
    ),

    # ── Presentation 61 (event 25 — Eighth Session UN-GGIM) ──────────────
    (
        'Application of geospatial information related to land administration '
        'and management ',
        'Eighth Session of the United Nations Committee of Experts on Global '
        'Geospatial Information Management (UN-GGIM)',
        'Committee of Experts on Global Geospatial Information Management', '-'
    ),
]


# ===========================================================================
# HELPERS
# ===========================================================================

def _get_presentation(pres_title, event_title):
    """Resolves a Presentation by title + event_title (strip-safe)."""
    event = Event.objects.filter(event_title=event_title).first()
    if not event:
        event = Event.objects.filter(event_title=event_title.strip()).first()
    if not event:
        return None, f"Event not found: '{event_title[:60]}'"

    pres = Presentation.objects.filter(title=pres_title, event=event).first()
    if not pres:
        return None, f"Presentation not found: '{pres_title[:60]}'"
    return pres, None


def _get_speaker(name, country_name):
    """Resolves a Speaker by name + country."""
    country = Country.objects.filter(country__iexact=country_name).first()
    if not country:
        return None, f"Country not found: '{country_name}'"
    speaker = Speaker.objects.filter(name=name, country=country).first()
    if not speaker:
        return None, f"Speaker not found: '{name}' ({country_name})"
    return speaker, None


# ===========================================================================
# LOAD — Part 1: EventAgency
# ===========================================================================

print("=" * 60)
print("PART 1 — EventAgency relations")
print("=" * 60)

ea_created = 0
ea_skipped = 0
ea_errors  = 0

for event_title, agency_name in EVENT_AGENCY_DATA:
    event = Event.objects.filter(event_title=event_title).first()
    if not event:
        event = Event.objects.filter(event_title=event_title.strip()).first()
    if not event:
        print(f"  [!] ERROR — Event not found: '{event_title[:60]}'")
        ea_errors += 1
        continue

    agency = Agency.objects.filter(name__iexact=agency_name).first()
    if not agency:
        print(f"  [!] ERROR — Agency not found: '{agency_name}'")
        ea_errors += 1
        continue

    relation, created = EventAgency.objects.get_or_create(
        event=event,
        agency=agency
    )
    if created:
        ea_created += 1
        print(f"  [+] {event.event_title[:50]}  ←→  {agency.name}")
    else:
        ea_skipped += 1

print()
print(f"EventAgency — Created: {ea_created} | Skipped: {ea_skipped} | "
      f"Errors: {ea_errors} | Total: {EventAgency.objects.count()}")


# ===========================================================================
# LOAD — Part 2: PresentationSpeaker
# ===========================================================================

print()
print("=" * 60)
print("PART 2 — PresentationSpeaker relations")
print("=" * 60)

ps_created = 0
ps_skipped = 0
ps_errors  = 0

for pres_title, event_title, speaker_name, speaker_country in PRESENTATION_SPEAKER_DATA:

    presentation, err = _get_presentation(pres_title, event_title)
    if err:
        print(f"  [!] ERROR — {err}")
        ps_errors += 1
        continue

    speaker, err = _get_speaker(speaker_name, speaker_country)
    if err:
        print(f"  [!] ERROR — {err}")
        ps_errors += 1
        continue

    relation, created = PresentationSpeaker.objects.get_or_create(
        presentation=presentation,
        speaker=speaker
    )
    if created:
        ps_created += 1
        print(f"  [+] {speaker_name}  →  {pres_title[:55]}")
    else:
        ps_skipped += 1

print()
print(f"PresentationSpeaker — Created: {ps_created} | Skipped: {ps_skipped} | "
      f"Errors: {ps_errors} | Total: {PresentationSpeaker.objects.count()}")

print()
print("=" * 60)
print("All relations loaded.")
print("=" * 60)
