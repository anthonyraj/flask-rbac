-- set schema 'emctest';

-- Modules
INSERT INTO "rbac_modules" VALUES(1,'AC','Account Configuration','Account Configuration: enables configuring flexible data types');
INSERT INTO "rbac_modules" VALUES(2,'DASH','Dashboards','');
INSERT INTO "rbac_modules" VALUES(3,'REC','Records','');
INSERT INTO "rbac_modules" VALUES(4,'PROJ','Projects','');
INSERT INTO "rbac_modules" VALUES(5,'RFQ','RFQs','');
INSERT INTO "rbac_modules" VALUES(6,'ALERT','Alerts: In-App & Email','');
INSERT INTO "rbac_modules" VALUES(20,'RBAC','RBAC Console','');

-- Fake Module
INSERT INTO "rbac_modules" VALUES(1000,'FAKE','Fake Module','');

-- Sub Modules / Screen
-- sub_module_id | module_id | sub_module_code

INSERT INTO "rbac_sub_modules" VALUES(300,1,'AC_ENTERPRISE_SETTTINGS','Enterprise settings');
INSERT INTO "rbac_sub_modules" VALUES(301,1,'AC_APPROVED_VENDORS','Approved vendors');
INSERT INTO "rbac_sub_modules" VALUES(302,1,'AC_RECORD_TYPES','Record types');
INSERT INTO "rbac_sub_modules" VALUES(303,1,'AC_USER_ROLES','User roles');
INSERT INTO "rbac_sub_modules" VALUES(304,1,'AC_USERS','Users');
INSERT INTO "rbac_sub_modules" VALUES(305,1,'AC_FILTERS','Filters');
INSERT INTO "rbac_sub_modules" VALUES(306,1,'AC_ACCREDITATION_MANAGER','Accreditation manager');
INSERT INTO "rbac_sub_modules" VALUES(307,1,'AC_COMPETENCY_MANAGER','Competency manager');
INSERT INTO "rbac_sub_modules" VALUES(308,1,'AC_USER_ACTIVITY','User activity');
INSERT INTO "rbac_sub_modules" VALUES(309,1,'AC_PRODUCTS','Products');
INSERT INTO "rbac_sub_modules" VALUES(310,1,'AC_NOTIFICATIONS','Notifications');

-- INSERT INTO "rbac_sub_modules" VALUES(310,1,'AC_RECORD_ATTRIBUTES','Record Attributes');
-- INSERT INTO "rbac_sub_modules" VALUES(306,1,'AC_FILTER_TYPES','Filter Types');

INSERT INTO "rbac_sub_modules" VALUES(350,2,'DASH_LIST_VIEW','Dashboard list view');
INSERT INTO "rbac_sub_modules" VALUES(351,2,'DASH_GRAPHICAL_VIEW','Dashboard graphical view');
INSERT INTO "rbac_sub_modules" VALUES(352,2,'DASH_REPORT_VIEW','Dashboard report view');

--INSERT INTO "rbac_sub_modules" VALUES(400,3,'REC_VIEW','View Permissions');
INSERT INTO "rbac_sub_modules" VALUES(400,3,'REC_LIST_VIEW','Records repository');
--INSERT INTO "rbac_sub_modules" VALUES(401,3,'REC_AUDIT_VIEW','Record audit view');
INSERT INTO "rbac_sub_modules" VALUES(402,3,'REC_NOTIFICATIONS','Record notifications');

INSERT INTO "rbac_sub_modules" VALUES(450,4,'PROJ_LIST_VIEW','Project list view');
INSERT INTO "rbac_sub_modules" VALUES(451,4,'PROJ_NOTIFICATIONS','Project notifications');

INSERT INTO "rbac_sub_modules" VALUES(500,5,'RFQ_LIST_VIEW','RFQ list view');
INSERT INTO "rbac_sub_modules" VALUES(501,5,'RFQ_NOTIFICATIONS','RFQ notifications');

INSERT INTO "rbac_sub_modules" VALUES(550,6,'ALERT_LIST_VIEW','Notification list view');

INSERT INTO "rbac_sub_modules" VALUES(600,20,'RBAC_CONSOLE_VIEW','RBAC console view');

-- Fake Sub Module
INSERT INTO "rbac_sub_modules" VALUES(1000,1000,'FAKE_LIST_VIEW','Fake list view');
INSERT INTO "rbac_sub_modules" VALUES(1001,1000,'FAKE_GRAPHICAL_VIEW','Fake graphical view');
INSERT INTO "rbac_sub_modules" VALUES(1002,1000,'FAKE_REPORT_VIEW','Fake report view');

-- Templates
-- template_id, template_name, template_file
INSERT INTO "rbac_templates" VALUES(1,'rbac_acount_configuration','rbac/account_config.html');
INSERT INTO "rbac_templates" VALUES(2,'rbac_dashboards','rbac/dashboards.html');
INSERT INTO "rbac_templates" VALUES(3,'rbac_records','rbac/records.html');
INSERT INTO "rbac_templates" VALUES(4,'rbac_projects','rbac/projects.html');
INSERT INTO "rbac_templates" VALUES(5,'modules_dashboards','modules/dashboards.html');
INSERT INTO "rbac_templates" VALUES(6,'modules_records','modules/records.html');
INSERT INTO "rbac_templates" VALUES(7,'modules_projects','modules/projects.html');

-- Templates Map
-- template_id, module_id, perm_id
INSERT INTO "rbac_template_map" VALUES(1,5,9);
INSERT INTO "rbac_template_map" VALUES(1,5,10);
INSERT INTO "rbac_template_map" VALUES(2,5,11);
INSERT INTO "rbac_template_map" VALUES(2,5,12);
INSERT INTO "rbac_template_map" VALUES(3,5,13);
INSERT INTO "rbac_template_map" VALUES(3,5,14);
INSERT INTO "rbac_template_map" VALUES(4,5,15);
INSERT INTO "rbac_template_map" VALUES(4,5,16);


-- Permission Details
-- perm_id | perm_type_code | entity_name | operation_name | function_name| wf_name | object_name
INSERT INTO "rbac_permission_details" (perm_id, perm_type_code, entity_name, operation_name) VALUES(1,'E','ENTERPRISE_SETTINGS','READ');
INSERT INTO "rbac_permission_details" (perm_id, perm_type_code, entity_name, operation_name) VALUES(2,'E','ENTERPRISE_SETTINGS','UPDATE');
INSERT INTO "rbac_permission_details" (perm_id, perm_type_code, entity_name, operation_name) VALUES(3,'E','DASH','READ');
INSERT INTO "rbac_permission_details" (perm_id, perm_type_code, entity_name, operation_name) VALUES(4,'E','DASH','READ');
INSERT INTO "rbac_permission_details" (perm_id, perm_type_code, entity_name, operation_name) VALUES(5,'E','RECORD','READ');
INSERT INTO "rbac_permission_details" (perm_id, perm_type_code, entity_name, operation_name) VALUES(6,'E','RECORD','UPDATE');
INSERT INTO "rbac_permission_details" (perm_id, perm_type_code, entity_name, operation_name) VALUES(7,'E','PROJ','READ');
INSERT INTO "rbac_permission_details" (perm_id, perm_type_code, entity_name, operation_name) VALUES(8,'E','PROJ','READ');
INSERT INTO "rbac_permission_details" (perm_id, perm_type_code, entity_name, operation_name) VALUES(9,'E','RECORD','UPDATE');

-- Permission Type
INSERT INTO "rbac_permission_type" VALUES(1,'E','ENTITY','Entity Permission Type');
INSERT INTO "rbac_permission_type" VALUES(2,'F','FUNCTIONALITY','Funcationality Permission Type');
INSERT INTO "rbac_permission_type" VALUES(3,'W','WORKFLOW','Workflow Permission Type');
INSERT INTO "rbac_permission_type" VALUES(4,'N','NONE','No Access Permission Type');
INSERT INTO "rbac_permission_type" VALUES(5,'A','ALL','All Access Permission Type');
INSERT INTO "rbac_permission_type" VALUES(6,'O','OBJECT','Domain Object Permission Type');

-- Roles
INSERT INTO "rbac_roles" VALUES(1,'Super Admin','Full access. All permissions. Total control.',1);
INSERT INTO "rbac_roles" VALUES(2,'Administrator','Administrator: Sample Privileges',1);
INSERT INTO "rbac_roles" VALUES(3,'Compliance Manager','Compliance Manager: Sample Privileges',1);
INSERT INTO "rbac_roles" VALUES(4,'Executive','Executive: Sample Privileges',0);
INSERT INTO "rbac_roles" VALUES(5,'Engineer','Engineer: Sample Privileges',0);
INSERT INTO "rbac_roles" VALUES(6,'Sales','Sales: Sample Privileges',0);
INSERT INTO "rbac_roles" VALUES(7,'External Collaborator','External Collaborator: Sample Privileges',0);

-- Role Types
INSERT INTO "rbac_role_type" VALUES (0, 'Role can be deleted from the system');
INSERT INTO "rbac_role_type" VALUES (1, 'Role cannot be deleted from the system');

-- Perm Types
INSERT INTO "rbac_perm_type" VALUES (0, 'Permission can be omitted in custom permissions');
INSERT INTO "rbac_perm_type" VALUES (1, 'Permission needs to be present as default');

--Other sql performed –
--INSERT INTO "rbac_roles" VALUES(5,'Test Role'); -- Role_id=5
--update rbac_users set role_id=5 where user_id=4; --(4,5,'sdave@equipa.com');
--update rbac_permission_inventory set perm_name ='DASH_LIST_VIEW' where perm_name='DASH_VIEW_RECORDS';

-- Access Control
-- acl_id, role_id, perm_id

-- SUPER ADMIN
-- Super Admin has Full Access
-- acl_id | role_id | perm_id
-- SuperAdmin has full access to all Modules
--INSERT INTO "rbac_access_control" VALUES(1,1,100);
--INSERT INTO "rbac_access_control" VALUES(2,1,101);
--INSERT INTO "rbac_access_control" VALUES(3,1,102);
--INSERT INTO "rbac_access_control" VALUES(4,1,103);
--INSERT INTO "rbac_access_control" VALUES(5,1,104);

-- MANAGER
-- Manager has no access to Account Config
-- Manager has full access to Dashboard
--INSERT INTO "rbac_access_control" VALUES(6,2,101);
-- Manager has full access to Records
--INSERT INTO "rbac_access_control" VALUES(7,2,102);
-- Manager has full access to Projects
--INSERT INTO "rbac_access_control" VALUES(8,2,103);

-- ENGINEER
-- Engineer has no access to Account Config
-- Engineer has full access to Dashboards
--INSERT INTO "rbac_access_control" VALUES(9,3,101);
-- Engineer has full access to Records
--INSERT INTO "rbac_access_control" VALUES(10,3,102);
-- Engineer has no access to Projects

-- SALES
-- Sales has no access to Account Config
-- Sales has custom access to Dashboards
--INSERT INTO "rbac_access_control" VALUES(11,4,101);
-- INSERT INTO "rbac_access_control" VALUES(12,4,4);

-- Sales has custom access to Records
-- INSERT INTO "rbac_access_control" VALUES(13,4,5);
-- INSERT INTO "rbac_access_control" VALUES(14,4,6);
-- Sales has no access to Projects


-- Users
-- user_id | role_id | login_id
-- INSERT INTO "rbac_users" VALUES(1,1,'araj@equipa.com');
-- INSERT INTO "rbac_users" VALUES(2,2,'jng@equipa.com');
-- INSERT INTO "rbac_users" VALUES(3,3,'sdave@equipa.com');
-- INSERT INTO "rbac_users" VALUES(4,4,'corta@equipa.com');

-- Entities
-- INSERT INTO "rbac_entities" VALUES(1,'RECORDS','Records Entity');
-- INSERT INTO "rbac_entities" VALUES(2,'FILTERS','Filters Entity');
-- INSERT INTO "rbac_entities" VALUES(3,'PROJECTS','Projects Entity');
-- INSERT INTO "rbac_entities" VALUES(4,'ENTERPRISE_SETTINGS','Enterprise Settings Entity');
-- INSERT INTO "rbac_entities" VALUES(5,'APPROVED_VENDORS','Approved Vendors Entity');
-- INSERT INTO "rbac_entities" VALUES(6,'RECORD_ATTRIBUTES','Record Attributes Entity');
-- INSERT INTO "rbac_entities" VALUES(7,'RECORD_TYPES','Record Types Entity');
-- INSERT INTO "rbac_entities" VALUES(8,'FILTER_TYPES','Filter Types Entity');
-- INSERT INTO "rbac_entities" VALUES(9,'ROLES','Roles Entity');
-- INSERT INTO "rbac_entities" VALUES(10,'USERS','Users Entity');

-- Operations
-- INSERT INTO "rbac_operations" VALUES(1,'CREATE','Create Entity');
-- INSERT INTO "rbac_operations" VALUES(2,'READ','Read Entity');
-- INSERT INTO "rbac_operations" VALUES(3,'UPDATE','Update Entity');
-- INSERT INTO "rbac_operations" VALUES(4,'DELETE','Delete Entity');

-- Permission Package
-- package_id | module_id | package_name | package_description
-- INSERT INTO "rbac_permission_package" VALUES(1,1,'View Enterprise Settings','');
-- INSERT INTO "rbac_permission_package" VALUES(2,1,'View and Edit Enterprise Settings','');

-- Permission Package Details
-- package_id, entity_id, operation_id, module_id
--INSERT INTO "rbac_permission_package_details" VALUES(1,4,2,1);
--INSERT INTO "rbac_permission_package_details" VALUES(2,4,2,1);
--INSERT INTO "rbac_permission_package_details" VALUES(2,4,3,1);

-- INSERT INTO "" VALUES(1,'');

-- Reset Sequences
--SELECT setval('rbac_modules_module_id_seq', (SELECT max(module_id) FROM rbac_modules));
--SELECT setval('rbac_users_user_id_seq', (SELECT max(user_id) FROM rbac_users));
--SELECT setval('rbac_access_control_acl_id_seq', (SELECT max(acl_id) FROM rbac_access_control));
--SELECT setval('rbac_roles_role_id_seq', (SELECT max(role_id) FROM rbac_roles));
--SELECT setval('rbac_permission_inventory_perm_id_seq', (SELECT max(perm_id) FROM rbac_permission_inventory));

