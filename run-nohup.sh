MODULE=AccessControl

rm nohup.out

BASE_PATH=/root 
echo $BASE_PATH


export APP_SETTINGS=$BASE_PATH/$MODULE/source/$MODULE/app.config
echo $APP_SETTINGS

PYTHON=$BASE_PATH/$MODULE/venv/bin/python
RUN_SERVER=$BASE_PATH/$MODULE/source/runserver.py

echo $PYTHON
echo $RUN_SERVER

#nohup $BASE_PATH/$MODULE/venv/bin/python $BASE_PATH/$MODULE/source/runserver.py &
CMD="nohup $PYTHON $RUN_SERVER &"
echo $CMD

eval $CMD
