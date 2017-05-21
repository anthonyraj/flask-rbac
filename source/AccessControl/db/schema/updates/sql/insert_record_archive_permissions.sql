-- Database patch to take care of the default View Access
set search_path to :schema;

-- Insert ARCHIVAL permissions for RECORDS
DELETE from "rbac_permission_inventory" where perm_id in (108,109);
INSERT INTO "rbac_permission_inventory" VALUES(108,3,400,'REC_ARCHIVE_RECORD','Archive record',8,0,0);
INSERT INTO "rbac_permission_inventory" VALUES(109,3,400,'REC_VIEW_ARCHIVED_RECORD','View archived records',9,0,0);

