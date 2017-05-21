
HOST=$1
PORT=$2

SCHEMA=$3
ROLE_ID=$4

for MODULE_ID in 1 2 3 4 
do
	URL="https://$HOST:$PORT/set_full_access?customer_db=$SCHEMA&role_id=$ROLE_ID&module_id=$MODULE_ID&output=JSON"
	echo $URL
	curl -k $URL
done
