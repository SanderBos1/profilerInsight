class BaseConnector:
    """
    Abstract base class for database connectors.

    This class defines the interface for database connectors. Each subclass should 
    implement these methods to interact with a particular type of database. 
    The methods include connecting to the database, executing queries, and 
    retrieving metadata about tables and columns.

    Attributes:
        - connection_details (dict): A dictionary containing the details required 
                                   to establish a connection to the database.
        - password (str): The password for the database connection.
    """

    def __init__(self, connection: dict, password:str):
        """
        Initialize the BaseConnector with connection details.

        Args:
            connection_details (dict): A dictionary containing the necessary details 
                                       to connect to the database
        - password (str): The password for the database connection.
        """
        self.connection = connection
        self.password = password

    def get_connection(self) -> object:
        """
        Establish and returns a database connection.

        This method should be overridden by subclasses to provide the actual 
        implementation for connecting to the specific database.

        Returns:
            object: A database connection object.

        Raises:
            NotImplementedError: If not overridden by subclasses.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def execute_query(self, query: str, params=None) -> object:
        """
        Execute a database query.

        This method should be overridden by subclasses to provide the actual 
        implementation for executing queries against the database.

        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): Parameters to be used with the query.

        Returns:
            object: The result of the query execution.

        Raises:
            NotImplementedError: If not overridden by subclasses.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_all_tables(self) -> list:
        """
        Retrieve a list of all tables in the database.

        This method should be overridden by subclasses to provide the actual 
        implementation for retrieving all table names from the database.

        Returns:
            list: A list of table names.

        Raises:
            NotImplementedError: If not overridden by subclasses.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_table_columns(self, schema: str, table: str) -> list:
        """
        Retrieve a list of columns for a specific table in a given schema.

        This method should be overridden by subclasses to provide the actual 
        implementation for retrieving column names for a specified table and schema.

        Args:
            schema (str): The name of the schema.
            table (str): The name of the table.

        Returns:
            list: A list of column names for the specified table.

        Raises:
            NotImplementedError: If not overridden by subclasses.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def get_column_data(self, schema: str, table: str, column: str) -> list:
        """
        Retrieve data from a specific column in a given table and schema.

        This method should be overridden by subclasses to provide the actual 
        implementation for retrieving data from a specified column.

        Args:
            schema (str): The name of the schema.
            table (str): The name of the table.
            column (str): The name of the column.

        Returns:
            list: A list of values from the specified column.

        Raises:
            NotImplementedError: If not overridden by subclasses.
        """
        raise NotImplementedError("This method should be overridden by subclasses")
