-- Database patch to take care of the default View Access
set search_path to :schema;

-- Update the perm_type to default '1' for all LIST permissions
update rbac_permission_inventory set perm_type=1 where perm_name like '%LIST%';

-- Update the Sub-module for 2 DASH sub_modules
update rbac_permission_inventory set sub_module_id=350 where perm_name in ('DASH_GRAPH_VIEW','DASH_REPORT_VIEW');

-- Update the permission description for 2 permissions
update rbac_permission_inventory set perm_description = 'View graphical dashboard' where perm_id=55;
update rbac_permission_inventory set perm_description = 'View report' where perm_id=56;

-- Delete the sub_module_id mappings since the permissions have been merged with 350
delete from rbac_sub_modules where sub_module_id in (351,352);

