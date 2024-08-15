from sqlalchemy import create_engine, text

from .base_connector import BaseConnector

class AzureSQLConnector(BaseConnector):
    """
    A connector for interfacing with a Azure SQL database.

    This class handles the establishment of a connection to a Azure SQL database and provides
    methods to execute queries and retrieve metadata about tables and columns.

    Attributes:
        connection_details (dict): A dictionary containing database connection parameters.
        password (str): The password for the database user.
    """
    def get_connection(self) -> object:
        """
        Establish a connection to a Azure SQL database.

        Returns:
        - engine: an sqlachemy engine object.
        """
        connection_string = f"mssql+pymssql://{self.connection['username']}:{self.password}@{self.connection['server']}:{self.connection['port']}/{self.connection['database']}"
        engine = create_engine(connection_string)
        return engine

    def execute_query(self, query:str, params=None):
        """
        Execute a SQL query on the a Azure SQL database.

        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): The parameters to be passed to the query.

        Returns:
            list: A list of tuples containing the results of the query.

        Raises:
            Exception: If an error occurs during query execution.
        """
        engine = self.get_connection()
        with engine.connect() as connection:
            result = connection.execute(text(query), params)
            return result.fetchall()
            
    def get_all_tables(self) -> list:
        """
        Get a list of all tables in a Azure SQL database.

        Returns:
        - list: A list of table names.
        """
        query = f"""
            SELECT TABLE_SCHEMA, TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE';
        """
        result = self.execute_query(query)
        return result
    

    def get_table_columns(self, schema:str, table:str)  -> list:
        """
        Get a list of columns in a table in a Azure SQL database.

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
            SELECT TOP(10) * 
            FROM {schema}."{table}";
        """
        return self.execute_query(query)
    
    def get_column_data(self, schema:str, table:str, column:str) -> list:
        """
        Get the data in a column in a table in a Azure SQL database.

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
