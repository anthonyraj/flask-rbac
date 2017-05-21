from flask import Flask, request
import logging


def create_app():
	app = Flask(__name__)
	return app
	
app = create_app()
	
# -------
# Logging
# -------
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)


import AccessControl.views
