-- =====================================================
-- 03_load_clean_data.sql
-- Project: Workforce Operations & Benefits Cost Intelligence Dashboard
-- Purpose: Create CSV file format, stage, and COPY commands
-- =====================================================

USE DATABASE WORKFORCE_OPS_BI;
USE SCHEMA CLEAN;

-- Create CSV file format
CREATE OR REPLACE FILE FORMAT CLEAN_CSV_FORMAT
    TYPE = CSV
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('', 'NULL', 'None', 'nan')
    EMPTY_FIELD_AS_NULL = TRUE;

-- Create internal stage for clean CSV files
CREATE OR REPLACE STAGE CLEAN_DATA_STAGE
    FILE_FORMAT = CLEAN_CSV_FORMAT;

-- =====================================================
-- Upload instructions
-- =====================================================
-- Upload the clean CSV files from:
-- data/clean/
--
-- Into Snowflake stage:
-- WORKFORCE_OPS_BI.CLEAN.CLEAN_DATA_STAGE
--
-- Files to upload:
-- employees_clean.csv
-- departments_clean.csv
-- payroll_clean.csv
-- benefits_enrollment_clean.csv
-- benefits_claims_clean.csv
-- vendors_clean.csv
-- operations_tickets_clean.csv
-- employee_payroll_summary.csv
-- employee_modeling.csv
-- department_scorecard.csv

-- =====================================================
-- Load clean CSV files into Snowflake tables
-- =====================================================

COPY INTO EMPLOYEES_CLEAN
FROM @CLEAN_DATA_STAGE/employees_clean.csv
FILE_FORMAT = CLEAN_CSV_FORMAT
ON_ERROR = 'CONTINUE';

COPY INTO DEPARTMENTS_CLEAN
FROM @CLEAN_DATA_STAGE/departments_clean.csv
FILE_FORMAT = CLEAN_CSV_FORMAT
ON_ERROR = 'CONTINUE';

COPY INTO PAYROLL_CLEAN
FROM @CLEAN_DATA_STAGE/payroll_clean.csv
FILE_FORMAT = CLEAN_CSV_FORMAT
ON_ERROR = 'CONTINUE';

COPY INTO BENEFITS_ENROLLMENT_CLEAN
FROM @CLEAN_DATA_STAGE/benefits_enrollment_clean.csv
FILE_FORMAT = CLEAN_CSV_FORMAT
ON_ERROR = 'CONTINUE';

COPY INTO BENEFITS_CLAIMS_CLEAN
FROM @CLEAN_DATA_STAGE/benefits_claims_clean.csv
FILE_FORMAT = CLEAN_CSV_FORMAT
ON_ERROR = 'CONTINUE';

COPY INTO VENDORS_CLEAN
FROM @CLEAN_DATA_STAGE/vendors_clean.csv
FILE_FORMAT = CLEAN_CSV_FORMAT
ON_ERROR = 'CONTINUE';

COPY INTO OPERATIONS_TICKETS_CLEAN
FROM @CLEAN_DATA_STAGE/operations_tickets_clean.csv
FILE_FORMAT = CLEAN_CSV_FORMAT
ON_ERROR = 'CONTINUE';

COPY INTO EMPLOYEE_PAYROLL_SUMMARY
FROM @CLEAN_DATA_STAGE/employee_payroll_summary.csv
FILE_FORMAT = CLEAN_CSV_FORMAT
ON_ERROR = 'CONTINUE';

COPY INTO EMPLOYEE_MODELING
FROM @CLEAN_DATA_STAGE/employee_modeling.csv
FILE_FORMAT = CLEAN_CSV_FORMAT
ON_ERROR = 'CONTINUE';

COPY INTO DEPARTMENT_SCORECARD
FROM @CLEAN_DATA_STAGE/department_scorecard.csv
FILE_FORMAT = CLEAN_CSV_FORMAT
ON_ERROR = 'CONTINUE';

-- =====================================================
-- Row count validation
-- =====================================================

SELECT 'EMPLOYEES_CLEAN' AS table_name, COUNT(*) AS row_count FROM EMPLOYEES_CLEAN
UNION ALL
SELECT 'DEPARTMENTS_CLEAN', COUNT(*) FROM DEPARTMENTS_CLEAN
UNION ALL
SELECT 'PAYROLL_CLEAN', COUNT(*) FROM PAYROLL_CLEAN
UNION ALL
SELECT 'BENEFITS_ENROLLMENT_CLEAN', COUNT(*) FROM BENEFITS_ENROLLMENT_CLEAN
UNION ALL
SELECT 'BENEFITS_CLAIMS_CLEAN', COUNT(*) FROM BENEFITS_CLAIMS_CLEAN
UNION ALL
SELECT 'VENDORS_CLEAN', COUNT(*) FROM VENDORS_CLEAN
UNION ALL
SELECT 'OPERATIONS_TICKETS_CLEAN', COUNT(*) FROM OPERATIONS_TICKETS_CLEAN
UNION ALL
SELECT 'EMPLOYEE_PAYROLL_SUMMARY', COUNT(*) FROM EMPLOYEE_PAYROLL_SUMMARY
UNION ALL
SELECT 'EMPLOYEE_MODELING', COUNT(*) FROM EMPLOYEE_MODELING
UNION ALL
SELECT 'DEPARTMENT_SCORECARD', COUNT(*) FROM DEPARTMENT_SCORECARD;