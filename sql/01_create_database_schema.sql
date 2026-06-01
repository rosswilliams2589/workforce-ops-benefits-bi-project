-- =====================================================
-- 01_create_database_schema.sql
-- Project: Workforce Operations & Benefits Cost Intelligence Dashboard
-- Purpose: Create Snowflake database and schemas
-- =====================================================

CREATE DATABASE IF NOT EXISTS WORKFORCE_OPS_BI;

CREATE SCHEMA IF NOT EXISTS WORKFORCE_OPS_BI.RAW;
CREATE SCHEMA IF NOT EXISTS WORKFORCE_OPS_BI.CLEAN;
CREATE SCHEMA IF NOT EXISTS WORKFORCE_OPS_BI.REPORTING;

USE DATABASE WORKFORCE_OPS_BI;
USE SCHEMA CLEAN;
