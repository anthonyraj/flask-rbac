-- RBAC Schema Creation 

-- Creating Lab Schema
drop schema if exists :schema;
create schema :schema;

set search_path to :schema;
\i rbac_schema.sql


