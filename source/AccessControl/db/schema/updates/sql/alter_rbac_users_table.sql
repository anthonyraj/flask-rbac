-- Database patch to take care of the default View Access
set search_path to :schema;

--- Alter the rbac_users table to include an additional column called 'is_suspended'
--- ALTER table rbac_users delete column is_suspended;
ALTER table rbac_users add column is_suspended integer not null default 0;
