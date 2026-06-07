-- ==========================================
-- 03. Silver Layer — Data Cleaning & Transformation
-- ==========================================
-- Description : Cleanse raw Bronze data — handle nulls,
--               standardize values, and populate Silver layer.
-- Platform    : Snowflake
-- Author      : Shahzaman Jalil
-- ==========================================

USE DATABASE hotel_dw;
USE SCHEMA silver;

CREATE OR REPLACE TABLE silver.hotel_clean AS
SELECT
    hotel,
    is_canceled,
    lead_time,
    arrival_date_year,
    arrival_date_month,
    arrival_date_week_number,
    arrival_date_day_of_month,

    stays_in_weekend_nights,
    stays_in_week_nights,

    adults,
    COALESCE(children, 0)         AS children,   -- NULL → 0
    babies,

    meal,
    COALESCE(country, 'Unknown')  AS country,    -- NULL → 'Unknown'

    market_segment,
    distribution_channel,
    is_repeated_guest,

    reserved_room_type,
    assigned_room_type,

    booking_changes,
    deposit_type,

    COALESCE(agent, -1)           AS agent,      -- NULL → -1 (no agent)

    days_in_waiting_list,
    customer_type,

    adr,
    total_of_special_requests,

    reservation_status,
    reservation_status_date

FROM bronze.hotel_raw;

-- Verification
SELECT COUNT(*) AS total_clean_rows FROM silver.hotel_clean;
