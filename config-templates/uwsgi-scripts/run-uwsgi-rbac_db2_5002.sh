LOCAL=127.0.0.1
CEREBRO=cerebro.onrule.com
IP=$LOCAL
PORT=5002
APP=WSGI:app
VENV=/var/www/AccessControl/venv/bin
BASE=`pwd`
MODULE=AccessControl
CONFIG=app.config.rbac_db2_5002
WSGI_FILE=WSGI.py

export APP_SETTINGS=$BASE/$MODULE/$CONFIG
#$VENV/uwsgi --socket $IP:$PORT -w $APP &
#$VENV/uwsgi --socket --enable-threads $IP:$PORT -w $APP &

# To get uWSGI communicate with Nginx using HTTP:
#$VENV/uwsgi --socket $IP:$PORT --protocol=http -w $APP &

# To dun uWSGI as a HTTP server:
#$VENV/uwsgi --http $IP:$PORT --wsgi-file $WSGI_FILE --master --processes 4 --threads 2

#$VENV/uwsgi --http $IP:$PORT -w $APP --master --processes 4 --threads 2
$VENV/uwsgi --socket $IP:$PORT -w $APP --master --processes 4 --threads 2


