-- RBAC Validation

-- Validating Lab Schema
set schema 'emctest';
\i rbac_validation.sql

set schema 'universal';
\i rbac_validation.sql

set schema 'safetytest';
\i rbac_validation.sql

-- Validating OEM Schema
set schema 'collaboration';
\i rbac_validation.sql

set schema 'equipa';
\i rbac_validation.sql

set schema 'manufacto';
\i rbac_validation.sql

set schema 'acme';
\i rbac_validation.sql
