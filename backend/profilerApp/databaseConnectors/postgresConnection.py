import psycopg2
from .database import Database

class postgresConnection(Database):
    def __init__(self, connection:dict, password:str):
        self.connectionDetails = connection
        self.password = password

    def get_connection(self) -> object:
        """
        Establishes a connection to a PostgreSQL database.

        Returns:
        - psycopg2.extensions.connection: A connection object for the database.
        """
        conn = psycopg2.connect(
            dbname=self.connectionDetails['database'],
            user=self.connectionDetails['username'],
            password=self.password,
            host=self.connectionDetails['host'],
            port=self.connectionDetails['port']
        )
        return conn

    def execute_query(self, query:str, params=None):
        """
        Executes a SQL query on a PostgreSQL database.

        Args:
        - query (str): The SQL query to be executed.
        - params (tuple): The parameters for the query.

        Returns:
        - list: A list of tuples containing the results of the query.

        Raises:
        - Exception: If an error occurs during query execution.
        """
        conn = self.get_connection()
        with conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
            
    def get_all_tables(self) -> list:
        """
        Gets a list of all tables in a PostgreSQL database.

        Returns:
        - list: A list of table names.
        """
        query = f"""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE'
            AND table_catalog = '{self.connectionDetails['database']}'
            AND table_schema NOT IN ('pg_catalog', 'information_schema', 'excluded_schema_name');
        """

        return self.execute_query(query)
    

    def get_table_columns(self, schema:str, table:str)  -> list:
        """
        Gets a list of columns in a table in a PostgreSQL database.

        Args:
        - schema (str): The schema of the table.
        - table (str): The name of the table.

        Returns:
        - list: A list of column names.
        """
        query = f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = '{schema}'
            AND table_name = '{table}';
        """

        return self.execute_query(query)
    
    def get_column_data(self, schema:str, table:str, column:str) -> list:
        """
        Gets the data in a column in a table in a PostgreSQL database.

        Args:
        - schema (str): The schema of the table.
        - table (str): The name of the table.
        - column (str): The name of the column.

        Returns:
        - list: A list of column data.
        """
        query = f"""
            SELECT "{column}"
            FROM {schema}.{table};
        """

        return self.execute_query(query)