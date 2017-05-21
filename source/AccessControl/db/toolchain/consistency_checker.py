import psycopg2, urllib, urllib2, json

#--[ Configuration Parameters ]--
#Service Configuration
SERVER_NAME="zurich"
SERVER_PORT="5001"
HOST_NAME=SERVER_NAME+".equipa.com"+":"+SERVER_PORT	

# Datase Configuration
DB_VER="3" # Keep empty if no version Eg. DB_ENV="3" or DB_ENV=""
DB_ENV="" # Keep empty if no environment Eg. DB_ENV="_dev" or DB_ENV=""
DB="equipa_db"+DB_VER+DB_ENV # Final output DB="equipa_db3_dev" or DB="equipa_db"
DB_USER="postgres"

# Script Run configuration type
#ENV="dev"
ENV="prod"
#---

conn = psycopg2.connect(database=DB, user=DB_USER)
cur = conn.cursor()

# List of Entities for OEM/Lab
#oem_list = ['equipa','acme','manufacto']
#lab_list = ['emctest','safetytest','universal']
with open('oem.txt') as f:oem_list = f.read().splitlines()
with open('lab.txt') as f:lab_list = f.read().splitlines()

def _set_search_path(customer_db):
	print '+-------------------------------------------'
	print 'Setting SEARCH PATH to customer_db=',customer_db
	print '+-------------------------------------------'
	cur.execute('set search_path to %s', (customer_db,) )

def get_users():
	#cur.execute('SELECT user_id,login_id,role_id FROM orv_login_details_tbl where is_suspended=0 order by user_id;')
	cur.execute('SELECT user_id,login_id,role_id FROM orv_login_details_tbl order by user_id;')
	users = [ dict(user_id = row[0], login_id = row[1], role_id = row[2]) for row in cur.fetchall()]
	return users

def get_users_for_role(role_id):
	cur.execute('SELECT user_id,login_id,role_id FROM orv_login_details_tbl where role_id = %s order by user_id;',(role_id,))
	users = [ dict(user_id = row[0], login_id = row[1], role_id = row[2]) for row in cur.fetchall()]
	return users

# Select the list of columns which are present in the required table
# Helps track the columns in the required tables
def _get_column_list(db,schema,table):
	cur.execute('select column_name from information_schema.columns where table_catalog=%s and table_schema=%s and table_name=%s;',(db,schema,table))
	columns = [ row[0] for row in cur.fetchall()]
	return columns

def get_roles(schema):
	db=DB
	table='orv_role_master_tbl'
	columns = _get_column_list(db,schema,table)
	# Catching the corner case when role_description is not available within orv_role_master_tbl
	if 'role_description' in columns:
		cur.execute('select role_id,role_name,role_description from orv_role_master_tbl order by role_id;')
		roles = [ dict(role_id = row[0], role_name = row[1], role_description = row[2]) for row in cur.fetchall()]
	else: 
		cur.execute('select role_id,role_name from orv_role_master_tbl order by role_id;')
		roles = [ dict(role_id = row[0], role_name = row[1], role_description = '' ) for row in cur.fetchall()]
	return roles

def get_modules():
	cur.execute('select module_id,module_name from orv_module_lookup_tbl order by module_id;')
	modules = [ dict(module_id = row[0], module_name = row[1]) for row in cur.fetchall()]
	return modules

def get_permissions(role_id):
	print 'role_id=',role_id
	cur.execute('select role_id,module_id,module_action_name from orv_module_role_map_tbl where role_id = %s order by module_id;', (role_id,))
	permissions = [ dict(role_id = row[0], module_id = row[1], module_action_name = row[2]) for row in cur.fetchall()]
	return permissions

def get_role_perm_map(schema,roles):
	print '+-------------------------------------------'
	print 'Role-Perm Map processing for schema=',schema
	print '+-------------------------------------------'
	_set_search_path(schema)
	result = {}
	for role in roles:
		data = {}
		print 'role=',role
		data['permissions'] = get_permissions(role['role_id'])
		print 'permissions=',data['permissions']
		print '---------------------'
		data['total_perm'] = len(data['permissions'])
		data['role_id'] = role['role_id']
		result[role['role_name']] = data
	return result

def get_role_user_map(schema,roles):
	#print '+-------------------------------------------'
	#print 'Role-User Map processing for schema=',schema
	#print '+-------------------------------------------'
	#_set_search_path(schema)
	result = {}
	for role in roles:
		data = {}
		#print 'role=',role
		data['users'] = get_users_for_role(role['role_id'])
		#print 'users=',data['users']
		#print '---------------------'
		data['total_users'] = len(data['users'])
		data['role_id'] = role['role_id']
		result[role['role_name']] = data
	return result

def rbac_get_roles(schema):
	api="/roles?customer_db="+schema
	url="https://"+HOST_NAME+api
	print url
	response = urllib2.urlopen(url).read()
	return response

def rbac_add_role(schema,role_name,role_description):
	url="https://"+HOST_NAME+"/add_role"	
	params = urllib.urlencode({
		'customer_db': schema,
		'role_name': role_name,
		'role_description': role_description,
		'output': 'json'
	})
	print url,params
	response = urllib2.urlopen(url,params).read()
	return response

def rbac_add_role_login_id_map(schema,login_id,role_id,user_id):
	url="https://"+HOST_NAME+"/add_login_id_mapping"	
	params = urllib.urlencode({
		'customer_db': schema,
		'login_id': login_id,
		'role_id': role_id,
		'user_id': user_id,
		'output': 'json'
	})
	print url,params
	#response = urllib2.urlopen(url,params).read()
	#Throws a connection reset error
	url1= url+'?'+params
	response = urllib2.urlopen(url1).read()
	print response
	return response

def diff_roles(local_roles_list,rbac_roles_list): 
	roles_match = []
	roles_no_match = []
	local_roles_list.sort()
	rbac_roles_list.sort()

	print 'local_roles_list',local_roles_list	
	print 'rbac_roles_list=',rbac_roles_list
	#for local_role in local_roles_list:
	#	if local_role in rbac_roles_list: roles_match.append(local_role)
	#	else: roles_no_match.append(local_role)
	for rbac_role in rbac_roles_list:
		if rbac_role in local_roles_list: roles_match.append(rbac_role)
		else: roles_no_match.append(rbac_role)		

	print '+---------------------------+'
	print '| Roles Matching Algorithm: |'
	print '+---------------------------+'
	print 'roles_match=',roles_match
	print 'roles_no_match=',roles_no_match
	
	return roles_match,roles_no_match

def process_local_roles(schema):
	translate = {'Admin':'Administrator', 'Manager':'Compliance Manager'}
	#_set_search_path(schema)
	local_roles_list = []
	local_roles_dict = {}
	# Local Schema Roles
	local_roles_data_dict = get_roles(schema)
	for role in local_roles_data_dict: 
		if translate.has_key(role['role_name']):
			role_name = translate[role['role_name']]	
		else: role_name = role['role_name']
		local_roles_list.append(role_name)
		local_roles_dict[role_name] = { 'role_id':role['role_id'], 'role_description':role['role_description']}
	return local_roles_list,local_roles_dict

def process_rbac_roles(schema):
	#_set_search_path(schema)
	rbac_roles_list = []
	rbac_roles_tuple = []
	rbac_roles_dict = {}
	# Get RBAC Roles
	rbac_roles = rbac_get_roles(schema)
	#print rbac_roles

	# Load JSON into an object
	rbac_roles_json = json.loads(rbac_roles)
	data = rbac_roles_json['data']

	# Filter out Roles
	for item in data:
		rbac_roles_list.append(item['role_name'])
		#rbac_roles_tuple.append((item['role_name'],item['role_description'],item['user_count']))
		rbac_roles_dict[item['role_name']] = {'role_id':item['role_id'],'role_description':item['role_description']}
	return rbac_roles_list,rbac_roles_dict

def map_role_ids(schema):
	#_set_search_path(schema)
	mapped_role_id_dict = {}

	local_roles_list,local_roles_dict = process_local_roles(schema)
	rbac_roles_list,rbac_roles_dict = process_rbac_roles(schema)

	for k,v in local_roles_dict.iteritems():
		local_role_name = k
		local_role_id = v['role_id']
		
		if rbac_roles_dict.has_key(k):
			rbac_role_id = rbac_roles_dict[k]['role_id']
			mapped_role_id_dict[local_role_id] = rbac_role_id
	return mapped_role_id_dict # local role_id -> mapped to rbac role_id
		
def rbac_get_users(schema):
	api="/users?customer_db="+schema
	url="https://"+HOST_NAME+api
	print url
	response = urllib2.urlopen(url).read()
	return response

def synchronize_roles(schema):
	#_set_search_path(schema)
	print '*** Verifying consistency of Roles ***'

	local_roles_list,local_roles_dict = process_local_roles(schema)
	rbac_roles_list,rbac_roles_dict = process_rbac_roles(schema)
	roles_match,roles_no_match = diff_roles(local_roles_list,rbac_roles_list)
	#print 'roles_match=',roles_match
	#print 'roles_no_match=',roles_no_match

	print '~~~~~~~~~~~~~~~~~~~'
	print 'Consistency Check:'
	print '~~~~~~~~~~~~~~~~~~~'
	if len(roles_no_match) == 0: sync_status = 'success'
	else : sync_status = 'failure'
	print 'RBAC sync status check ... ',sync_status

	if len(local_roles_list) == len(rbac_roles_list): count_status = 'success'
	else: count_status = 'failure'
	print 'Verify count => (Local roles == RBAC roles) ... ',count_status
	print '~~~~~~~~~~~~~~~~~~~'

	# Synchronize the roles not present on RBAC
	#for role_name in roles_no_match:
	#	print 'role_name=',role_name
	#	rbac_add_role(schema, role_name, local_roles_dict[role_name]['role_description'])
	status = {}
	status['sync_status'] = sync_status
	status['count_status'] = count_status
	return status

def diff_users(local_login_id_list,rbac_login_id_list): 
	users_match = []
	users_no_match = []
	local_login_id_list.sort()
	rbac_login_id_list.sort()

	print 'local_login_id_list',local_login_id_list	
	print 'rbac_roles_list=',rbac_login_id_list
	#for local_user in local_login_id_list:
	#	if local_user in rbac_login_id_list: users_match.append(local_user)
	#	else: users_no_match.append(local_user)
	
	#total = local_login_id_list + rbac_login_id_list

	#users_no_match = list(set(local_login_id_list) - set(rbac_login_id_list))
	#users_match = list(set(total_list) - set(users_no_match)) 

	for rbac_user in rbac_login_id_list:
		if rbac_user in local_login_id_list: users_match.append(rbac_user)
		else: users_no_match.append(rbac_user)

	print '+---------------------------+'
	print '| Users Matching Algorithm: |'
	print '+---------------------------+'
	print 'users_match=',users_match
	print 'users_no_match=',users_no_match
	
	return users_match,users_no_match	

def synchronize_login_id(schema):
	#_set_search_path(schema)
	print '*** Verifying consistency of Users ***'

	mapped_role_ids_dict = map_role_ids(schema)
	#print 'mapped_role_ids_dict=',mapped_role_ids_dict 

	roles = get_roles(schema)
	role_user_map = get_role_user_map(schema,roles)
	#print '#------------#'
	#print 'local_users:',role_user_map
	#print '#------------#'

	rbac_users = rbac_get_users(schema)
	# Load JSON into an object
	rbac_users_json = json.loads(rbac_users)
	#print 'rbac_users:',rbac_users_json
	#print '----------------'

	print 'Local Users:'
	local_login_id_list = []
	for role_name,role_data in role_user_map.iteritems():
		user_list = role_data['users']
		
		login_id_list = []
		for user_dict in user_list:	
			login_id = user_dict['login_id']
			login_id_list.append(login_id)
		if len(login_id_list):
			print role_name,login_id_list
			local_login_id_list += login_id_list

	print 'RBAC Users:'
	rbac_login_id_list = []
	rbac_login_id_dict = {}
	for item in rbac_users_json:
		rbac_login_id_dict[item['role_name']] = []

	for item in rbac_users_json:
		rbac_login_id_list.append(item['login_id'])
		rbac_login_id_dict[item['role_name']].append(item['login_id'])
	print 'Users:',rbac_login_id_list
	for k,v in rbac_login_id_dict.iteritems(): print k,v

	print '~~~~~~~~~~~~~~~~~~~'
	print 'Consistency Check:'
	print '~~~~~~~~~~~~~~~~~~~'
	users_match,users_no_match=diff_users(local_login_id_list,rbac_login_id_list)
	if (len(set(local_login_id_list).intersection(rbac_login_id_list)) > 0): sync_status = 'success'
	else : sync_status = 'failure'
	print 'User sync status check ... ',sync_status

	if (local_login_id_list == rbac_login_id_list): count_status = 'success'
	else: count_status = 'failure'
	print 'Verify count => (Local users == RBAC users) ... ',count_status		
	print '~~~~~~~~~~~~~~~~~~~'

	status = {}
	status['sync_status'] = sync_status
	status['count_status'] = count_status
	status['local_login'] = local_login_id_list
	status['rbac_login'] = rbac_login_id_list
	return status

def rbac_update_access_control(schema,role_id,module_id):
	url="https://"+HOST_NAME+"/update_access_control"	
	params = urllib.urlencode({
		'customer_db': schema,
		'role_id': role_id,
		'module_id': module_id,
		'output': 'json'
	})
	print url,params
	#response = urllib2.urlopen(url,params).read()
	#Throws a connection reset error
	url1= url+'?'+params
	response = urllib2.urlopen(url1).read()
	print response
	return response

def rbac_set_full_access(schema,role_id,module_id):
	url="https://"+HOST_NAME+"/set_full_access"	
	params = urllib.urlencode({
		'customer_db': schema,
		'role_id': role_id,
		'module_id': module_id,
		'output': 'json'
	})
	print url,params
	url1= url+'?'+params
	response = urllib2.urlopen(url1).read()
	#print response
	return response

def rbac_set_sub_module_full_access(schema,role_id,module_id,sub_module_id):
	url="https://"+HOST_NAME+"/set_sub_module_full_access"	
	params = urllib.urlencode({
		'customer_db': schema,
		'role_id': role_id,
		'module_id': module_id,
		'sub_module_id': sub_module_id,		
		'output': 'json'
	})
	url1= url+'?'+params
	print url1
	response = urllib2.urlopen(url1).read()
	#print response
	return response

def rbac_set_perm_access(schema,role_id,perm_id):
	url="https://"+HOST_NAME+"/set_perm_access"	
	params = urllib.urlencode({
		'customer_db': schema,
		'role_id': role_id,
		'perm_id': perm_id,		
		'output': 'json'
	})
	url1= url+'?'+params
	print url1
	response = urllib2.urlopen(url1).read()
	print response
	return response	

#https://zurich.equipa.com:5001/permission_inventory?customer_db=equipa
def rbac_get_permission_inventory(schema):
	url="https://"+HOST_NAME+"/permission_inventory"	
	params = urllib.urlencode({
		'customer_db': schema
	})
	url1= url+'?'+params
	print url1
	response = urllib2.urlopen(url1).read()
	#print response
	return response

def _filter_perm_inventory(schema):
	rbac_perm_inventory=rbac_get_permission_inventory(schema)
	rbac_perm_inventory_json = json.loads(rbac_perm_inventory)	
	rbac_perm_inventory_dict = {}
	print '+--------------------'
	print 'Permission Inventory'
	print '+--------------------'
	print rbac_perm_inventory_json['data']

	for perm in rbac_perm_inventory_json['data']:
		#print perm
		rbac_perm_inventory_dict[perm['perm_name']] = perm['perm_id']
	return rbac_perm_inventory_dict

def process_local_permissions(role_perm_map):
	perm_list
	for role in role_perm_map:
		permissions = role['permissions']
		for perm in permissions:
			perm_list.append(perm['module_action_name'])

	return perm_list

# Retrieve the list of permisions and create a dictionary for lookup of PERM_NAME=>PERM_ID
def process_rbac_permissions(schema):
	local_rbac_perm_map_dict = {
		'dashboardListView': ['DASH_LIST_VIEW','DASH_VIEW_RECORDS','DASH_OPEN_DOC','DASH_DOWNLOAD_DOC'],
		'dashboardGraphicalView': ['DASH_GRAPH_VIEW'],
		'dashboardReportsView': ['DASH_REPORT_VIEW'],
		'recordsListView': ['REC_LIST_VIEW'],
		'recordsUpload': ['REC_ADD_RECORD'],
		'recordsAuditView': ['REC_EDIT_RECORD'],
		'projectsListView': ['PROJ_LIST_VIEW'],
		'projectsNewProject': ['PROJ_NEW_PROJECT','PROJ_EDIT_PROJECT']
	}
	local_rbac_perm_translation_dict = {}
	#---

	perm_inventory_dict = _filter_perm_inventory(schema)

	for local_perm,rbac_perm in local_rbac_perm_map_dict.iteritems():
		perm_ids = []
		for rbac_perm in rbac_perm: 
			perm_ids.append(perm_inventory_dict[rbac_perm])

		local_rbac_perm_translation_dict[local_perm]=perm_ids
	return local_rbac_perm_translation_dict

def synchronize_access_control(schema):
	#_set_search_path(schema)
	print '*** Verifying consistency of Permissions ***'

	roles = get_roles(schema)
	local_role_perm_map = get_role_perm_map(schema,roles)
	mapped_role_ids_dict = map_role_ids(schema)
	#print 'mapped_role_ids_dict=',mapped_role_ids_dict 
	print '+--------------------'
	print 'Role Perm Map'
	print '+--------------------'
	print local_role_perm_map
	local_rbac_perm_translation_dict = process_rbac_permissions(schema)
	print '+--------------------'
	print 'Local Perm mapping to Rbac Permissions'
	print '+--------------------'
	print local_rbac_perm_translation_dict
	# Get the role=>permision mapping from local role_master
	for local_role,data in local_role_perm_map.iteritems():
		print local_role
		local_perm_list = data['permissions']
		local_role_id = data['role_id']
		
		# Get the local perm_names mapped to each Role
		for local_perm in local_perm_list:
			local_perm_name = local_perm['module_action_name']
			# Get the rbac perm_ids for each local_perm_name
			if local_rbac_perm_translation_dict.has_key(local_perm_name):
				perm_ids = local_rbac_perm_translation_dict[local_perm_name]
				print 'perm_ids=',perm_ids
				# Set the rbac permissions for each local role
				for rbac_perm_id in perm_ids:
					rbac_role_id = mapped_role_ids_dict[local_role_id]
					#rbac_set_perm_access(schema,rbac_role_id,rbac_perm_id)

def run1(schema):
	_set_search_path(oem)
	users = get_users()
	print users
	print '-----'

	modules = get_modules()
	print modules
	print '-----'

	roles = get_roles(schema)
	print roles
	print '-----'

	role_perm_map = get_role_perm_map(schema,roles)
	print role_perm_map
	print '-----'

	role_user_map = get_role_user_map(schema,roles)
	print role_user_map
	print '-----'

def run_test():
	_set_search_path('equipa')
	print get_permissions(3)
	print get_users_for_role(3)

def print_report(report,type):
	print '+---------------------------------------------------'
	print '  '+type+' Report  '
	print '+---------------------------------------------------'
	#print 'schema     |    role_status    |     user_status    '
	head = "schema\trole_status\tuser_status"
	print head
	print '+---------------------------------------------------'
	for k,v in report.iteritems():
		#print k,'=>'
		#print 'role_status:',v['roles_status']
		#print 'user_status:',v['users_status']
		#print '-------------------'
		print k,'\t',v['roles_status']['sync_status'],'\t',v['users_status']['sync_status']

	#for schema in report:
	#	print schema
    #	for item in report[schema]:
    #    	print (item,':',report[schema][item])

def run_oem_test():
	oem_list = ['equipa']
	report = {}
	for oem in oem_list:
		_set_search_path(oem)
		status = {}
		roles_status = synchronize_roles(oem)
		users_status = synchronize_login_id(oem)
		#synchronize_access_control(oem)

		status['role_status'] = role_status
		status['users_status'] = users_status
		report[oem] = status
		print_report(report)

def run_oem():
	#oem_list = ['equipa']
	report = {}
	for oem in oem_list:
		_set_search_path(oem)
		status = {}
		roles_status = synchronize_roles(oem)
		users_status = synchronize_login_id(oem)
		#synchronize_access_control(oem)
		
		status['roles_status'] = roles_status
		status['users_status'] = users_status
		report[oem] = status
	return report

def run_lab():
	#lab_list = ['emctest']
	report = {}
	for lab in lab_list:
		_set_search_path(lab)
		status = {}
		roles_status = synchronize_roles(lab)
		users_status = synchronize_login_id(lab)
		#synchronize_access_control(oem)
		
		status['roles_status'] = roles_status
		status['users_status'] = users_status
		report[lab] = status
	return report

def run():
	oem_report = run_oem()
	lab_report = run_lab()
	print_report(oem_report,'OEM')
	print_report(lab_report,'LAB')

if ENV == 'dev':
	# Keep this turned off for production
	run_oem_test()

if ENV == 'prod':
	# Keep this turned on for production
	run()
