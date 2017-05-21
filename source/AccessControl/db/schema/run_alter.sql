-- RBAC Schema Alteration

-- Creating Lab Schema
set schema 'emctest';
\i rbac_schema_alter.sql

set schema 'universal';
\i rbac_schema_alter.sql

set schema 'safetytest';
\i rbac_schema_alter.sql

-- Creating OEM Schema
set schema 'collaboration';
\i rbac_schema_alter.sql

set schema 'equipa';
\i rbac_schema_alter.sql

set schema 'manufacto';
\i rbac_schema_alter.sql

set schema 'acme';
\i rbac_schema_alter.sql
