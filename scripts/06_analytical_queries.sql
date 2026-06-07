-- ==========================================
-- 06. Analytical Queries (Gold Layer)
-- ==========================================
-- Description : Business intelligence queries for
--               revenue, cancellations, and market analysis.
-- Platform    : Snowflake
-- Author      : Shahzaman Jalil
-- ==========================================

USE DATABASE hotel_dw;
USE SCHEMA gold;

-- -------------------------------------------
-- Query 1: Year-over-Year Revenue Growth
-- -------------------------------------------
-- Compares total revenue per year and calculates YoY growth %
WITH yearly_revenue AS (
    SELECT
        d.year,
        ROUND(SUM(f.adr * (f.stays_in_weekend_nights + f.stays_in_week_nights)), 2) AS total_revenue
    FROM gold.fact_bookings f
    JOIN gold.dim_date d ON f.date_id = d.date_id
    WHERE f.is_canceled = 0
    GROUP BY d.year
)
SELECT
    year,
    total_revenue,
    LAG(total_revenue) OVER (ORDER BY year)  AS prev_year_revenue,
    ROUND(
        (total_revenue - LAG(total_revenue) OVER (ORDER BY year))
        / NULLIF(LAG(total_revenue) OVER (ORDER BY year), 0) * 100, 2
    ) AS yoy_growth_pct
FROM yearly_revenue
ORDER BY year;


-- -------------------------------------------
-- Query 2: Top 10 Countries by Total Bookings
-- -------------------------------------------
-- Identifies which countries generate the most bookings and revenue
SELECT
    c.country,
    COUNT(f.booking_id)                                                              AS total_bookings,
    ROUND(SUM(f.adr * (f.stays_in_weekend_nights + f.stays_in_week_nights)), 2)     AS total_revenue,
    ROUND(AVG(f.adr), 2)                                                             AS avg_daily_rate
FROM gold.fact_bookings f
JOIN gold.dim_customer c ON f.customer_id = c.customer_id
WHERE f.is_canceled = 0
GROUP BY c.country
ORDER BY total_bookings DESC
LIMIT 10;


-- -------------------------------------------
-- Query 3: Cancellation Rate by Hotel Type
-- -------------------------------------------
-- Shows which hotel type has higher cancellation rate
SELECT
    h.hotel_name,
    COUNT(f.booking_id)                                              AS total_bookings,
    SUM(f.is_canceled)                                               AS total_cancellations,
    ROUND(SUM(f.is_canceled) * 100.0 / COUNT(f.booking_id), 2)      AS cancellation_rate_pct
FROM gold.fact_bookings f
JOIN gold.dim_hotel h ON f.hotel_id = h.hotel_id
GROUP BY h.hotel_name
ORDER BY cancellation_rate_pct DESC;


-- -------------------------------------------
-- Query 4: Monthly Revenue Trend with Cumulative Total
-- -------------------------------------------
-- Shows month-by-month revenue and running cumulative total per year
WITH monthly_revenue AS (
    SELECT
        d.year,
        d.month,
        ROUND(SUM(f.adr * (f.stays_in_weekend_nights + f.stays_in_week_nights)), 2) AS monthly_revenue
    FROM gold.fact_bookings f
    JOIN gold.dim_date d ON f.date_id = d.date_id
    WHERE f.is_canceled = 0
    GROUP BY d.year, d.month
)
SELECT
    year,
    month,
    monthly_revenue,
    ROUND(SUM(monthly_revenue) OVER (
        PARTITION BY year ORDER BY
        CASE month
            WHEN 'January'   THEN 1  WHEN 'February'  THEN 2
            WHEN 'March'     THEN 3  WHEN 'April'     THEN 4
            WHEN 'May'       THEN 5  WHEN 'June'      THEN 6
            WHEN 'July'      THEN 7  WHEN 'August'    THEN 8
            WHEN 'September' THEN 9  WHEN 'October'   THEN 10
            WHEN 'November'  THEN 11 WHEN 'December'  THEN 12
        END
    ), 2) AS cumulative_revenue
FROM monthly_revenue
ORDER BY year,
    CASE month
        WHEN 'January'   THEN 1  WHEN 'February'  THEN 2
        WHEN 'March'     THEN 3  WHEN 'April'     THEN 4
        WHEN 'May'       THEN 5  WHEN 'June'      THEN 6
        WHEN 'July'      THEN 7  WHEN 'August'    THEN 8
        WHEN 'September' THEN 9  WHEN 'October'   THEN 10
        WHEN 'November'  THEN 11 WHEN 'December'  THEN 12
    END;


-- -------------------------------------------
-- Query 5: Top Performing Market Segments by Revenue
-- -------------------------------------------
-- Ranks market segments based on total revenue generated
WITH segment_performance AS (
    SELECT
        m.market_segment,
        m.distribution_channel,
        COUNT(f.booking_id)                                                          AS total_bookings,
        ROUND(SUM(f.adr * (f.stays_in_weekend_nights + f.stays_in_week_nights)), 2) AS total_revenue,
        ROUND(AVG(f.lead_time), 2)                                                   AS avg_lead_time,
        ROUND(SUM(f.is_canceled) * 100.0 / COUNT(f.booking_id), 2)                  AS cancellation_rate_pct
    FROM gold.fact_bookings f
    JOIN gold.dim_market m ON f.market_id = m.market_id
    GROUP BY m.market_segment, m.distribution_channel
)
SELECT
    market_segment,
    distribution_channel,
    total_bookings,
    total_revenue,
    avg_lead_time,
    cancellation_rate_pct,
    RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank
FROM segment_performance
ORDER BY revenue_rank;
