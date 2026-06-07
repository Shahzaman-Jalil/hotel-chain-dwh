-- ==========================================
-- 02. Bronze Layer — Staging & Raw Ingestion
-- ==========================================
-- Description : Create external stage, define raw table
--               schema, and load CSV data into Bronze layer.
-- Platform    : Snowflake
-- Author      : Shahzaman Jalil
-- ==========================================

USE DATABASE hotel_dw;
USE SCHEMA bronze;

-- Define stage for file ingestion
CREATE OR REPLACE STAGE bronze.hotel_stage
FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1);

-- Define raw table structure matching CSV source schema
CREATE OR REPLACE TABLE bronze.hotel_raw (
    hotel                           STRING,
    is_canceled                     INT,
    lead_time                       INT,
    arrival_date_year               INT,
    arrival_date_month              STRING,
    arrival_date_week_number        INT,
    arrival_date_day_of_month       INT,
    stays_in_weekend_nights         INT,
    stays_in_week_nights            INT,
    adults                          INT,
    children                        FLOAT,
    babies                          INT,
    meal                            STRING,
    country                         STRING,
    market_segment                  STRING,
    distribution_channel            STRING,
    is_repeated_guest               INT,
    previous_cancellations          INT,
    previous_bookings_not_canceled  INT,
    reserved_room_type              STRING,
    assigned_room_type              STRING,
    booking_changes                 INT,
    deposit_type                    STRING,
    agent                           FLOAT,
    company                         FLOAT,
    days_in_waiting_list            INT,
    customer_type                   STRING,
    adr                             FLOAT,
    required_car_parking_spaces     INT,
    total_of_special_requests       INT,
    reservation_status              STRING,
    reservation_status_date         DATE
);

-- Load data from stage into Bronze table
-- Note: 'NA' and empty strings are treated as NULL
COPY INTO bronze.hotel_raw
FROM @bronze.hotel_stage/hotel_bookings.csv
FILE_FORMAT = (
    TYPE       = 'CSV'
    SKIP_HEADER = 1
    NULL_IF    = ('NULL', 'null', '', 'NA')
);

-- Verification
SELECT COUNT(*) AS total_rows  FROM bronze.hotel_raw;
SELECT *                       FROM bronze.hotel_raw LIMIT 10;
