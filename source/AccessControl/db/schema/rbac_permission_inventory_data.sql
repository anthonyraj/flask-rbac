-- Permission Inventory
-- perm_id | module_id | sub_module_id | perm_name | perm_description
-- START: ACCOUNT CONFIG
-- module_code: AC , module_id:1

-- DEFAULT Permission is used for high-level URL view
-- sub_module_id = 1000 because it does not actually belong to any sub_module
INSERT INTO "rbac_permission_inventory" VALUES(1,1,1000,'AC_DEFAULT','View Dashboard Default for Config Link',0);
INSERT INTO "rbac_permission_inventory" VALUES(2,1,300,'AC_VIEW_ENTERPRISE_SETTINGS','View enterprise settings',1);
INSERT INTO "rbac_permission_inventory" VALUES(3,1,300,'AC_EDIT_ENTERPRISE_SETTINGS','Edit enterprise settings',2);

INSERT INTO "rbac_permission_inventory" VALUES(4,1,301,'AC_VIEW_APPROVED_VENDORS','View approved vendors',1);
INSERT INTO "rbac_permission_inventory" VALUES(5,1,301,'AC_EDIT_APPROVED_VENDORS','Edit approved vendors',2);

INSERT INTO "rbac_permission_inventory" VALUES(6,1,302,'AC_VIEW_RECORD_TYPES','View record types',1);
INSERT INTO "rbac_permission_inventory" VALUES(7,1,302,'AC_ADD_RECORD_TYPES','Add record types',2);
INSERT INTO "rbac_permission_inventory" VALUES(8,1,302,'AC_EDIT_RECORD_TYPES','Edit record types',3);

INSERT INTO "rbac_permission_inventory" VALUES(9,1,303,'AC_VIEW_USER_ROLES','View user roles',1);
INSERT INTO "rbac_permission_inventory" VALUES(10,1,303,'AC_ADD_USER_ROLES','Add user roles',2);
INSERT INTO "rbac_permission_inventory" VALUES(11,1,303,'AC_EDIT_USER_ROLES','Edit user roles',3);

INSERT INTO "rbac_permission_inventory" VALUES(12,1,304,'AC_VIEW_USERS','view users',1);
INSERT INTO "rbac_permission_inventory" VALUES(13,1,304,'AC_ADD_USERS','add users',2);
INSERT INTO "rbac_permission_inventory" VALUES(14,1,304,'AC_EDIT_USERS','edit users',3);


INSERT INTO "rbac_permission_inventory" VALUES(15,1,306,'AC_VENDOR_VIEW_ACCREDITATION_MANAGER','View accreditation manager',1);
INSERT INTO "rbac_permission_inventory" VALUES(16,1,306,'AC_VENDOR_EDIT_ACCREDITATION_MANAGER','Edit accreditation manager',2);
INSERT INTO "rbac_permission_inventory" VALUES(17,1,307,'AC_VENDOR_VIEW_COMPETENCY_MANAGER','View competency manager',3);
INSERT INTO "rbac_permission_inventory" VALUES(18,1,307,'AC_VENDOR_EDIT_COMPETENCY_MANAGER','Edit competency manager',4);

INSERT INTO "rbac_permission_inventory" VALUES(19,1,308,'AC_VIEW_USER_ACTIVITY','View user activity',1);

INSERT INTO "rbac_permission_inventory" VALUES(20,1,309,'AC_VIEW_PRODUCTS','View product list',1);
INSERT INTO "rbac_permission_inventory" VALUES(21,1,309,'AC_ADD_PRODUCT','Add product',2);
INSERT INTO "rbac_permission_inventory" VALUES(22,1,309,'AC_EDIT_PRODUCT','Edit product',3);
INSERT INTO "rbac_permission_inventory" VALUES(23,1,309,'AC_EDIT_PRODUCT_SPEC','Edit product specifications',4);
INSERT INTO "rbac_permission_inventory" VALUES(24,1,309,'PROJ_ADD_PRODUCT_FAMILY','Add product family',5);
INSERT INTO "rbac_permission_inventory" VALUES(25,1,309,'PROJ_EDIT_PRODUCT_FAMILY','Edit product family',6);

INSERT INTO "rbac_permission_inventory" VALUES(26,1,305,'AC_CREATE_PERSONAL_FILTER','Save personal filters',1);
INSERT INTO "rbac_permission_inventory" VALUES(27,1,305,'AC_CREATE_PUBLIC_FILTER','Save public filters',2);

INSERT INTO "rbac_permission_inventory" VALUES(28,1,310,'AC_SUSPENDED_USER_NOTIFICATION_INAPP','Suspended user (inApp notification)',1);
INSERT INTO "rbac_permission_inventory" VALUES(29,1,310,'AC_STANDARD_EXPIRATION_NOTIFICATION_INAPP','Standard expiration (inApp notification)',2);
-- END: ACCOUNT CONFIG

-- START: DASHBOARD
-- module_code: DASH, module_id:2
--INSERT INTO "rbac_permission_inventory" VALUES(50,2,350,'DASH_DEFAULT','View Dashboard Default for Dashboard Link');
INSERT INTO "rbac_permission_inventory" VALUES(51,2,350,'DASH_LIST_VIEW','View compliance dashboard',1);
INSERT INTO "rbac_permission_inventory" VALUES(52,2,350,'DASH_VIEW_RECORDS','Display compliance records',2);
INSERT INTO "rbac_permission_inventory" VALUES(53,2,350,'DASH_OPEN_DOC','Open records',3);
INSERT INTO "rbac_permission_inventory" VALUES(54,2,350,'DASH_DOWNLOAD_DOC','Download records',4);

INSERT INTO "rbac_permission_inventory" VALUES(55,2,351,'DASH_GRAPH_VIEW','View Dashboard Graphical View',1);
INSERT INTO "rbac_permission_inventory" VALUES(56,2,352,'DASH_REPORT_VIEW','View Dashboard Report View',1);

--INSERT INTO "rbac_permission_inventory" VALUES(57,2,350,'DASH_VIEW_DOC_DETAILS','View document details');
--INSERT INTO "rbac_permission_inventory" VALUES(58,2,350,'DASH_VIEW_EXPIRED_RECORDS','View Expired Records');

--INSERT INTO "rbac_permission_inventory" VALUES(59,2,352,'DASH_GRAPH_TIMELINE_EXPIRATIONS','Timelie expiration graph');
--INSERT INTO "rbac_permission_inventory" VALUES(60,2,352,'DASH_GRAPH_CERT_STATUS_BY_PERCENTAGE_DISTRIBUTION','Certification status by percentage distribution');
--INSERT INTO "rbac_permission_inventory" VALUES(61,2,352,'DASH_GRAPH_CERT_STATUS_BY_GEO','Certification status by geography');

-- END: DASHBOARD

-- START: RECORD
--INSERT INTO "rbac_permission_inventory" VALUES(100,3,400,'REC_DEFAULT','View Records Default');
--INSERT INTO "rbac_permission_inventory" VALUES(101,3,400,'REC_VIEW_RECORD','View Record');
INSERT INTO "rbac_permission_inventory" VALUES(101,3,400,'REC_LIST_VIEW','View records list',1);
INSERT INTO "rbac_permission_inventory" VALUES(102,3,400,'REC_ADD_RECORD','Add record',2); 
INSERT INTO "rbac_permission_inventory" VALUES(103,3,400,'REC_EDIT_RECORD','Edit record',3);

INSERT INTO "rbac_permission_inventory" VALUES(104,3,400,'REC_PUBLISH_CONCEAL_RECORD','Publish/Conceal record',4);
INSERT INTO "rbac_permission_inventory" VALUES(105,3,400,'REC_OPEN_RECORD','Open record',5);
INSERT INTO "rbac_permission_inventory" VALUES(106,3,400,'REC_DOWNLOAD_RECORD','Download record',6);
INSERT INTO "rbac_permission_inventory" VALUES(107,3,400,'REC_DELETE_RECORD','Delete record',7);

--INSERT INTO "rbac_permission_inventory" VALUES(105,3,401,'REC_AUDIT_VIEW','Records Audit View');
--INSERT INTO "rbac_permission_inventory" VALUES(106,3,400,'REC_SHARE_RECORD','Share Record');

--INSERT INTO "rbac_permission_inventory" VALUES(110,3,400,'REC_VIEW_RECORD_DETAILS','View Document Details');

INSERT INTO "rbac_permission_inventory" VALUES(112,3,402,'REC_DOCUMENT_EXPIRATION_NOTIFICATION_INAPP','Record expiration (inApp notification)',1);
INSERT INTO "rbac_permission_inventory" VALUES(113,3,402,'REC_DOCUMENT_EXPIRATION_NOTIFICATION_EMAIL','Record expiration (email notification)',2);

-- END: RECORD

-- START: PROJECT
--INSERT INTO "rbac_permission_inventory" VALUES(150,4,450,'PROJ_DEFAULT','View Projects Default');

-- LAB/OEM PERM
INSERT INTO "rbac_permission_inventory" VALUES(151,4,450,'PROJ_LIST_VIEW','View projects list',1);

-- OEM PERM
INSERT INTO "rbac_permission_inventory" VALUES(152,4,450,'PROJ_NEW_PROJECT','Add project',2);
INSERT INTO "rbac_permission_inventory" VALUES(153,4,450,'PROJ_EDIT_PROJECT','Edit Project',3);
INSERT INTO "rbac_permission_inventory" VALUES(154,4,450,'PROJ_DELETE_PROJECT','Cancel/ Delete a Project',4);

-- LAB PERM
INSERT INTO "rbac_permission_inventory" VALUES(155,4,450,'PROJ_EDIT_PROJECT','Access and Edit Project',2); 

-- INSERT INTO "rbac_permission_inventory" VALUES(155,4,450,'PROJ_OPEN_PROJECT','Open Project');
-- INSERT INTO "rbac_permission_inventory" VALUES(156,4,450,'PROJ_CANCEL_PROJECT','Cancel Project');

-- OEM PROJECT NOTIFICATIOINS
INSERT INTO "rbac_permission_inventory" VALUES(157,4,451,'RFQ_REQUEST_FOR_QUOTE_ISSUE_NOTIFICATION_INAPP','RFQ issue successful self confirmation (inApp)',1);
INSERT INTO "rbac_permission_inventory" VALUES(158,4,451,'PROJ_RFQ_UPLOADED_NOTIFICATION_EMAIL','Quote submitted by vendor (email)',2);
INSERT INTO "rbac_permission_inventory" VALUES(159,4,451,'PROJ_DELIVERABLE_UPLOADED_NOTIFICATION_INAPP','Deliverable submitted by vendor (inApp)',3);
INSERT INTO "rbac_permission_inventory" VALUES(160,4,451,'PROJ_DELIVERABLE_UPLOADED_NOTIFICATION_EMAIL','Deliverable submitted by vendor (email)',4);
INSERT INTO "rbac_permission_inventory" VALUES(161,4,451,'PROJ_SUPPORTING_DOCUMENT_UPLOAD_NOTIFICATION_INAPP','Supporting files submitted by vendor (inApp)',5);

INSERT INTO "rbac_permission_inventory" VALUES(162,4,451,'PROJ_DOCUMENT_ACCEPTANCE_NOTIFICATION_INAPP','Accept Document Notification (inApp)');
INSERT INTO "rbac_permission_inventory" VALUES(163,4,451,'PROJ_DOCUMENT_ACCEPTANCE_NOTIFICATION_EMAIL','Accept Document Notification (email)');

-- LAB PROJECT NOTIFICATIONS
INSERT INTO "rbac_permission_inventory" VALUES(164,4,451,'PROJ_PROJECT_AWARD_NOTIFICATION_INAPP','Project awarded (inApp)',1);
INSERT INTO "rbac_permission_inventory" VALUES(165,4,451,'PROJ_PROJECT_AWARD_NOTIFICATION_EMAIL','Project awarded (email)',2);
INSERT INTO "rbac_permission_inventory" VALUES(166,4,451,'PROJ_PROJECT_AWARD_NOTIFICATION_INAPP','Project awarded (inApp)',1);
INSERT INTO "rbac_permission_inventory" VALUES(167,4,451,'PROJ_PROJECT_AWARD_NOTIFICATION_EMAIL','Project awarded (email)',2);

INSERT INTO "rbac_permission_inventory" VALUES(168,4,451,'PROJ_PROJECT_CANCELLATION_NOTIFICATION_EMAIL','Project Cancellation Notification (email)');

-- END: PROJECT

-- START: RFQ
INSERT INTO "rbac_permission_inventory" VALUES(170,5,500,'RFQ_LIST_VIEW','RFQ List View');
INSERT INTO "rbac_permission_inventory" VALUES(171,5,500,'RFQ_EDIT_RFQ','Edit RFQ');

-- LAB RFQ NOTIFICATIONS
INSERT INTO "rbac_permission_inventory" VALUES(172,5,501,'RFQ_REQUEST_FOR_QUOTE_NOTIFICATION','Request for Quote Notification');
INSERT INTO "rbac_permission_inventory" VALUES(173,5,501,'RFQ_QUOTE_ACCEPTED_NOTIFICATION','Quote Acceptance Notification');
INSERT INTO "rbac_permission_inventory" VALUES(174,5,501,'RFQ_EXPIRATION_NOTIFICATION','Quote Expiration Notification');
-- END: RFQ

-- START: ALERT
INSERT INTO "rbac_permission_inventory" VALUES(180,6,550,'ALERT_LIST_VIEW','View Alert Notifications');
INSERT INTO "rbac_permission_inventory" VALUES(181,6,550,'ALERT_DELETE_ALERT','Delete Alert Notifications');
-- END: ALERT

-- START: RBAC
INSERT INTO "rbac_permission_inventory" VALUES(200,20,600,'RBAC_VIEW_AC','View Account Configuration Console');
INSERT INTO "rbac_permission_inventory" VALUES(201,20,600,'RBAC_EDIT_AC','Edit Account Configuration RBAC Console');
INSERT INTO "rbac_permission_inventory" VALUES(202,20,600,'RBAC_VIEW_DASH','View Dashboard RBAC Console');
INSERT INTO "rbac_permission_inventory" VALUES(203,20,600,'RBAC_EDIT_DASH','Edit Dashboard RBAC Console');
INSERT INTO "rbac_permission_inventory" VALUES(204,20,600,'RBAC_VIEW_REC','View Records RBAC Console');
INSERT INTO "rbac_permission_inventory" VALUES(205,20,600,'RBAC_EDIT_REC','Edit Records RBAC Console');
INSERT INTO "rbac_permission_inventory" VALUES(206,20,600,'RBAC_VIEW_PROJECT','View Projects RBAC Console');
INSERT INTO "rbac_permission_inventory" VALUES(207,20,600,'RBAC_EDIT_PROJECT','Edit Projects RBAC Console');
INSERT INTO "rbac_permission_inventory" VALUES(208,20,1000,'RBAC_DEFAULT','View RBAC Default');
-- END: RBAC

-- Adding Submodule direct permissions for permission_inventory
INSERT INTO "rbac_permission_inventory" VALUES(300,1,300,'AC_ENTERPRISE_SETTTINGS_FULL_ACCESS','Enterprise Settings Full Access');
INSERT INTO "rbac_permission_inventory" VALUES(301,1,301,'AC_APPROVED_VENDORS_FULL_ACCESS','Approved Vendors Full Access');
INSERT INTO "rbac_permission_inventory" VALUES(302,1,302,'AC_RECORD_TYPES_FULL_ACCESS','Record Types Full Access');
INSERT INTO "rbac_permission_inventory" VALUES(303,1,303,'AC_USER_ROLES_FULL_ACCESS','User Roles Full Access');
INSERT INTO "rbac_permission_inventory" VALUES(304,1,304,'AC_USERS_FULL_ACCESS','Users Full Access');
INSERT INTO "rbac_permission_inventory" VALUES(305,1,305,'AC_FILTERS_FULL_ACCESS','Filters Full Access');
--INSERT INTO "rbac_permission_inventory" VALUES(306,1,306,'AC_FILTER_TYPES_FULL_ACCESS','Filter Types Full Access');
INSERT INTO "rbac_permission_inventory" VALUES(306,1,306,'AC_ACCREDITATION_MANAGER_FULL_ACCESS','Accreditation Manager Full Access');
INSERT INTO "rbac_permission_inventory" VALUES(307,1,307,'AC_COMPETENCY_MANAGER_FULL_ACCESS','Competency Manager Full Access');
INSERT INTO "rbac_permission_inventory" VALUES(308,1,308,'AC_USER_ACTIVITY_FULL_ACCESS','User Activity Full Access');
INSERT INTO "rbac_permission_inventory" VALUES(309,1,309,'AC_PRODUCTS_FULL_ACCESS','Products Full Access');

INSERT INTO "rbac_permission_inventory" VALUES(350,2,350,'DASH_LIST_VIEW_FULL_ACCESS','Dashboard List View Full Access');
INSERT INTO "rbac_permission_inventory" VALUES(351,2,351,'DASH_GRAPHICAL_VIEW_FULL_ACCESS','Dashboard Graphical View Full Access');
INSERT INTO "rbac_permission_inventory" VALUES(352,2,352,'DASH_REPORT_VIEW_FULL_ACCESS','Dashboard Report View Full Access');

INSERT INTO "rbac_permission_inventory" VALUES(360,3,400,'REC_LIST_VIEW_FULL_ACCESS','Record List View Full Access');
INSERT INTO "rbac_permission_inventory" VALUES(361,3,401,'REC_AUDIT_VIEW_FULL_ACCESS','Record Audit View Full Access');

INSERT INTO "rbac_permission_inventory" VALUES(370,4,450,'PROJ_LIST_VIEW_FULL_ACCESS','Project List View Full Access');

INSERT INTO "rbac_permission_inventory" VALUES(380,5,500,'RFQ_LIST_VIEW_FULL_ACCESS','RFQ List View Full Access');

INSERT INTO "rbac_permission_inventory" VALUES(390,6,550,'ALERT_LIST_VIEW_FULL_ACCESS','Notificaitons List View Full Access');

-- FULL ACCESS
-- sub_module_id = 2000 because it does not actually belong to any sub_module
INSERT INTO "rbac_permission_inventory" VALUES(400,1,2000,'AC_FULL_ACCESS','All Access');
INSERT INTO "rbac_permission_inventory" VALUES(401,2,2000,'DASH_FULL_ACCESS','All Access');
INSERT INTO "rbac_permission_inventory" VALUES(402,3,2000,'REC_FULL_ACCESS','All Access');
INSERT INTO "rbac_permission_inventory" VALUES(403,4,2000,'PROJ_FULL_ACCESS','All Access');
INSERT INTO "rbac_permission_inventory" VALUES(404,5,2000,'RFQ_FULL_ACCESS','All Access');
INSERT INTO "rbac_permission_inventory" VALUES(405,6,2000,'ALERT_FULL_ACCESS','All Access');
INSERT INTO "rbac_permission_inventory" VALUES(406,20,2000,'RBAC_FULL_ACCESS','All Access');

-- Fake Permissions
INSERT INTO "rbac_permission_inventory" VALUES(1000,1000,3000,'FAKE_DEFAULT','Fake Default Link');
INSERT INTO "rbac_permission_inventory" VALUES(1001,1000,3001,'FAKE_LIST_VIEW','Fake List View Link');
INSERT INTO "rbac_permission_inventory" VALUES(1002,1000,3002,'FAKE_GRAPHICAL_VIEW','Fake Graphical View Link');
INSERT INTO "rbac_permission_inventory" VALUES(1003,1000,3003,'FAKE_REPORT_VIEW','Fake Report View Link');

