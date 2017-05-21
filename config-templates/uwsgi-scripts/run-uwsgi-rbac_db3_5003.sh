LOCAL=127.0.0.1
CEREBRO=cerebro.onrule.com
IP=$CEREBRO
PORT=5003
APP=WSGI:app
VENV=/var/www/AccessControl/venv/bin
BASE=`pwd`
MODULE=AccessControl
CONFIG=app.config.rbac_db3_5003

export APP_SETTINGS=$BASE/$MODULE/$CONFIG
$VENV/uwsgi --socket $IP:$PORT -w $APP &
#$VENV/uwsgi --socket --enable-threads $IP:$PORT -w $APP &

# To get uWSGI communicate with Nginx using HTTP:
# env/bin/uwsgi --socket $IP:$PORT --protocol=http -w WSGI:app

