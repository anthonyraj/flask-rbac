DB=$1
declare -a myarray
declare -a myarray1

#SCHEMA_FILE=schema.txt
#OEM_SCHEMA_FILE=oem.txt
#LAB_SCHEMA_FILE=lab.txt
OEM_SCHEMA_FILE=oem-virtual.txt
LAB_SCHEMA_FILE=lab-dummy.txt

# Load schema file into array.
let i=0
while IFS=$'\n' read -r line_data; do
    myarray[i]="${line_data}"
    ((++i))
done < $OEM_SCHEMA_FILE

let i=0
while (( ${#myarray[@]} > i )); do
    SCHEMA=${myarray[i++]}
    printf "Processing schema => $SCHEMA\n"

	# Create and Insert data
	psql -U postgres -d $DB -v schema=$SCHEMA < run_create_generic.sql
	psql -U postgres -d $DB -v schema=$SCHEMA < oem/run_insert.sql
	psql -U postgres -d $DB -v schema=$SCHEMA < run_sequence_generic.sql

	# Custom permissions tailoring
	psql -U postgres -d $DB -v schema=$SCHEMA < oem/run_custom.sql

	# Validating RBAC setup
	psql -U postgres -d $DB -v schema=$SCHEMA < run_validation_generic.sql

done

# Load LAB schema file into array.
let i=0
while IFS=$'\n' read -r line_data; do
    myarray1[i]="${line_data}"
    ((++i))
done < $LAB_SCHEMA_FILE

let i=0
while (( ${#myarray1[@]} > i )); do
    SCHEMA=${myarray1[i++]}
    printf "Processing schema => $SCHEMA\n"

	# Create and Insert data
	psql -U postgres -d $DB -v schema=$SCHEMA < run_create_generic.sql
	psql -U postgres -d $DB -v schema=$SCHEMA < lab/run_insert.sql
	psql -U postgres -d $DB -v schema=$SCHEMA < run_sequence_generic.sql

	# Custom permissions tailoring
	psql -U postgres -d $DB -v schema=$SCHEMA < lab/run_custom.sql

	# Validating RBAC setup
	psql -U postgres -d $DB -v schema=$SCHEMA < run_validation_generic.sql

done

