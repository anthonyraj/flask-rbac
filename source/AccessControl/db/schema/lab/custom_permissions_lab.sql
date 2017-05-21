--Lab:

set search_path to :schema;

--Remove perm: All EXCEPT - users, roles, acc manager, comp. manager, user activity
delete from rbac_access_control where perm_id in (select perm_id from rbac_permission_inventory where sub_module_id in (select sub_module_id from rbac_sub_modules where sub_module_code in ('AC_ENTERPRISE_SETTTINGS','AC_APPROVED_VENDORS','AC_RECORD_TYPES','AC_FILTERS','AC_PRODUCTS','DASH_LIST_VIEW','DASH_GRAPHICAL_VIEW','DASH_REPORT_VIEW','REC_LIST_VIEW','REC_AUDIT_VIEW')));

delete from rbac_permission_inventory where sub_module_id in (select sub_module_id from rbac_sub_modules where sub_module_code in ('AC_ENTERPRISE_SETTTINGS','AC_APPROVED_VENDORS','AC_RECORD_TYPES','AC_FILTERS','AC_PRODUCTS','DASH_LIST_VIEW','DASH_GRAPHICAL_VIEW','DASH_REPORT_VIEW','REC_LIST_VIEW','REC_AUDIT_VIEW'));

delete from rbac_sub_modules where sub_module_code in ('AC_ENTERPRISE_SETTTINGS','AC_APPROVED_VENDORS','AC_RECORD_TYPES','AC_FILTERS','AC_PRODUCTS','DASH_LIST_VIEW','DASH_GRAPHICAL_VIEW','DASH_REPORT_VIEW','REC_LIST_VIEW','REC_AUDIT_VIEW');
--select * from rbac_sub_modules where sub_module_code in ('AC_ENTERPRISE_SETTTINGS','AC_APPROVED_VENDORS','AC_RECORD_TYPES','AC_FILTERS','AC_PRODUCTS','DASH_LIST_VIEW','DASH_GRAPHICAL_VIEW','DASH_REPORT_VIEW','REC_LIST_VIEW','REC_AUDIT_VIEW');

--Remove module: Dashbard, records, check in projects(keep Projects List View, Edit Project only)
delete from rbac_access_control where perm_id in (select perm_id from rbac_permission_inventory where sub_module_id in (select sub_module_id from rbac_sub_modules where module_id in (select module_id  from rbac_modules where module_code in ('DASH','REC','RBAC','ALERT','FAKE'))));

delete from rbac_permission_inventory where sub_module_id in (select sub_module_id from rbac_sub_modules where module_id in (select module_id  from rbac_modules where module_code in ('DASH','REC','RBAC','ALERT','FAKE')));

delete from rbac_sub_modules where module_id in (select module_id  from rbac_modules where module_code in ('DASH','REC','RBAC','ALERT','FAKE'));
delete from rbac_modules where module_code in ('DASH','REC','RBAC','ALERT','FAKE');

--Remove Full Access from permission inventory:
delete from rbac_access_control where perm_id in (select perm_id from rbac_permission_inventory  where perm_name like '%_FULL_ACCESS%');
delete from rbac_permission_inventory where perm_name like '%_FULL_ACCESS%';

--Remove OEM Specific Notifications:
delete from rbac_permission_inventory where perm_name in ('PROJ_ACCEPT_DOCUMENT_NOTIFICATION','PROJ_DELIVERABLE_UPLOADED_NOTIFICATION','PROJ_RFQ_UPLOADED_NOTIFICATION','REC_DOCUMENT_EXPIRATION_NOTIFICATION','AC_SUSPENDED_USER_NOTIFICATION','AC_STANDARD_EXPIRATION_NOTIFICATION');
delete from rbac_sub_modules where sub_module_code='AC_NOTIFICATIONS';
