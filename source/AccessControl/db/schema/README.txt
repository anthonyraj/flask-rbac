Important rbac db setup scripts:
run_sql.sh
	|- run_create.sh
		|- Create OEM Schema : schema-psql-oem.sql
		|- Create LAB Schema : schema-psql-lab.sql
	|- run_insert.sh
		|- Populate OEM: collaboration-oem.sql	
		|- Populate LAB: collaboration-lab.sql
