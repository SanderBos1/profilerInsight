import psycopg2
class postgresqlConnection:

    def __init__(self, host, port, user, password, dbname ):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None

    def getConnection(self):
        if self.connection == None:
            try:
                connection = psycopg2.connect(
                    dbname= self.dbname,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
                self.connection = connection
                self.cursor = connection.cursor()
            except Exception as e:
                print(e)
        else:
            self.cursor = self.connection.cursor()
    
    def closeConnection(self):
        self.connection = None
        self.cursor = None

    def queryDB(self, query):
        if self.connection == None:
            self.getConnection()
        cursor = self.cursor
        try:
            cursor.execute(query)
            dataset = cursor.fetchall()
            return dataset
        except Exception as e:
            return str(e)
    


