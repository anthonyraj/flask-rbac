#for DB in rbac_db3_dev rbac_db3_qa rbac_db3_uat rbac_db3_uat1
#for DB in rbac_db3 
for DB in rbac_db
do
	#psql -U postgres -d $DB < run_update_vendors.sh
	#psql -U postgres -d $DB < run_update_dashboard_permissions.sh
	./run_schema_update.sh $DB
done
