set search_path to :schema;

-- Add the new sub-module to manage Business Profile
insert into rbac_sub_modules values(309,1,'AC_BUSINESS_PROFILE','Business Profile');

-- Add the new permission 
insert into rbac_permission_inventory values(20,1,309,'AC_VIEW_BUSINESS_PROFILE','View business profile',1,1,0);
insert into rbac_permission_inventory values(21,1,309,'AC_EDIT_BUSINESS_PROFILE','Edit business profile',2,0,0);

-- Add the access control for the new permission and map it to Super Admin
delete from rbac_access_control where role_id=1 and perm_id=20;
insert into rbac_access_control (role_id, perm_id) values (1,20);
delete from rbac_access_control where role_id=1 and perm_id=21;
insert into rbac_access_control (role_id, perm_id) values (1,21);
