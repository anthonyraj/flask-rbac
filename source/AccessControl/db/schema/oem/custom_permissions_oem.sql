--OEM:
--Remove perm: Accreditation, Competencies
delete from rbac_access_control where perm_id in (select perm_id from rbac_permission_inventory where sub_module_id in (select sub_module_id from rbac_sub_modules where sub_module_code in ('AC_ACCREDITATION_MANAGER','AC_COMPETENCY_MANAGER')));
delete from rbac_permission_inventory where sub_module_id in (select sub_module_id from rbac_sub_modules where sub_module_code in ('AC_ACCREDITATION_MANAGER','AC_COMPETENCY_MANAGER'));
delete from rbac_sub_modules where sub_module_code in ('AC_ACCREDITATION_MANAGER','AC_COMPETENCY_MANAGER');

--Remove module: RFQ,ALERT,RBAC,FAKE --

delete from rbac_access_control where perm_id in (select perm_id from rbac_permission_inventory where sub_module_id in (select sub_module_id from rbac_sub_modules where module_id in (select module_id from rbac_modules where module_id in (select module_id from rbac_modules where module_code in ('RFQ','ALERT','RBAC','FAKE')))));
delete from rbac_permission_inventory where sub_module_id in (select sub_module_id from rbac_sub_modules where module_id in (select module_id from rbac_modules where module_id in (select module_id from rbac_modules where module_code in ('RFQ','ALERT','RBAC','FAKE'))));
delete from rbac_sub_modules where module_id in (select module_id from rbac_modules where module_id in (select module_id from rbac_modules where module_code in ('RFQ','ALERT','RBAC','FAKE')));
delete from rbac_modules where module_code in ('RFQ','ALERT','RBAC','FAKE');

---------------------------------------------------------

--Remove Full Access from permission inventory:
delete from rbac_access_control where perm_id in (select perm_id from rbac_permission_inventory  where perm_name like '%_FULL_ACCESS%');
delete from rbac_permission_inventory where perm_name like '%_FULL_ACCESS%';

--Remove LAB Specific Notifications:
delete from rbac_permission_inventory where perm_name in ('RFQ_REQUEST_FOR_QUOTE_NOTIFICATION','RFQ_QUOTE_ACCEPTED_NOTIFICATION','RFQ_EXPIRATION_NOTIFICATION','PROJ_PROJECT_AWARD_NOTIFICATION','PROJ_PROJECT_CANCELLATION_NOTIFICATION');
