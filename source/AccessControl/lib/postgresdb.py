import psycopg2

class postgresdb:
	"""A class to manage TBAC functions"""

	def __init__(self,config):
		self.config = config
		self.db_connection = self.connect_db()
		if self.db_connection is not None:	
			self.db_cursor = self.db_connection.cursor()
			print 'cursor instantiated'

	def connect_db(self):
		config = self.config
		try:
			return psycopg2.connect(database=config['DBNAME'],user=config['DBUSER'], password=config['DBPASS'])
		except:
			print "Postgres database connection failure."	
	
	def query(self,sql):
		self.db_cursor.execute('select customer_id, customer_db from customer_info_master')
		data = [ dict(customer_id = row[0], customer_db = row[1]) for row in self.db_cursor.fetchall()]
		return data


	# If connection is still open close the connection
	def __del__(self):
		if self.db_connection is not None: self.db_connection.commit()
		if self.db_cursor is not None: self.db_cursor.close() 
		if self.db_connection is not None: self.db_connection.close()  

##### END OF FUNCTIONS ######

if __name__ == "__main__":
	config = {'DBNAME':'console_db', 'DBUSER':'postgres','DBPASS':''}
	pgdb = postgres_db(config)
	pgdb.connect_db()
	sql = 'select * from customer_info_master'
	data = pgdb.query(sql)
	print data
