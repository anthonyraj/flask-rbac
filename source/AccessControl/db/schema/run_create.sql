-- RBAC Schema Creation 

-- Creating Lab Schema
drop schema if exists "emctest";
create schema "emctest";
set schema 'emctest';
\i rbac_schema.sql

drop schema if exists "universal";
create schema "universal";
set schema 'universal';
\i rbac_schema.sql

drop schema if exists "safetytest";
create schema "safetytest";
set schema 'safetytest';
\i rbac_schema.sql

-- Creating OEM Schema
drop schema if exists "collaboration";
create schema "collaboration";
set schema 'collaboration';
\i rbac_schema.sql

drop schema if exists "equipa";
create schema "equipa";
set schema 'equipa';
\i rbac_schema.sql

drop schema if exists "manufacto";
create schema "manufacto";
set schema 'manufacto';
\i rbac_schema.sql

drop schema if exists "acme";
create schema "acme";
set schema 'acme';
\i rbac_schema.sql
