import psycopg2

from .base_connector import BaseConnector

class PostgresConnector(BaseConnector):
    """
    A connector for interfacing with a PostgreSQL database.

    This class handles the establishment of a connection to a PostgreSQL database and provides
    methods to execute queries and retrieve metadata about tables and columns.

    Attributes:
        connection_details (dict): A dictionary containing database connection parameters.
        password (str): The password for the database user.
    """
    def get_connection(self) -> object:
        """
        Establish a connection to a PostgreSQL database.

        Returns:
        - psycopg2.extensions.connection: A connection object for the database.
        """
        conn = psycopg2.connect(
            dbname=self.connection['database'],
            user=self.connection['username'],
            password=self.password,
            host=self.connection['host'],
            port=self.connection['port']
        )
        return conn

    def execute_query(self, query:str, params=None):
        """
        Execute a SQL query on the PostgreSQL database.

        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): The parameters to be passed to the query.

        Returns:
            list: A list of tuples containing the results of the query.

        Raises:
            Exception: If an error occurs during query execution.
        """
        conn = self.get_connection()
        with conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
            
    def get_all_tables(self) -> list:
        """
        Get a list of all tables in a PostgreSQL database.

        Returns:
        - list: A list of table names.
        """
        query = f"""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE'
            AND table_catalog = '{self.connection['database']}'
            AND table_schema NOT IN ('pg_catalog', 'information_schema', 'excluded_schema_name');
        """

        return self.execute_query(query)
    

    def get_table_columns(self, schema:str, table:str)  -> list:
        """
        Get a list of columns in a table in a PostgreSQL database.

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
        columns = self.execute_query(query)
        columns = [column[0] for column in columns]
        return columns

    
    def get_preview_data(self, schema:str, table:str) -> object:
        """
        Get the data residing in the first 10 rows of the database.
        Load it into a Pandas Dataframe and convert it to html.
        
        Params:
            - schema (str): The schema where the table is saved
            - table (str): The chosen table.
        """
        query = f"""
            SELECT * 
            FROM {schema}."{table}"
            Limit 10;
        """
        return self.execute_query(query)
    
    def get_column_data(self, schema:str, table:str, column:str) -> list:
        """
        Get the data in a column in a table in a PostgreSQL database.

        Args:
        - schema (str): The schema of the table.
        - table (str): The name of the table.
        - column (str): The name of the column.

        Returns:
        - list: A list of column data.
        """
        query = f"""
            SELECT "{column}"
            FROM {schema}."{table}";
        """
        return self.execute_query(query)
