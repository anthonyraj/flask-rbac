set search_path to :schema;

SELECT setval('rbac_modules_module_id_seq', (SELECT max(module_id) FROM rbac_modules));
SELECT setval('rbac_users_user_id_seq', (SELECT max(user_id) FROM rbac_users));
SELECT setval('rbac_access_control_acl_id_seq', (SELECT max(acl_id) FROM rbac_access_control));
SELECT setval('rbac_roles_role_id_seq', (SELECT max(role_id) FROM rbac_roles));
SELECT setval('rbac_permission_inventory_perm_id_seq', (SELECT max(perm_id) FROM rbac_permission_inventory));
