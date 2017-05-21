import psycopg2
from postgresdb import postgresdb

class tenancy_manager:
	"""A class to manage TBAC functions"""
    
	def __init__(self,config):
		self.pgdb = postgresdb(config)

	def get_customer_schema(self,customer_id):
		customer_db = ''
		#print 'customer_id=',customer_id
		self.pgdb.db_cursor.execute('select customer_db from customer_info_master where customer_id=%s', (customer_id,) )
		
		customer_db = self.pgdb.db_cursor.fetchone()
		#print 'customer_db=',customer_db
		
		if (customer_db): return customer_db[0]
		else: return ''

	# If connection is still open close the connection
	def __del__(self):
		#self.pgdb.__del__()
		pass 

##### END OF FUNCTIONS ######

if __name__ == "__main__":
	config = {'DBNAME':'console_db', 'DBUSER':'postgres','DBPASS':''}
	tm = tenancy_manager(config)
	customer_id = 105
	customer_db = tm.get_customer_schema(customer_id)
	print 'Customer schema for customer_id='+str(customer_id)+' -> customer_db='+customer_db
