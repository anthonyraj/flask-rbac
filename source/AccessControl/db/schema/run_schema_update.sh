DB_VER="1"
DB_NAME=rbac_db$DB_VER

# Alter Schema and Update data
psql -U postgres -d $DB_NAME < run_alter.sql
psql -U postgres -d $DB_NAME < run_update.sql
psql -U postgres -d $DB_NAME < run_sequence.sql

