-- ==========================================
-- 04. Gold Layer — Dimension Tables (Star Schema)
-- ==========================================
-- Description : Build all 6 dimension tables for the
--               Star Schema from cleansed Silver data.
-- Platform    : Snowflake
-- Author      : Shahzaman Jalil
-- ==========================================

USE DATABASE hotel_dw;
USE SCHEMA gold;

-- -------------------------------------------
-- DIM_HOTEL
-- -------------------------------------------
CREATE OR REPLACE TABLE gold.dim_hotel AS
SELECT
    ROW_NUMBER() OVER (ORDER BY hotel) AS hotel_id,
    hotel                              AS hotel_name
FROM (SELECT DISTINCT hotel FROM silver.hotel_clean);

-- -------------------------------------------
-- DIM_CUSTOMER
-- -------------------------------------------
CREATE OR REPLACE TABLE gold.dim_customer AS
SELECT
    ROW_NUMBER() OVER (ORDER BY country) AS customer_id,
    country,
    customer_type,
    is_repeated_guest
FROM (SELECT DISTINCT country, customer_type, is_repeated_guest FROM silver.hotel_clean);

-- -------------------------------------------
-- DIM_DATE
-- -------------------------------------------
CREATE OR REPLACE TABLE gold.dim_date AS
SELECT
    ROW_NUMBER() OVER (ORDER BY year, month, day) AS date_id,
    year,
    month,
    day
FROM (
    SELECT DISTINCT
        arrival_date_year          AS year,
        arrival_date_month         AS month,
        arrival_date_day_of_month  AS day
    FROM silver.hotel_clean
);

-- -------------------------------------------
-- DIM_ROOM
-- -------------------------------------------
CREATE OR REPLACE TABLE gold.dim_room AS
SELECT
    ROW_NUMBER() OVER (ORDER BY reserved_room_type) AS room_id,
    reserved_room_type,
    assigned_room_type
FROM (SELECT DISTINCT reserved_room_type, assigned_room_type FROM silver.hotel_clean);

-- -------------------------------------------
-- DIM_MARKET
-- -------------------------------------------
CREATE OR REPLACE TABLE gold.dim_market AS
SELECT
    ROW_NUMBER() OVER (ORDER BY market_segment) AS market_id,
    market_segment,
    distribution_channel
FROM (SELECT DISTINCT market_segment, distribution_channel FROM silver.hotel_clean);

-- -------------------------------------------
-- DIM_AGENT
-- -------------------------------------------
CREATE OR REPLACE TABLE gold.dim_agent AS
SELECT
    ROW_NUMBER() OVER (ORDER BY agent) AS agent_id,
    agent
FROM (SELECT DISTINCT agent FROM silver.hotel_clean);
