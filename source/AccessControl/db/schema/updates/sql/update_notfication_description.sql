set search_path to :schema;
update rbac_permission_inventory set perm_description = replace(perm_description, 'inApp notification', 'InApp');
update rbac_permission_inventory set perm_description = replace(perm_description, 'Email notification', 'Email');
