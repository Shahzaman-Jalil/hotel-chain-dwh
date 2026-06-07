-- ==========================================
-- 01. Infrastructure Setup
-- ==========================================
-- Description : Initialize database, medallion schemas,
--               and compute warehouse for hotel_dw project.
-- Platform    : Snowflake
-- Author      : Shahzaman Jalil
-- ==========================================

-- Initialize database
CREATE OR REPLACE DATABASE hotel_dw;
USE DATABASE hotel_dw;

-- Create medallion architecture schemas
CREATE OR REPLACE SCHEMA bronze;
CREATE OR REPLACE SCHEMA silver;
CREATE OR REPLACE SCHEMA gold;

-- Configure compute warehouse
CREATE OR REPLACE WAREHOUSE hotel_wh
WITH WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND    = 60
AUTO_RESUME     = TRUE;
