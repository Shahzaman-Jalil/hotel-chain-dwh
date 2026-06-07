# 🏨 Hotel Chain Management — Data Warehouse Project

A production-grade, end-to-end **Data Warehouse & Analytics** solution built on **Snowflake**, processing 119,390 hotel booking records using **Medallion Architecture** and a fully normalized **Star Schema**.

---

## 📌 Project Overview

This project transforms raw hotel booking data into a structured analytical model to support business intelligence and data-driven decision-making in the hospitality industry.

**Dataset:** 119,390 booking records | 2015–2017 | 178 countries | 7 market segments

---

## 🏗️ Architecture — Medallion Design

```
Raw CSV  →  Bronze Layer  →  Silver Layer  →  Gold Layer  →  Streamlit Dashboard
             (Ingestion)      (Cleansing)     (Star Schema)
```

| Layer | Description |
|-------|-------------|
| 🟫 **Bronze** | Landing zone for raw CSV ingestion. Preserves original data lineage. |
| 🥈 **Silver** | Data cleaning — null handling, type casting, standardization. |
| 🥇 **Gold** | Star Schema with 1 Fact Table + 6 Dimension Tables for analytics. |

---

## ⭐ Star Schema Design

```
                    DIM_HOTEL
                       │
DIM_AGENT ──── FACT_BOOKINGS ──── DIM_CUSTOMER
                  │         │
              DIM_DATE   DIM_ROOM
                  │
              DIM_MARKET
```

**Fact Table:** `fact_bookings` — booking_id, measures (adr, lead_time, stays, etc.), status

**Dimension Tables:**
- `dim_hotel` — Hotel type
- `dim_customer` — Country, customer type, repeat guest flag
- `dim_date` — Year, month, day
- `dim_room` — Reserved & assigned room types
- `dim_market` — Market segment & distribution channel
- `dim_agent` — Booking agent

---

## 🚀 Tech Stack

| Tool | Purpose |
|------|---------|
| **Snowflake** | Cloud Data Platform (Warehouses, Stages, CTAS) |
| **SQL** | ETL, Data Modeling (CTEs, Window Functions, Joins) |
| **Python / Pandas** | Data exploration & transformation |
| **Streamlit** | Interactive analytics dashboard |
| **Jupyter Notebook** | ETL pipeline development |

---

## 📁 Repository Structure

```
hotel-chain-dwh/
│
├── datasets/
│   └── hotel_bookings.csv          # Raw source data (119,390 records)
│
├── scripts/
│   ├── 01_infrastructure_setup.sql # Database, schemas, warehouse setup
│   ├── 02_bronze_ingestion.sql     # Stage creation & raw data load
│   ├── 03_silver_cleaning.sql      # Null handling & data cleansing
│   ├── 04_gold_dimensions.sql      # 6 Dimension tables (Star Schema)
│   ├── 05_gold_fact_table.sql      # Central Fact table with all joins
│   └── 06_analytical_queries.sql   # Business intelligence queries
│
├── notebooks/
│   └── Hotel_Chain_ETL.ipynb       # Python ETL pipeline notebook
│
├── dashboard/
│   └── app.py                      # Streamlit dashboard application
│
├── docs/
│   ├── ERD.PNG                     # Entity Relationship Diagram
│   └── ERD.html                    # Interactive ERD
│
└── README.md
```

---

## 📊 Analytical Queries

Five business intelligence queries built on the Gold layer:

1. **Year-over-Year Revenue Growth** — YoY revenue comparison with growth %
2. **Top 10 Countries by Bookings** — Revenue & booking volume by country
3. **Cancellation Rate by Hotel Type** — Which hotel type cancels more
4. **Monthly Revenue Trend** — Month-by-month revenue with cumulative total
5. **Market Segment Performance** — Revenue ranking by market segment

---

## 🛠️ How to Run

**Prerequisites:** Snowflake account, Python 3.8+, Streamlit

**Step 1 — Run SQL scripts in order:**
```sql
-- Run in Snowflake worksheet in this exact order:
01_infrastructure_setup.sql
02_bronze_ingestion.sql
03_silver_cleaning.sql
04_gold_dimensions.sql
05_gold_fact_table.sql
06_analytical_queries.sql
```

**Step 2 — Upload dataset to Snowflake stage:**
```sql
PUT file://datasets/hotel_bookings.csv @bronze.hotel_stage;
```

**Step 3 — Run Streamlit dashboard:**
```bash
pip install streamlit pandas snowflake-connector-python
streamlit run dashboard/app.py
```

---

## 👤 Author

**Shahzaman Jalil**
[![GitHub](https://img.shields.io/badge/GitHub-Shahzaman--Jalil-181717?logo=github)](https://github.com/Shahzaman-Jalil)
