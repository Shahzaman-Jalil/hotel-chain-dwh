# ============================================================
#  Hotel Chain Management — Streamlit in Snowflake Dashboard
#  Paste this entire file into your Snowflake Streamlit editor
# ============================================================

import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Hotel Chain Analytics",
    page_icon="🏨",
    layout="wide",
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d1117;
    color: #e6edf3;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #f0c040 !important;
}

.kpi-card {
    background: linear-gradient(135deg, #161b22 0%, #1c2333 100%);
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 20px 16px;
    text-align: center;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    transition: transform 0.2s;
    min-height: 110px;
}
.kpi-card:hover { transform: translateY(-3px); }
.kpi-label {
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #8b949e;
    margin-bottom: 8px;
    white-space: nowrap;
}
.kpi-value {
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    color: #f0c040;
    font-weight: 700;
    white-space: nowrap;
}
.kpi-sub {
    font-size: 11px;
    color: #6e7681;
    margin-top: 4px;
    white-space: nowrap;
}

section[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #30363d;
}

div[data-testid="stMetric"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 12px 16px;
}

.stTabs [data-baseweb="tab"] {
    color: #8b949e;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    color: #f0c040 !important;
    border-bottom: 2px solid #f0c040 !important;
}

.stDataFrame { border-radius: 10px; overflow: hidden; }

footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Snowflake session ─────────────────────────────────────────
session = get_active_session()

# ── Helper ───────────────────────────────────────────────────
@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    return session.sql(sql).to_pandas()

# ── Sidebar filters ──────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏨 Hotel Analytics")
    st.markdown("---")

    years = run_query("SELECT DISTINCT year FROM hotel_dw.gold.dim_date ORDER BY year")
    year_list = years["YEAR"].tolist()
    selected_years = st.multiselect("📅 Filter by Year", year_list, default=year_list)

    hotels = run_query("SELECT DISTINCT hotel_name FROM hotel_dw.gold.dim_hotel ORDER BY hotel_name")
    hotel_list = hotels["HOTEL_NAME"].tolist()
    selected_hotels = st.multiselect("🏩 Filter by Hotel", hotel_list, default=hotel_list)

    st.markdown("---")
    st.caption("Data: Hotel Bookings 2015–2017")
    st.caption("MUET — Data Warehousing Project")

year_filter = ", ".join([f"'{y}'" for y in selected_years]) if selected_years else "'2015','2016','2017'"
hotel_filter = ", ".join([f"'{h}'" for h in selected_hotels]) if selected_hotels else "'Resort Hotel','City Hotel'"

# ── Title ────────────────────────────────────────────────────
st.markdown("<h1 style='text-align:center; font-size:42px;'>Hotel Chain Management</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8b949e; letter-spacing:3px; font-size:13px;'>ANALYTICS DASHBOARD · DATA WAREHOUSE</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── KPI Cards ────────────────────────────────────────────────
kpi_sql = f"""
SELECT
    COUNT(f.booking_id)                                                        AS total_bookings,
    ROUND(SUM(f.adr * (f.stays_in_weekend_nights + f.stays_in_week_nights)), 0) AS total_revenue,
    ROUND(SUM(f.is_canceled) * 100.0 / COUNT(f.booking_id), 1)                AS cancel_rate,
    ROUND(AVG(f.adr), 2)                                                       AS avg_adr,
    ROUND(AVG(f.stays_in_weekend_nights + f.stays_in_week_nights), 1)         AS avg_stay,
    ROUND(AVG(f.lead_time), 0)                                                 AS avg_lead
FROM hotel_dw.gold.fact_bookings f
JOIN hotel_dw.gold.dim_date d    ON f.date_id  = d.date_id
JOIN hotel_dw.gold.dim_hotel h   ON f.hotel_id = h.hotel_id
WHERE d.year IN ({year_filter})
  AND h.hotel_name IN ({hotel_filter})
"""
kpi = run_query(kpi_sql).iloc[0]

row1 = st.columns(3)
row2 = st.columns(3)
cards = [
    (row1[0], "TOTAL BOOKINGS",    f"{int(kpi['TOTAL_BOOKINGS']):,}",  "reservations"),
    (row1[1], "TOTAL REVENUE",     f"${int(kpi['TOTAL_REVENUE']):,}",  "ADR x nights"),
    (row1[2], "CANCELLATION RATE", f"{kpi['CANCEL_RATE']}%",           "of all bookings"),
    (row2[0], "AVG DAILY RATE",    f"${kpi['AVG_ADR']}",               "per night"),
    (row2[1], "AVG STAY",          f"{kpi['AVG_STAY']} nights",        "per booking"),
    (row2[2], "AVG LEAD TIME",     f"{int(kpi['AVG_LEAD'])} days",     "advance booking"),
]
for col, label, value, sub in cards:
    with col:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>{label}</div>
            <div class='kpi-value'>{value}</div>
            <div class='kpi-sub'>{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Revenue Trends",
    "🌍 Geographic",
    "🏩 Hotel & Cancellations",
    "📦 Market Segments",
    "🔍 Raw Data",
])

# ── TAB 1: Revenue Trends ────────────────────────────────────
with tab1:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Year-over-Year Revenue Growth")
        yoy_sql = f"""
        WITH yr AS (
            SELECT d.year,
                   ROUND(SUM(f.adr*(f.stays_in_weekend_nights+f.stays_in_week_nights)),2) AS total_revenue
            FROM hotel_dw.gold.fact_bookings f
            JOIN hotel_dw.gold.dim_date d  ON f.date_id  = d.date_id
            JOIN hotel_dw.gold.dim_hotel h ON f.hotel_id = h.hotel_id
            WHERE f.is_canceled = 0
              AND d.year IN ({year_filter})
              AND h.hotel_name IN ({hotel_filter})
            GROUP BY d.year
        )
        SELECT year,
               total_revenue,
               ROUND((total_revenue - LAG(total_revenue) OVER (ORDER BY year))
                     / NULLIF(LAG(total_revenue) OVER (ORDER BY year),0)*100, 2) AS yoy_growth_pct
        FROM yr ORDER BY year
        """
        yoy = run_query(yoy_sql)
        st.bar_chart(yoy.set_index("YEAR")["TOTAL_REVENUE"], color="#f0c040")
        st.dataframe(yoy, use_container_width=True)

    with col_b:
        st.subheader("Monthly Revenue Trend")
        monthly_sql = f"""
        WITH mr AS (
            SELECT d.year, d.month,
                   ROUND(SUM(f.adr*(f.stays_in_weekend_nights+f.stays_in_week_nights)),2) AS monthly_revenue
            FROM hotel_dw.gold.fact_bookings f
            JOIN hotel_dw.gold.dim_date d  ON f.date_id  = d.date_id
            JOIN hotel_dw.gold.dim_hotel h ON f.hotel_id = h.hotel_id
            WHERE f.is_canceled = 0
              AND d.year IN ({year_filter})
              AND h.hotel_name IN ({hotel_filter})
            GROUP BY d.year, d.month
        )
        SELECT year, month, monthly_revenue,
               ROUND(SUM(monthly_revenue) OVER (
                   PARTITION BY year ORDER BY
                   CASE month
                       WHEN 'January' THEN 1 WHEN 'February' THEN 2 WHEN 'March' THEN 3
                       WHEN 'April' THEN 4 WHEN 'May' THEN 5 WHEN 'June' THEN 6
                       WHEN 'July' THEN 7 WHEN 'August' THEN 8 WHEN 'September' THEN 9
                       WHEN 'October' THEN 10 WHEN 'November' THEN 11 WHEN 'December' THEN 12
                   END), 2) AS cumulative_revenue
        FROM mr
        ORDER BY year,
            CASE month
                WHEN 'January' THEN 1 WHEN 'February' THEN 2 WHEN 'March' THEN 3
                WHEN 'April' THEN 4 WHEN 'May' THEN 5 WHEN 'June' THEN 6
                WHEN 'July' THEN 7 WHEN 'August' THEN 8 WHEN 'September' THEN 9
                WHEN 'October' THEN 10 WHEN 'November' THEN 11 WHEN 'December' THEN 12
            END
        """
        monthly = run_query(monthly_sql)
        monthly["PERIOD"] = monthly["YEAR"].astype(str) + "-" + monthly["MONTH"].str[:3]
        st.line_chart(monthly.set_index("PERIOD")[["MONTHLY_REVENUE", "CUMULATIVE_REVENUE"]])

# ── TAB 2: Geographic ────────────────────────────────────────
with tab2:
    st.subheader("Top 10 Countries by Bookings & Revenue")
    geo_sql = f"""
    SELECT c.country,
           COUNT(f.booking_id) AS total_bookings,
           ROUND(SUM(f.adr*(f.stays_in_weekend_nights+f.stays_in_week_nights)),2) AS total_revenue,
           ROUND(AVG(f.adr),2) AS avg_daily_rate
    FROM hotel_dw.gold.fact_bookings f
    JOIN hotel_dw.gold.dim_customer c ON f.customer_id = c.customer_id
    JOIN hotel_dw.gold.dim_date d      ON f.date_id     = d.date_id
    JOIN hotel_dw.gold.dim_hotel h     ON f.hotel_id    = h.hotel_id
    WHERE f.is_canceled = 0
      AND d.year IN ({year_filter})
      AND h.hotel_name IN ({hotel_filter})
    GROUP BY c.country
    ORDER BY total_bookings DESC
    LIMIT 10
    """
    geo = run_query(geo_sql)
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(geo.set_index("COUNTRY")["TOTAL_BOOKINGS"], color="#f0c040")
    with col2:
        st.bar_chart(geo.set_index("COUNTRY")["TOTAL_REVENUE"], color="#3fb950")
    st.dataframe(geo, use_container_width=True)

# ── TAB 3: Hotel & Cancellations ─────────────────────────────
with tab3:
    st.subheader("Cancellation Rate by Hotel Type")
    cancel_sql = f"""
    SELECT h.hotel_name,
           COUNT(f.booking_id)                                          AS total_bookings,
           SUM(f.is_canceled)                                           AS total_cancellations,
           ROUND(SUM(f.is_canceled)*100.0/COUNT(f.booking_id), 2)      AS cancellation_rate_pct
    FROM hotel_dw.gold.fact_bookings f
    JOIN hotel_dw.gold.dim_hotel h ON f.hotel_id = h.hotel_id
    JOIN hotel_dw.gold.dim_date d  ON f.date_id  = d.date_id
    WHERE d.year IN ({year_filter})
      AND h.hotel_name IN ({hotel_filter})
    GROUP BY h.hotel_name
    ORDER BY cancellation_rate_pct DESC
    """
    cancel = run_query(cancel_sql)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Resort Hotel Cancellation", f"{cancel[cancel['HOTEL_NAME']=='Resort Hotel']['CANCELLATION_RATE_PCT'].values[0]}%" if 'Resort Hotel' in cancel['HOTEL_NAME'].values else "N/A")
    with col2:
        st.metric("City Hotel Cancellation", f"{cancel[cancel['HOTEL_NAME']=='City Hotel']['CANCELLATION_RATE_PCT'].values[0]}%" if 'City Hotel' in cancel['HOTEL_NAME'].values else "N/A")
    st.dataframe(cancel, use_container_width=True)

    st.markdown("---")
    st.subheader("Bookings by Customer Type")
    ctype_sql = f"""
    SELECT c.customer_type,
           COUNT(f.booking_id) AS bookings,
           ROUND(AVG(f.adr),2) AS avg_adr
    FROM hotel_dw.gold.fact_bookings f
    JOIN hotel_dw.gold.dim_customer c ON f.customer_id = c.customer_id
    JOIN hotel_dw.gold.dim_date d      ON f.date_id     = d.date_id
    JOIN hotel_dw.gold.dim_hotel h     ON f.hotel_id    = h.hotel_id
    WHERE f.is_canceled = 0
      AND d.year IN ({year_filter})
      AND h.hotel_name IN ({hotel_filter})
    GROUP BY c.customer_type ORDER BY bookings DESC
    """
    ctype = run_query(ctype_sql)
    st.bar_chart(ctype.set_index("CUSTOMER_TYPE")["BOOKINGS"], color="#58a6ff")

# ── TAB 4: Market Segments ───────────────────────────────────
with tab4:
    st.subheader("Market Segment Performance & Rankings")
    seg_sql = f"""
    WITH sp AS (
        SELECT m.market_segment, m.distribution_channel,
               COUNT(f.booking_id) AS total_bookings,
               ROUND(SUM(f.adr*(f.stays_in_weekend_nights+f.stays_in_week_nights)),2) AS total_revenue,
               ROUND(AVG(f.lead_time),2) AS avg_lead_time,
               ROUND(SUM(f.is_canceled)*100.0/COUNT(f.booking_id),2) AS cancellation_rate_pct
        FROM hotel_dw.gold.fact_bookings f
        JOIN hotel_dw.gold.dim_market m ON f.market_id = m.market_id
        JOIN hotel_dw.gold.dim_date d   ON f.date_id   = d.date_id
        JOIN hotel_dw.gold.dim_hotel h  ON f.hotel_id  = h.hotel_id
        WHERE d.year IN ({year_filter})
          AND h.hotel_name IN ({hotel_filter})
        GROUP BY m.market_segment, m.distribution_channel
    )
    SELECT *, RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank FROM sp ORDER BY revenue_rank
    """
    seg = run_query(seg_sql)
    st.bar_chart(seg.set_index("MARKET_SEGMENT")["TOTAL_REVENUE"], color="#f0c040")
    st.dataframe(seg, use_container_width=True)

# ── TAB 5: Raw Data ──────────────────────────────────────────
with tab5:
    st.subheader("Fact Table Sample (Top 500 rows)")
    raw_sql = f"""
    SELECT f.booking_id, h.hotel_name, d.year, d.month, d.day,
           c.country, c.customer_type, r.reserved_room_type, r.assigned_room_type,
           m.market_segment, f.adr,
           f.stays_in_weekend_nights, f.stays_in_week_nights,
           f.lead_time, f.is_canceled, f.reservation_status
    FROM hotel_dw.gold.fact_bookings f
    JOIN hotel_dw.gold.dim_hotel    h ON f.hotel_id    = h.hotel_id
    JOIN hotel_dw.gold.dim_date     d ON f.date_id     = d.date_id
    JOIN hotel_dw.gold.dim_customer c ON f.customer_id = c.customer_id
    JOIN hotel_dw.gold.dim_room     r ON f.room_id     = r.room_id
    JOIN hotel_dw.gold.dim_market   m ON f.market_id   = m.market_id
    WHERE d.year IN ({year_filter})
      AND h.hotel_name IN ({hotel_filter})
    LIMIT 500
    """
    raw = run_query(raw_sql)
    st.dataframe(raw, use_container_width=True)
    st.caption(f"Showing {len(raw)} rows")