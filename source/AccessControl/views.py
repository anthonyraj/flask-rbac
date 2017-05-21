from AccessControl import app
from flask import render_template, request, make_response, abort, redirect, url_for, session, g, flash, jsonify, json, Response
#from flask_bootstrap import Bootstrap
from contextlib import closing
import psycopg2, datetime,os, hashlib, requests, time, urllib
from datetime import date, timedelta as td

# Secure Upload import
from werkzeug import secure_filename
from flask import send_from_directory
#from flask.ext.cors import cross_origin
import re, shutil
from email.utils import parseaddr
import bleach

# Custom classes
from lib.postgresdb import postgresdb
from lib.tenancy_manager import tenancy_manager

#Integration with Angular Template Plugin
#from flask.ext.triangle import Triangle

app.config.from_envvar('APP_SETTINGS', silent=True)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

#TODO: move enviornment vars into app.config
app.config['CRT'] = '/'.join([ app.config['CERT_PATH'], 'server.crt' ])
app.config['KEY'] = '/'.join([ app.config['CERT_PATH'], 'server.key' ])

# Cookie Secure Flag set to True
app.config['SESSION_COOKIE_SECURE'] = True 
##

# Error Codes
app.config['MISSING_PARAM_ERROR'] = {'error':'customer_db or customer_id parameter incorrect or missing'}

##### DB INITIALIZATION FUNCTIONS ######
def connect_db(DBNAME=app.config['DBNAME']):
    print "DBNAME=",DBNAME
    try:
        return psycopg2.connect(database=DBNAME,user=app.config['DBUSER'], password=app.config['DBPASS'])
    except:
        print "Postgres database connection failure."

##### BASIC ROUTE FUNCTIONS ######
# TODO: Needs to be removed and configured for dynamic requests ONLY
@app.before_request
def before_request():
    if not _static_request():
        app.logger.info("[before_request] Initialize GDATA called.")
        g.conn = connect_db()
        g.db = g.conn.cursor()
        _initialize_gdata()
    #print "-----------------------------"

# TODO: Remove the Fonts specific CORS. Enabled for every request across the site
#@app.after_request                                                                                                                                       
def after_request(response):
    app.logger.info("[after_request] After request processing completed")
    app.logger.debug("Filter to add CORS to fonts formats fired")
    _add_headers_to_static_files(response)
    return response

@app.teardown_request
def teardown_request(exception):
    conn = getattr(g, 'conn', None)
    cur = getattr(g, 'db', None)
    if conn is not None: conn.commit()
    if cur is not None: cur.close() 
    if conn is not None: conn.close()                

@app.route('/redirect')
def redirect1():
    return redirect(url_for('test_error'))

@app.route('/test_error')
def test_error():
    abort(404)

##### REQUEST/RESPONSE FUNCTIONS ######
def _static_request():
    """
    Function used to manage the call to pre-processing of session
    """
    static = 0
    if (request.path and re.search(r'static', request.path)): 
        static = 1
        app.logger.debug("STATIC Request:"+request.path)
    return static

def _add_headers_to_static_files(response):
    """
    Fix for font files: after Flask static send_file() does its thing, but before the response is sent, 
    add an Access-Control-Allow-Origin: *
    HTTP header to the response (otherwise browsers complain).
    """
    if (request.path and re.search(r'\.(ttf|woff|svg|eot)$', request.path)):
        response.headers.add('Access-Control-Allow-Origin', '*')
    return response

##### INDEX PAGE FUNCTIONS ######
#@app.route("/index")
#@cross_origin()
def INDEX():    
    if not g.data['logged_in']:
        abort(404)
        return redirect(url_for('login'))
    else:
        response = make_response(render_template('index.html',user_name=g.data['user_name'], user_id=g.data['user_id']))
        return response  

##### SESSION FUNCTIONS ######
def _get_session_param():
    g.session_param = {'ENTITY_TYPE':'', 'CUSTOMER_ID': '0', 'CUSTOMER_DB':'', 'CUSTOMER_NAME':'', 'FNAME':'', 'USER_ID':'-1', 'USER_NAME':'', 'LOGIN_ID':'', 'CAS_TOKEN':'', 'SESSION_SOURCE':''}
    return g.session_param

def _get_session_map():
    _get_session_param()
    g.session_map = {}
    for k in g.session_param.iterkeys():
        g.session_map[k.lower()] = k
    return g.session_map

def _get_parameters():
    g.session_param = _get_session_param()
    g.session_map = _get_session_map()
    return g.session_param, g.session_map

@app.route('/login', methods=['GET', 'POST'])
#@cross_origin()
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USER_NAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            flash('You were logged in')
            _set_session(app.config)
            response = make_response(render_template('index.html'))
            return response
    return render_template('login.html', error=error)

def _set_session(session_var):
    session['logged_in'] = True                    
    app.logger.info('Username:'+session_var['USER_NAME']+' User Id='+session_var['USER_ID']+' First Name:'+session_var['FNAME'])

    session_map = _get_session_map()
    for KEY1,KEY2 in session_map.iteritems():
        session[KEY1] = session_var[KEY2]
        session_log = 'session-> '+ str(KEY1) + ' : ' + str(session[KEY1])
 
    _initialize_gdata()

    return session

def _initialize_gdata():
    g.data = _validate_session()    
    g.db.execute('set search_path to %s', (session['customer_db'],) )
    g.data['username']=g.data['user_name']  

# http://blog.luisrei.com/articles/flaskrest.html
@app.route('/validate_session')
def validate_session():
    # No session found within data['logged_in']
    session = _validate_session()
    data = _get_session()
    json_response = json.dumps(data)
    response = Response(json_response, status=200, mimetype='application/json')
    return response

def _validate_session():
    if 'logged_in' in session: 
        #app.logger.info('Returning an existing session object ... ok')
        return session
    else: 
        #app.logger.info('session not present. creating a session ... ok')
        _set_session(app.config)
        return session

def _get_session():
    _get_parameters()
    #paramlist = ['user_name','user_id','fname','customer_id','customer_db','customer_name','cas_token','entity_type']
    data = {}
    if 'logged_in' in session: 
        #for session_key in paramlist: 
        for session_key in g.session_map.iterkeys():
            data[session_key] = session[session_key]
    return data

def _delete_session():
    _get_parameters()
    paramlist = ['user_name','user_id','fname','customer_id','customer_db','customer_name','cas_token','entity_type']
    if 'logged_in' in session: 
        for session_key in paramlist:                   
            session[session_key] = ''
        session.pop('logged_in', None)
    return 'successful logout'    

@app.route('/logout')
def logout():
    _delete_session()

    response = make_response(render_template('index.html'))
    #response.set_cookie('session', '', expires=0)
    response.delete_cookie('session', path='/', domain=app.config['DOMAIN'])

    flash('You were logged out')
    #return redirect(url_for('index'))
    return response

def _get_user_details(user_name,customer_db):
    #print 'username:',user_name
    g.db.execute('set search_path to %s', (customer_db,) )
    g.db.execute('select user_id,login_id,user_name from orv_login_details_tbl where user_name=%s', (user_name,))
    user_details = [ dict(user_id = row[0], login_id = row[1], user_name = row[2]) for row in g.db.fetchall()]
    if user_details is not None: return user_details[0]
    else: return []

def _get_user_details_from_loginid(login_id,customer_db):
    #print 'login_id:',login_id
    g.db.execute('set search_path to %s', (customer_db,) )

    g.db.execute('select user_id,login_id,user_name from orv_login_details_tbl where login_id=%s', (login_id,))
    user_details = [ dict(user_id = row[0], login_id = row[1], user_name = row[2]) for row in g.db.fetchall()]
    app.logger.info('user_details')
    app.logger.info(user_details)
    if user_details is not None: return user_details[0]
    else: return 0

##### ERROR FUNCTIONS ######
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'),404

##### CONFIGURATION FUNCTIONS ######
@app.route('/user/<username>')
def get_profile(username):
    # show the user profile for that user
    #return 'User %s' % username

    return render_template('hello.html', user_name=user_name,user_id=user_id)   
 
### TODO: Move it to the appropiate location
##### UTILITY FUNCTIONS ####
def decode_string(data):
    if data is not None:
        data1 = data.replace('%20',' ')
    return data1

def format_date(date):
    #date1 = date.split(' ')[0].split('-')
    #date2 = '/'.join( [ date1[1], date1[2], date1[0] ] )
    if date is not None:
        date2 = date.strftime("%A, %d. %B %Y %I:%M%p")
        return date2
    else: return date

# HTML Entity conversion    
html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

def _extract_post_param(request,params):
    request_data = {}

    for k,v in params.iteritems():
        if k in request.form:
            #request_data[k] = request.form[k]
            #request_data[k] = bleach.clean(request.form[k])
            #request_data[k] = html_escape(request_data[k])
            request_data[k] = html_escape(request.form[k])
        else:
            if v == 'str':request_data[k] = ''
            elif v == 'int':request_data[k] = 0
            elif v == 'date':request_data[k] = '2015/01/01'

    return request_data

def _extract_get_param(request,params):
    # Parse the prams and check if the required parameters are present in the request object
    # If the parameters are present, then extract them and add to request_data object
    request_data = {}

    for k,v in params.iteritems():
        if k in request.args:
            # Call bleach ??
            #if v == 'str': request_data[k] = request.args.get(k)
            if v == 'str': 
                #request_data[k] = bleach.clean(request.args.get(k))
                #request_data[k] = html_escape(request_data[k])
                request_data[k] = html_escape(request.args.get(k))

            #if v == 'str': request_data[k] = urllib.quote( request.args.get(k) )
            elif v == 'int': request_data[k] = request.args.get(k, 0, type=int)
        else:
            if v == 'str':request_data[k] = ''
            elif v == 'int':request_data[k] = 0
            elif v == 'date':request_data[k] = '2015/01/01'

    return request_data

def _request_parser(request,params):
    #params = {'project_id':'int','task_id':'int','entity_type':'str','entity_name':'str'}

    if request.method == 'POST':
        request_data = _extract_post_param(request,params)

    if request.method == 'GET':
        request_data = _extract_get_param(request,params)

    return request_data    


##### RBAC UX FUNCTIONS #####
#@app.route('/rbac')
def rbac():

    return render_template('rbac/account-config.html', customer_id=app.config['CUSTOMER_ID'],)        

def rbac_template_manager(r):
    if r['bootstrap']: bootstrap = r['bootstrap']
    else: bootstrap = 0

    template_name = r['module_name']
    template_html = '.'.join([ template_name, 'html' ])

    if bootstrap == 1:
        r['template'] = '/'.join([ app.config['RBAC_BOOTSTRAP_PATH'], template_html ])
    else: 
        r['template'] = '/'.join([ app.config['RBAC_PATH'], template_html ])
    return r

#@app.route('/rbac_account_config')
def rbac_account_config():
    params = {'customer_id':'int','customer_db':'str', 'bootstrap': 'int'}
    r = _request_parser(request,params)

    r['module_name'] = 'account-config'
    r = rbac_template_manager(r)
    return render_template(r['template'], customer_db=r['customer_db'],) 

#@app.route('/rbac_dashboards')
def rbac_dashboards():
    params = {'customer_id':'int','customer_db':'str', 'bootstrap': 'int'}
    r = _request_parser(request,params)

    r['module_name'] = 'dashboards'
    r = rbac_template_manager(r)
    return render_template(r['template'], customer_db=r['customer_db'],) 
    #return render_template('rbac/dashboards.html', customer_id=app.config['CUSTOMER_ID'],) 

#@app.route('/rbac_records')
def rbac_records():
    params = {'customer_id':'int','customer_db':'str', 'bootstrap': 'int'}
    r = _request_parser(request,params)

    r['module_name'] = 'records'
    r = rbac_template_manager(r)
    return render_template(r['template'], customer_db=r['customer_db'],) 
    #return render_template('rbac/records.html', customer_id=app.config['CUSTOMER_ID'],) 

#@app.route('/rbac_projects')
def rbac_projects():
    params = {'customer_id':'int','customer_db':'str', 'bootstrap': 'int'}
    r = _request_parser(request,params)

    r['module_name'] = 'projects'
    r = rbac_template_manager(r)
    return render_template(r['template'], customer_db=r['customer_db'],) 
    #return render_template('rbac/projects.html', customer_id=app.config['CUSTOMER_ID'],) 

@app.route('/rbac_roles')
def rbac_roles():
    params = {'customer_id':'int','customer_db':'str', 'bootstrap': 'int'}
    r = _request_parser(request,params)

    r['module_name'] = 'roles'
    r = rbac_template_manager(r)

    roles = {}
    customer_db= r['customer_db']
    hostname = app.config['HOSTNAME']
    status = _check_customer_db(r)

    if status:
        roles = _get_roles()
        template_name = r['template']
    else: 
        template_name = app.config['ERROR_PAGE']

    #DEBUG
    print 'template = ', template_name
    
    return render_template(template_name, customer_db=customer_db, roles=roles, hostname=hostname) 
    #return render_template('rbac/roles.html', customer_id=app.config['CUSTOMER_ID'], roles=roles, hostname=hostname) 

#@app.route('/rbac_roles1')
def rbac_roles1():
    params = {'customer_id':'int','customer_db':'str', 'bootstrap': 'int'}
    r = _request_parser(request,params)

    r['module_name'] = 'roles'
    r = rbac_template_manager(r)

    roles = {}
    customer_db= r['customer_db']
    hostname = app.config['HOSTNAME']
    status = _check_customer_db(r)

    if status:
        roles = _get_roles()
        template_name = '/rbac/roles1.html'
    else: 
        template_name = app.config['ERROR_PAGE']

    #DEBUG
    print 'template = ', template_name
    
    return render_template(template_name, customer_db=customer_db, hostname=hostname) 
    #return render_template('rbac/roles.html', customer_id=app.config['CUSTOMER_ID'], roles=roles, hostname=hostname) 


##### RBAC MICROSERVICE FUNCTIONS #####

##### CONSOLE: METHODS TO ACCESS CUSTOMER INFO #####
def _set_search_path(customer_db):
    print 'Setting SEARCH PATH to customer_db=',customer_db
    g.db.execute('set search_path to %s', (customer_db,) )

def _read_customer_schema(customer_id):
    config = {'DBNAME':'console_db', 'DBUSER':'postgres','DBPASS':''}
    tm = tenancy_manager(config)
    customer_db = tm.get_customer_schema(customer_id)
    print 'customer_db=',customer_db
    return customer_db

##### RBAC: MODULE/PERMISSION INVENTORY #####
#@app.route('/')
def nothing():
    return '.'

#Comment for Security
@app.route('/')
def docs():
    template_name = 'docs/index.html'
    hostname = app.config['HOSTNAME']
    return render_template(template_name, hostname=hostname)

#Comment for Security
@app.route('/docs')
def docs1():
    return redirect(url_for('docs'))

@app.route('/modules')
def get_modules():
    app.logger.info("+++++[ REQUEST:/modules ]+++++")
    params = {'customer_id':'int','customer_db':'str'}
    r = _request_parser(request,params)
    app.logger.info("/modules request params")
    app.logger.info(r)    

    status = _check_customer_db(r) # sets the search path to the required customer_db
    if status:    
        g.db.execute('select module_id, module_name from rbac_modules')
        modules_dict = [ dict(module_id = row[0], module_name = row[1]) 
            for row in g.db.fetchall()]
        modules = json.dumps(modules_dict)
    else: 
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404   

    return modules

def _get_module_names():
    g.db.execute('select module_id, module_name from rbac_modules')
    modules = { row[0]:row[1] for row in g.db.fetchall()}
    return modules    

@app.route('/permission_inventory')
def get_full_permission_inventory():
    app.logger.info("+++++[ REQUEST:/permission_inventory ]+++++")
    params = {'customer_id':'int','customer_db':'str'}
    r = _request_parser(request,params)
    app.logger.info("/permission_inventory request params")
    app.logger.info(r)    

    permission_inventory = {}
    error_message = 'customer_db or customer_id parameter missing'
    status = _check_customer_db(r)
    
    if status: permission_inventory = _get_permission_inventory_for_customer_db(r)
    else: 
        #permission_inventory['error'] = error_message
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404  

    return json.dumps(permission_inventory)

def _get_permission_inventory_for_customer_db(r):
    permission_inventory = {}

    #TODO: Need to move to app.config configuration or db table
    start_perm_id = 0
    end_perm_id = 1000

    g.db.execute('select perm_id, module_id, perm_name, perm_description from rbac_permission_inventory where perm_id>%s and perm_id<%s', (start_perm_id,end_perm_id))
    permission_inventory_list = [ dict(perm_id = row[0], module_id = row[1], perm_name = row[2], perm_description = row[3]) for row in g.db.fetchall() ]
    permission_inventory['data'] = permission_inventory_list
    
    if len(permission_inventory['data'])>0: permission_inventory['status'] = 'ok'
    else: permission_inventory['status'] = 'no data'

    return permission_inventory

#@app.route('/get_users_granted_access')
def get_users_granted_access():
    app.logger.info("+++++[ REQUEST:/get_users_granted_access ]+++++")
    params = {'customer_id':'int','customer_db':'str','perm_name':'str'}
    r = _request_parser(request,params)
    app.logger.info("/get_users_granted_access request params")
    app.logger.info(r)    

    data = {'data':[],'error':''}
    
    error_message = 'customer_db or customer_id or perm_name parameter missing or incorrect' 
    status = _check_customer_db(r) # sets the search path to the required customer_db
    if status:    
        if r['perm_name']:
            data['data'] = _get_users_granted_access(r['perm_name'])
        else:
            data['error'] += error_message
    else:
        data['error'] = error_message 

    return json.dumps(data)

def _get_users_granted_access(perm_name):
    
    perm_id = _get_permission_id_for_permission_name(perm_name)
    print 'perm_id=',perm_id
    login_ids = []
    if perm_id:
        role_ids = _get_role_id_mapped_with_permission_id(perm_id)
        print 'role_ids=',role_ids
        if len(role_ids):
            login_ids = _get_login_ids_mapped_with_role_ids(role_ids)
        print 'login_ids',login_ids
    #else: login_ids = []

    return login_ids

def _get_permission_id_for_permission_name(perm_name):
    g.db.execute('select perm_id from rbac_permission_inventory where perm_name = %s', (perm_name,))
    perm_id_tuple = g.db.fetchone()
    print 'perm_id_tuple=',perm_id_tuple
    if perm_id_tuple is not None:
        if len (perm_id_tuple)>0: perm_id = perm_id_tuple[0]
        else: perm_id = 0
    else: perm_id = 0
    return perm_id

def _get_role_id_mapped_with_permission_id(permission_id):
    g.db.execute('select role_id from rbac_access_control where perm_id in (%s) order by role_id;', (permission_id,))
    roles_ids= [ row[0]  for row in g.db.fetchall()]
    return roles_ids

def _get_login_ids_mapped_with_role_ids(role_ids):
    g.db.execute('select login_id from rbac_users where role_id in %s and is_suspended=0;', (tuple(role_ids),) )
    login_ids= [ row[0] for row in g.db.fetchall()]    
    return login_ids

# The New version of the API has the user_id and the login_id in the response.
# The previous version needs to be phased out which has a single response related to login_ids
@app.route('/get_users_granted_access')
def get_users_granted_access1():
    app.logger.info("+++++[ REQUEST:/get_users_granted_access ]+++++")
    params = {'customer_id':'int','customer_db':'str','perm_name':'str'}
    r = _request_parser(request,params)
    app.logger.info("/get_users_granted_access request params")
    app.logger.info(r)    

    data = {'data':[],'error':''}
    
    error_message = 'customer_db or customer_id or perm_name parameter missing or incorrect' 
    status = _check_customer_db(r) # sets the search path to the required customer_db
    if status:    
        if r['perm_name']:
            data['data'] = _get_users_granted_access1(r['perm_name'])
        else:
            data['error'] += error_message
    else:
        #data['error'] = error_message 
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404  

    return json.dumps(data)

def _get_users_granted_access1(perm_name):
    
    perm_id = _get_permission_id_for_permission_name(perm_name)
    print 'perm_id=',perm_id
    login_ids = []
    if perm_id:
        role_ids = _get_role_id_mapped_with_permission_id(perm_id)
        print 'role_ids=',role_ids
        if len(role_ids):
            login_ids = _get_login_ids_mapped_with_role_ids1(role_ids)
        print 'login_ids',login_ids
    #else: login_ids = []

    return login_ids

def _get_login_ids_mapped_with_role_ids1(role_ids):
    g.db.execute('select user_id,login_id from rbac_users where role_id in %s and is_suspended=0;', (tuple(role_ids),) )
    login_ids= [ [row[0],row[1]] for row in g.db.fetchall()]    
    return login_ids    

##### RBAC: ROLES #####
@app.route('/roles')
def get_roles():
    app.logger.info("+++++[ REQUEST:/roles ]+++++")
    params = {'customer_id':'int','customer_db':'str'}
    r = _request_parser(request,params)
    app.logger.info("/roles request params")
    app.logger.info(r)    

    status = _check_customer_db(r)
    if status:
        roles_dict = {}      
        roles_list = _get_roles()
        roles_dict['data'] = roles_list 
        roles_dict['total_roles'] = len(roles_list)
        if len(roles_list): roles_dict['status'] = 'ok'
        else: roles_dict['status'] = 'nodata'
    else: 
        #roles_dict['error'] = ' customer_db or customer_id parameter missing' 
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404  
    return json.dumps(roles_dict) # json response

def _get_roles():
    g.db.execute('select role_id, role_name, role_description,role_type from rbac_roles order by role_name')
    roles = [ dict(role_id = row[0], role_name = row[1], role_description = row[2], role_type = row[3], user_count=_get_role_count(row[0]), users=_get_users(row[0]) ) for row in g.db.fetchall()]
    return roles

def _get_role_count(role_id):
    g.db.execute('select count(*) from rbac_users where role_id=%s and is_suspended=0', (role_id,))
    role_count = g.db.fetchone()
    if role_count is None: role_count=0
    return role_count[0]

@app.route('/add_role', methods=['GET','POST'])
def add_role():
    app.logger.info("+++++[ REQUEST:/add_role ]+++++")
    params = {'customer_id':'int','customer_db':'str','role_name':'str','role_description':'str','output':'str','response':'int'}
    r = _request_parser(request,params)
    app.logger.info("/add_role request params")
    app.logger.info(r)
    
    status = _check_customer_db(r)
    roles_dict = {}
    role_id = 0
    if status: 
        role_id = _add_role(r['role_name'],r['role_description']) 
        roles_dict['role_id'] = role_id
        # FULL ROLES INFO NOT NEEDED
            #roles_list = _get_roles()   
            #roles_dict['data'] = roles_list
            #roles_dict['total_roles'] = len(roles_list)
            #if len(roles_list): roles_dict['status'] = 'ok'
            #else: roles_dict['status'] = 'nodata'
        if role_id: roles_dict['status'] = 'ok'
        else: roles_dict['status'] = 'nodata'
    else: 
        #roles_dict['error'] = ' customer_db or customer_id parameter incorrect or missing' 
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404  

    if r['output'] == 'json': return json.dumps(roles_dict) # json response
    else: return redirect(url_for('rbac_roles',customer_db=r['customer_db'])) # html response

def _add_role(role_name,role_description):
    g.db.execute('insert into rbac_roles (role_name,role_description) values (%s,%s) returning role_id', (role_name,role_description) )
    last_role_id = g.db.fetchone()
    if len(last_role_id) > 0: return last_role_id[0]
    else: return 0

#TODO: Remove the API completely. This API is not required any more
#@app.route('/add_role_with_access_control', methods=['POST','GET'])
def add_role_with_access_control():
    params = {'customer_id':'str' ,'customer_db':'str', 'module_id':'int', 'sub_module_id':'int', 'sub_module_code':'str', 'radio_access_type':'str','output':'str', 'role_name':'str', 'role_description':'str'}
    r = _request_parser(request,params)

    app.logger.info("/add_role_with_access_control request params")
    app.logger.info(r)

    status = _check_customer_db(r)
    r['role_id'] = _add_role(r['role_name'],r['role_description']) 
    #DEBUG
    print 'role_id = ',r['role_id']

    r = _update_access_control(request,r)

    return redirect(url_for('display_access_control',customer_db=r['customer_db'], role_id=r['role_id'], module_id=r['module_id'], output=r['output']))

@app.route('/delete_role', methods=['GET','POST'])
def delete_role():
    app.logger.info("+++++[ REQUEST:/delete_role ]+++++")
    params = {'customer_id':'int','customer_db':'str','role_id':'int','output':'str'}
    r = _request_parser(request,params)
    app.logger.info("/delete_role request params")
    app.logger.info(r)
    
    status = _check_customer_db(r)
    roles_dict = {}
    if status:     
        _delete_role(r['role_id']) 
        roles_list = _get_roles()   
        roles_dict['data'] = roles_list
        roles_dict['total_roles'] = len(roles_list)
        if len(roles_list): roles_dict['status'] = 'ok'
        else: roles_dict['status'] = 'nodata'
    else: 
        #roles_dict['error'] = ' customer_db or customer_id parameter missing' 
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404  

    if r['output']: return json.dumps(roles_dict) # json response
    else: return redirect(url_for('rbac_roles',customer_db=r['customer_db'])) # html response

def _delete_role(role_id):
    g.db.execute('delete from rbac_roles where role_id = %s and role_type=0', (role_id,) )

@app.route('/update_role', methods=['GET','POST'])
def update_role():
    app.logger.info("+++++[ REQUEST:/delete_role ]+++++")
    params = {'customer_id':'int','customer_db':'str','role_id':'int','role_name':'str','role_description':'str'}
    r = _request_parser(request,params)
    app.logger.info("/update_role request params")
    app.logger.info(r)
    
    status = _check_customer_db(r)
    roles_dict = {}
    if status:     
        _update_role(r['role_name'],r['role_description'],r['role_id']) 
        roles_info = _get_role_info(r['role_id'])  
        roles_dict['data'] = roles_info
        if len(roles_info): roles_dict['status'] = 'ok'
        else: roles_dict['status'] = 'nodata'
    else: 
        #roles_dict['error'] = ' customer_db or customer_id parameter missing'
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404  

    return json.dumps(roles_dict) # json response

def _update_role(role_name,role_description,role_id):
    g.db.execute('update rbac_roles set role_name=%s, role_description=%s where role_id = %s', (role_name,role_description,role_id) )

@app.route('/role_info')
def get_role_info():
    app.logger.info("+++++[ REQUEST:/roles ]+++++")
    params = {'customer_id':'int','customer_db':'str','role_id':'int'}
    r = _request_parser(request,params)
    app.logger.info("/role_info request params")
    app.logger.info(r)    

    status = _check_customer_db(r)
    roles_dict = {}   
    if status:
        roles_info = _get_role_info(r['role_id'])
        roles_dict['data'] = roles_info
        if len(roles_info): 
            roles_dict['status'] = 'ok'
        else: 
            roles_dict['status'] = 'nodata'
    else: 
        #roles_dict['error'] = 'customer_db or customer_id parameter missing'
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404  

    return json.dumps(roles_dict)

def _get_role_info(role_id):
    g.db.execute('select role_id, role_name, role_description from rbac_roles where role_id=%s', (role_id,))
    roles_info = [ dict(role_id = row[0], role_name = row[1], role_description = row[2] ) for row in g.db.fetchall()]
    if len(roles_info) == 1: return roles_info[0]
    else: return []

"""
 Get the users for a Role for a customer
"""
@app.route('/users')
def get_users():
    app.logger.info("+++++[ REQUEST:/modules ]+++++")
    params = {'customer_id':'int','customer_db':'str','role_id':'int'}
    r = _request_parser(request,params)
    app.logger.info("/modules request params")
    app.logger.info(r)    

    users = {}
    error_message = 'customer_db or customer_id or role_id parameter missing' 

    status = _check_customer_db(r)
    if status: users = _get_users(r['role_id'])
    else: 
        #users['error'] = error_message   
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404  

    return json.dumps(users)

def _get_users(role_id):
    print 'ROLE_ID:',role_id
    users = {}
    if role_id>0:    
        g.db.execute('select a.user_id, a.role_id, a.login_id, b.role_name, b.role_description, a.is_suspended from rbac_users a, rbac_roles b where a.role_id=b.role_id and a.role_id=%s', (role_id,))
    else:
        g.db.execute('select a.user_id, a.role_id, a.login_id, b.role_name, b.role_description, a.is_suspended from rbac_users a, rbac_roles b where a.role_id=b.role_id')
    
    users_list = [ dict(user_id = row[0], role_id = row[1], login_id = row[2], role_name = row[3], role_description = row[4], is_suspended = row[5]) for row in g.db.fetchall()]
    #users['data'] = users_list

    #if len(users['data']) > 0: users['status'] = 'ok'
    #else: users['status'] = 'no data'

    #return users
    if len(users_list): return users_list
    else: return []

"""
 Get the Role for a login_id 
"""
def _get_user_role(login_id):
    g.db.execute('select role_id from rbac_users where login_id=%s', (login_id,) )
    role_id = g.db.fetchone()
    print 'Role ID= ',role_id
    if role_id is not None and len(role_id)>0: return role_id
    else: return []

"""
 Manage Users Staus: Suspend or Activate
"""
@app.route('/manage_user_status')
def manage_user_status():
    app.logger.info("+++++[ REQUEST:/roles ]+++++")
    params = {'customer_id':'int','customer_db':'str','login_id':'str','is_suspended':'int'}
    r = _request_parser(request,params)
    app.logger.info("/manage_user_status request params")
    app.logger.info(r)    

    status = _check_customer_db(r)
    response = {'data':[],'error':'no error'}
    if status:
        g.db.execute('update rbac_users set is_suspended=%s where login_id=%s', (r['is_suspended'],r['login_id']) )
        r['role_id']=0  
        response['data'] = _get_users(r['role_id'])
    else: 
        #roles_dict['error'] = 'customer_db or customer_id parameter missing'
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404  

    return json.dumps(response)


@app.route('/check_user_status')
def check_user_status():
    app.logger.info("+++++[ REQUEST:/roles ]+++++")
    params = {'customer_id':'int','customer_db':'str','login_id':'str'}
    r = _request_parser(request,params)
    app.logger.info("/check_user_status request params")
    app.logger.info(r)    

    status = _check_customer_db(r)
    response = {'data':{},'error':'no error'}
    if status:
        response['data'] = {'login_id': r['login_id'], 'is_suspended':_check_user_status(r['login_id'])}
    else: 
        #roles_dict['error'] = 'customer_db or customer_id parameter missing'
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404  

    return json.dumps(response)

def _check_user_status(login_id):
    g.db.execute('select is_suspended from rbac_users where login_id=%s', (login_id,) )
    user_status = g.db.fetchone()
    print 'User Status= ',user_status
    if user_status is not None and len(user_status)>0: return user_status[0]
    else: return 0

"""
    Service Name: add_login_id_mapping 
    Parameters: login_id, role_id
    Response: success/failure message

    Description: 
    Used to map the login_id with the role_id within rbac_users table
    The mapping is maintained in order to provide appropriate permissions when requesting for permissions for the login_id.
"""
#@app.route('/add_login_id_mapping')
def add_login_id_mapping():
    app.logger.info("+++++[ REQUEST:/add_login_id_mappingrequest ]+++++")
    params = {'customer_id':'int','customer_db':'str','role_id':'int','login_id':'str'}
    r = _request_parser(request,params)
    app.logger.info("/add_login_id_mappingrequest params")
    app.logger.info(r) 

    status = _check_customer_db(r)
    response_flag = app.config['FAILURE']
    status_flag = 'not ok'
    error_flag = 'no error'
    data_flag = {'login_id':r['login_id'], 'role_id':r['role_id']}

    if status:
        role_id = _get_user_role(r['login_id'])
        if not len(role_id): 
            _add_user(r['login_id'],r['role_id'])
            new_role_id = _get_user_role(r['login_id'])
            if len(new_role_id): 
                response_flag = app.config['SUCCESS']
                status_flag = 'ok'
            else: error_flag = 'role_id not added successfully'
        else: error_flag = 'role_id has been previously assigned to the requested login_id. Cannot add duplicate mapping'        
    else: error_flag = app.config['MISSING_PARAM_ERROR']
    json_response = {'response':response_flag, 'status':status_flag, 'error': error_flag, 'data':data_flag }
    return json.dumps(json_response)

def _add_user(login_id,role_id):
    g.db.execute('insert into rbac_users (login_id,role_id) values (%s,%s)', (login_id, role_id ) )

# Added User_id for optimizing the parameter consumption. 
# Once the APIs have been satisfactorily tested, the previous version needs to be phased out.
@app.route('/add_login_id_mapping')
def add_login_id_mapping1():
    app.logger.info("+++++[ REQUEST:/add_login_id_mappingrequest ]+++++")
    params = {'customer_id':'int','customer_db':'str','role_id':'int','login_id':'str','user_id':'int'}
    r = _request_parser(request,params)
    app.logger.info("/add_login_id_mappingrequest params")
    app.logger.info(r) 

    status = _check_customer_db(r)
    response_flag = app.config['FAILURE']
    status_flag = 'not ok'
    error_flag = 'no error'
    data_flag = {'login_id':r['login_id'], 'role_id':r['role_id'], 'user_id':r['user_id']}

    if status:
        role_id = _get_user_role(r['login_id'])
        if not len(role_id): 
            _add_user1(r['login_id'],r['role_id'],r['user_id'])
            new_role_id = _get_user_role(r['login_id'])
            if len(new_role_id): 
                response_flag = app.config['SUCCESS']
                status_flag = 'ok'
            else: error_flag = 'role_id not added successfully'
        else: error_flag = 'role_id has been previously assigned to the requested login_id. Cannot add duplicate mapping'        
    else: 
        #error_flag = app.config['MISSING_PARAM_ERROR']
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404  

    json_response = {'response':response_flag, 'status':status_flag, 'error': error_flag, 'data':data_flag }
    return json.dumps(json_response)

def _add_user1(login_id,role_id,user_id):
    g.db.execute('insert into rbac_users (user_id,login_id,role_id) values (%s,%s,%s)', (user_id, login_id, role_id ) )

def _add_user2(login_id,role_id):
    response = {}
    role_id = _get_user_role(login_id)
    if len(role_id):
        g.db.execute('insert into rbac_users (login_id,role_id) values (%s,%s)', (login_id, role_id ) )
        role_id = _get_user_role(login_id)
        if len(role_id):
            response['error'] = 'login_id mapping failed'
        else:
            response['status'] = 'ok'
    else: 
        response['error'] = 'login_id mapped to role_id'
    return response

"""
>>> parseaddr('test_user@equipa.com3268a<script>alert(1)<%2fscript>fa612')
('', 'test_user@equipa.com3268a')
"""
def _sanitize_login_id(login_id):
    output = parseaddr(login_id)
    if '@' in output[1]: 
        return output[1]
    else: return ''

# def _does_mapping_exist(login_id,role_id):
    #     g.db.execute('select role_id from rbac_users where login_id=%s and role_id=%s', (login_id,role_id) )
    #     role_id = g.db.fetchone()
    #     print 'Role ID= ',role_id
    #     if (role_id>0): return role_id
    #     else: return 0    

"""
    Service Name: update_login_id_mapping 
    Parameters: login_id, role_id
    Response: success/failure message

    Description: 
    Used to update the login_id <=> role_id mapping within rbac_users table The mapping is maintained in order to provide appropriate permissions when requesting for permissions for the login_id.
"""
@app.route('/update_login_id_mapping')
def update_login_id_mapping():
    app.logger.info("+++++[ REQUEST:/update_login_id_mappingrequest ]+++++")
    params = {'customer_id':'int','customer_db':'str','role_id':'int','login_id':'str'}
    r = _request_parser(request,params)
    app.logger.info("/update_login_id_mapping request params")
    app.logger.info(r)  

    status = _check_customer_db(r)
    response_flag = app.config['FAILURE']
    status_flag = 'not ok'
    error_flag = 'no error'
    data_flag = {'login_id':r['login_id'], 'role_id':r['role_id']}

    if status:
        r['login_id'] = _sanitize_login_id(r['login_id'])
        if r['login_id']:
            data_flag['login_id']=r['login_id']
            role_id = _get_user_role(r['login_id'])
            if len(role_id): 
                _update_user(r['login_id'],r['role_id'])
                new_role_id = _get_user_role(r['login_id'])
                # DEBUG
                print 'NEW ROLE ID= ',new_role_id
                if len(new_role_id):
                    if new_role_id[0] == r['role_id']: 
                        response_flag = app.config['SUCCESS']
                        status_flag = 'ok'
                    else: error_flag = 'role_id not added successfully'
                else: error_flag = 'role_id returned a empty tuple'
            else: error_flag = 'Invalid login_id provided. There is no login_id<=>role_id mapping in the database.'  
        else: return json.dumps(app.config['MISSING_PARAM_ERROR']),404  
    else: 
        #error_flag = app.config['MISSING_PARAM_ERROR']
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404 
    json_response = {'response':response_flag, 'status':status_flag, 'error': error_flag, 'data':data_flag }
    return json.dumps(json_response)

def _update_user(login_id,role_id):
    g.db.execute('update rbac_users set role_id = %s where login_id = %s', (role_id, login_id) )

@app.route('/validate_role1')
def validate_role1():
    app.logger.info("+++++[ REQUEST:/validate_role request ]+++++")
    params = {'customer_id':'int','customer_db':'str','role_name':'str'}
    r = _request_parser(request,params)

    app.logger.info("/validate_role request params")
    app.logger.info(r)  

    status_flag = app.config['FAILURE']
    error_flag = 'no error'
    data_flag = {'role_name':r['role_name']}

    status = _check_customer_db(r)
    if status:
        role_id = _get_role_id_for_role_name(r['role_name'])
        if len(role_id) == 1: 
            status_flag = app.config['SUCCESS']
            data_flag['role_id'] = role_id[0]
        elif len(role_id) > 1:
            status_flag = app.config['SUCCESS']
            data_flag['role_id'] = role_id
            error_flag = 'Too many roles with the same name'
        else : error_flag = 'role_name does not exist'
    else:
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404 

    json_response = {'status':status_flag, 'error': error_flag, 'data':data_flag }
    return json.dumps(json_response)

# FIX: Adding the fix to incorporate checks for the existence of a ROLE_NAME with the same ROLE_NAME & same ROLE_ID as being updated by
@app.route('/validate_role')
def validate_role():
    app.logger.info("+++++[ REQUEST:/validate_role request ]+++++")
    params = {'customer_id':'int','customer_db':'str','role_name':'str','role_id':'int'}
    r = _request_parser(request,params)

    # This FIX has been added to prevent the URL ENCODED string 'Super%20Admin' from being added when the value within the database is 'Super Admin'
    # Resulting in 2 entries which looks alike but one has %20 ie. encoded value for space, within the name.
    r['role_name'] = urllib.unquote(r['role_name'])
    
    app.logger.info("/validate_role request params")
    app.logger.info(r)  

    status_flag = app.config['FAILURE']
    error_flag = 'no error'
    data_flag = {'role_name':r['role_name']}

    status = _check_customer_db(r)
    if status:
        role_id = _get_role_id_for_role_name(r['role_name'])
        if len(role_id) >= 1: 
            if (r['role_id'] in role_id):
                error_flag = 'The role_id that is being validated exists with the same role name'
            else:
                status_flag = app.config['SUCCESS']
            data_flag['role_id'] = role_id[0]
            error_flag = 'Roles with the same name'    
        else : error_flag = 'role_name does not exist'
    else:
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404 

    json_response = {'status':status_flag, 'error': error_flag, 'data':data_flag }
    return json.dumps(json_response)

def _get_role_id_for_role_name(role_name):
    g.db.execute('select role_id from rbac_roles where role_name=%s', (role_name,))
    #role_id = g.db.fetchone()
    role_id = [ row[0] for row in g.db.fetchall()]
    print 'Role ID= ',role_id
    if len(role_id)>0: return role_id
    else: return []

@app.route('/validate_login')
def validate_login():   
    app.logger.info("+++++[ REQUEST:/validate_login request ]+++++")
    params = {'customer_id':'int','customer_db':'str','login_id':'str'}
    r = _request_parser(request,params)
    app.logger.info("/validate_login request params")
    app.logger.info(r)  

    status_flag = app.config['FAILURE']
    error_flag = 'no error'
    data_flag = {'login_id':r['login_id']}

    status = _check_customer_db(r)
    if status:
        role_id = _get_user_role(r['login_id'])
        if len(role_id) == 1: 
            status_flag = app.config['SUCCESS']
            data_flag['role_id'] = role_id[0]
            data_flag['is_suspended'] = _check_user_status(r['login_id'])
        else : error_flag = 'login_id does not exist'
    else:
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404 

    json_response = {'status':status_flag, 'error': error_flag, 'data':data_flag }
    return json.dumps(json_response)


##### RBAC: ACCESS CONTROL #####

## START: ACCESS CONTROL API ##

"""
 API to display the Access Control defined for a Role 
"""
@app.route('/access_control')
def get_access_control():
    app.logger.info("+++++[ REQUEST:/modules ]+++++")
    params = {'customer_id':'int','customer_db':'str','role_id':'int'}
    r = _request_parser(request,params)
    app.logger.info("/modules    request params")
    app.logger.info(r)    

    access_control = {}
    #TODO: Move the error_message to a CONSTANTS file or DB table for central access
    error_message = 'customer_db or customer_id or role_id parameter missing'
    status = _check_customer_db(r)

    if status:  access_control = _get_access_control(r['role_id'])
    else: 
        #access_control['error'] = error_message
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404 

    return json.dumps(access_control)

def _get_access_control(role_id):
    access_control_list = []
    access_control = {}

    print 'ROLE_ID:',role_id
    if role_id>0:
        g.db.execute('select a.acl_id, a.role_id, a.perm_id, p.perm_name from rbac_access_control a, rbac_permission_inventory p where a.role_id=%s and a.perm_id=p.perm_id', (role_id,))
    else :
        g.db.execute('select a.acl_id, a.role_id, a.perm_id, p.perm_name from rbac_access_control a, rbac_permission_inventory p where a.perm_id=p.perm_id')

    access_control_list = [ dict(acl_id = row[0], role_id = row[1], perm_id = row[2], perm_name = row[3]) for row in g.db.fetchall()]
    access_control['data'] = access_control_list

    if len(access_control['data']) > 0: access_control['status'] = 'ok'
    else: access_control['status'] = 'no data'

    print 'access_control=',access_control
        
    return access_control    

## END: ACCESS CONTROL API ##

## HELPER FUNCTIONS for UI processing ##

"""
 Method to setup the schema for access.
"""
def _check_customer_db(r):
    # Sets the customer_id as required within the schema. Once the setting is in place, the queries are fired against the set schema.    
    customer_db = ''    
    if r['customer_db']: customer_db = r['customer_db']
    if r['customer_id']: customer_db = _read_customer_schema(r['customer_id'])
    print 'customer_db = ',customer_db

    status = 0
    if customer_db: 
        flag = _is_schema_present(customer_db)
        if flag:
            _set_search_path(customer_db)
            status = 1
    return status

def _is_schema_present(customer_db):
    g.db.execute('SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s;', (customer_db,))
    schema_name = g.db.fetchone()
    if schema_name is not None and len(schema_name) > 0:return 1
    else: return 0

"""
 Get the name of the template baed on the module that is requested.
"""
def _get_template(module_id):
    # TODO: Get the module list from the function mapped to the table.
    modules = {1:'account-config',2:'dashboards',3:'records',4:'projects', 5:'rfqs'}
    #modules = _get_module_names()
    print modules
    rbac_folder='rbac'  
    #templates = {1:'account-config.html',2:'dashboards.html',3:'records.html',4:'projects.html'}
    #templates = {1:'account-config1.html',2:'dashboards.html',3:'records.html',4:'projects.html'}
    #templates = {1:'account-config2.html',2:'dashboards.html',3:'records.html',4:'projects.html'}
    display_temp = 'display-access-control.html'
    templates = {1:display_temp, 2:display_temp, 3:display_temp, 4:display_temp, 5:display_temp}

    if module_id>0: 
        module_name = modules[module_id]
        template_name = os.path.join(rbac_folder,templates[module_id])
    return template_name

"""
    Get Default Module ID
"""
def _get_module_id(module_id):
    default_module_id = app.config['DEFAULT_MODULE_ID']
    module_id = int(module_id)
    if not module_id: module_id = default_module_id # Set default module_id if not set.
    return module_id

"""
 Validate the user access using the permissions for the Role that the user belongs to.
 Get the access control for the user.
"""
@app.route('/validate_user_access', methods=['GET'])
def validate_user_access():
    app.logger.info("+++++[ REQUEST:/role_permissions ]+++++")
    params = {'perm_id':'int','login_id':'str','perm_name':'str','customer_id':'int','customer_db':'str'}
    r = _request_parser(request,params)
    app.logger.info("/role_permissions request params")
    app.logger.info(r)    

    status = _check_customer_db(r)
    if status:
        role_id = _get_user_role(r['login_id'])
        permissions = _get_access_control(role_id)
        acl_id,status = _validate_access(role_id,r['perm_id'],r['perm_name'])
        access_dict = {'login_id':r['login_id'],'status':status,'acl_id':acl_id, 'permissions':permissions}
        access_response = json.dumps(access_dict)
    else: 
        #access_response = 'error: customer_db or customer_id parameter missing'
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404 

    return access_response

def _validate_access(role_id,perm_id,perm_name):
    check_acl_id = 0
    acl_id = 0
    acl_response = 'F'

    # NOT REQUIRED UNTIL perm_id is being passed
        #if perm_id:
        #    g.db.execute('select acl_id from rbac_access_control acl where role_id=%s and perm_id=%s', (role_id,perm_id))
        #    check_acl_id =1 

    if perm_name:
        g.db.execute('select a.acl_id from rbac_access_control a, rbac_permission_inventory p where a.role_id=%s and p.perm_name=%s and a.perm_id=p.perm_id', (role_id,perm_name))
        check_acl_id = 1
    if check_acl_id: 
        acl_id = g.db.fetchone()
        if (acl_id>0): acl_response = 'T'
        else : acl_id, acl_response = _check_full_access(role_id,perm_name)

    return acl_id, acl_response

def _get_module_code_from_perm_name(perm_name):
    return perm_name.split('_')[0]

def _check_full_access(role_id,perm_name):
    module_code = _get_module_code_from_perm_name(perm_name)
    access_control = _get_access_control(role_id)
    acl_id = 0
    acl_response = 'F'
    for acl_item in access_control:
        if acl_item['perm_name'] == module_code+'_FULL_ACCESS':
            acl_id = acl_item['acl_id'] 
            acl_response = 'T' 
            return acl_id, acl_response
    return acl_id,acl_response

@app.route('/get_user_permissions', methods=['GET'])
def get_user_permissions():
    app.logger.info("+++++[ REQUEST:/role_permissions ]+++++")
    params = {'login_id':'str','customer_id':'int','customer_db':'str'}
    r = _request_parser(request,params)
    app.logger.info("/role_permissions request params")
    app.logger.info(r)    

    permission_response = {'login_id':r['login_id'],'permissions':[]}
    status = _check_customer_db(r)
    if status:
        if r['login_id']:
            is_suspended = _check_user_status(r['login_id'])
            if not is_suspended:
                role_id = _get_user_role(r['login_id'])
                if len(role_id):
                    role_info = _get_role_info(role_id[0])
                    print 'role_info=',role_info
                    permissions = _get_access_control(role_id)
                    permission_response = {'role_id':role_id[0], 'role_name':role_info['role_name'], 'permissions':permissions['data'], 'status':permissions['status']}
                else: permission_response['error'] = 'role_id for the login_id not found'
            else: permission_response['error'] = 'login_id has been suspended'
        else: permission_response['error'] = 'login_id parameter missing'
    else : permission_response['error'] = 'customer_db or customer_id parameter missing'

    return json.dumps(permission_response)

"""
    Function to display the permissions for the selected ROLE

    http://zurich.equipa.com:5001/rbac_roles?customer_db=equipa
    output: display UX to manage the permissions for Account Configuration

    http://zurich.equipa.com:5001/rbac_roles?customer_db=equipa&module_id=2
    output: display UX to manage the permissions for  dashboards

    Module Id: Module Name
    1: Account Configuration
    2: Dashboards 
    3: Records
    4: Projects
"""
# @app.route('/manage_access_control', methods=['GET', 'POST'])
    # def manage_access_control():
    #     app.logger.info("+++++[ REQUEST:/manage_access_control ]+++++")
    #     params = {'role_id':'int','module_id':'int','customer_id':'int','customer_db':'str'}
    #     r = _request_parser(request,params)
    #     app.logger.info("/manage_access_control request params")
    #     app.logger.info(r)

    #     r['acl'] = {}
    #     r['permission_inventory'] = {}
    #     r['module_perm_mapping'] = {}

    #     status = _check_customer_db(r)

    #     print 'DEBUG: Trying to get to the actual acl data ...'
    #     if status:
    #         r['acl'] = _get_access_control(r['role_id'])
    #         #DEBUG
    #         #print 'acl= ',r['acl']
    #         r['module_id'] =  _get_module_id(r['module_id'])
    #         r['permission_inventory'] = _get_permission_inventory(r['module_id'])
    #         r['module_perm_mapping'] = _get_sub_modules(r)
    #         r['template_name'] = _get_template(r['module_id'])
    #     else: 
    #         r['template_name'] = app.config['ERROR_PAGE']

    #     return render_template(r['template_name'], customer_db=r['customer_db'], acl=r['acl'], role_id=r['role_id'], module_id=r['module_id'], permission_inventory=r['permission_inventory'],module_perm_mapping=r['module_perm_mapping'])

## START: UI to display the permissions using sub-modules ##
#@app.route('/display_access_control', methods=['GET','POST'])
def display_access_control():
    app.logger.info("+++++[ REQUEST:/display_permissions ]+++++")
    params = {'customer_id':'int','customer_db':'str','role_id':'int','module_id':'int','output':'str'}
    r = _request_parser(request,params)
    app.logger.info("/display_permissions request params")
    app.logger.info(r)

    r['module_id'] =  _get_module_id(r['module_id'])
    sub_module_list = _get_sub_modules(r)

    if sub_module_list:
        r['permission_inventory'] = []
        r['saved_permission'] = _get_perm_id_for_role_id(r['role_id'])
        #DEBUG
        print 'saved_permission= ',r['saved_permission']

        for item in sub_module_list:
            sub_module_id = item['sub_module_id']
            sub_module_code = item['sub_module_code']
            item['perm_inventory'] = _get_permission_inventory_for_sub_mod_id(sub_module_id,)
            item['perm_count'] = len(item['perm_inventory'])
            r['permission_inventory'].append(item)   
        r['template_name'] = _get_template(r['module_id'])
    else: 
        r['template_name'] = app.config['ERROR_PAGE']

    r['noaccess'] = ['true','false']

    if r['output'] == 'json':
        #return json.dumps(r['permission_inventory'])
        return json.dumps(r)
    else:

        return render_template(r['template_name'], customer_db=r['customer_db'], role_id=r['role_id'], module_id=r['module_id'], permission_inventory=r['permission_inventory'],saved_permission=r['saved_permission'],noaccess=r['noaccess'] )
  
def _get_sub_modules(r):
    status = _check_customer_db(r) # sets the search path to the required customer_db
    if status:    
        g.db.execute('select sub_module_id, sub_module_code, sub_module_name from rbac_sub_modules where module_id=%s', (r['module_id'],) )
        sub_module_list = [ dict(sub_module_id = row[0], sub_module_code = row[1], sub_module_name= row[2]) for row in g.db.fetchall()]
    else: sub_module_list = []  

    return sub_module_list

def _get_permission_inventory_for_sub_mod_id(sub_module_id):
    g.db.execute('select perm_id, perm_name, perm_description, sort_order, perm_type, perm_dependency from rbac_permission_inventory where sub_module_id=%s order by sub_module_id, sort_order', (sub_module_id,) )
    sub_mod_perm_inventory = [ dict(perm_id = row[0], perm_name = row[1], perm_description = row[2], sort_order = row[3], perm_type = row[4], perm_dependency = row[5]) for row in g.db.fetchall()]
 
    return sub_mod_perm_inventory

## END: display_permissions ##

"""
    Function to update the ACCESS CONTROL for a specific ROLE_ID & SUB_MODULE_ID within a CUSTOMER_DB
"""
#@app.route('/update_access_control', methods=['POST','GET'])
def update_access_control():
    params = {'customer_id':'str' ,'customer_db':'str','role_id':'str', 'module_id':'int', 'sub_module_id':'int', 'sub_module_code':'str', 'radio_access_type':'str','output':'str'}
    r = _request_parser(request,params)

    app.logger.info("/update_access_control request params")
    app.logger.info(r)

    r = _update_access_control(request,r)
    return redirect(url_for('display_access_control',customer_db=r['customer_db'], role_id=r['role_id'], module_id=r['module_id'], output=r['output']))

def _update_access_control(request,r):
    r,q = _extract_proposed_perm_from_request(request,r) 
    app.logger.info(q)

    response = {}
    error_message = 'customer_db or customer_id or role_id parameter missing' 
    status = _check_customer_db(r)
    
    if status:  
        response = _synchronize_access(r,q)
        r['module_id'] =  _get_module_id(r['module_id'])
        r['template_name'] = _get_template(r['module_id'])
    else: 
        r['template_name'] = app.config['404_PAGE']    
    return r

def _extract_proposed_perm_from_request(request,r):
    q = {}
    if r['sub_module_id']:
        perm_params = {}
        sub_mod_perm_ids = []
        perm_inventory_for_sub_module_id = _get_permission_inventory_for_sub_mod_id(r['sub_module_id'])

        for perm in perm_inventory_for_sub_module_id:
            perm_name = perm['perm_name']
            perm_id = perm['perm_id']
            perm_params[perm_name] = 'int'   
            sub_mod_perm_ids.append(perm_id)

        access_type  = r['radio_access_type']
        perm_params[access_type] = 'int'
        q = _request_parser(request, perm_params)
        r['sub_mod_perm_ids'] = sub_mod_perm_ids

    return r,q

def _synchronize_access(r,q):
    perm_ids = _get_perm_ids(r,q)
    print 'clean all permissions for the sub-module and re-insert the newly defined ones'
    _delete_full_access_for_sub_module(r,q)
    # DEBUG
    print 'perm_ids to be added: ',perm_ids
    #sync_response = _synchronize_access(r['role_id'],perm_ids) 
    sync_response = _insert_access_control_entries(r['role_id'],perm_ids)
    response = {}
    response ['status'] = sync_response
    return response

def _insert_access_control_entries(role_id,perm_ids):             
    for perm_id in perm_ids:
        print "role_id=",role_id," perm_id=",perm_id
        g.db.execute('INSERT into rbac_access_control (role_id,perm_id) SELECT %s,%s WHERE NOT EXISTS (SELECT * from rbac_access_control where role_id=%s and perm_id=%s)', (role_id, perm_id,role_id, perm_id) )
    return 'success'

#TODO: rename to _get_perm_ids when the OLD one is removed
def _get_perm_ids(r,q):
    # Extract perm_ids for all the Permissions
    radio_access_type = r['radio_access_type']
    access_type = int(q[radio_access_type])
    q.pop(radio_access_type) # delete from q for perm_id processing
    #DEBUG
    print 'access_type= ',access_type
    perm_ids=[]

    if access_type == 1: # NO Access
        app.logger.info('Module NO Access') 

    elif access_type ==2 : # FULL Access
        app.logger.info('Module FULL Access')
        #sub_mod_full_access_perm_id = _get_full_access_perm_id_for_sub_mod_id1(r['sub_module_id'])
        #if sub_mod_full_access_perm_id['perm_id']>0: perm_ids.append(sub_mod_full_access_perm_id['perm_id'])

        sub_mod_full_access_perm_id = _get_full_access_perm_id_for_sub_mod_id(r['sub_module_id'])
        if len(sub_mod_full_access_perm_id)>0: perm_ids = perm_ids + sub_mod_full_access_perm_id

    elif access_type == 3: # CUSTOM Access
        app.logger.info('Module CUSTOM Access')  
       
        for item in q.iteritems(): 
            if item[1] != 0: perm_ids.append(item[1])

    return perm_ids

#TODO: Phase out the API once the FULL_ACCESS has been fully removed.
    # def _get_full_access_perm_id_for_sub_mod_id1(sub_module_id):
    #     g.db.execute('select perm_id, perm_name, perm_description from rbac_permission_inventory where sub_module_id=%s and perm_id>=%s;', (sub_module_id,app.config['FULL_ACCESS']) )
    #     #g.db.execute('select perm_id, perm_name, perm_description from rbac_permission_inventory where sub_module_id=%s and perm_id<%s;', (sub_module_id,app.config['FULL_ACCESS']) )
    #     sub_mod_full_access_perm_id = [dict(perm_id = row[0], perm_name = row[1], perm_description = row[2]) for row in g.db.fetchall()]
    #     #DEBUG
    #     print 'sub_mod_full_access_perm_id= ',sub_mod_full_access_perm_id
    #     if len(sub_mod_full_access_perm_id)>0:
    #         return sub_mod_full_access_perm_id[0]
    #     else: return {'perm_id':0} # recover from no records in db related to the sub_module_id

def _get_full_access_perm_id_for_sub_mod_id(sub_module_id):
    g.db.execute('select perm_id from rbac_permission_inventory where sub_module_id=%s and perm_id<%s;', (sub_module_id,app.config['FULL_ACCESS']) )
    sub_mod_full_access_perm_id = [ row[0] for row in g.db.fetchall() ]
    #DEBUG
    print 'sub_mod_full_access_perm_id= ',sub_mod_full_access_perm_id
    if len(sub_mod_full_access_perm_id)>0:
        return sub_mod_full_access_perm_id
    else: return [] # recover from no records in db related to the sub_module_id

"""
 In order to remove full access from the rbac_access_control table, 
 we need to compute the sub_module full access permmission_id

"""
def _delete_full_access_for_sub_module(r,q):
    status = _check_customer_db(r)
    #DEBUG
    print 'sub_mod_perm_ids= ',r['sub_mod_perm_ids']
    if status:
        for perm_id in r['sub_mod_perm_ids']:
            #DEBUG
            print 'deleting perm_id ...',perm_id
            g.db.execute('DELETE from rbac_access_control where role_id=%s and perm_id=%s', (r['role_id'], perm_id) )

def _get_perm_id_for_role_id(role_id):
    perm_id_list = []
    perm_id_dict = {}

    print 'ROLE_ID:',role_id
    if role_id>0:
        #g.db.execute('select a.acl_id, a.role_id, a.perm_id, p.perm_name from rbac_access_control a, rbac_permission_inventory p where a.role_id=%s and a.perm_id=p.perm_id', (role_id,))
        g.db.execute('select a.perm_id from rbac_access_control a, rbac_permission_inventory p where a.role_id=%s and a.perm_id=p.perm_id', (role_id,))        
    else :
        g.db.execute('select a.perm_id from rbac_access_control a, rbac_permission_inventory p where a.perm_id=p.perm_id')

    perm_id_list = [ row[0] for row in g.db.fetchall() ]
    perm_id_dict['data'] = perm_id_list

    if len(perm_id_dict['data']) > 0: perm_id_dict['status'] = 'ok'
    else: perm_id_dict['status'] = 'no data'

    #DEBUG
    print 'perm_id_dict=',perm_id_dict
        
    return perm_id_dict    

# DISPLAY ACCESS CONTROL FOR FULL ACCESS
@app.route('/display_access_control', methods=['GET','POST'])
def display_access_control1():
    app.logger.info("+++++[ REQUEST:/display_permissions ]+++++")
    params = {'customer_id':'int','customer_db':'str','role_id':'int','module_id':'int','output':'str'}
    r = _request_parser(request,params)
    app.logger.info("/display_permissions request params")
    app.logger.info(r)

    status = _check_customer_db(r)
    if status:
        r['module_id'] =  _get_module_id(r['module_id'])
        sub_module_list = _get_sub_modules(r)

        if sub_module_list:
            r['permission_inventory'] = []
            r['saved_permission'] = _get_perm_id_for_role_id(r['role_id'])
            #DEBUG
            print 'saved_permission= ',r['saved_permission']

            for item in sub_module_list:
                sub_module_id = item['sub_module_id']
                sub_module_code = item['sub_module_code']
                item['perm_inventory'] = _get_permission_inventory_for_sub_mod_id(sub_module_id,)
                item['perm_count'] = len(item['perm_inventory'])
                r['permission_inventory'].append(item)   
            r['template_name'] = _get_template(r['module_id'])
        else: 
            r['template_name'] = app.config['ERROR_PAGE']

        r['module_names'] = _get_module_names()
        r['noaccess'] = ['true','false']
    else:
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404 

    if r['output'] == 'json':
        #return json.dumps(r['permission_inventory'])
        return json.dumps(r)
    else:
        r['template_name'] = 'rbac/display-access-control-full.html'
        return render_template(r['template_name'], customer_db=r['customer_db'], role_id=r['role_id'], module_id=r['module_id'], permission_inventory=r['permission_inventory'],saved_permission=r['saved_permission'],noaccess=r['noaccess'],module_names=r['module_names'])

# UPDATE ACCESS CONTROL FOR FULL ACCESS 
@app.route('/update_access_control', methods=['POST','GET'])
def update_access_control1():
    params = {'customer_id':'str' ,'customer_db':'str','role_id':'str', 'module_id':'int', 'sub_module_id':'int', 'sub_module_code':'str', 'radio_access_type':'str','output':'str'}
    r = _request_parser(request,params)

    app.logger.info("/update_access_control1 request params")
    app.logger.info(r)

    status = _check_customer_db(r)
    
    if status:
        r = _update_access_control1(request,r)
    else:
        #r['template_name'] = app.config['404_PAGE']    
        return json.dumps(app.config['MISSING_PARAM_ERROR']),404 

    return redirect(url_for('display_access_control1',customer_db=r['customer_db'], role_id=r['role_id'], module_id=r['module_id'], output=r['output']))

def _update_access_control1(request,r):

    if r['module_id']:
        r,q = _extract_proposed_perm_from_request1(request,r) 
        print 'OUTPUT of q'
        app.logger.info(q)
        s = _extract_proposed_radio_from_request1(request,r) 
        print 'OUTPUT of s'
        app.logger.info(s)

    response = {}
    error_message = 'customer_db or customer_id or role_id parameter missing' 
  
    response = _synchronize_access1(r,q,s)
    r['module_id'] =  _get_module_id(r['module_id'])
    r['template_name'] = _get_template(r['module_id'])
    return r

# Remove once the bug fix in _update_access_control1 works.
def _update_access_control2(request,r):
    if r['module_id']:
        r,q = _extract_proposed_perm_from_request1(request,r) 
        print 'OUTPUT of q'
        app.logger.info(q)
        s = _extract_proposed_radio_from_request1(request,r) 
        print 'OUTPUT of s'
        app.logger.info(s)

    response = {}
    error_message = 'customer_db or customer_id or role_id parameter missing' 
    status = _check_customer_db(r)
    
    if status:  
        response = _synchronize_access1(r,q,s)
        r['module_id'] =  _get_module_id(r['module_id'])
        r['template_name'] = _get_template(r['module_id'])
    else: 
        r['template_name'] = app.config['404_PAGE']    
    return r

def _extract_proposed_perm_from_request1(request,r):
    q = {}
    perm_params = {}
    sub_mod_perm_ids = []
    
    perm_inventory_for_module_id = _get_permission_inventory_for_mod_id(r['module_id'])
    print 'perm_inventory_for_module_id=',perm_inventory_for_module_id

    for perm in perm_inventory_for_module_id:
        perm_name = perm['perm_name']
        perm_id = perm['perm_id']
        perm_params[perm_name] = 'int'   
        sub_mod_perm_ids.append(perm_id)
    r['sub_mod_perm_ids'] = sub_mod_perm_ids
    print 'perm_params=',perm_params
    q = _request_parser(request, perm_params)
    
    return r,q

def _extract_proposed_radio_from_request1(request,r):
    s = {}
    radio_params = {}
    r['sub_modules'] = _get_sub_modules(r)
    # DEBUG
    print 'sub_modules:',r['sub_modules']

    for sub_module in r['sub_modules']:
        access_type  = sub_module['sub_module_code']+'_TYPE_RADIO'
        radio_params[access_type] = 'int'

    s = _request_parser(request, radio_params)
    
    return s

def _synchronize_access1(r,q,s):
    perm_ids = []

    perm_ids = _get_perm_ids1(r,q,s)
    print 'perm_ids = ',perm_ids

    print 'clean all permissions for the sub-module and re-insert the newly defined ones'
    _delete_full_access_for_sub_module(r,q)
    # DEBUG
    print 'perm_ids to be added: ',perm_ids
    sync_response = _insert_access_control_entries(r['role_id'],perm_ids)
    response = {}
    response ['status'] = sync_response
    return response

#TODO: rename to _get_perm_ids when the OLD one is removed
def _get_perm_ids1(r,q,s):
    # Extract perm_ids for all the Permissions
    perm_ids=[]
    posted_perm_ids = []
    
    # Get Perm Ids from q => Gives you all the Custom Perm Ids
    for item in q.iteritems(): 
        if item[1] != 0: posted_perm_ids.append(item[1])
    print 'posted_perm_ids=',posted_perm_ids

    for sub_module in r['sub_modules']:
        radio_access_type = sub_module['sub_module_code']+'_TYPE_RADIO'
        access_type = int(s[radio_access_type])
        #s.pop(radio_access_type) # delete from s for perm_id processing
        #DEBUG
        print 'access_type= ',access_type

        sub_mod_full_access_perm_id = _get_full_access_perm_id_for_sub_mod_id(sub_module['sub_module_id'])

        if access_type == 1: # NO Access
            app.logger.info(radio_access_type+' NO Access') 
            for perm_id in sub_mod_full_access_perm_id:
                perm_id = str(perm_id)
                if perm_id in posted_perm_ids: posted_perm_ids.remove(perm_id)

        elif access_type ==2 : # FULL Access
            app.logger.info(radio_access_type+' FULL Access')
            if len(sub_mod_full_access_perm_id)>0: perm_ids += sub_mod_full_access_perm_id

        elif access_type == 3: # CUSTOM Access
            app.logger.info(radio_access_type+' CUSTOM Access')
            for perm_id in sub_mod_full_access_perm_id:
                perm_id = str(perm_id)
                if perm_id in posted_perm_ids: perm_ids.append(perm_id)

    perm_ids += posted_perm_ids

    return perm_ids

def _get_permission_inventory_for_mod_id(module_id):
    g.db.execute('select perm_id, perm_name, perm_description from rbac_permission_inventory where module_id=%s', (module_id,) )
    sub_mod_perm_inventory = [ dict(perm_id = row[0], perm_name = row[1], perm_description = row[2]) for row in g.db.fetchall()]
 
    return sub_mod_perm_inventory

# TODO: OLD Functions which needs to be removed. These functions where designed for ENTITY and not SUB-MODULE.
# START: Functions to be removed
    # def _update_access_control(r):
    #     perm_ids = _get_perm_ids(r)
    #     entity_name = 'ENTERPRISE_SETTINGS'
    #     entity_id = 4
    #     sync_response = _synchronize_access(r['role_id'],perm_ids)
        
    #     response = {}
    #     response ['status'] = sync_response

    #     return response

    # def _get_perm_ids(r):
    #     # Extract perm_ids for all the Permissions
    #     perm_ids = _enterprise_settings(r)
    #     return perm_ids

    # def _enterprise_settings(r):    
    #     access_type = int(r['et_acess_type_radio'])
    #     perm_ids=[]
    #     if access_type == 1: # NO Access
    #         app.logger.info('Enterprise Settings NO Access')    
    #     elif access_type >= 100: # FULL Access
    #         app.logger.info('Enterprise Settings FULL Access')
    #         perm_ids.append(access_type)
    #     elif access_type == 3: # CUSTOM Access
    #         _delete_full_access_for_entity(r)
    #         app.logger.info('Enterpise Settings CUSTOM Access')
    #         print 'VIEW:',r['et_view_access'],' EDIT:',r['et_edit_access']
    #         if r['et_view_access']: perm_ids.append(r['et_view_access'])
    #         if r['et_edit_access']: perm_ids.append(r['et_edit_access'])    
    #     return perm_ids

    # """
    #  In order to remove full access from the rbac_access_control table, 
    #  we need to compute the sub_module full access permmission_id

    # """
    # def _delete_full_access_for_entity(r):
    #     module_id = r['module_id']
    #     status = _check_customer_db(r)
    #     if status:
    #         g.db.execute('DELETE from rbac_access_control where module_id=%s and role_id=', (r['module_id'],r['role_id']) )

    # def _get_permission_inventory(module_id):
    #     modules = {1:'account-config',2:'dashboards',3:'records',4:'projects'}

    #     full_permission_inventory = { 
    #         1:{'et_full_access':'100', 'et_view_access':1, 'et_edit_access':2},
    #         2:{'dash_full_access':'100', 'dash_view_access':1, 'et_edit_access':2},
    #         3:{'dash_full_access':'100', 'dash_view_access':1, 'et_edit_access':2},
    #         4:{'dash_full_access':'100', 'dash_view_access':1, 'et_edit_access':2}
    #         }

    #     print 'MODULE_ID:',module_id

    #     if module_id>0:
    #         permission_inventory = full_permission_inventory[module_id]

    #     return permission_inventory
# END: Functions to be removed

# SET FULL PERMISSIONS FOR ACCESS_CONTROL
@app.route('/set_full_access', methods=['POST','GET'])
def set_module_full_access():
    params = {'customer_id':'str' ,'customer_db':'str','role_id':'int', 'module_id':'int', 'output':'str'}
    r = _request_parser(request,params)

    app.logger.info("/set_full_access request params")
    app.logger.info(r)  
    
    status = _check_customer_db(r)
    
    if status: response = _set_full_access(r)
    else:  return json.dumps(app.config['MISSING_PARAM_ERROR']),404 

    return redirect(url_for('display_access_control1',customer_db=r['customer_db'], role_id=r['role_id'], module_id=r['module_id'], output=r['output']))

def _set_full_access(r):
    perm_ids = []
    response = {}
    if r['module_id']:

        print 'clean all permissions for the module and re-insert the modules full permission_inventory'
        _delete_full_access_for_module(r)

        perm_ids = _get_full_access_for_module(r)
        # DEBUG
        print 'perm_ids to be added: ',perm_ids

        sync_response = _insert_access_control_entries(r['role_id'],perm_ids)
        response ['status'] = sync_response
    return response 

def _delete_full_access_for_module(r):
    #DEBUG
    print 'module_id= ',r['module_id']
    g.db.execute('DELETE from rbac_access_control where role_id=%s and perm_id in (SELECT perm_id from rbac_permission_inventory where module_id=%s)', (r['role_id'],r['module_id']) )

def _get_full_access_for_module(r):
    #DEBUG
    #print 'module_id= ',r['module_id']
    g.db.execute('SELECT perm_id from rbac_permission_inventory where module_id=%s', (r['module_id'],) )
    module_perm_inventory = [ row[0] for row in g.db.fetchall()]
 
    return module_perm_inventory

# SET FULL PERMISSIONS FOR ACCESS_CONTROL
@app.route('/set_sub_module_full_access', methods=['POST','GET'])
def set_sub_module_full_access():
    params = {'customer_id':'str' ,'customer_db':'str','role_id':'int', 'module_id':'int', 'sub_module_id':'int', 'output':'str'}
    r = _request_parser(request,params)

    app.logger.info("/set_sub_module_full_access request params")
    app.logger.info(r)  
    
    status = _check_customer_db(r)
    
    if status: response = _set_sub_module_full_access1(r)
    else:  return json.dumps(app.config['MISSING_PARAM_ERROR']),404 

    return redirect(url_for('display_access_control1',customer_db=r['customer_db'], role_id=r['role_id'], module_id=r['module_id'], output=r['output']))

def _set_sub_module_full_access1(r):
    perm_ids = []
    response = {}
    if r['module_id']:

        print 'clean all permissions for the sub-module and re-insert the sub-modules full permission_inventory'
        _delete_full_access_for_sub_module1(r)

        perm_ids = _get_full_access_for_sub_module1(r)
        # DEBUG
        print 'perm_ids to be added: ',perm_ids

        sync_response = _insert_access_control_entries(r['role_id'],perm_ids)
        response ['status'] = sync_response
    return response 

def _delete_full_access_for_sub_module1(r):
    #DEBUG
    print 'module_id= ',r['module_id'],'sub_module_id=',r['sub_module_id']
    g.db.execute('DELETE from rbac_access_control where role_id=%s and perm_id in (SELECT perm_id from rbac_permission_inventory where module_id=%s and sub_module_id=%s)', (r['role_id'],r['module_id'],r['sub_module_id']) )

def _get_full_access_for_sub_module1(r):
    #DEBUG
    #print 'module_id= ',r['module_id']
    g.db.execute('SELECT perm_id from rbac_permission_inventory where module_id=%s and sub_module_id=%s', (r['module_id'],r['sub_module_id']) )
    sub_module_perm_inventory = [ row[0] for row in g.db.fetchall()]
 
    return sub_module_perm_inventory

# INSERT INDIVIDIAL PERMISSIONS FOR ACCESS_CONTROL
@app.route('/set_perm_access', methods=['POST','GET'])
def set_perm_access():
    params = {'customer_id':'str' ,'customer_db':'str','role_id':'int','module_id':'int', 'perm_id':'int', 'output':'str'}
    r = _request_parser(request,params)

    app.logger.info("/set_sub_module_full_access request params")
    app.logger.info(r)  
    
    status = _check_customer_db(r)
    
    if status:
        _insert_access_control_entry(r['role_id'], r['perm_id'])
    else:  return json.dumps(app.config['MISSING_PARAM_ERROR']),404 

    #return redirect(url_for('display_access_control1',customer_db=r['customer_db'], role_id=r['role_id'], module_id=r['module_id'], output=r['output']))
    response = {'status':'Updated permission successfully','error':'no error'}
    return json.dumps(response)

def _insert_access_control_entry(role_id,perm_id):
    print "role_id=",role_id," perm_id=",perm_id
    g.db.execute('INSERT into rbac_access_control (role_id,perm_id) SELECT %s,%s WHERE NOT EXISTS (SELECT * from rbac_access_control where role_id=%s and perm_id=%s)', (role_id, perm_id, role_id, perm_id) )
    return 'success'

# GET USER LISTING HAVING PROJECT ADD/EDIT PERMISSIONS 
@app.route('/get_project_membership_users_list', methods=['POST','GET'])
def get_project_membership_users_list():
    params = {'customer_id':'str' ,'customer_db':'str', 'output':'str'}
    r = _request_parser(request,params)

    app.logger.info("/get_project_contacts request params")
    app.logger.info(r)  
    
    status = _check_customer_db(r)
    error = 'no error'
    login_ids = []
    
    if status:
        login_ids = _get_project_users()
    else:  return json.dumps(app.config['MISSING_PARAM_ERROR']),404 

    #return redirect(url_for('display_access_control1',customer_db=r['customer_db'], role_id=r['role_id'], module_id=r['module_id'], output=r['output']))
    response = {"data": login_ids, "error":error}
    return json.dumps(response) 
    #return 'success'

def _get_project_users():
    patterns_dict = {"project_edit":"PROJ_EDIT_PROJECT","project_notification":"PROJ%NOTIFICATION%"}
    login_ids_dict = _filter_project_permission_ids(patterns_dict)
    common_login_ids = []
    for login_id in login_ids_dict['project_edit']:
        if login_id in login_ids_dict['project_notification']: 
            common_login_ids.append(login_id)
    return common_login_ids

def _filter_project_permission_ids(patterns_dict):
    login_ids_dict = {}
    for perm_type,perm_pattern in patterns_dict.iteritems():
        #g.db.execute('SELECT perm_id from rbac_permission_inventory where perm_name in %s', (perm_pattern,) )
        g.db.execute('select u.login_id from rbac_users u, rbac_access_control a where a.role_id = u.role_id and a.perm_id in (select perm_id from rbac_permission_inventory where perm_name like %s) and is_suspended=0', (perm_pattern,))
        login_ids = [ row[0] for row in g.db.fetchall()]
        login_ids_dict[perm_type] = login_ids

    print "login_ids_dict=",login_ids_dict
    return login_ids_dict    

##### MODULE UX FUNCTIONS ######
# @app.route('/dashboards')
# def dashboards():

#     return render_template('modules/dashboards.html', customer_id=app.config['CUSTOMER_ID'],) 

# @app.route('/records')
# def records():

#     return render_template('modules/records.html', customer_id=app.config['CUSTOMER_ID'],) 

# @app.route('/projects')
# def projects():

#     return render_template('modules/projects.html', customer_id=app.config['CUSTOMER_ID'],) 

# @app.route('/notifications')
# def notifications():

#     return render_template('modules/notifications.html', customer_id=app.config['CUSTOMER_ID'],) 


##### END OF FUNCTIONS ######

if __name__ == "__main__":
	# ---------
	#Non-SSL Setup
	# ---------
	#app.run(host='0.0.0.0', port=5000, debug=True)

	# ---------
	# SSL Setup 
	# ---------
	#app.run(host='0.0.0.0', port=5000, ssl_context=(app.config['CRT'], app.config['KEY']))
	print 'CRT=',app.config['CRT']
	print 'KEY=',app.config['KEY']

	#app.run('0.0.0.0', debug=True, port=5000, ssl_context=(app.config['CRT'], app.config['KEY']))
	app.run('0.0.0.0', port=8200, ssl_context=(app.config['CRT'], app.config['KEY']))
	#app.run('0.0.0.0', debug=True, port=8100, ssl_context=(crt, key) )
	# ---
