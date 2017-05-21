#for DB in rbac_db3_onboarding
for DB in rbac_db
do

	#DB_VER=3
	#DB_ENV="_onboarding" 
	#DB=rbac_db$DB_VER$DB_ENV # 

	PG="psql -U postgres "

	# Drop and Create database
	SQL="DROP DATABASE IF EXISTS $DB;"
	#CMD="$PG -c '$SQL'"
	#echo $CMD; eval $CMD

	SQL="CREATE DATABASE $DB;"
	#CMD="$PG -c '$SQL'"
	#echo $CMD; eval $CMD
	#--

	./run_schema_setup.sh $DB
done

