 
import psycopg2

class postgresql:

    __environment = ''
    __port = 5432
    __user = 'postgres'
    __host = 'localhost'
    __database = 'Research'
    __password = 'One_Drive^@11'

    def __init__(self,environment='Local'):
        self.__environment = environment
        self.__init_server_conn_fxn(environment)
    
    def __init_server_conn_fxn(self,environment='Local'):
        try:
            self.conn = psycopg2.connect(
                user = self.__user,
                password = self.__password,
                host = self.__host,
                port = self.__port,
                database = self.__database
                )
            print('Successful PostgreSQL connection')
        except RuntimeError as e:
            print(e)
    
    def set_schema_fxn(self, db_schema):
        try:
            if db_schema == self.__db_schema:
                cursor = self.conn.cursor()
            else:
                self.db_schema = db_schema
                self.conn.select_db(self.db_schema)
                cursor = self.conn.cursor()
        except (AttributeError, psycopg2.OperationalError):
            self.__init_server_conn_fxn(self)
            cursor = self.conn.cursor()
        return cursor    

    def query_no_return_fxn(self, db_schema, query_string):
        cursor = self.set_schema_fxn(db_schema)

        # Execute query
        try:
            cursor.execute(query_string)
            self.conn.commit()
            cursor.close()
        except RuntimeError as e:
            print(e)
            cursor.close()
    
    def query_fxn(self, db_schema, query_string):
        cursor = self.set_schema_fxn(db_schema)

        # Execute query
        try:
            cursor.execute(query_string)
            self.conn.commit()
            data = cursor.fetchall()
            cursor.close()
            return data
        except RuntimeError as e:
            print(e)
            cursor.close()

    def write_fxn_list(self, db_schema, table, insertList, columns):
        columnstring = " ("
        endstring = "("
        for item in columns:
            columnstring = columnstring + item + ","
            endstring = endstring + "%s,"
       
        columnstring = columnstring[:-1]
        columnstring = columnstring + ") "

        endstring = endstring[:-1]
        endstring = endstring + ");"
        query_string = 'INSERT INTO ' + db_schema + '.' + table + columnstring +' VALUES ' + endstring
    
        cursor = self.set_schema_fxn(db_schema)

        # Execute query
        try:
            cursor.executemany(query_string, insertList)
            self.conn.commit()
        except RuntimeError as e:
            print(e)

    def close_connect(self):
        
        
