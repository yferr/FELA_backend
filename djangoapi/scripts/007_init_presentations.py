"""
scripts/007_init_presentations.py

Loads initial Presentation data into the events"."presentation table.
Data sourced from the original backupFELA.py (presentations table).

Each presentation references an Event by its exact event_title.
Run AFTER 005_init_events.py.

NOTES:
  - The original language field was a single VARCHAR.
    In the new model it is an ArrayField of VARCHAR.
    Values like 'Inglés' and 'Español' are stored as ['Inglés'] and ['Español'].
    Multi-language values like 'Inglés, Español' are split into ['Inglés', 'Español'].
  - The original presentations table linked to events via event_title text.
    The new model uses a ForeignKey to Event.id resolved by event_title lookup.

Run via:
    python manage.py shell < scripts/007_init_presentations.py
"""
from FELA.models import Event, Presentation


def _parse_language(raw):
    """
    Converts the original single-string language field into a list.
    Example: 'Inglés, Español'  →  ['Inglés', 'Español']
             'Inglés'           →  ['Inglés']
             None / ''          →  []
    """
    if not raw:
        return []
    return [lang.strip() for lang in raw.split(',') if lang.strip()]


# ---------------------------------------------------------------------------
# Source data
# Tuple: (event_title, presentation_title, language_raw, url_document, observations)
# event_title must match exactly (or very close) to Event.event_title in DB.
# ---------------------------------------------------------------------------
PRESENTATIONS_DATA = [
    # ── Event 1: FIG Joint Land Administration Conference ──────────────────
    (
        'FIG Joint Land Administration Conference',
        'Claves del éxito del catastro español y sus retos para el Furturo '
        'con relación con el FELA',
        'Español', None, None
    ),

    # ── Event 2: Unlocking FELA ────────────────────────────────────────────
    (
        'Unlocking FELA a global dialogue on land administration ',
        'FELA implementation experiences: Key achievement of FELA Principles '
        'in Sierra Leone',
        'Inglés', None, None
    ),
    (
        'Unlocking FELA a global dialogue on land administration ',
        'FELA implementation experiences: El estado de la administracion de '
        'tierras en Mexico, una perspectiva registral y catastral desde el FELA ',
        'Español', None,
        'Analisis basado en los resultados del Censo Nacional de Gobiernos '
        'Estatales 2025'
    ),
    (
        'Unlocking FELA a global dialogue on land administration ',
        'FELA implementation experiences: Towards Effective Land Administration: '
        'Lessons For and From Nigeria',
        'Inglés', None,
        'FELA progress across States in Nigeria'
    ),
    (
        'Unlocking FELA a global dialogue on land administration ',
        'FELA implementation experiences: de SIT a SAT Orientaciones para '
        'integrar FELa en la provincia de Córdoba, Argentina ',
        'Español', None,
        'Modernizar el SIT y mejorar la administracion territorial provincial, '
        'integrando municipios y comunas '
    ),
    (
        'Unlocking FELA a global dialogue on land administration ',
        'Tools for land administration: FELA implementation: French urban '
        'planning geoportal',
        'Inglés', None, None
    ),
    (
        'Unlocking FELA a global dialogue on land administration ',
        'Tools for land administration: UN tools to implement FELA',
        'Español', None,
        'Herramientas de las UN que pueden ser usadas para la implementacion '
        'de FELA (GLTN)'
    ),
    (
        'Unlocking FELA a global dialogue on land administration ',
        'FELA and effective land Administration ',
        'Inglés', None, None
    ),

    # ── Event 3: International Workshop on challenges (FELA) ───────────────
    (
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'UN-GGIM Expert Group on Land administration and Management',
        'Inglés',
        'https://www.eurosdr.net/sites/default/files/images/inline/'
        'eurosdr_fela_paris_keynote-presentation.pdf',
        None
    ),
    (
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Introduction to UN-GGIM Framework for Effective Land Administration (FELA)',
        'Inglés',
        'https://www.eurosdr.net/sites/default/files/images/inline/'
        'eurosdr_fela_paris_intro-to-the_fela.pdf',
        None
    ),
    (
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Results of FELA surveys',
        'Inglés',
        'https://www.eurosdr.net/sites/default/files/images/inline/'
        'eurosdr_fela_paris_survey-results.pdf',
        None
    ),
    (
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Effective land administration in the Netherlands',
        'Inglés', None, None
    ),
    (
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'FELA implementation: French urban planning geoportal',
        'Inglés',
        'https://www.eurosdr.net/sites/default/files/images/inline/'
        'eurosdr_fela_french_urban_planning_geoportal.pdf',
        None
    ),
    (
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'FELA implementation: feedback from Latvia',
        'Inglés',
        'https://www.eurosdr.net/sites/default/files/images/inline/'
        'eurosdr_fela_implementation_feedbacks-from-latvia.pdf',
        None
    ),
    (
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Making land information systems the cornerstone of FELA implementation '
        'in Africa',
        'Inglés',
        'https://www.eurosdr.net/sites/default/files/images/inline/'
        'eurosdr_fela_lis-in-africa_feedbacks-from-ignfi.pdf',
        None
    ),
    (
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'Improving the usage of land administration data for education and '
        'capacity building',
        'Inglés',
        'https://www.eurosdr.net/sites/default/files/images/inline/'
        'eurosdr_fela_education-capacity-building.pdf',
        None
    ),
    (
        'International Workshop on challenges in relation to the UN Framework '
        'for Effective Land Administration (FELA)',
        'The use of GIS in FELA implementations',
        'Inglés',
        'https://www.eurosdr.net/sites/default/files/images/inline/'
        'eurosdr_fela_use-of-gis_esri.pdf',
        None
    ),

    # ── Event 4: Strengthening Academic Foundations ────────────────────────
    (
        'Strengthening Academic Foundations in Land Governance: Online Lectures '
        'Hosted in Collaboration with Al-Quds and Duhok Universities',
        'international frameworks and models',
        'Inglés',
        'https://arablandinitiative.gltn.net/media/news/'
        'strengthening-academic-foundations-in-land-governance-online-lectures-'
        'hosted-in-collaboration-with',
        None
    ),

    # ── Event 5: Technical pre-workshop 3rd Arab Land Conference ───────────
    (
        'Technical pre-workshop 3rd Arab Land Conference '
        '"Fit-for-Purpose Land Administration in the Arab Region"',
        '-',
        'Inglés, Arábico',
        'https://arablandinitiative.gltn.net/media/events/'
        'technical-pre-workshop-fit-for-purpose-land-administration-in-the-'
        'arab-region',
        None
    ),

    # ── Event 6: COBRAC 2024 ───────────────────────────────────────────────
    (
        'Congress of Multifinalial Cadastre and Territorial Management '
        '– COBRAC 2024',
        'International and national frameworks that link the Multifinality '
        'Territorial Cadastre with the Sustainable Development Goals',
        'Inglés',
        'https://cobrac.ufsc.br/es/programacao/',
        None
    ),
    (
        'Congress of Multifinalial Cadastre and Territorial Management '
        '– COBRAC 2024',
        'Where things are at with the FELA Working group ',
        'Inglés',
        'https://fig.net/resources/proceedings/fig_proceedings/7_2024/papers/'
        'ts02/TS02_velasco_12940_abs.pdf',
        None
    ),

    # ── Event 7: FIG COMMISSION 5, 7 ANNUAL MEETING 2024 ──────────────────
    (
        'FIG COMMISSION 5, 7 ANNUAL MEETING 2024 Framework for Effective Land '
        'Administration (WG7.1 FELA) + Fit for Purpose Land Administration '
        '(WG7.2 FFPLA)',
        'Fit-for-Purpose Land Administration Solutions from Trimble',
        'Inglés',
        'https://fig.net/resources/proceedings/fig_proceedings/7_2024/papers/'
        'ts02/TS02_koper_12946_abs.pdf',
        None
    ),
    (
        'FIG COMMISSION 5, 7 ANNUAL MEETING 2024 Framework for Effective Land '
        'Administration (WG7.1 FELA) + Fit for Purpose Land Administration '
        '(WG7.2 FFPLA)',
        'A prliminary UN-GGIM Work to integrate Land and Sea',
        'Inglés',
        'https://fig.net/resources/proceedings/fig_proceedings/7_2024/papers/'
        'ts02/TS02_soon_khoo_12866.pdf',
        None
    ),
    (
        'FIG COMMISSION 5, 7 ANNUAL MEETING 2024 Framework for Effective Land '
        'Administration (WG7.1 FELA) + Fit for Purpose Land Administration '
        '(WG7.2 FFPLA)',
        'From no Cadastre to 3D Cadastre: The evolving role of Spatially '
        'Enabled Framework',
        'Inglés',
        'https://fig.net/resources/proceedings/fig_proceedings/7_2024/papers/'
        'ts02/TS02_taiwo_12871_abs.pdf',
        None
    ),

    # ── Event 8: PCC ───────────────────────────────────────────────────────
    (
        'Permanent Committee on Cadastre in the European Union (PCC)',
        'Framework for Effective Land Administration (FELA)',
        'Inglés',
        'https://eurogeographics.org/app/uploads/2024/03/'
        'PPT-20-Magdalena-and-Amalia-Framework-for-effective-land-'
        'administration-FELA-in-PCC2024-1.pdf',
        None
    ),

    # ── Event 9: FIG Working Week 2024 ────────────────────────────────────
    (
        'FIG Woorking Week 2024 - Land Policy Issues and Innovations',
        'Framework for Effective Land Administration (FELA): Research Synthesis',
        'Inglés',
        'https://www.fig.net/resources/proceedings/fig_proceedings/fig2024/ppt/'
        'ts11g/TS11G_unger_valesco_et_al_12697_ppt.pdf',
        None
    ),
    (
        'FIG Woorking Week 2024 - Land Policy Issues and Innovations',
        'Exploring Technology Integration Through FELA in Nigeria',
        'Inglés',
        'https://www.fig.net/resources/proceedings/fig_proceedings/fig2024/ppt/'
        'ts11g/TS11G_ajayi_riekkinen_et_al_12501_ppt.pdf',
        None
    ),
    (
        'FIG Woorking Week 2024 - Land Policy Issues and Innovations',
        'Land Reforms and Implementation of the Framework for Effective Land '
        'Administration (FELA): a Case Study for Customary Land Registry '
        'Implementation in the Democratic Republic of Congo',
        'Inglés',
        'https://www.fig.net/resources/proceedings/fig_proceedings/fig2024/ppt/'
        'ts11g/TS11G_mballo_vutegha_et_al_12510_ppt.pdf',
        None
    ),

    # ── Event 10: Fifth EG-LAM meeting ────────────────────────────────────
    (
        'Fifth meeting of the Expert Group on Land Administration and '
        'Management and the International Seminar on UN-GGIM',
        'Implementing the framework for effective land administration in Barbados',
        'Inglés',
        'https://ggim.un.org/meetings/2024/Fifth-EG-LAM/documents/'
        '2.1_Leandre_Murrel-Forde.pdf',
        None
    ),
    (
        'Fifth meeting of the Expert Group on Land Administration and '
        'Management and the International Seminar on UN-GGIM',
        "Mexico's experiences in the implementation of FELA",
        'Inglés',
        'https://ggim.un.org/meetings/2024/Fifth-EG-LAM/documents/'
        '2.3_Claudio_Topete.pdf',
        None
    ),
    (
        'Fifth meeting of the Expert Group on Land Administration and '
        'Management and the International Seminar on UN-GGIM',
        'How the implementation of the Framework for Effective Land '
        'Administration can assist cadastral institutions in Iberoamerica',
        'Inglés, Español',
        'https://ggim.un.org/meetings/2024/Fifth-EG-LAM/documents/'
        '5.1_Amalia_Velasco.pdf',
        None
    ),
    (
        'Fifth meeting of the Expert Group on Land Administration and '
        'Management and the International Seminar on UN-GGIM',
        'Management of geospatial data and cadastral data in Chile, a pending '
        'challenge',
        'Inglés',
        'https://ggim.un.org/meetings/2024/Fifth-EG-LAM/documents/'
        '2.2._Raffaella_Olguin.pdf',
        None
    ),
    (
        'Fifth meeting of the Expert Group on Land Administration and '
        'Management and the International Seminar on UN-GGIM',
        'Key Elements of the Framework for Effective Land Management',
        'Inglés',
        'https://ggim.un.org/meetings/2024/Fifth-EG-LAM/documents/'
        '3.1._Ridomil_Alejandro.pdf',
        None
    ),
    (
        'Fifth meeting of the Expert Group on Land Administration and '
        'Management and the International Seminar on UN-GGIM',
        'We know the earth-we secure the future',
        'Inglés',
        'https://ggim.un.org/meetings/2024/Fifth-EG-LAM/documents/'
        '3.2._Markku_Markkula.pdf',
        None
    ),

    # ── Event 11: Nepal Workshop ───────────────────────────────────────────
    (
        'Effective Land Administration in Nepal: Navigating Governance, Legal, '
        'and Financial Pathways within the Climate Change – Land Nexus',
        '-',
        'Inglés',
        'https://www.kadaster.com/-/strengthening-land-administration-in-nepal-'
        'amidst-climate-change?redirect=%2Fabout-us%2Fnews',
        None
    ),

    # ── Event 12: CPCI ────────────────────────────────────────────────────
    (
        'XIV Simposio y IX Asamblea del CPCI',
        'Presentación de los trabajos realizados en 2023 por la Presidencia CPCI',
        'Español',
        'http://www.catastrolatino.org/documentos/2023/XIV%20congreso%20Chile/'
        'CPCIActaAsambleaChile2023%20def[21726].pdf',
        None
    ),

    # ── Event 13: UN-GGIM Americas X ──────────────────────────────────────
    (
        'X session UN-GGIM : Americas ',
        'Implementing the Framework for Effective Land Administration (FELA): '
        'New Workplan and Developments',
        'Inglés',
        'https://www.cepal.org/sites/default/files/presentations/'
        'framework-effective-land-administration-fela-chile-oct2023.pdf',
        None
    ),

    # ── Event 14: FIG Meeting Digital Transformation ──────────────────────
    (
        'FIG Meeting Digital Transformation for Responsible Land Administration',
        'Framework for efective land administration (WG7.1) Work plan 2023-2026',
        'Inglés',
        'https://www.fig.net/resources/proceedings/fig_proceedings/7_2023/'
        'papers/se01/SE01_velasco_velasco_12338_abs.pdf',
        None
    ),

    # ── Event 15: FIG Working Week 2023 ───────────────────────────────────
    (
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Implementing the Framework for Effective Land Administration (FELA): '
        'New Workplan and Developments',
        'Inglés',
        'https://fig.net/resources/proceedings/fig_proceedings/fig2023/ppt/'
        'ts01i/TS01I_soon_khoo_12061_ppt.pdf',
        None
    ),
    (
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'The UN-GGIM Integrated Geospatial Information Framework and the status '
        'of the High-Level Group of the IGIF',
        'Inglés',
        'https://fig.net/resources/proceedings/fig_proceedings/fig2023/ppt/'
        'ts01i/TS01I_lilje_11937_ppt.pdf',
        None
    ),
    (
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Improved Land Management, a Key Factor for a Stable and Protective '
        'Social Economic Development',
        'Inglés',
        'https://fig.net/resources/proceedings/fig_proceedings/fig2023/papers/'
        'ts01i/TS01I_lestang_12041.pdf',
        None
    ),
    (
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Land Registration for Conquering New SDG Frontiers',
        'Inglés',
        'https://fig.net/resources/proceedings/fig_proceedings/fig2023/ppt/'
        'ts01i/TS01I_griffith-charles_12099_ppt.pdf',
        None
    ),
    (
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'FELA-based Geospatial Knowledge Infrastructure',
        'Inglés',
        'https://fig.net/resources/proceedings/fig_proceedings/fig2023/ppt/'
        'ts01i/TS01I_tourtelotte_pickett_et_al_12127_ppt.pdf',
        None
    ),
    (
        'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers',
        'Fit-For-Purpose Land Administration and the Framework for Effective '
        'Land Administration in Chad',
        'Inglés',
        'https://fig.net/resources/proceedings/fig_proceedings/fig2023/ppt/'
        'ts01i/TS01I_unger_bennett_et_al_12242_ppt.pdf',
        None
    ),

    # ── Event 16: XXVII FIG Congress 2022 ─────────────────────────────────
    (
        'XXVII FIG Congress - Volunteering for the Future Geospatial Excellence '
        'for a better living',
        'GIS in Land Administration Can Help You Implement the FELA and Support '
        "the SDG's",
        'Inglés',
        'https://www.fig.net/resources/proceedings/fig_proceedings/fig2022/'
        'papers/ts02a/TS02A_tourtelotte_11559.pdf',
        None
    ),
    (
        'XXVII FIG Congress - Volunteering for the Future Geospatial Excellence '
        'for a better living',
        'Digital Transformation of Land Administration: Stages, Status, and '
        'Solutions',
        'Inglés',
        'https://www.fig.net/resources/proceedings/fig_proceedings/fig2022/'
        'papers/ts04b/TS04B_bennett_unger_et_al_11482.pdf',
        None
    ),

    # ── Event 17: UN-GGIM Twelfth Session ─────────────────────────────────
    (
        'Twelfth Session of the United Nations Committee of Experts on Global '
        'Geospatial Information Management (UN-GGIM)',
        'Application of geospatial information related to land administration '
        'and management ',
        'Inglés',
        'https://ggim.un.org/meetings/GGIM-committee/12th-Session/documents/'
        'E-C.20_2022_13_Add_1_Land_Administration_and_Management.pdf',
        'FELA translation into French and Dutch'
    ),

    # ── Event 18: Geospatial World Forum 2022 ─────────────────────────────
    (
        'Geospatial World Forum 2022, Symposium on Land Administration',
        'Modern Land Administration, Innovation and Investment for Sustainable '
        'Development',
        'Inglés', None, None
    ),

    # ── Event 19: Fourth EG-LAM meeting ───────────────────────────────────
    (
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management',
        'Framework for Effective Land Administration (FELA)',
        'Inglés',
        'https://ggim.un.org/meetings/2022/4th-EG-LAM/documents/'
        '1.3_Kees_de_Zeeuw.pdf',
        None
    ),
    (
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management',
        'Effective Land Administration - Digitally-Enabled Urban Planning in '
        'Singapore',
        'Inglés',
        'https://ggim.un.org/meetings/2022/4th-EG-LAM/documents/'
        '1.2_Ching_Tuan_Yee.pdf',
        None
    ),
    (
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management',
        "Enhancing Land Administration in Fiji through the IGIF and It's "
        'Country Action Plan',
        'Inglés',
        'https://ggim.un.org/meetings/2022/4th-EG-LAM/documents/'
        '1.4_Meizyanne_Hicks.pdf',
        None
    ),
    (
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management',
        'Progress Report on the Revision of the Land Administration Domain '
        'Model (LADM)',
        'Inglés',
        'https://ggim.un.org/meetings/2022/4th-EG-LAM/documents/'
        '2.2_Chris_Body.pdf',
        None
    ),
    (
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management',
        'Road Map to Implement the Framework for Effective Land Administration '
        'System in Sri Lanka',
        'Inglés',
        'https://ggim.un.org/meetings/2022/4th-EG-LAM/documents/'
        '6.2_MTM_Rafeek.pdf',
        None
    ),
    (
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management',
        'Leveraging FELA, Sharing Experiences from the Netherlands and Abroad',
        'Inglés',
        'https://ggim.un.org/meetings/2022/4th-EG-LAM/documents/'
        '6.3_Paula_Dijkstra.pdf',
        "Netherlands' implementation of FELA through Kadaster"
    ),
    (
        'Fourth expert meeting of the Expert Group on Land Administration and '
        'Management and International Seminar on United Nations Global '
        'Geospatial Information Management',
        'Implementing the Framework for Effective Land Administration (FELA)',
        'Inglés',
        'https://ggim.un.org/meetings/2022/4th-EG-LAM/documents/'
        '6.1_Eva_Marie_Unger.pdf',
        None
    ),

    # ── Event 20: EG-LAM Side Event (Eleventh Session) ────────────────────
    (
        'Expert Group on Land Administration and Management Side Event at the '
        'Eleventh Session of the Committee of Experts on Global Geospatial '
        'Information Management',
        'Framework for Effective Land Administration: -Implementation of the '
        'FELA, -FELA: Spanish, Arabic, Chinese, -Mexico\'s experience in the '
        'implementation of FELA',
        'Inglés',
        'https://www.youtube.com/watch?v=tp2RcZr1EgM',
        'FELA translation into Spanish, Arabic, Chineese'
    ),

    # ── Event 21: Tenth Session UN-GGIM ───────────────────────────────────
    (
        'Tenth Session of the United Nations Committee of Experts on Global '
        'Geospatial Information Management (UN-GGIM)',
        'Application of geospatial information related to land administration '
        'and management ',
        'Inglés',
        'https://ggim.un.org/meetings/GGIM-committee/10th-Session/documents/'
        'E_C.20_2020_29-LAM-S.pdf',
        'The members collaborated remotely to finalize FELA'
    ),

    # ── Event 22: Actual version FELA ─────────────────────────────────────
    (
        'Actual version FELA',
        '-',
        'Inglés',
        'https://ggim.un.org/meetings/GGIM-committee/10th-Session/documents/'
        'E-C.20-2020-29-Add_2-Framework-for-Effective-Land-Administration.pdf',
        None
    ),

    # ── Event 23: Eighth Plenary UN-GGIM-AP ───────────────────────────────
    (
        'Eighth Plenary Meeting of UN-GGIM-AP (Asia-Pacific)',
        'Report from UN-GGIM Expert Group on Land Administration and Management '
        '(within Session 6: Working Group 2 on Cadastre and Land Management)',
        'Inglés',
        'https://un-ggim-ap.org/sites/default/files/media/meetings/Plenary08/'
        'WG2_5A%20Rohan%20Bennett_Framework%20for%20Effective%20Land%20'
        'Administration%20%28FELA%29.pdf',
        'First introduction of FELA'
    ),

    # ── Event 24: Ninth Session UN-GGIM ───────────────────────────────────
    (
        'Ninth Session of the United Nations Committee of Experts on Global '
        'Geospatial Information Management (UN-GGIM)',
        'Application of geospatial information related to land administration '
        'and management ',
        'Inglés',
        'https://ggim.un.org/meetings/GGIM-committee/9th-Session/documents/'
        'E_C.20_2020_10_Add_1_LAM_background.pdf?',
        'First formal draft of the FELA'
    ),

    # ── Event 25: Eighth Session UN-GGIM ──────────────────────────────────
    (
        'Eighth Session of the United Nations Committee of Experts on Global '
        'Geospatial Information Management (UN-GGIM)',
        'Application of geospatial information related to land administration '
        'and management ',
        'Inglés',
        'https://ggim.un.org/meetings/GGIM-committee/8th-Session/documents/'
        'E_C.20_2018_12_land_administration_E.pdf',
        'The group proposed developing a global framework on land administration'
    ),
]

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
created_count = 0
skipped_count = 0
error_count   = 0

for event_title, pres_title, lang_raw, url, observations in PRESENTATIONS_DATA:

    # Resolve parent event
    event = Event.objects.filter(event_title=event_title).first()
    if not event:
        # Try a strip() in case of trailing spaces
        event = Event.objects.filter(event_title=event_title.strip()).first()
    if not event:
        print(f"  [!] ERROR — Event not found: '{event_title[:70]}'")
        error_count += 1
        continue

    language_list = _parse_language(lang_raw)

    presentation, created = Presentation.objects.get_or_create(
        title=pres_title,
        event=event,
        defaults={
            'language':     language_list,
            'url_document': url,
            'observations': observations,
        }
    )

    if created:
        created_count += 1
        print(f"  [+] Created : {pres_title[:70]}")
    else:
        skipped_count += 1
        print(f"  [=] Exists  : {pres_title[:70]}")

print()
print(f"Done. Created: {created_count} | Skipped: {skipped_count} | "
      f"Errors: {error_count} | Total presentations: {Presentation.objects.count()}")
