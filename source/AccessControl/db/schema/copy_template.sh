VER=3
DB=rbac_db$VER
DB_LIST=( "$DB-dev" "$DB-qa" "$DB-uat" "$DB-uat1" )
TS=`date +%Y%m%d.%H%M`
echo "Time Stamp:$TS"

for DB in rbac_db3
do
	echo $DB
	echo "len(DB_LIST)=" ${#DB_LIST[@]}
	echo "DB_LIST=" ${DB_LIST[@]}

	for DB1 in "${DB_LIST[@]}"
	do
		echo "Backing up $DB1 ..."
		ALT_SQL="ALTER DATABASE $DB1 RENAME TO $DB.$TS;"
		echo $ALT_SQL
		#psql -U postgres -c '$ALT_SQL'
		
		echo "Creating $DB1 ..."
		COPY_SQL="CREATE DATABASE $DB1 TEMPLATE $DB;"
		echo $COPY_SQL
		#psql -U postgres -c '$COPY_SQL'
	done

	echo 'done'

done
