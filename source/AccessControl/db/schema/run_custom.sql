-- RBAC Schema Creation 

-- Creating Lab Schema
set schema 'emctest';
\i custom_permissions_lab.sql

set schema 'universal';
\i custom_permissions_lab.sql

set schema 'safetytest';
\i custom_permissions_lab.sql

-- Creating OEM Schema
set schema 'collaboration';
\i custom_permissions_oem.sql

set schema 'equipa';
\i custom_permissions_oem.sql

set schema 'manufacto';
\i custom_permissions_oem.sql

set schema 'acme';
\i custom_permissions_oem.sql
