from AccessControl import app
#from flask_sslify import SSLify

#sslify = SSLify(app)

HOST = '0.0.0.0'
PORT = app.config['PORT']
SSL = app.config['SSL']
DEBUG = 'True'
CRT = app.config['CRT']
KEY = app.config['KEY']

if SSL == '1':
	# ---------
	# SSL Setup 
	# ---------
	print 'CRT=', CRT
	print 'KEY=', KEY
	app.run(host=HOST, debug=DEBUG, port=PORT, ssl_context=(CRT, KEY))
	# ---
else:
	# ---------
	#Non-SSL Setup
	# ---------
	app.run(host=HOST, port=PORT, debug=DEBUG)
