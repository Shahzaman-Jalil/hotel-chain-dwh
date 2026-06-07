-- ==========================================
-- 05. Gold Layer — Fact Table
-- ==========================================
-- Description : Build central FACT_BOOKINGS table by
--               joining Silver data with all dimension tables.
-- Platform    : Snowflake
-- Author      : Shahzaman Jalil
-- ==========================================

USE DATABASE hotel_dw;
USE SCHEMA gold;

CREATE OR REPLACE TABLE gold.fact_bookings AS
SELECT
    ROW_NUMBER() OVER (ORDER BY s.hotel) AS booking_id,

    -- Foreign Keys
    h.hotel_id,
    c.customer_id,
    d.date_id,
    r.room_id,
    m.market_id,
    a.agent_id,

    -- Measures
    s.lead_time,
    s.adr,
    s.stays_in_weekend_nights,
    s.stays_in_week_nights,
    s.adults,
    s.children,
    s.babies,
    s.total_of_special_requests,
    s.days_in_waiting_list,
    s.booking_changes,

    -- Status
    s.is_canceled,
    s.reservation_status,
    s.reservation_status_date

FROM silver.hotel_clean s
JOIN gold.dim_hotel    h ON s.hotel          = h.hotel_name
JOIN gold.dim_customer c ON s.country        = c.country
                        AND s.customer_type  = c.customer_type
                        AND s.is_repeated_guest = c.is_repeated_guest
JOIN gold.dim_date     d ON s.arrival_date_year         = d.year
                        AND s.arrival_date_month        = d.month
                        AND s.arrival_date_day_of_month = d.day
JOIN gold.dim_room     r ON s.reserved_room_type = r.reserved_room_type
                        AND s.assigned_room_type = r.assigned_room_type
JOIN gold.dim_market   m ON s.market_segment     = m.market_segment
                        AND s.distribution_channel = m.distribution_channel
JOIN gold.dim_agent    a ON s.agent = a.agent;

-- Verification
SELECT COUNT(*) AS total_bookings FROM gold.fact_bookings;
SELECT * FROM gold.fact_bookings LIMIT 10;
