HOST=qa-pnq.equipa.com
PORT=5001
ROLE_ID=1 # SuperAdmin

#OEM: Set Full Permissions for Super Admin
for SCHEMA in equipa acme manufacto
do
./set_full_perm_oem.sh $HOST $PORT $SCHEMA $ROLE_ID
done

#Lab: Set Full Permissions for Super Admin
for SCHEMA in emctest safetytest universal
do
./set_full_perm_lab.sh $HOST $PORT $SCHEMA $ROLE_ID
done

