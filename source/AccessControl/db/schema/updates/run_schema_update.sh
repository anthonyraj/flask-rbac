DB=$1
declare -a myarray
declare -a myarray1

#SCHEMA_FILE=schema.txt
#SCHEMA_FILE=schema-oem.txt
SCHEMA_FILE=schema-virtual.txt
SQL_FILE=sql.txt

# Load file into array.
let i=0
while IFS=$'\n' read -r line_data; do
    myarray[i]="${line_data}"
    ((++i))
done < $SCHEMA_FILE

let i=0
while IFS=$'\n' read -r line_data; do
    myarray1[i]="${line_data}"
    ((++i))
done < $SQL_FILE

let i=0
while (( ${#myarray[@]} > i )); do
	SCHEMA=${myarray[i++]}
    printf "Processing schema => $SCHEMA\n"

	let j=0
	while (( ${#myarray1[@]} > j )); do
		SQL=${myarray1[j++]}
		printf "Processing sql => $SQL\n"
		psql -U postgres -d $DB -v schema=$SCHEMA < $SQL
	done

done

#for SCHEMA in equipa manufacto acme
#do 
#	psql -U postgres -d $DB -v schema=$SCHEMA < update_vendors.sql
#done
