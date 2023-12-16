--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0
-- Dumped by pg_dump version 16.0

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: smartphone; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.smartphone (
    id integer NOT NULL,
    merek text NOT NULL,
    ram integer NOT NULL,
    processor text NOT NULL,
    versi_os text NOT NULL,
    battery integer NOT NULL,
    harga bigint NOT NULL,
    layar double precision NOT NULL
);


ALTER TABLE public.smartphone OWNER TO postgres;

--
-- Data for Name: smartphone; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.smartphone (id, merek, ram, processor, versi_os, battery, harga, layar) FROM stdin;
1	Vivo Y75	8	MediaTek Dimensity 700	Android 11	5000	2850000	6.58
2	Realme 8 5G	8	MediaTek Dimensity 700	Android 11	5000	2450000	6.5
3	OPPO A78 5G	8	MediaTek Dimensity 700	Android 12	5000	3535000	6.56
4	Asus Zenfrone 10	8	Qualcomm Snapdragon 8	Android 13	4300	8499000	5.92
5	OPPO Reno8 Pro 5G	12	MediaTek Dimensity 8100	Android 12	4500	6800000	6.7
6	Xiaomi 12T 5G	8	MediaTek Dimensity 8100	Android 12	5000	6599000	6.67
7	Realme GT Neo 3	8	MediaTek Dimensity 8100	Android 12	5000	5499000	6.7
8	Asus ROG Phone 7	12	Qualcomm Snapdragon 8	Android 13	6000	12799000	6.78
9	Xiaomi 12	12	Qualcomm Snapdragon 8	Android 12	4500	8000000	6.28
10	Samsung Galaxy S22 5G	8	Qualcomm Snapdragon 8	Android 12	3700	8000000	6.1
\.


--
-- Name: smartphone smartphone_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.smartphone
    ADD CONSTRAINT smartphone_pk PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
-- By Obi Agustian (201011400884)

