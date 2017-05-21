set search_path to :schema;
update rbac_permission_inventory set perm_name ='DASH_OPN_DOC' where perm_name='DASH_OPEN_DOC';
update rbac_permission_inventory set perm_name ='REC_OPN_RECORD' where perm_name='REC_OPEN_RECORD';

