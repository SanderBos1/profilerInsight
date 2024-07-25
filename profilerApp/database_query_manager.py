import psycopg2
from contextlib import contextmanager

@contextmanager
def get_connection(db_type, connection_details):
    """
    Context manager for establishing and managing a database connection.

    Parameters:
    - db_type (str): The type of database to connect to. Currently, only "postgresql" is supported.
    - connection_details (object): An object containing database connection parameters:
      - database (str): The name of the database.
      - username (str): The username for the database connection.
      - password (str): The password for the database connection.
      - host (str): The hostname or IP address of the database server.
      - port (int): The port number on which the database server is listening.

    Raises:
    - ValueError: If the provided db_type is not supported.

    Yields:
    - psycopg2.extensions.connection: A connection object for the database.
    """
    if db_type == "postgresql":
        conn = psycopg2.connect(
            dbname=connection_details.database,
            user=connection_details.username,
            password=connection_details.password,
            host=connection_details.host,
            port=connection_details.port
        )
    else:
        raise ValueError("Unsupported database type")
    
    try:
        yield conn
    finally:
        conn.close()

class DatabaseQueryManager:

    def __init__(self, dbType, connectionDetails):
        """
        Initializes the DatabaseQueryManager with the specified database type.

        Parameters:
        - dbType (str): The type of database (e.g., "postgresql").
        """
        self.dbType = dbType
        self.connectionDetails = connectionDetails

    def executeQuery(self, query, params=None):
        """
        Executes a SQL query and returns the results.

        Parameters:
        - connectionDetails (object): An object containing database connection parameters:
          - database (str): The name of the database.
          - username (str): The username for the database connection.
          - password (str): The password for the database connection.
          - host (str): The hostname or IP address of the database server.
          - port (int): The port number on which the database server is listening.
        - query (str): The SQL query to be executed.
        - params (tuple): The parameters for the query.

        Returns:
        - list: A list of tuples containing the results of the query.

        Raises:
        - Exception: If an error occurs during query execution.
        """
        connection = get_connection(self.dbType, self.connectionDetails)
        with connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()