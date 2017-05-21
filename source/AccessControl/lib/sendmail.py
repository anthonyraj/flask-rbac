import smtplib,os,urllib, json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_notification(notification_event,login_details,params):
	# TODO Create a table to keep track of the notification constant details
	print '[send_email_notification] login_details='+json.dumps(login_details)+' | params='+json.dumps(params)+ ' | notification_event='+notification_event
	notification_event_map = ['standards_update','quote_upload','deliverable_upload']

	if notification_event in notification_event_map:
		print 'notification match found!'
		#login_details = _get_login_details()
		_send_email_notification(notification_event,login_details,params)
		print '[send_email_notification] called send_email_notification'
	else: print '[send_email_notification] Something fishy !!'

def _get_login_details():
	# Using login_id extract the username Eg. arag from araj@equipa.com
	login_details = [{'login_id':'anthony@equipa.com', 'firstname':'Anthony', 'lastname':'Raj'}]
	return login_details

def _send_email_notification(notification_event,login_details,params):
	# Fixed variables
	server_details = {'server':'localhost','from':'hq@equipa.com'}

	# TODO: Retrieve EVENTS from DB
	mail_details = {
		'standards_update':{
		'message_details': {'subject_line':'ALERT: Standards Update'},
		'content_details':{'html':'standards_update.html','text':'standards_update.txt'}
		},
		'deliverable_upload':{
		'message_details': {'subject_line':'Deliverable Upload'},
		'content_details':{'html':'deliverable_upload.html','text':'deliverable_upload.txt'}
		},
		'quote_upload':{
		'message_details': {'subject_line':'Quote Upload'},
		'content_details':{'html':'quote_upload.html','text':'quote_upload.txt'}
		}}

	# Email Content format: HTML
	content_details = mail_details[notification_event]['content_details']
	message_details = mail_details[notification_event]['message_details']
	message_details['subject_line'] = '%s from %s' % (message_details['subject_line'],params['lab_name']) 
	print '[_send_email_notification] Defined all parameters'
	_process_email_notification(login_details,message_details,content_details,server_details,params)

def _process_email_notification(login_details,message_details,content_details,server_details,params):
	TEXT,HTML = _read_mail_content(content_details['text'],content_details['html'], params['email_content_path'])
	print '[_process_email_notification] Completed reading email content ..'
	for item in login_details:
		# Scrubbing the email to remove fake company names
		scrubbed_login_id = _scrub_email( item['login_id'] )
		print 'scrubbed_login_id:',scrubbed_login_id
		message_details['addressed_to'] = scrubbed_login_id
		print 'Sending email to: ',message_details['addressed_to']
		
		message_details['text'],message_details['html'] = _prepare_email(item['firstname'],HTML,TEXT,params)
		_send_email(message_details,server_details)

def _scrub_email(login_id):
	trigger = ['acme','equipa','manufacto','emctest','safetytest','universal','collaboration']
	scrubbed_login_id = login_id
	for t in trigger:
		if login_id.__contains__(t): scrubbed_login_id=login_id.replace(t,'equipa')
	print '[_scrub_email] before scrubbing:',login_id,' | after scrubbing:',scrubbed_login_id
	return scrubbed_login_id

# def _convert_to_real(email_id):
	# 	demo_list = ['acme','equipa','europa','emctest','safetytest','universal']
	# 	equipa_email = ''
	# 	for item in demo_list:
	# 		if item in email_id:
	# 			equipa_email = email_id.replace(item,'equipa')
	# 			print '[_convert_to_real] converted email:',equipa_email
	# 	return equipa_email

def _prepare_email(firstname,html_message,text_message,params):
	print '[_prepare_email] preping email with parameters ..'	
	TEXT1 = text_message % (firstname, params['project_name'], params['url'], params['url'], params['lab_name'])
	HTML1 = html_message % (firstname, params['project_name'], params['url'], params['url'], params['lab_name']) 
	print TEXT1
	return TEXT1,HTML1	

def _read_mail_content(textfile, htmlfile, email_path):
	#email_path = os.path.join(os.getcwd(),'email_content')

	textfile = os.path.join(email_path,textfile)
	htmlfile = os.path.join(email_path,htmlfile)

	TEXT = _grab_mail_content(textfile)
	HTML = _grab_mail_content(htmlfile)
	#print HTML
	return TEXT,HTML

def _grab_mail_content(filename):
	# Read message from the Message file
	fp = open(filename, 'rb')
	message = fp.read()
	fp.close()
	return message

def _send_email(message_details,server_details):
	# Create message container - the correct MIME type is multipart/alternative.
	print '[_send_email] sending email ..'
	print message_details

	msg = MIMEMultipart('alternative')
	msg['Subject'] = message_details['subject_line']
	msg['From'] = server_details['from']

	#convert any demo account emails as needed
	msg['To'] = message_details['addressed_to']

	# Prepare actual 	message
	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(message_details['text'], 'plain')
	part2 = MIMEText(message_details['html'], 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	server = smtplib.SMTP(server_details['server'])
	server.sendmail(server_details['from'], message_details['addressed_to'], msg.as_string())
	server.quit()

def run():
	# Fixed variables
	server_details = {'server':'localhost','from':'hq@equipa.com'}
	# Dynamic variables
	login_details = [{'login_id':'araj@equipa.com', 'firstname':'Anthony', 'lastname':'Raj'}]
	content_details = {'html':'standard-update.html','text':'standard-update.txt'}
	message_details = {'subject_line':'ALERT: Standard Update'}

	process_email_notification(login_details,message_details,content_details,server_details)

def run1():
	email_path = os.path.join(os.getcwd(),'email_content')
	notification_event = 'quote_upload'
	login_details = _get_login_details()
	quote_url = 'http://app.equipa.com/app/viewQuote?project_id=1&logical_name=xxxxxxx'
	#encoded_quote_url = urllib.quote_plus(quote_url)
	params = {'project_name':'Polka','lab_name':'EMCTEST','url':quote_url, 'email_content_path':email_path}

	send_email_notification(notification_event,login_details,params)

#run()
#run1()
