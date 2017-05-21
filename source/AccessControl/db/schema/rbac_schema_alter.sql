-- Role type changed have been merged in the master schema
-- Address the issue with the role_type for protecting the roles from being deleted
-- ALTER TABLE rbac_roles ADD COLUMN role_type integer default 0;

-- ALTER TABLE rbac_permission_inventory perm_type integer default 0;
