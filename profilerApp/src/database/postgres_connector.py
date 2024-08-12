"""
This module defines the `PostgresConnector` class, 
which provides an interface for interacting with a PostgreSQL database.

The `PostgresConnector` class is designed to handle database operations such as 
 * establishing connections
 * executing queries,
 * retrieving metadata about tables and columns. 
 
It inherits from the `BaseConnector` class and utilizes the `psycopg2`
library to manage connections and execute SQL commands.

Key functionalities of `PostgresConnector` include:
- Establishing a connection to a PostgreSQL database.
- Executing SQL queries and returning query results.
- Retrieving a list of all tables in the database.
- Retrieving column names for a specific table.
- Fetching data from a specific column in a table.

Dependencies:
- `psycopg2`: A PostgreSQL adapter for Python.
- `BaseConnector`: The base class providing a common interface for database connectors.

Classes:
- `PostgresConnector`: A connector for interfacing with a PostgreSQL database.

Methods:
- `get_connection() -> object`: Establishes and returns a connection to the PostgreSQL database.
- `execute_query(query: str, params=None) -> list`: 
    Executes a SQL query with optional parameters and returns the results.
- `get_all_tables() -> list`: 
        Retrieves a list of all tables in the PostgreSQL database.
- `get_table_columns(schema: str, table: str) -> list`: 
        Retrieves a list of column names for a specified table.
- `get_column_data(schema: str, table: str, column: str) -> list`: 
        Retrieves data from a specified column in a table.
"""

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
        Establishes a connection to a PostgreSQL database.

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
        Executes a SQL query on the PostgreSQL database.

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
        Gets a list of all tables in a PostgreSQL database.

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
            FROM {schema}."{table}";
        """
        return self.execute_query(query)
