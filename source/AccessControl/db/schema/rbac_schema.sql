-- Permission Inventory
-- CREATE TABLE tbac_permission_inventory

-- CREATE TABLE tbac_plans

-- Modules
-- List of Modules
drop table if exists rbac_modules;
create table rbac_modules (
 module_id serial primary key ,
 module_code text not null,
 module_name text not null,
 module_description text
);

-- Sub Modules
-- List of Sub Modules
drop table if exists rbac_sub_modules;
create table rbac_sub_modules (
 sub_module_id serial primary key ,
 module_id int not null,
 sub_module_code text not null,
 sub_module_name text not null,
 sub_module_description text
);


-- Permission Inventory
-- Clone of tbac_permission_inventory (centrally managed via services)
drop table if exists rbac_permission_inventory;
create table rbac_permission_inventory (
 perm_id serial primary key ,
 module_id int not null,
 sub_module_id int,  -- not null needed
 perm_name text not null,
 perm_description text,
 sort_order int not null,
 perm_type integer default 0,
 perm_dependency integer default 0
);

-- Permission Inventory Mapping
-- drop table if exists rbac_permission_inventory_mapping;
-- create table rbac_permission_inventory_mapping (
-- id serial primary key ,
-- sub_module_id int not null,
-- sub_module_perm_id int not null,
-- perm_id text
--);


-- Permission Details
drop table if exists rbac_permission_details;
create table rbac_permission_details (
 perm_id integer not null,
 perm_type_code text not null,
 entity_name text,
 operation_name text,
 function_name text,
 workflow_name text,
 object_name text
);

-- Permission Type
drop table if exists rbac_permission_type;
create table rbac_permission_type (
 perm_type_id serial primary key ,
 perm_type_code text not null,
 perm_type_name text not null,
 perm_type_description text
);
	
-- Roles 
-- role_type=1 means the role is a permanent role
-- role_type=0 means the role is a temporary role 
drop table if exists rbac_roles;
create table rbac_roles (
 role_id serial primary key ,
 role_name text not null,
 role_description text,
 role_type integer default 0
);

-- Access Control
drop table if exists rbac_access_control;
create table rbac_access_control (
 acl_id serial primary key ,
 role_id integer not null,
 perm_id integer not null
);

-- Users
drop table if exists rbac_users;
create table rbac_users (
 user_id serial primary key ,
 role_id integer not null,
 login_id text not null
);

-- Templates
drop table if exists rbac_templates;
create table rbac_templates (
 template_id serial primary key ,
 template_name text,
 template_file text
);

-- Template Mapping
drop table if exists rbac_template_map;
create table rbac_template_map (
 template_id int,
 module_id int,
 perm_id int
);

-- Role Type
drop table if exists rbac_role_type;
create table rbac_role_type (
 role_type int,
 role_type_description text
);

-- Role Type
drop table if exists rbac_perm_type;
create table rbac_perm_type (
 perm_type int,
 perm_type_description text
);

-- Entities
-- drop table if exists rbac_entities;
-- create table rbac_entity (
--  entity_id serial primary key ,
--  entity_name text not null,
--  entity_description text
-- );

-- Operations
-- drop table if exists rbac_operations;
-- create table rbac_operations (
--  operation_id serial primary key ,
--  operation_name text not null,
--  operation_description text
-- );

-- Permission Package
-- drop table if exists rbac_permission_package;
-- create table rbac_permission_package (
--  package_id serial primary key,
--  module_id integer,
--  package_name text not null,
--  package_description text
-- );

-- Permission Package Details
-- drop table if exists rbac_permission_package_details;
-- create table rbac_permission_package_details (
--  package_id integer not null ,
--  permission_id integer
-- );
