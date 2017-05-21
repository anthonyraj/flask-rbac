-- Role type changes have been merged in the master
-- Address the issue with the role_type for protecting the roles from being deleted
--UPDATE rbac_roles set role_type=1 where role_id in (1,2,3);
--UPDATE rbac_roles set role_type=0 where role_id in (4,5,6,7);

