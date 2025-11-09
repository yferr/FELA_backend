--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4 (Debian 16.4-1.pgdg110+2)
-- Dumped by pg_dump version 16.1

-- Started on 2025-10-25 13:29:41 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 7 (class 2615 OID 36230)
-- Name: eventos; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA eventos;


ALTER SCHEMA eventos OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 246 (class 1259 OID 52576)
-- Name: agencies; Type: TABLE; Schema: eventos; Owner: postgres
--

CREATE TABLE eventos.agencies (
    id integer NOT NULL,
    nombre character varying(150) NOT NULL,
    long_name text
);


ALTER TABLE eventos.agencies OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 52575)
-- Name: agencies_id_seq; Type: SEQUENCE; Schema: eventos; Owner: postgres
--

CREATE SEQUENCE eventos.agencies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE eventos.agencies_id_seq OWNER TO postgres;

--
-- TOC entry 4371 (class 0 OID 0)
-- Dependencies: 245
-- Name: agencies_id_seq; Type: SEQUENCE OWNED BY; Schema: eventos; Owner: postgres
--

ALTER SEQUENCE eventos.agencies_id_seq OWNED BY eventos.agencies.id;


--
-- TOC entry 244 (class 1259 OID 52475)
-- Name: cities; Type: TABLE; Schema: eventos; Owner: postgres
--

CREATE TABLE eventos.cities (
    country character varying(100) NOT NULL,
    city character varying(100) NOT NULL,
    geom public.geometry(Point,4326)
);


ALTER TABLE eventos.cities OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 44335)
-- Name: cities_tmp; Type: TABLE; Schema: eventos; Owner: postgres
--

CREATE TABLE eventos.cities_tmp (
    country character varying(100),
    city character varying(100),
    lat numeric(10,6),
    lon numeric(10,6)
);


ALTER TABLE eventos.cities_tmp OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 52468)
-- Name: countries; Type: TABLE; Schema: eventos; Owner: postgres
--

CREATE TABLE eventos.countries (
    country character varying(100) NOT NULL,
    geom public.geometry(Point,4326)
);


ALTER TABLE eventos.countries OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 44332)
-- Name: countries_tmp; Type: TABLE; Schema: eventos; Owner: postgres
--

CREATE TABLE eventos.countries_tmp (
    country character varying(100),
    lat numeric(10,6),
    lon numeric(10,6)
);


ALTER TABLE eventos.countries_tmp OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 52585)
-- Name: events; Type: TABLE; Schema: eventos; Owner: postgres
--

CREATE TABLE eventos.events (
    id integer NOT NULL,
    date character varying(50),
    year integer,
    agency text[],
    type character varying(100),
    country_e character varying(100) NOT NULL,
    city_e character varying(100) NOT NULL,
    event_title text NOT NULL
);


ALTER TABLE eventos.events OWNER TO postgres;

--
-- TOC entry 254 (class 1259 OID 52646)
-- Name: events_agencies; Type: TABLE; Schema: eventos; Owner: postgres
--

CREATE TABLE eventos.events_agencies (
    id_event integer NOT NULL,
    id_agencia integer NOT NULL
);


ALTER TABLE eventos.events_agencies OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 52584)
-- Name: events_id_seq; Type: SEQUENCE; Schema: eventos; Owner: postgres
--

CREATE SEQUENCE eventos.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE eventos.events_id_seq OWNER TO postgres;

--
-- TOC entry 4372 (class 0 OID 0)
-- Dependencies: 247
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: eventos; Owner: postgres
--

ALTER SEQUENCE eventos.events_id_seq OWNED BY eventos.events.id;


--
-- TOC entry 253 (class 1259 OID 52631)
-- Name: presentation_speakers; Type: TABLE; Schema: eventos; Owner: postgres
--

CREATE TABLE eventos.presentation_speakers (
    id_presentation integer NOT NULL,
    id_speaker integer NOT NULL
);


ALTER TABLE eventos.presentation_speakers OWNER TO postgres;

--
-- TOC entry 250 (class 1259 OID 52606)
-- Name: presentations; Type: TABLE; Schema: eventos; Owner: postgres
--

CREATE TABLE eventos.presentations (
    id integer NOT NULL,
    title text NOT NULL,
    event_title text NOT NULL,
    language character varying(50),
    url_document text,
    observations text
);


ALTER TABLE eventos.presentations OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 52605)
-- Name: presentations_id_seq; Type: SEQUENCE; Schema: eventos; Owner: postgres
--

CREATE SEQUENCE eventos.presentations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE eventos.presentations_id_seq OWNER TO postgres;

--
-- TOC entry 4373 (class 0 OID 0)
-- Dependencies: 249
-- Name: presentations_id_seq; Type: SEQUENCE OWNED BY; Schema: eventos; Owner: postgres
--

ALTER SEQUENCE eventos.presentations_id_seq OWNED BY eventos.presentations.id;


--
-- TOC entry 252 (class 1259 OID 52620)
-- Name: speakers; Type: TABLE; Schema: eventos; Owner: postgres
--

CREATE TABLE eventos.speakers (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    country_s character varying(100) NOT NULL,
    agency_s character varying(150)
);


ALTER TABLE eventos.speakers OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 52619)
-- Name: speakers_id_seq; Type: SEQUENCE; Schema: eventos; Owner: postgres
--

CREATE SEQUENCE eventos.speakers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE eventos.speakers_id_seq OWNER TO postgres;

--
-- TOC entry 4374 (class 0 OID 0)
-- Dependencies: 251
-- Name: speakers_id_seq; Type: SEQUENCE OWNED BY; Schema: eventos; Owner: postgres
--

ALTER SEQUENCE eventos.speakers_id_seq OWNED BY eventos.speakers.id;


--
-- TOC entry 4171 (class 2604 OID 52579)
-- Name: agencies id; Type: DEFAULT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.agencies ALTER COLUMN id SET DEFAULT nextval('eventos.agencies_id_seq'::regclass);


--
-- TOC entry 4172 (class 2604 OID 52588)
-- Name: events id; Type: DEFAULT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.events ALTER COLUMN id SET DEFAULT nextval('eventos.events_id_seq'::regclass);


--
-- TOC entry 4173 (class 2604 OID 52609)
-- Name: presentations id; Type: DEFAULT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.presentations ALTER COLUMN id SET DEFAULT nextval('eventos.presentations_id_seq'::regclass);


--
-- TOC entry 4174 (class 2604 OID 52623)
-- Name: speakers id; Type: DEFAULT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.speakers ALTER COLUMN id SET DEFAULT nextval('eventos.speakers_id_seq'::regclass);


--
-- TOC entry 4357 (class 0 OID 52576)
-- Dependencies: 246
-- Data for Name: agencies; Type: TABLE DATA; Schema: eventos; Owner: postgres
--

INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (1, 'FIG', 'Fédération Internationale des Géomètres');
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (2, 'Un-GGIM (EG-LAM)', 'United Nations Global Geospatial Information Management (Group of Experts on Land Administration and Management)');
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (3, 'EuroSDR', 'European Spatial Data Research');
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (4, 'IGN France', 'Institut National de l’Information Géographique et Forestière');
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (5, 'UN-GGIM Europe', 'Europe Regional Committee of the United Nations Committee on Global Geospatial Information Management');
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (6, 'EuroGeographics', NULL);
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (7, 'ARA-LG', 'Arab Academic Network for Land Governance ');
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (8, 'Arab Land Initiative', NULL);
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (9, 'SLAS', 'School for Land Administration Studies');
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (10, 'Kadaster', 'The Netherlands’ Cadastre, Land Registry and Mapping Agency');
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (12, 'School of Geomatic Sciences and Land Survey Engineering at Institut Agronomique et Vétérinaire Hassan II', NULL);
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (14, 'PCC', 'Permanent Committee on Cadastre in the European Union');
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (15, 'CLRKEN EuroGeographics', 'EuroGeographics Cadastre and Land Registry Knowledge Exchange Network');
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (16, 'UN-GGIM', 'United Nations Global Geospatial Information Management');
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (17, 'CPCI', 'Comité Permanente del Catastro en Iberoamérica');
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (18, 'GLTN', 'Global Land Tool Network');
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (19, 'Land Management Training Center of Government of Nepal', NULL);
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (20, 'UN-Habitat', 'United Nations Human Settlements Programme');
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (21, 'Kadaster International', NULL);
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (22, 'UN-GGIM Américas', 'United Nations Regional Committee on Global Geospatial Information Management for the Americas');
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (23, 'Geospatial World', NULL);
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (11, 'ITC Faculty University of Twente', 'Faculty of Geo-information Sciences and Earth Observation at the University of Twente');
INSERT INTO eventos.agencies (id, nombre, long_name) VALUES (13, 'UFSC', 'Universidade Federal de Santa Catarina');


--
-- TOC entry 4355 (class 0 OID 52475)
-- Dependencies: 244
-- Data for Name: cities; Type: TABLE DATA; Schema: eventos; Owner: postgres
--

INSERT INTO eventos.cities (country, city, geom) VALUES ('Morocco', 'Rabat', '0101000020E61000002041F163CC5D1BC0423EE8D9AC024140');
INSERT INTO eventos.cities (country, city, geom) VALUES ('Malaysia', 'Sarawak', '0101000020E6100000492EFF21FD965B405F07CE1951DAF83F');
INSERT INTO eventos.cities (country, city, geom) VALUES ('Belgium', 'Brujes', '0101000020E61000005EF415A419CB0940103B53E8BC9A4940');
INSERT INTO eventos.cities (country, city, geom) VALUES ('Ghana', 'Accra', '0101000020E6100000CC608C48145ACABFF0F78BD992751640');
INSERT INTO eventos.cities (country, city, geom) VALUES ('Mexico', 'Aguascalientes', '0101000020E6100000DFE00B93A99259C018265305A3E23540');
INSERT INTO eventos.cities (country, city, geom) VALUES ('Nepal', 'Dhulikhel', '0101000020E6100000BB270F0BB5625540567DAEB6629F3B40');
INSERT INTO eventos.cities (country, city, geom) VALUES ('USA', 'Orlando', '0101000020E61000002AA913D0445854C0D26F5F07CE893C40');
INSERT INTO eventos.cities (country, city, geom) VALUES ('USA', 'New York', '0101000020E610000015A8C5E0618052C0D5AF743E3C5B4440');
INSERT INTO eventos.cities (country, city, geom) VALUES ('Poland', 'Warsaw', '0101000020E6100000DE02098A1F03354013F241CF661D4A40');
INSERT INTO eventos.cities (country, city, geom) VALUES ('the Netherlands', 'Amsterdam', '0101000020E61000000F27309DD69D134041F2CEA10C2F4A40');
INSERT INTO eventos.cities (country, city, geom) VALUES ('the Netherlands', 'Deventer', '0101000020E6100000F241CF66D5A71840713D0AD7A3204A40');
INSERT INTO eventos.cities (country, city, geom) VALUES ('Singapore', 'Singapore', '0101000020E6100000B1506B9A77F45940E0BE0E9C33A2F53F');
INSERT INTO eventos.cities (country, city, geom) VALUES ('Australia', 'Canberra', '0101000020E61000005C8FC2F528A4624024B9FC87F4A341C0');
INSERT INTO eventos.cities (country, city, geom) VALUES ('France', 'Paris', '0101000020E6100000BC96900F7A36FE3F053411363C4D4740');
INSERT INTO eventos.cities (country, city, geom) VALUES ('Spain', 'Madrid', '0101000020E61000003C4ED1915CFE0DC0DE9387855A3B4440');
INSERT INTO eventos.cities (country, city, geom) VALUES ('Kenya', 'Nairobi', '0101000020E61000008C4AEA0434694240EA95B20C71ACF4BF');
INSERT INTO eventos.cities (country, city, geom) VALUES ('Online', 'Online', '0101000020E6100000AE47E17A14AE3C4033333333335344C0');
INSERT INTO eventos.cities (country, city, geom) VALUES ('-', '-', '0101000020E6100000AE47E17A14AE3C4033333333335344C0');
INSERT INTO eventos.cities (country, city, geom) VALUES ('Brazil', 'Florianópolis', '0101000020E610000001C11C3D7E4748C00E2DB29DEF973BC0');
INSERT INTO eventos.cities (country, city, geom) VALUES ('Chile', 'Santiago de Chile', '0101000020E61000009FCDAACFD5AA51C05396218E75B940C0');


--
-- TOC entry 4353 (class 0 OID 44335)
-- Dependencies: 242
-- Data for Name: cities_tmp; Type: TABLE DATA; Schema: eventos; Owner: postgres
--

INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('Morocco', 'Rabat', 34.020900, -6.841600);
INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('Brazil ', 'Florianópolis', -27.593500, -48.558540);
INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('Malaysia', 'Sarawak', 1.553300, 110.359200);
INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('Belgium', 'Brujes', 51.208890, 3.224170);
INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('Ghana', 'Accra', 5.614818, -0.205874);
INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('Mexico', 'Aguascalientes', 21.885300, -102.291600);
INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('Nepal', 'Dhulikhel', 27.622600, 85.542300);
INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('Chile ', 'Santiago de Chile ', -33.448900, -70.669300);
INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('USA', 'Orlando', 28.538300, -81.379200);
INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('USA', 'New York', 40.712776, -74.005974);
INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('Poland', 'Warsaw', 52.229700, 21.012200);
INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('the Netherlands', 'Amsterdam', 52.367573, 4.904139);
INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('the Netherlands', 'Deventer', 52.255000, 6.163900);
INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('Singapore', 'Singapore', 1.352100, 103.819800);
INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('Australia', 'Canberra', -35.280900, 149.130000);
INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('France', 'Paris', 46.603400, 1.888300);
INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('Spain', 'Madrid', 40.463700, -3.749200);
INSERT INTO eventos.cities_tmp (country, city, lat, lon) VALUES ('Kenya', 'Nairobi', -1.292100, 36.821900);


--
-- TOC entry 4354 (class 0 OID 52468)
-- Dependencies: 243
-- Data for Name: countries; Type: TABLE DATA; Schema: eventos; Owner: postgres
--

INSERT INTO eventos.countries (country, geom) VALUES ('Morocco', '0101000020E61000002041F163CC5D1BC0423EE8D9AC024140');
INSERT INTO eventos.countries (country, geom) VALUES ('Malaysia', '0101000020E6100000492EFF21FD965B405F07CE1951DAF83F');
INSERT INTO eventos.countries (country, geom) VALUES ('Belgium', '0101000020E61000005EF415A419CB0940103B53E8BC9A4940');
INSERT INTO eventos.countries (country, geom) VALUES ('Ghana', '0101000020E6100000CC608C48145ACABFF0F78BD992751640');
INSERT INTO eventos.countries (country, geom) VALUES ('Mexico', '0101000020E6100000DFE00B93A99259C018265305A3E23540');
INSERT INTO eventos.countries (country, geom) VALUES ('Nepal', '0101000020E6100000BB270F0BB5625540567DAEB6629F3B40');
INSERT INTO eventos.countries (country, geom) VALUES ('USA', '0101000020E61000000C022B8716A558C06EA301BC05EA4340');
INSERT INTO eventos.countries (country, geom) VALUES ('Poland', '0101000020E6100000DE02098A1F03354013F241CF661D4A40');
INSERT INTO eventos.countries (country, geom) VALUES ('the Netherlands', '0101000020E61000000F27309DD69D134041F2CEA10C2F4A40');
INSERT INTO eventos.countries (country, geom) VALUES ('Singapore', '0101000020E6100000B1506B9A77F45940E0BE0E9C33A2F53F');
INSERT INTO eventos.countries (country, geom) VALUES ('Australia', '0101000020E610000026E4839ECDB86040BC0512143F4639C0');
INSERT INTO eventos.countries (country, geom) VALUES ('France', '0101000020E6100000BC96900F7A36FE3F053411363C4D4740');
INSERT INTO eventos.countries (country, geom) VALUES ('Spain', '0101000020E61000003C4ED1915CFE0DC0DE9387855A3B4440');
INSERT INTO eventos.countries (country, geom) VALUES ('Argentina', '0101000020E610000000000000000050C000000000000041C0');
INSERT INTO eventos.countries (country, geom) VALUES ('Germany', '0101000020E6100000BA490C022BE724403E7958A835954940');
INSERT INTO eventos.countries (country, geom) VALUES ('Sweden', '0101000020E6100000DBF97E6ABCA4324071AC8BDB68104E40');
INSERT INTO eventos.countries (country, geom) VALUES ('Finland', '0101000020E61000000000000000003A400000000000005040');
INSERT INTO eventos.countries (country, geom) VALUES ('Democratic Republic of Congo', '0101000020E6100000A779C7293AC2354048BF7D1D382710C0');
INSERT INTO eventos.countries (country, geom) VALUES ('Kenya', '0101000020E61000008C4AEA0434694240EA95B20C71ACF4BF');
INSERT INTO eventos.countries (country, geom) VALUES ('Barbados', '0101000020E6100000F697DD9387C54DC088635DDC46632A40');
INSERT INTO eventos.countries (country, geom) VALUES ('Republica Dominicana', '0101000020E6100000CAC342AD698A51C0CEAACFD556BC3240');
INSERT INTO eventos.countries (country, geom) VALUES ('Trinidad And Tobago', '0101000020E610000014AE47E17A9C4EC0E0BE0E9C33622540');
INSERT INTO eventos.countries (country, geom) VALUES ('Chad', '0101000020E610000096218E7571BB3240B8AF03E78CE82E40');
INSERT INTO eventos.countries (country, geom) VALUES ('Rwanda', '0101000020E610000072F90FE9B7DF3D405DDC4603780BFFBF');
INSERT INTO eventos.countries (country, geom) VALUES ('Egypt', '0101000020E61000003D0AD7A370CD3E40FC1873D712D23A40');
INSERT INTO eventos.countries (country, geom) VALUES ('Armenia', '0101000020E6100000865AD3BCE3844640A913D044D8084440');
INSERT INTO eventos.countries (country, geom) VALUES ('Indonesia', '0101000020E610000082734694F67A5C401973D712F241E9BF');
INSERT INTO eventos.countries (country, geom) VALUES ('Fiji', '0101000020E6100000AE47E17A1442664066F7E461A1B631C0');
INSERT INTO eventos.countries (country, geom) VALUES ('Sri Lanka', '0101000020E610000061C3D32B65315440E78C28ED0D7E1F40');
INSERT INTO eventos.countries (country, geom) VALUES ('China', '0101000020E61000000000000000C059404A7B832F4CEE4140');
INSERT INTO eventos.countries (country, geom) VALUES ('Online', '0101000020E610000033333333335344C0AE47E17A14AE3C40');
INSERT INTO eventos.countries (country, geom) VALUES ('United Kingdom', '0101000020E6100000B0726891ED7C0BC00E4FAF9465B04B40');
INSERT INTO eventos.countries (country, geom) VALUES ('-', '0101000020E610000033333333335344C0AE47E17A14AE3C40');
INSERT INTO eventos.countries (country, geom) VALUES ('Slovenia', '0101000020E610000004560E2DB2FD2D40DE9387855A134740');
INSERT INTO eventos.countries (country, geom) VALUES ('Latvia', '0101000020E61000007CF2B0506B9A3840E3C798BB96704C40');
INSERT INTO eventos.countries (country, geom) VALUES ('Sierra Leone', '0101000020E6100000014D840D4F8F27C0401361C3D3EB2040');
INSERT INTO eventos.countries (country, geom) VALUES ('Chile', '0101000020E61000009FCDAACFD5AA51C05396218E75B940C0');
INSERT INTO eventos.countries (country, geom) VALUES ('Brazil', '0101000020E6100000917EFB3A70F649C0B81E85EB51782CC0');
INSERT INTO eventos.countries (country, geom) VALUES ('Nigeria', '0101000020E610000044FAEDEBC0592140448B6CE7FB292240');
INSERT INTO eventos.countries (country, geom) VALUES ('Kingdom of Saudi Arabia', '0101000020E6100000EEEBC039238A4640C286A757CAE23740');


--
-- TOC entry 4352 (class 0 OID 44332)
-- Dependencies: 241
-- Data for Name: countries_tmp; Type: TABLE DATA; Schema: eventos; Owner: postgres
--

INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Morocco', 34.020900, -6.841600);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Brazil ', -14.235000, -51.925300);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Malaysia', 1.553300, 110.359200);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Belgium', 51.208890, 3.224170);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Ghana', 5.614818, -0.205874);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Mexico', 21.885300, -102.291600);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Nepal', 27.622600, 85.542300);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Chile ', -33.448900, -70.669300);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('USA', 39.828300, -98.579500);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Poland', 52.229700, 21.012200);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('the Netherlands', 52.367573, 4.904139);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Singapore', 1.352100, 103.819800);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Australia', -25.274400, 133.775100);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('France', 46.603400, 1.888300);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Spain', 40.463700, -3.749200);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Argentina', -34.000000, -64.000000);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Germany', 51.165700, 10.451500);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Nigeria ', 9.082000, 8.675300);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Sweden', 60.128200, 18.643500);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Finland', 64.000000, 26.000000);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Democratic Republic of Congo', -4.038300, 21.758700);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Kenya', -1.292100, 36.821900);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Barbados', 13.193900, -59.543200);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Republica Dominicana', 18.735700, -70.162700);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Trinidad And Tobago', 10.691800, -61.222500);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Chad', 15.454200, 18.732200);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Rwanda', -1.940300, 29.873900);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Egypt', 26.820600, 30.802500);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Armenia', 40.069100, 45.038200);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Indonesia', -0.789300, 113.921300);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Fiji', -17.713400, 178.065000);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Sri Lanka', 7.873100, 80.771800);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Kingdom of Saudi Arabia ', 23.885900, 45.079200);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('China', 35.861700, 103.000000);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Online', 28.680000, -40.650000);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('United Kingdom', 55.378100, -3.436000);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('-', 28.680000, -40.650000);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Slovenia', 46.151200, 14.995500);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Latvia', 56.879600, 24.603200);
INSERT INTO eventos.countries_tmp (country, lat, lon) VALUES ('Sierra Leone', 8.460600, -11.779900);


--
-- TOC entry 4359 (class 0 OID 52585)
-- Dependencies: 248
-- Data for Name: events; Type: TABLE DATA; Schema: eventos; Owner: postgres
--

INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (1, '3-5 november 2025', 2025, '{FIG}', 'Conference', 'Brazil', 'Florianópolis', 'FIG Joint Land Administration Conference');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (2, '17 july 2025', 2025, '{"Un-GGIM (EG-LAM)"}', 'Webinar', 'Online', 'Online', 'Unlocking FELA a global dialogue on land administration ');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (3, '16-17 June 2025', 2025, '{EuroSDR,"IGN France","UN-GGIM Europe",EuroGeographics}', 'Workshop', 'France', 'Paris', 'International Workshop on challenges in relation to the UN Framework for Effective Land Administration (FELA)');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (4, '30 April 2025, 20 May 2025', 2025, '{"Arab Academic Network for Land Governance (ARA-LG)","Arab Land Initiative"}', 'Lectures', 'Online', 'Online', 'Strengthening Academic Foundations in Land Governance: Online Lectures Hosted in Collaboration with Al-Quds and Duhok Universities');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (6, '11-13 November 2024', 2024, '{"UFSC (Federal University of Santa Catarina)"}', 'Congress', 'Brazil', 'Florianópolis', 'Congress of Multifinalial Cadastre and Territorial Management – COBRAC 2024');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (7, '24-26 September 2024', 2024, '{FIG}', 'ANNUAL MEETING', 'Malaysia', 'Sarawak', 'FIG COMMISSION 5, 7 ANNUAL MEETING 2024 Framework for Effective Land Administration (WG7.1 FELA) + Fit for Purpose Land Administration (WG7.2 FFPLA)');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (8, '17-19 June 2024', 2024, '{PCC,"CLRKEN EuroGeographics"}', 'Conference', 'Belgium', 'Brujes', 'Permanent Committee on Cadastre in the European Union (PCC)');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (9, '19-24 May 2024', 2024, '{FIG}', 'Congress', 'Ghana', 'Accra', 'FIG Woorking Week 2024 - Land Policy Issues and Innovations');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (10, '8-11 April 2024', 2024, '{UN-GGIM,CPCI}', 'Seminar', 'Mexico', 'Aguascalientes', 'Fifth meeting of the Expert Group on Land Administration and Management and the International Seminar on UN-GGIM');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (11, '27-29 February 2024', 2024, '{GLTN,"Land Management Training Center of Government of Nepal",UN-Habitat,"Kadaster International"}', 'Workshop', 'Nepal', 'Dhulikhel', 'Effective Land Administration in Nepal: Navigating Governance, Legal, and Financial Pathways within the Climate Change – Land Nexus');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (12, '4-7 December 2023', 2023, '{CPCI}', 'Assembly', 'Chile', 'Santiago de Chile', 'XIV Simposio y IX Asamblea del CPCI');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (13, '18-20 october 2023', 2023, '{"UN-GGIM Américas"}', 'Expert Group Meeting', 'Chile', 'Santiago de Chile', 'X session UN-GGIM : Americas ');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (14, '2-4 october 2023', 2023, '{FIG}', 'Meeting', 'the Netherlands', 'Deventer', 'FIG Meeting Digital Transformation for Responsible Land Administration');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (15, '28 may- 1 June 2023', 2023, '{FIG}', 'Congress', 'USA', 'Orlando', 'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (16, '11-15 September 2022', 2022, '{FIG}', 'Congress', 'Poland', 'Warsaw', 'XXVII FIG Congress - Volunteering for the Future Geospatial Excellence for a better living');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (17, '3-5 august  2022', 2022, '{UN-GGIM}', 'Expert Group Meeting', 'Online', 'Online', 'Twelfth Session of the United Nations Committee of Experts on Global Geospatial Information Management (UN-GGIM)');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (18, '11-12 May 2022', 2022, '{"Geospatial World"}', 'Seminar', 'the Netherlands', 'Amsterdam', 'Geospatial World Forum 2022, Symposium on Land Administration');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (19, '17-18 May 2022', 2022, '{UN-GGIM}', 'Expert Group Meeting', 'Singapore', 'Singapore', 'Fourth expert meeting of the Expert Group on Land Administration and Management and International Seminar on United Nations Global Geospatial Information Management');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (20, '12 August 2021', 2021, '{UN-GGIM}', 'Expert Group Meeting', 'Online', 'Online', 'Expert Group on Land Administration and Management Side Event at the Eleventh Session of the Committee of Experts on Global Geospatial Information Management');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (21, '26-27 August - 4 September  2020', 2020, '{UN-GGIM}', 'Expert Group Meeting', 'Online', 'Online', 'Tenth Session of the United Nations Committee of Experts on Global Geospatial Information Management (UN-GGIM)');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (22, 'may-20', 2020, '{UN-GGIM}', 'Document', '-', '-', 'Actual version FELA');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (23, '3-5 November 2019', 2019, '{UN-GGIM}', 'Meeting', 'Australia', 'Canberra', 'Eighth Plenary Meeting of UN-GGIM-AP (Asia-Pacific)');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (24, '5 - 9 August 2019', 2019, '{UN-GGIM}', 'Expert Group Meeting', 'USA', 'New York', 'Ninth Session of the United Nations Committee of Experts on Global Geospatial Information Management (UN-GGIM)');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (25, '2-4 August 2017', 2017, '{UN-GGIM}', 'Expert Group Meeting', 'USA', 'New York', 'Eighth Session of the United Nations Committee of Experts on Global Geospatial Information Management (UN-GGIM)');
INSERT INTO eventos.events (id, date, year, agency, type, country_e, city_e, event_title) VALUES (5, '17 February 2025', 2025, '{"School for Land Administration Studies (SLAS)",Kadaster,"ITC Faculty of University of Twente ","School of Geomatic Sciences and Land Survey Engineering at Institut Agronomique et Vétérinaire Hassan II"}', 'pre-workshop', 'Morocco', 'Rabat', 'Technical pre-workshop 3rd Arab Land Conference “Fit-for-Purpose Land Administration in the Arab Region”');


--
-- TOC entry 4365 (class 0 OID 52646)
-- Dependencies: 254
-- Data for Name: events_agencies; Type: TABLE DATA; Schema: eventos; Owner: postgres
--

INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (1, 1);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (2, 2);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (3, 3);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (3, 4);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (3, 5);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (3, 6);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (4, 7);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (4, 8);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (5, 9);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (5, 10);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (5, 11);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (5, 12);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (6, 13);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (7, 1);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (8, 14);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (8, 15);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (9, 1);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (10, 16);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (10, 17);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (11, 18);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (11, 19);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (11, 20);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (11, 21);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (12, 17);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (13, 22);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (14, 1);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (15, 1);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (16, 1);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (17, 16);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (18, 23);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (19, 16);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (20, 16);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (21, 16);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (22, 16);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (23, 16);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (24, 16);
INSERT INTO eventos.events_agencies (id_event, id_agencia) VALUES (25, 16);


--
-- TOC entry 4364 (class 0 OID 52631)
-- Dependencies: 253
-- Data for Name: presentation_speakers; Type: TABLE DATA; Schema: eventos; Owner: postgres
--

INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (1, 1);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (2, 36);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (3, 57);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (4, 6);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (5, 2);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (6, 69);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (7, 68);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (8, 10);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (8, 55);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (9, 19);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (10, 10);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (11, 66);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (11, 67);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (12, 33);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (13, 69);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (14, 70);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (15, 71);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (15, 26);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (16, 73);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (16, 74);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (17, 29);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (17, 75);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (18, 72);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (19, 65);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (20, 1);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (22, 1);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (23, 4);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (23, 5);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (24, 6);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (25, 1);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (25, 7);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (26, 10);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (26, 1);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (26, 8);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (26, 9);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (27, 11);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (27, 12);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (27, 13);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (28, 14);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (28, 15);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (28, 16);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (29, 17);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (30, 18);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (31, 1);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (32, 19);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (33, 20);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (34, 21);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (35, 24);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (35, 22);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (35, 23);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (35, 10);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (35, 16);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (36, 1);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (37, 19);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (38, 1);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (39, 4);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (39, 5);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (40, 25);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (41, 26);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (42, 27);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (43, 30);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (43, 28);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (43, 29);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (44, 10);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (44, 9);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (44, 31);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (44, 32);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (44, 33);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (44, 34);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (44, 35);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (44, 3);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (44, 37);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (44, 38);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (45, 30);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (46, 9);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (46, 10);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (46, 39);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (46, 40);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (46, 41);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (46, 42);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (46, 43);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (46, 44);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (46, 45);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (47, 46);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (48, 47);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (49, 29);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (50, 48);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (51, 49);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (52, 50);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (52, 51);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (52, 52);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (52, 53);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (53, 54);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (54, 55);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (55, 10);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (56, 29);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (56, 56);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (56, 10);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (56, 9);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (56, 18);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (56, 58);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (56, 59);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (56, 60);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (56, 61);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (56, 62);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (57, 46);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (58, 46);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (59, 29);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (59, 63);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (59, 64);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (59, 9);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (59, 10);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (60, 46);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (61, 46);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (20, 2);
INSERT INTO eventos.presentation_speakers (id_presentation, id_speaker) VALUES (21, 3);


--
-- TOC entry 4361 (class 0 OID 52606)
-- Dependencies: 250
-- Data for Name: presentations; Type: TABLE DATA; Schema: eventos; Owner: postgres
--

INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (1, 'Claves del éxito del catastro español y sus retos para el Furturo con relación con el FELA', 'FIG Joint Land Administration Conference', 'Español', NULL, NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (2, 'FELA implementation experiences: Key achievement of FELA Principles in Sierra Leone', 'Unlocking FELA a global dialogue on land administration ', 'Inglés', NULL, NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (3, 'FELA implementation experiences: El estado de la administracion de tierras en Mexico, una perspectiva registral y catastral desde el FELA ', 'Unlocking FELA a global dialogue on land administration ', 'Español', NULL, 'Analisis basado en los resultados del Censo Nacional de Gobiernos Estatales 2025');
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (4, 'FELA implementation experiences: Towards Effective Land Administration: Lessons For and From Nigeria', 'Unlocking FELA a global dialogue on land administration ', 'Inglés', NULL, 'FELA progress across States in Nigeria');
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (5, 'FELA implementation experiences: de SIT a SAT Orientaciones para integrar FELa en la provincia de Córdoba, Argentina ', 'Unlocking FELA a global dialogue on land administration ', 'Español', NULL, 'Modernizar el SIT y mejorar la administracion territorial provincial, integrando municipios y comunas ');
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (6, 'Tools for land administration: FELA implementation: French urban planning geoportal', 'Unlocking FELA a global dialogue on land administration ', 'Inglés', NULL, NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (7, 'Tools for land administration: UN tools to implement FELA', 'Unlocking FELA a global dialogue on land administration ', 'Español', NULL, 'Herramientas de las UN que pueden ser usadas para la implementacion de FELA (GLTN)');
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (8, 'FELA and effective land Administration ', 'Unlocking FELA a global dialogue on land administration ', 'Inglés', NULL, NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (9, 'UN-GGIM Expert Group on Land administration and Management', 'International Workshop on challenges in relation to the UN Framework for Effective Land Administration (FELA)', 'Inglés', 'https://www.eurosdr.net/sites/default/files/images/inline/eurosdr_fela_paris_keynote-presentation.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (10, 'Introduction to UN-GGIM Framework for Effective Land Administration (FELA)', 'International Workshop on challenges in relation to the UN Framework for Effective Land Administration (FELA)', 'Inglés', 'https://www.eurosdr.net/sites/default/files/images/inline/eurosdr_fela_paris_intro-to-the_fela.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (11, 'Results of FELA surveys', 'International Workshop on challenges in relation to the UN Framework for Effective Land Administration (FELA)', 'Inglés', 'https://www.eurosdr.net/sites/default/files/images/inline/eurosdr_fela_paris_survey-results.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (12, 'Effective land administration in the Netherlands', 'International Workshop on challenges in relation to the UN Framework for Effective Land Administration (FELA)', 'Inglés', NULL, NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (13, 'FELA implementation: French urban planning geoportal', 'International Workshop on challenges in relation to the UN Framework for Effective Land Administration (FELA)', 'Inglés', 'https://www.eurosdr.net/sites/default/files/images/inline/eurosdr_fela_french_urban_planning_geoportal.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (14, 'FELA implementation: feedback from Latvia', 'International Workshop on challenges in relation to the UN Framework for Effective Land Administration (FELA)', 'Inglés', 'https://www.eurosdr.net/sites/default/files/images/inline/eurosdr_fela_implementation_feedbacks-from-latvia.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (15, 'Making land information systems the cornerstone of FELA implementation in Africa', 'International Workshop on challenges in relation to the UN Framework for Effective Land Administration (FELA)', 'Inglés', 'https://www.eurosdr.net/sites/default/files/images/inline/eurosdr_fela_lis-in-africa_feedbacks-from-ignfi.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (16, 'Improving the usage of land administration data for education and capacity building', 'International Workshop on challenges in relation to the UN Framework for Effective Land Administration (FELA)', 'Inglés', 'https://www.eurosdr.net/sites/default/files/images/inline/eurosdr_fela_education-capacity-building.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (17, 'The use of GIS in FELA implementations', 'International Workshop on challenges in relation to the UN Framework for Effective Land Administration (FELA)', 'Inglés', 'https://www.eurosdr.net/sites/default/files/images/inline/eurosdr_fela_use-of-gis_esri.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (18, 'international frameworks and models', 'Strengthening Academic Foundations in Land Governance: Online Lectures Hosted in Collaboration with Al-Quds and Duhok Universities', 'Inglés', 'https://arablandinitiative.gltn.net/media/news/strengthening-academic-foundations-in-land-governance-online-lectures-hosted-in-collaboration-with', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (19, '-', 'Technical pre-workshop 3rd Arab Land Conference “Fit-for-Purpose Land Administration in the Arab Region”', 'Inglés, Arábico', 'https://arablandinitiative.gltn.net/media/events/technical-pre-workshop-fit-for-purpose-land-administration-in-the-arab-region', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (20, 'International and national frameworks that link the Multifinality Territorial Cadastre with the Sustainable Development Goals', 'Congress of Multifinalial Cadastre and Territorial Management – COBRAC 2024', 'Inglés', 'https://cobrac.ufsc.br/es/programacao/', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (21, 'Fit-for-Purpose Land Administration Solutions from Trimble', 'FIG COMMISSION 5, 7 ANNUAL MEETING 2024 Framework for Effective Land Administration (WG7.1 FELA) + Fit for Purpose Land Administration (WG7.2 FFPLA)', 'Inglés', 'https://fig.net/resources/proceedings/fig_proceedings/7_2024/papers/ts02/TS02_koper_12946_abs.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (22, 'Where things are at with the FELA Working group ', 'FIG COMMISSION 5, 7 ANNUAL MEETING 2024 Framework for Effective Land Administration (WG7.1 FELA) + Fit for Purpose Land Administration (WG7.2 FFPLA)', 'Inglés', 'https://fig.net/resources/proceedings/fig_proceedings/7_2024/papers/ts02/TS02_velasco_12940_abs.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (23, 'A prliminary UN-GGIM Work to integrate Land and Sea', 'FIG COMMISSION 5, 7 ANNUAL MEETING 2024 Framework for Effective Land Administration (WG7.1 FELA) + Fit for Purpose Land Administration (WG7.2 FFPLA)', 'Inglés', 'https://fig.net/resources/proceedings/fig_proceedings/7_2024/papers/ts02/TS02_soon_khoo_12866.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (24, 'From no Cadastre to 3D Cadastre: The evolving role of Spatially Enabled Framework', 'FIG COMMISSION 5, 7 ANNUAL MEETING 2024 Framework for Effective Land Administration (WG7.1 FELA) + Fit for Purpose Land Administration (WG7.2 FFPLA)', 'Inglés', 'https://fig.net/resources/proceedings/fig_proceedings/7_2024/papers/ts02/TS02_taiwo_12871_abs.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (25, 'Framework for Effective Land Administration (FELA)', 'Permanent Committee on Cadastre in the European Union (PCC)', 'Inglés', 'https://eurogeographics.org/app/uploads/2024/03/PPT-20-Magdalena-and-Amalia-Framework-for-effective-land-administration-FELA-in-PCC2024-1.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (26, 'Framework for Effective Land Administration (FELA): Research Synthesis', 'FIG Woorking Week 2024 - Land Policy Issues and Innovations', 'Inglés', 'https://www.fig.net/resources/proceedings/fig_proceedings/fig2024/ppt/ts11g/TS11G_unger_valesco_et_al_12697_ppt.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (27, 'Exploring Technology Integration Through FELA in Nigeria', 'FIG Woorking Week 2024 - Land Policy Issues and Innovations', 'Inglés', 'https://www.fig.net/resources/proceedings/fig_proceedings/fig2024/ppt/ts11g/TS11G_ajayi_riekkinen_et_al_12501_ppt.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (28, 'Land Reforms and Implementation of the Framework for Effective Land Administration (FELA): a Case Study for Customary Land Registry Implementation in the Democratic Republic of Congo', 'FIG Woorking Week 2024 - Land Policy Issues and Innovations', 'Inglés', 'https://www.fig.net/resources/proceedings/fig_proceedings/fig2024/ppt/ts11g/TS11G_mballo_vutegha_et_al_12510_ppt.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (29, 'Implementing the framework for effective land administration in Barbados', 'Fifth meeting of the Expert Group on Land Administration and Management and the International Seminar on UN-GGIM', 'Inglés', 'https://ggim.un.org/meetings/2024/Fifth-EG-LAM/documents/2.1_Leandre_Murrel-Forde.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (30, 'Mexico''s experiences in the implementation of FELA', 'Fifth meeting of the Expert Group on Land Administration and Management and the International Seminar on UN-GGIM', 'Inglés', 'https://ggim.un.org/meetings/2024/Fifth-EG-LAM/documents/2.3_Claudio_Topete.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (31, 'How the implementation of the Framework for Effective Land Administration can assist cadastral institutions in Iberoamerica', 'Fifth meeting of the Expert Group on Land Administration and Management and the International Seminar on UN-GGIM', 'Inglés, Español', 'https://ggim.un.org/meetings/2024/Fifth-EG-LAM/documents/5.1_Amalia_Velasco.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (32, 'Management of geospatial data and cadastral data in Chile, a pending challenge', 'Fifth meeting of the Expert Group on Land Administration and Management and the International Seminar on UN-GGIM', 'Inglés', 'https://ggim.un.org/meetings/2024/Fifth-EG-LAM/documents/2.2._Raffaella_Olguin.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (33, 'Key Elements of the Framework for Effective Land Management', 'Fifth meeting of the Expert Group on Land Administration and Management and the International Seminar on UN-GGIM', 'Inglés', 'https://ggim.un.org/meetings/2024/Fifth-EG-LAM/documents/3.1._Ridomil_Alejandro.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (34, 'We know the earth-we secure the future', 'Fifth meeting of the Expert Group on Land Administration and Management and the International Seminar on UN-GGIM', 'Inglés', 'https://ggim.un.org/meetings/2024/Fifth-EG-LAM/documents/3.2._Markku_Markkula.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (35, '-', 'Effective Land Administration in Nepal: Navigating Governance, Legal, and Financial Pathways within the Climate Change – Land Nexus', 'Inglés', 'https://www.kadaster.com/-/strengthening-land-administration-in-nepal-amidst-climate-change?redirect=%2Fabout-us%2Fnews', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (36, 'Presentación de los trabajos realizados en 2023 por la Presidencia CPCI', 'XIV Simposio y IX Asamblea del CPCI', 'Español', 'http://www.catastrolatino.org/documentos/2023/XIV%20congreso%20Chile/CPCIActaAsambleaChile2023%20def[21726].pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (37, 'Implementing the Framework for Effective Land Administration (FELA): New Workplan and Developments', 'X session UN-GGIM : Americas ', 'Inglés', 'https://www.cepal.org/sites/default/files/presentations/framework-effective-land-administration-fela-chile-oct2023.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (38, 'Framework for efective land administration (WG7.1) Work plan 2023-2026', 'FIG Meeting Digital Transformation for Responsible Land Administration', 'Inglés', 'https://www.fig.net/resources/proceedings/fig_proceedings/7_2023/papers/se01/SE01_velasco_velasco_12338_abs.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (39, 'Implementing the Framework for Effective Land Administration (FELA): New Workplan and Developments', 'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers', 'Inglés', 'https://fig.net/resources/proceedings/fig_proceedings/fig2023/ppt/ts01i/TS01I_soon_khoo_12061_ppt.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (40, 'The UN-GGIM Integrated Geospatial Information Framework and the status of the High-Level Group of the IGIF', 'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers', 'Inglés', 'https://fig.net/resources/proceedings/fig_proceedings/fig2023/ppt/ts01i/TS01I_lilje_11937_ppt.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (41, 'Improved Land Management, a Key Factor for a Stable and Protective Social Economic Development', 'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers', 'Inglés', 'https://fig.net/resources/proceedings/fig_proceedings/fig2023/papers/ts01i/TS01I_lestang_12041.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (42, 'Land Registration for Conquering New SDG Frontiers', 'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers', 'Inglés', 'https://fig.net/resources/proceedings/fig_proceedings/fig2023/ppt/ts01i/TS01I_griffith-charles_12099_ppt.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (43, 'FELA-based Geospatial Knowledge Infrastructure', 'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers', 'Inglés', 'https://fig.net/resources/proceedings/fig_proceedings/fig2023/ppt/ts01i/TS01I_tourtelotte_pickett_et_al_12127_ppt.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (44, 'Fit-For-Purpose Land Administration and the Framework for Effective Land Administration in Chad', 'FIG Woorking Week 2023 - Protecting Our World, Conquering New Frontiers', 'Inglés', 'https://fig.net/resources/proceedings/fig_proceedings/fig2023/ppt/ts01i/TS01I_unger_bennett_et_al_12242_ppt.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (45, 'GIS in Land Administration Can Help You Implement the FELA and Support the SDG’s', 'XXVII FIG Congress - Volunteering for the Future Geospatial Excellence for a better living', 'Inglés', 'https://www.fig.net/resources/proceedings/fig_proceedings/fig2022/papers/ts02a/TS02A_tourtelotte_11559.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (46, 'Digital Transformation of Land Administration: Stages, Status, and Solutions', 'XXVII FIG Congress - Volunteering for the Future Geospatial Excellence for a better living', 'Inglés', 'https://www.fig.net/resources/proceedings/fig_proceedings/fig2022/papers/ts04b/TS04B_bennett_unger_et_al_11482.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (47, 'Application of geospatial information related to land administration and management ', 'Twelfth Session of the United Nations Committee of Experts on Global Geospatial Information Management (UN-GGIM)', 'Inglés', 'https://ggim.un.org/meetings/GGIM-committee/12th-Session/documents/E-C.20_2022_13_Add_1_Land_Administration_and_Management.pdf', 'FELA translation into French and Dutch');
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (48, 'Modern Land Administration, Innovation and Investment for Sustainable Development', 'Geospatial World Forum 2022, Symposium on Land Administration', 'Inglés', NULL, NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (49, 'Framework for Effective Land Administration (FELA)', 'Fourth expert meeting of the Expert Group on Land Administration and Management and International Seminar on United Nations Global Geospatial Information Management', 'Inglés', 'https://ggim.un.org/meetings/2022/4th-EG-LAM/documents/1.3_Kees_de_Zeeuw.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (50, 'Effective Land Administration - Digitally-Enabled Urban Planning in Singapore', 'Fourth expert meeting of the Expert Group on Land Administration and Management and International Seminar on United Nations Global Geospatial Information Management', 'Inglés', 'https://ggim.un.org/meetings/2022/4th-EG-LAM/documents/1.2_Ching_Tuan_Yee.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (51, 'Enhancing Land Administration in Fiji through the IGIF and It''s Country Action Plan', 'Fourth expert meeting of the Expert Group on Land Administration and Management and International Seminar on United Nations Global Geospatial Information Management', 'Inglés', 'https://ggim.un.org/meetings/2022/4th-EG-LAM/documents/1.4_Meizyanne_Hicks.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (52, 'Progress Report on the Revision of the Land Administration Domain Model (LADM)', 'Fourth expert meeting of the Expert Group on Land Administration and Management and International Seminar on United Nations Global Geospatial Information Management', 'Inglés', 'https://ggim.un.org/meetings/2022/4th-EG-LAM/documents/2.2_Chris_Body.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (53, 'Road Map to Implement the Framework for Effective Land Administration System in Sri Lanka', 'Fourth expert meeting of the Expert Group on Land Administration and Management and International Seminar on United Nations Global Geospatial Information Management', 'Inglés', 'https://ggim.un.org/meetings/2022/4th-EG-LAM/documents/6.2_MTM_Rafeek.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (54, 'Leveraging FELA, Sharing Experiences from the Netherlands and Abroad', 'Fourth expert meeting of the Expert Group on Land Administration and Management and International Seminar on United Nations Global Geospatial Information Management', 'Inglés', 'https://ggim.un.org/meetings/2022/4th-EG-LAM/documents/6.3_Paula_Dijkstra.pdf', 'Netherlands'' implementation of FELA through Kadaster');
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (55, 'Implementing the Framework for Effective Land Administration (FELA)', 'Fourth expert meeting of the Expert Group on Land Administration and Management and International Seminar on United Nations Global Geospatial Information Management', 'Inglés', 'https://ggim.un.org/meetings/2022/4th-EG-LAM/documents/6.1_Eva_Marie_Unger.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (56, 'Framework for Effective Land Administration: -Implementation of the FELA, -FELA: Spanish, Arabic, Chinese, -Mexico’s experience in the implementation of FELA', 'Expert Group on Land Administration and Management Side Event at the Eleventh Session of the Committee of Experts on Global Geospatial Information Management', 'Inglés', 'https://www.youtube.com/watch?v=tp2RcZr1EgM', 'FELA translation into Spanish, Arabic, Chineese');
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (57, 'Application of geospatial information related to land administration and management ', 'Tenth Session of the United Nations Committee of Experts on Global Geospatial Information Management (UN-GGIM)', 'Inglés', 'https://ggim.un.org/meetings/GGIM-committee/10th-Session/documents/E_C.20_2020_29-LAM-S.pdf', 'The members collaborated remotely to finalize FELA');
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (58, '-', 'Actual version FELA', 'Inglés', 'https://ggim.un.org/meetings/GGIM-committee/10th-Session/documents/E-C.20-2020-29-Add_2-Framework-for-Effective-Land-Administration.pdf', NULL);
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (59, 'Report from UN-GGIM Expert Group on Land Administration and Management (within Session 6: Working Group 2 on Cadastre and Land Management)', 'Eighth Plenary Meeting of UN-GGIM-AP (Asia-Pacific)', 'Inglés', 'https://un-ggim-ap.org/sites/default/files/media/meetings/Plenary08/WG2_5A%20Rohan%20Bennett_Framework%20for%20Effective%20Land%20Administration%20%28FELA%29.pdf', 'First introduction of FELA');
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (60, 'Application of geospatial information related to land administration and management ', 'Ninth Session of the United Nations Committee of Experts on Global Geospatial Information Management (UN-GGIM)', 'Inglés', 'https://ggim.un.org/meetings/GGIM-committee/9th-Session/documents/E_C.20_2020_10_Add_1_LAM_background.pdf?', 'First formal draft of the FELA');
INSERT INTO eventos.presentations (id, title, event_title, language, url_document, observations) VALUES (61, 'Application of geospatial information related to land administration and management ', 'Eighth Session of the United Nations Committee of Experts on Global Geospatial Information Management (UN-GGIM)', 'Inglés', 'https://ggim.un.org/meetings/GGIM-committee/8th-Session/documents/E_C.20_2018_12_land_administration_E.pdf', 'The group proposed developing a global framework on land administration');


--
-- TOC entry 4363 (class 0 OID 52620)
-- Dependencies: 252
-- Data for Name: speakers; Type: TABLE DATA; Schema: eventos; Owner: postgres
--

INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (1, 'Amalia Velasco', 'Spain', 'Direccion General del Catastro España');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (2, 'Mario Piumetto', 'Argentina', 'Universidad de Córdoba');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (3, 'Markus Koper', 'Germany', 'Trimble');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (4, 'Kean Huat Soon', 'Singapore', 'Singapore Land Authority');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (5, 'Victor Khoo', 'Singapore', 'Singapore Land Authority');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (6, 'Israel Taiwo', 'Nigeria', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (7, 'Magdalena Andersson', 'Sweden', 'THE SWEDISH MAPPING');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (8, 'Joep Crompvoets', 'Belgium', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (9, 'Rohan Bennett', 'Australia', 'Chair FIG Commission 7');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (10, 'Eva-Maria Unger', 'the Netherlands', 'Kadaster');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (11, 'Kirsikka Riekkinen', 'Finland', 'AALTO UNIVERSITY');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (12, 'Oluwafemi Adekola', 'Finland', 'AALTO UNIVERSITY');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (13, 'Opeyemi Michael Ajayi', 'Finland', 'AALTO UNIVERSITY');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (14, 'Mamadou Mballo', 'Democratic Republic of Congo', 'UN-Habitat - GLTN');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (15, 'Hellen Ndungu', 'Kenya', 'UN-Habitat - GLTN');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (16, 'John Gitau', 'Kenya', 'UN-Habitat - GLTN');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (17, 'Leandre Murrell-Forde', 'Barbados', 'The Lands and Survey Department');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (18, 'Claudio Martínez Topete', 'Mexico', 'INEGI');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (19, 'Raffaella Anilio Olguín', 'Chile', 'SNIT-IDE, Ministerio de Bienes Nacionales, UN-GGIM Américas');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (20, 'Ridomil Alejandro Rojas Ferreyra', 'Republica Dominicana', 'Dirección Nacional de Mensuras Catastrales, Registro Inmobiliario');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (21, 'Markku Markkula', 'Finland', 'National Land Survey of Finland');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (22, 'Ganesh Prasad Bhatta', 'Nepal', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (23, 'Raja Ram Chhatkuli ', 'Nepal', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (24, 'Janak Raj Joshi', 'Nepal', 'MoLMCPA');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (25, 'Mikael Lilje', 'Sweden', 'Swedish Mapping (Lantmäteriet)');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (26, 'Jean-Philippe Lestang', 'France', 'IGN France');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (27, 'Charisse Griffith-Charles', 'Trinidad And Tobago', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (28, 'Katie Pickett', 'USA', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (29, 'Kees de Zeeuw', 'the Netherlands', 'Kadaster International / Co-chair UN GGIM Expert Group');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (30, 'Brandon Tourtelotte', 'USA', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (31, 'Mahamat Abdoulaye Malloum', 'Chad', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (32, 'Claudia Stöcker', 'Germany', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (33, 'Christelle van den Berg', 'the Netherlands', 'Kadaster');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (34, 'Kaspar Kundert', 'Rwanda', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (35, 'Dina Naguib', 'Egypt', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (36, 'Jobo Samba', 'Sierra Leone', 'Land Avisor at Sierra Leone Land Administration Project');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (37, 'Divyani Kohli', 'the Netherlands', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (38, 'Mila Koeva', 'the Netherlands', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (39, 'Vincent Verheij', 'the Netherlands', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (40, 'Haico Van der Vegt', 'the Netherlands', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (41, 'Suren Tovmasyan', 'Armenia', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (42, 'Indra Hutabarat', 'Indonesia', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (43, 'Aram Gugarats', 'Armenia', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (44, 'Aulia Latif', 'Indonesia', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (45, 'Chalemyan Trdat', 'Armenia', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (46, 'Committee of Experts on Global Geospatial Information Management', '-', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (47, 'Brent Jones', 'USA', 'ESRI');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (48, 'Ching Tuan Yee', 'Singapore', 'Urban Redevelopment Authority');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (49, 'Meizyanne Hicks', 'Fiji', 'Ministry of Lands and Mineral Resources');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (50, 'Chris Body', 'Australia', 'International Organization for Standardization Technical Committee 211');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (51, 'Christiaan Lemmen', 'the Netherlands', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (52, 'Abdullah Kara', '-', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (53, 'Peter van Oosterom', 'the Netherlands', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (54, 'Mohamed Rafeek', 'Sri Lanka', 'Survey Department');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (55, 'Paula Dijkstra', 'the Netherlands', 'Kadaster International');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (56, 'Ingrid van de Berghe', 'Belgium', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (57, 'Mario Cruz', 'Mexico', 'INEGI');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (58, 'Cristian Araneda Hernandez', 'Chile', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (59, 'Ali Alawaji', 'Kingdom of Saudi Arabia', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (60, 'Liao Rong', 'China', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (61, 'Liu Yong', 'China', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (62, 'Zhong Taiyang', 'China', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (63, 'Trevor Benn', '-', 'UN-GGIM Expert Group on Land Administration and Management');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (64, 'Teo Chee Hai', '-', 'UN-GGIM Expert Group on Land Administration and Management');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (65, 'Expert Group', '-', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (66, 'Anka Lisec', 'Slovenia', 'University of Ljubljana');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (67, 'Frédéric Cantat', 'France', 'IGN France');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (68, 'Regina Orvananos', 'Mexico', 'ONU Habitat');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (69, 'Elisabeth Leblanc', 'France', 'IGN France');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (70, 'Vents Priedoliņš', 'Latvia', 'State Land Service of Latvia');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (71, 'Aurélia Decherf', 'France', 'IGN France');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (72, 'Kholoud Saad Salama', 'Egypt', NULL);
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (73, 'Bénédicte Bucher', 'France', 'IGN France');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (74, 'Romain Vialle', 'France', 'IGN France');
INSERT INTO eventos.speakers (id, name, country_s, agency_s) VALUES (75, 'Nick Land', 'United Kingdom', 'ESRI');


--
-- TOC entry 4375 (class 0 OID 0)
-- Dependencies: 245
-- Name: agencies_id_seq; Type: SEQUENCE SET; Schema: eventos; Owner: postgres
--

SELECT pg_catalog.setval('eventos.agencies_id_seq', 23, true);


--
-- TOC entry 4376 (class 0 OID 0)
-- Dependencies: 247
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: eventos; Owner: postgres
--

SELECT pg_catalog.setval('eventos.events_id_seq', 25, true);


--
-- TOC entry 4377 (class 0 OID 0)
-- Dependencies: 249
-- Name: presentations_id_seq; Type: SEQUENCE SET; Schema: eventos; Owner: postgres
--

SELECT pg_catalog.setval('eventos.presentations_id_seq', 61, true);


--
-- TOC entry 4378 (class 0 OID 0)
-- Dependencies: 251
-- Name: speakers_id_seq; Type: SEQUENCE SET; Schema: eventos; Owner: postgres
--

SELECT pg_catalog.setval('eventos.speakers_id_seq', 75, true);


--
-- TOC entry 4180 (class 2606 OID 52583)
-- Name: agencies agencies_nombre_key; Type: CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.agencies
    ADD CONSTRAINT agencies_nombre_key UNIQUE (nombre);


--
-- TOC entry 4182 (class 2606 OID 52581)
-- Name: agencies agencies_pkey; Type: CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.agencies
    ADD CONSTRAINT agencies_pkey PRIMARY KEY (id);


--
-- TOC entry 4178 (class 2606 OID 52481)
-- Name: cities cities_pkey; Type: CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.cities
    ADD CONSTRAINT cities_pkey PRIMARY KEY (country, city);


--
-- TOC entry 4176 (class 2606 OID 52474)
-- Name: countries countries_pkey; Type: CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.countries
    ADD CONSTRAINT countries_pkey PRIMARY KEY (country);


--
-- TOC entry 4194 (class 2606 OID 52650)
-- Name: events_agencies events_agencies_pkey; Type: CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.events_agencies
    ADD CONSTRAINT events_agencies_pkey PRIMARY KEY (id_event, id_agencia);


--
-- TOC entry 4184 (class 2606 OID 52594)
-- Name: events events_event_title_key; Type: CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.events
    ADD CONSTRAINT events_event_title_key UNIQUE (event_title);


--
-- TOC entry 4186 (class 2606 OID 52592)
-- Name: events events_pkey; Type: CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- TOC entry 4192 (class 2606 OID 52635)
-- Name: presentation_speakers presentation_speakers_pkey; Type: CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.presentation_speakers
    ADD CONSTRAINT presentation_speakers_pkey PRIMARY KEY (id_presentation, id_speaker);


--
-- TOC entry 4188 (class 2606 OID 52613)
-- Name: presentations presentations_pkey; Type: CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.presentations
    ADD CONSTRAINT presentations_pkey PRIMARY KEY (id);


--
-- TOC entry 4190 (class 2606 OID 52625)
-- Name: speakers speakers_pkey; Type: CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.speakers
    ADD CONSTRAINT speakers_pkey PRIMARY KEY (id);


--
-- TOC entry 4195 (class 2606 OID 52482)
-- Name: cities fk_cities_country; Type: FK CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.cities
    ADD CONSTRAINT fk_cities_country FOREIGN KEY (country) REFERENCES eventos.countries(country) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 4202 (class 2606 OID 52656)
-- Name: events_agencies fk_events_agencies_agencia; Type: FK CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.events_agencies
    ADD CONSTRAINT fk_events_agencies_agencia FOREIGN KEY (id_agencia) REFERENCES eventos.agencies(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4203 (class 2606 OID 52651)
-- Name: events_agencies fk_events_agencies_event; Type: FK CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.events_agencies
    ADD CONSTRAINT fk_events_agencies_event FOREIGN KEY (id_event) REFERENCES eventos.events(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4196 (class 2606 OID 52600)
-- Name: events fk_events_city; Type: FK CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.events
    ADD CONSTRAINT fk_events_city FOREIGN KEY (country_e, city_e) REFERENCES eventos.cities(country, city) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 4197 (class 2606 OID 52595)
-- Name: events fk_events_country; Type: FK CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.events
    ADD CONSTRAINT fk_events_country FOREIGN KEY (country_e) REFERENCES eventos.countries(country) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- TOC entry 4200 (class 2606 OID 52636)
-- Name: presentation_speakers fk_presentation_speakers_presentation; Type: FK CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.presentation_speakers
    ADD CONSTRAINT fk_presentation_speakers_presentation FOREIGN KEY (id_presentation) REFERENCES eventos.presentations(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4201 (class 2606 OID 52641)
-- Name: presentation_speakers fk_presentation_speakers_speaker; Type: FK CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.presentation_speakers
    ADD CONSTRAINT fk_presentation_speakers_speaker FOREIGN KEY (id_speaker) REFERENCES eventos.speakers(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4198 (class 2606 OID 52614)
-- Name: presentations fk_presentations_event; Type: FK CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.presentations
    ADD CONSTRAINT fk_presentations_event FOREIGN KEY (event_title) REFERENCES eventos.events(event_title) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 4199 (class 2606 OID 52626)
-- Name: speakers fk_speakers_country; Type: FK CONSTRAINT; Schema: eventos; Owner: postgres
--

ALTER TABLE ONLY eventos.speakers
    ADD CONSTRAINT fk_speakers_country FOREIGN KEY (country_s) REFERENCES eventos.countries(country) ON UPDATE CASCADE ON DELETE RESTRICT;


-- Completed on 2025-10-25 13:29:42 UTC

--
-- PostgreSQL database dump complete
--

