#DB_VER=3
DB_VER=4

#DB_ENV="_dev"
DB_ENV="" 

#DB_NAME="rbac_db3_dev"
DB_NAME=rbac_db$DB_VER$DB_ENV # 

PG="psql -U postgres "

# Drop and Create database
SQL="DROP DATABASE IF EXISTS $DB_NAME;"
CMD="$PG -c '$SQL'"
echo $CMD; eval $CMD

SQL="CREATE DATABASE $DB_NAME;"
CMD="$PG -c '$SQL'"
echo $CMD; eval $CMD
#--

# Create and Insert data
psql -U postgres -d $DB_NAME < run_create.sql
psql -U postgres -d $DB_NAME < run_insert.sql
psql -U postgres -d $DB_NAME < run_sequence.sql

# Custom permissions tailoring
psql -U postgres -d $DB_NAME < run_custom.sql

# Validating RBAC setup
psql -U postgres -d $DB_NAME < run_validation.sql
