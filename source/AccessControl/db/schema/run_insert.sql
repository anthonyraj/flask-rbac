-- Lab Schema
set schema 'emctest';
\i rbac_data.sql
\i rbac_permission_inventory_data_lab.sql
-- Users
-- user_id | role_id | login_id
INSERT INTO "rbac_users" VALUES(1,1,'araj@emctest.com');
INSERT INTO "rbac_users" VALUES(2,2,'jng@emctest.com');
INSERT INTO "rbac_users" VALUES(3,3,'sdave@emctest.com');
INSERT INTO "rbac_users" VALUES(4,4,'corta@emctest.com');
INSERT INTO "rbac_users" VALUES(5,5,'test@emctest.com');


set schema 'universal';
\i rbac_data.sql
\i rbac_permission_inventory_data_lab.sql
-- Users
-- user_id | role_id | login_id
INSERT INTO "rbac_users" VALUES(1,1,'araj@universal.com');
INSERT INTO "rbac_users" VALUES(2,2,'jng@universal.com');
INSERT INTO "rbac_users" VALUES(3,3,'sdave@universal.com');
INSERT INTO "rbac_users" VALUES(4,4,'corta@universal.com');
INSERT INTO "rbac_users" VALUES(5,5,'test@universal.com');

set schema 'safetytest';
\i rbac_data.sql
\i rbac_permission_inventory_data_lab.sql
-- Users
-- user_id | role_id | login_id
INSERT INTO "rbac_users" VALUES(1,1,'araj@safetytest.com');
INSERT INTO "rbac_users" VALUES(2,2,'jng@safetytest.com');
INSERT INTO "rbac_users" VALUES(3,3,'sdave@safetytest.com');
INSERT INTO "rbac_users" VALUES(4,4,'corta@safetytest.com');
INSERT INTO "rbac_users" VALUES(5,5,'test@usafetytest.com');

-- OEM Schema
set schema 'collaboration';
\i rbac_data.sql
\i rbac_permission_inventory_data_oem.sql
-- Users
-- user_id | role_id | login_id
INSERT INTO "rbac_users" VALUES(1,1,'araj@collaboration.com');
INSERT INTO "rbac_users" VALUES(2,2,'jng@collaboration.com');
INSERT INTO "rbac_users" VALUES(3,3,'sdave@collaboration.com');
INSERT INTO "rbac_users" VALUES(4,4,'corta@collaboration.com');
INSERT INTO "rbac_users" VALUES(5,5,'test@collaboration.com');

set schema 'equipa';
\i rbac_data.sql
\i rbac_permission_inventory_data_oem.sql
-- Users
-- user_id | role_id | login_id
INSERT INTO "rbac_users" VALUES(1,1,'araj@equipa.com');
INSERT INTO "rbac_users" VALUES(2,2,'jng@equipa.com');
INSERT INTO "rbac_users" VALUES(3,3,'corta@equipa.com');
INSERT INTO "rbac_users" VALUES(4,4,'sdave@equipa.com');
INSERT INTO "rbac_users" VALUES(5,5,'test@equipa.com');

set schema 'manufacto';
\i rbac_data.sql
\i rbac_permission_inventory_data_oem.sql
-- Users
-- user_id | role_id | login_id
INSERT INTO "rbac_users" VALUES(1,1,'sdave@manufacto.com');
INSERT INTO "rbac_users" VALUES(2,2,'corta@manufacto.com');
INSERT INTO "rbac_users" VALUES(3,3,'jng@manufacto.com');
INSERT INTO "rbac_users" VALUES(4,4,'araj@manufacto.com');
INSERT INTO "rbac_users" VALUES(5,5,'test@manufacto.com');

set schema 'acme';
\i rbac_data.sql
\i rbac_permission_inventory_data_oem.sql
-- Users
-- user_id | role_id | login_id
INSERT INTO "rbac_users" VALUES(1,1,'araj@acme.com');
INSERT INTO "rbac_users" VALUES(2,2,'jng@acme.com');
INSERT INTO "rbac_users" VALUES(3,3,'sdave@acme.com');
INSERT INTO "rbac_users" VALUES(4,4,'corta@acme.com');
INSERT INTO "rbac_users" VALUES(5,5,'test@acme.com');

