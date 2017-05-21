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
with open('customer.txt') as f:customer_list = f.read().splitlines()
#customer_list = ['equipa','manufacto','acme','safetytest','emctest','universal']

def _set_search_path(customer_db):
	print '+-------------------------------------------'
	print 'Setting SEARCH PATH to customer_db=',customer_db
	print '+-------------------------------------------'
	cur.execute('set search_path to %s', (customer_db,) )

def get_users():
	#cur.execute('SELECT user_id,login_id,role_id FROM orv_login_details_tbl where is_suspended=0 order by user_id;')
	cur.execute('SELECT user_id,login_id,is_suspended FROM orv_login_details_tbl order by user_id;')
	users = [ dict(user_id = row[0], login_id = row[1], is_suspended = row[2]) for row in cur.fetchall()]
	return users

def rbac_manage_user_status(schema,login_id,is_suspended):
	url="https://"+HOST_NAME+"/manage_user_status"	
	params = urllib.urlencode({
		'customer_db': schema,
		'login_id': login_id,
		'is_suspended': is_suspended
	})
	print url,params
	url1= url+'?'+params
	response = urllib2.urlopen(url1).read()
	return response	

def rbac_check_user_status(schema,login_id):
	url="https://"+HOST_NAME+"/check_user_status"	
	params = urllib.urlencode({
		'customer_db': schema,
		'login_id': login_id
	})
	print url,params
	url1= url+'?'+params
	response = urllib2.urlopen(url1).read()
	return response	

def synchronize_user_status(schema):
	users_list = get_users()
	print users_list

	rbac_users_status = []
	for user_info in users_list:
		rbac_manage_user_status(schema, user_info['login_id'], user_info['is_suspended'] )
		user_status = json.loads(rbac_check_user_status(schema,user_info['login_id']) )
		print user_status['data']

		status = {}
		status['login_id'] = user_info['login_id']
		status['is_suspended'] =  user_status['data']['is_suspended']

		rbac_users_status.append(status)
	return rbac_users_status

def run():
	report = {}
	for schema in customer_list:
		_set_search_path(schema)
		status = {}
		users_status = synchronize_user_status(schema)
		
		status['users_status'] = users_status
		report[schema] = status
	return report

if ENV == 'prod':
	report = run()
	print report

