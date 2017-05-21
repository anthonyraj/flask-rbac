-- Database patch to take care of the default View Access
set search_path to :schema;

-- Update the perm_name from RFQ to PROJ
update rbac_permission_inventory set perm_name = 'PROJ_REQUEST_FOR_QUOTE_ISSUE_NOTIFICATION_EMAIL' where perm_name = 'RFQ_REQUEST_FOR_QUOTE_ISSUE_NOTIFICATION_EMAIL';

