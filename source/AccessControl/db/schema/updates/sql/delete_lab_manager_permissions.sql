-- Database patch to take care of the default View Access
set search_path to :schema;

-- Delete the Accreditation/Competency Manager permission from LAB tables
delete from rbac_permission_inventory where perm_name like '%MANAGER%';
delete from rbac_sub_modules where sub_module_code like '%MANAGER%';
