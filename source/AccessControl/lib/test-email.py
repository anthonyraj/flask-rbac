from mysendmail import *
import os

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
        notification_event = 'quote-upload'
        #login_details = _get_login_details()
	login_details = [{'login_id':'araj@equipa.com', 'firstname':'Anthony', 'lastname':'Raj'}]
        quote_url = 'http://app.equipa.com/app/viewQuote?project_id=1&logical_name=xxxxxxx'
        #encoded_quote_url = urllib.quote_plus(quote_url)
        params = {'project_name':'Polka','lab_name':'EMCTEST','url':quote_url}

        send_email_notification(notification_event,login_details,params)

#run()
run1()
