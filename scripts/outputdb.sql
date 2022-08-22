
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET default_tablespace = '';
SET default_with_oids = false;


CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    category VARCHAR(30),
    stars SMALLINT,
    price_in_pounds REAL,
    in_stock BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);